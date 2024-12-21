#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
命令行接口模块
"""

import sys
import os
from pathlib import Path
import configparser
from .api import AliyunDriveApi
from .auth import AliyundriveAuth


def print_usage():
    print("""
使用方法:
    上传文件:
        aliyundrive upload file_path [parent_name]
        例如:
        aliyundrive upload ./test.txt
        aliyundrive upload ./test_folder x/y
    
    下载文件:
        aliyundrive download <文件路径或文件名> [保存路径]
        例如:
        aliyundrive download test.txt                     # 下载根目录下的 test.txt
        aliyundrive download 充电/file.txt                # 下载指定文件夹下的文件
        aliyundrive download test.txt /Users/downloads/   # 指定保存路径
    
    列出文件:
        aliyundrive list [文件夹名称]
        例如:
        aliyundrive list                    # 列出根目录文件
        aliyundrive list 充电               # 列出"充电"文件夹内容
        
        提示: 
        1. 可以直接使用文件夹名称，无需记忆 ID
        2. 如果文件夹名称包含空格，请用引号括起来
        3. 支持多级目录，如：文件夹1/文件夹2
    
    搜索文件:
        aliyundrive search keyword
        例如:
        aliyundrive search test.txt         # 搜索文件名包含 test.txt 的文件
        aliyundrive search 充电             # 搜索文件名包含"充电"的文件/文件夹
    """)


def init_config():
    """初始化配置"""
    auth = AliyundriveAuth()
    auth.get_tokens_from_web()
    print("配置初始化完成！")


def main():
    """命令行入口函数"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action='store_true', help='初始化配置')
    parser.add_argument('--debug', action='store_true', help='显示调试信息')
    parser.add_argument('command', nargs='?', help='命令')
    parser.add_argument('args', nargs='*', help='命令参数')
    
    args = parser.parse_args()
    
    if args.init:
        init_config()
        return
        
    if args.debug:
        config_path = os.path.join(str(Path.home()), '.aliyundrive', 'config.ini')
        print(f"配置文件路径: {config_path}")
        if os.path.exists(config_path):
            print("配置文件存在")
            config = configparser.ConfigParser()
            config.read(config_path)
            print("配置内容:")
            print(config.sections())
        else:
            print("配置文件不存在")
    
    if not args.command:
        print_usage()
        return
        
    argv = [args.command] + args.args  # 组合命令和参数
    api = AliyunDriveApi()

    if argv[0] == 'list':
        path = argv[1] if len(argv) > 1 else 'root'
        if path == 'root':
            files = api.list_files()
        else:
            file_info = api.get_file_by_path(path)
            if not file_info:
                print(f"未找到文件夹: {path}")
                return
            if file_info['type'] != 'folder':
                print(f"'{path}' 不是文件夹")
                return
            files = api.list_files(file_info['file_id'])

        if not files:
            print("\n当前文件夹为空")
            print("\n提示:")
            print("1. 使用 'aliyundrive upload 文件路径' 上传文件到当前目录")
            print("2. 使用 'aliyundrive list' 返回根目录")
            print("3. 使用 'aliyundrive search 关键词' 搜索文件")
        else:
            print(f"\n共找到 {len(files)} 个文件/文件夹:")
            print("=" * 50)
            for i, file in enumerate(files, 1):
                api.print_file_info(file, index=i)
                print("-" * 50)
            print("\n提示: ")
            print("1. 使用文件/文件夹���称进行操作")
            print("2. 下载文件示例: aliyundrive download \"文件名\"")
            print("3. 查看文件夹内容示例: aliyundrive list \"文件夹名\"")
            print("4. 如果找不到想要的文件，可以使用 'aliyundrive search 关键词' 搜索")
    elif argv[0] == 'upload':
        if len(argv) == 2:
            api.upload_folders(argv[1])
        elif len(argv) == 3:
            api.upload_folders(argv[1], argv[2])
        else:
            print_usage()
    elif argv[0] == 'download':
        if len(argv) == 2:
            api.download_by_path(argv[1])
        elif len(argv) == 3:
            api.download_by_path(argv[1], argv[2])
        else:
            print_usage()
    elif argv[0] == 'search':
        if len(argv) != 2:
            print_usage()
        else:
            keyword = argv[1]
            print(f"\n正在搜索: {keyword}")
            files = api.search_file(keyword)
            if not files:
                print(f"\n未找到包含 '{keyword}' 的文件或文件夹")
                print("\n提示:")
                print("1. 尝试使用不同的关键词")
                print("2. 关键词不区分大小写")
                print("3. 可以使用 'aliyundrive list' 浏览所有文件")
            else:
                print(f"\n共找到 {len(files)} 个匹配项:")
                print("=" * 50)
                for i, file in enumerate(files, 1):
                    api.print_file_info(file, index=i)
                    print("-" * 50)
    else:
        print_usage()


if __name__ == '__main__':
    main() 