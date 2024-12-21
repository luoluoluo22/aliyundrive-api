#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
阿里云盘 API 的核心实现
"""

import os
import hashlib
from typing import Union, List
import requests
from tqdm import tqdm

from .utils.config import Config
from .utils.file import ChunksIter
from .auth import AliyundriveAuth

class AliyunDriveApi:
    """阿里云盘 API 封装类"""
    
    base_api = 'https://api.aliyundrive.com/v2/'

    def __init__(self, config_path='./config.ini'):
        """
        初始化 API 客户端
        :param config_path: 配置文件路径
        """
        self.config = Config(config_path)
        self.auth = AliyundriveAuth()
        self.tokens = self.auth.get_config()
        self.access_token = self.tokens['access_token']
        self.refresh_token = self.tokens['refresh_token']
        self.drive_id = self.tokens['default_drive_id']

        self.headers = {
            "accept": "application/json, text/plain, */*",
            "authorization": self.access_token,
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://www.aliyundrive.com",
            "referer": "https://www.aliyundrive.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
        }

        # 如果没有配置drive_id, 首先请求一下drive_id
        if not self.drive_id:
            self.get_user_info()

        self.root = []

    def do_refresh_token(self):
        """刷新 access token"""
        data = {
            "refresh_token": self.refresh_token
        }
        res = requests.post("https://websv.aliyundrive.com/token/refresh", headers={
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://www.aliyundrive.com",
            "referer": "https://www.aliyundrive.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
        }, json=data).json()

        self.access_token = res.get('access_token')
        self.headers['authorization'] = self.access_token
        self.config.update_access_token(self.access_token)
        return True

    def get_user_info(self):
        """获取用户信息"""
        res = requests.post(self.base_api + 'user/get', headers=self.headers, json={}).json()
        if res.get('code') == 'AccessTokenInvalid':
            if self.do_refresh_token():
                return self.get_user_info()
            else:
                print('Refresh Token Failed!')
                exit(-1)
        self.drive_id = res.get('default_drive_id')
        self.config.update_drive_id(self.drive_id)
        return res

    def list_files(self, parent_file_id='root', next_marker=None):
        """
        获取文件列表
        :param parent_file_id: 父文件夹ID，默认为root
        :param next_marker: 分页标记
        :return: 文件列表
        """
        data = {
            "drive_id": self.drive_id,
            "parent_file_id": parent_file_id,
            "limit": 100,
            "all": False,
            "fields": "*",
            "order_by": "name",
            "order_direction": "ASC"
        }
        if next_marker:
            data["marker"] = next_marker

        res = requests.post(self.base_api + 'file/list', headers=self.headers, json=data).json()
        if res.get('code') == 'AccessTokenInvalid':
            if self.do_refresh_token():
                return self.list_files(parent_file_id, next_marker)
            else:
                print('Refresh Token Failed!')
                exit(-1)

        items = res.get('items', [])
        next_marker = res.get('next_marker', None)

        # 如果还有更多文件，继续获取
        if next_marker:
            items.extend(self.list_files(parent_file_id, next_marker))

        return items

    def search_file(self, name):
        """
        搜索文件
        :param name: 文件名
        :return: 文件列表
        """
        data = {
            "drive_id": self.drive_id,
            "limit": 100,
            "type": "all",  # 搜索所有类型
            "query": f"name match \"{name}\"",
            "return_total_count": True,
            "fields": "*",
            "order_by": "updated_at",
            "order_direction": "DESC"
        }

        # 先获取根目录文件列表
        root_files = self.list_files()
        results = []

        # 在根目录中搜索
        for file in root_files:
            if name.lower() in file['name'].lower():
                results.append(file)
            # 如果是文件夹，��归搜索
            if file['type'] == 'folder':
                folder_files = self.list_files(file['file_id'])
                for sub_file in folder_files:
                    if name.lower() in sub_file['name'].lower():
                        results.append(sub_file)

        return results

    def print_file_info(self, file_info, index=None, show_path=False):
        """
        打印文件信息
        :param file_info: 文件信息
        :param index: 序号
        :param show_path: 是否显示完整路径
        """
        file_type = '📁 ' if file_info['type'] == 'folder' else '📄 '
        index_str = f"[{index}] " if index is not None else ""
        
        # 基本信息
        print(f"{index_str}{file_type}{file_info['name']}")
        
        # 文件大小和更新时间
        if file_info['type'] != 'folder':
            size_mb = file_info['size'] / (1024 * 1024)
            print(f"    大小: {size_mb:.2f} MB")
            print(f"    更新时间: {file_info['updated_at']}")
            print(f"    下载命令: aliyundrive download \"{file_info['name']}\"")
        
        # 如果是文件夹，显示提示信息
        if file_info['type'] == 'folder':
            print(f"    提示: 使用 'aliyundrive list \"{file_info['name']}\"' 查看此文件夹���容")

    def download_file(self, file_id: str, save_path: str = None):
        """
        下载文件
        :param file_id: 文件ID
        :param save_path: 保存路径，默认为当前目录
        :return: bool
        """
        # 获取文件信息
        data = {
            "drive_id": self.drive_id,
            "file_id": file_id
        }
        file_info = requests.post(self.base_api + 'file/get', headers=self.headers, json=data).json()
        
        if file_info.get('code') == 'AccessTokenInvalid':
            if self.do_refresh_token():
                return self.download_file(file_id, save_path)
            else:
                print('Refresh Token Failed!')
                exit(-1)

        # 如果是文件夹，不能下载
        if file_info.get('type') == 'folder':
            print('不能下载文件夹！')
            return False

        # 获取下载地址
        res = requests.post(self.base_api + 'file/get_download_url', headers=self.headers, json=data).json()
        
        if not res.get('url'):
            print('获取下载地址失败！')
            return False

        # 准备下载路径
        if save_path is None:
            save_path = os.getcwd()
        elif not os.path.exists(save_path):
            os.makedirs(save_path)

        file_name = file_info.get('name', file_id)
        save_file_path = os.path.join(save_path, file_name)

        # 开始下载
        headers = {
            'Referer': 'https://www.aliyundrive.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
        }
        response = requests.get(res['url'], stream=True, headers=headers)
        total_size = int(response.headers.get('content-length', 0))

        with open(save_file_path, 'wb') as file, tqdm(
            desc=f'Downloading {file_name}',
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)

        print(f'文件已下载到: {save_file_path}')
        return True

    def _get_parent_file_id(self, parent: str) -> str:
        """
        获取父文件夹ID
        :param parent: parent格式 xxx/xxx/xxx
        :return: str
        """
        if not parent:
            return 'root'

        dirs = parent.split('/')
        parent_file_name = dirs[0]
        parent_file_id = 'root'

        for item in self.root:
            if item['name'] == parent_file_name:
                parent_file_id = item['file_id']

        if parent_file_name != 'root' and parent_file_id == 'root':
            parent_file_id = self.create_folder(parent_file_name)['file_id']

        if len(dirs) == 1:
            return parent_file_id

        for index, parent_file_name in enumerate(dirs[1:]):
            files = self.get_list(parent_file_id)['items']
            flag = True
            for item in files:
                if item['name'] == parent_file_name:
                    parent_file_id = item['file_id']
                    flag = False
            if flag:
                parent_file_id = self.create_folder(parent_file_name, parent_file_id)['file_id']
        return parent_file_id

    def create_folder(self, name, parent_file_id="root"):
        """
        创建文件夹
        :param name: 文件夹名称
        :param parent_file_id: 父文件夹的ID, 默认为root
        :return: dict
        """
        data = {
            "drive_id": self.drive_id,
            "parent_file_id": parent_file_id,
            "name": name,
            "check_name_mode": "refuse",
            "type": "folder"
        }
        return self._create(data)

    def _create(self, data):
        """创建文件/文件夹"""
        res = requests.post(self.base_api + 'file/create', headers=self.headers, json=data).json()
        if res.get('code') == 'AccessTokenInvalid':
            if self.do_refresh_token():
                print('Token Refresh Success!')
                return self._create(data)
            else:
                print('Token Refresh Failed!')
                exit(-1)
        return res

    def _create_file(self, parent_file_id, content_hash, name, size):
        """创建文件"""
        data = {
            "auto_rename": True,
            "content_hash": content_hash,
            "content_hash_name": 'sha1',
            "drive_id": self.drive_id,
            "hidden": False,
            "name": name,
            "parent_file_id": parent_file_id,
            "type": "file",
            "size": size,
        }
        return self._create(data)

    def on_complete(self, file_id, upload_id):
        """完成文件上传"""
        data = {
            "drive_id": self.drive_id,
            "file_id": file_id,
            "upload_id": upload_id,
        }
        res = requests.post(self.base_api + 'file/complete', headers=self.headers, json=data).json()
        if res.get('code') == 'AccessTokenInvalid':
            if self.do_refresh_token():
                print('Token Refresh Success!')
                return self.on_complete(file_id, upload_id)
            else:
                print('Token Refresh Failed!')
                exit(-1)
        return res

    @staticmethod
    def get_sha1_hash(filepath):
        """获取文件的 SHA1 哈希值"""
        with open(filepath, 'rb') as f:
            sha1 = hashlib.sha1()
            while True:
                chunk = f.readline()
                if not chunk:
                    break
                sha1.update(chunk)
            return sha1.hexdigest()

    def get_file_info(self, filepath):
        """获取文件信息"""
        name = os.path.basename(filepath)
        content_hash = self.get_sha1_hash(filepath)
        size = os.path.getsize(filepath)
        return {
            "content_hash": content_hash,
            "name": name,
            "size": size,
        }

    def _upload_file(self, filepath, parent_file_id='root'):
        """上传文件的内部实现"""
        file_info = self.get_file_info(filepath)
        create_res = self._create_file(parent_file_id, **file_info)
        if create_res.get('rapid_upload'):
            print(f'秒传成功: {filepath}')
            return True
        
        upload_uri = create_res['part_info_list'][0]['upload_url']
        file_id = create_res['file_id']
        upload_id = create_res['upload_id']
        
        with open(filepath, 'rb') as f:
            total_size = os.fstat(f.fileno()).st_size
            f = tqdm.wrapattr(f, "read", desc='上传中...', miniters=1, total=total_size)
            with f as f_iter:
                res = requests.put(
                    upload_uri,
                    data=ChunksIter(f_iter, total_size=total_size)
                )
                res.raise_for_status()
        
        return self.on_complete(file_id, upload_id)

    def upload_file(self, filepath, parent: Union[None, str] = None):
        """
        上传文件
        :param filepath: 文件路径
        :param parent: 父文件夹路径，格式：xxx/xxx/xxx
        :return: bool
        """
        parent_file_id = 'root'
        if parent is None:
            return self._upload_file(filepath, parent_file_id)
        parent_file_id = self._get_parent_file_id(parent)
        return self._upload_file(filepath, parent_file_id)

    def get_all_file(self, path) -> List:
        """获取目录下所有文件的路径"""
        result = []
        try:
            get_dir = os.listdir(path)
        except NotADirectoryError:
            return [path]
        for i in get_dir:
            sub_dir = os.path.join(path, i)
            if os.path.isdir(sub_dir):
                result.extend(self.get_all_file(sub_dir))
            else:
                result.append(sub_dir)
        return result

    def upload_folders(self, folder_path, parent: Union[None, str] = None):
        """
        上传文件夹
        :param folder_path: 文件夹路径
        :param parent: 父文件夹路径，格式：xxx/xxx/xxx
        :return: None
        """
        files = self.get_all_file(folder_path)
        for file in files:
            full_paths = file.split('/')[1:-1]
            if parent is None:
                self.upload_file(file, '/'.join(full_paths))
            else:
                self.upload_file(file, parent + '/' + '/'.join(full_paths)) 

    def get_file_by_path(self, path: str):
        """
        通过路径获取文件信息
        :param path: 文件路径，格式：folder1/folder2/file.txt
        :return: 文件信息或 None
        """
        if not path:
            return None

        parts = path.strip('/').split('/')
        current_id = 'root'
        current_files = self.list_files(current_id)

        for i, part in enumerate(parts):
            found = False
            for file in current_files:
                if file['name'].lower() == part.lower():
                    current_id = file['file_id']
                    found = True
                    if i == len(parts) - 1:  # 最后一个部分
                        return file
                    elif file['type'] == 'folder':  # 不是最后一个部分，必须是文件夹
                        current_files = self.list_files(current_id)
                        break
            if not found:
                return None
        return None

    def download_by_path(self, path: str, save_path: str = None):
        """
        通过路径下载文件
        :param path: 文件路径，格式：folder1/folder2/file.txt
        :param save_path: 保存路径，默认为当前目录
        :return: bool
        """
        file_info = self.get_file_by_path(path)
        if not file_info:
            print(f'未找到文件: {path}')
            print("\n提示:")
            print("1. 路径格式：folder1/folder2/file.txt")
            print("2. 路径区分大小写")
            print("3. 使用 'aliyundrive list' 查看可用的文件和文件夹")
            return False
        return self.download_file(file_info['file_id'], save_path) 