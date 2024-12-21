#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置文件处理模块
"""

from configparser import ConfigParser


class Config:
    """配置文件处理类"""

    def __init__(self, config_path):
        """
        初始化配置
        :param config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config = ConfigParser()
        self.config.read(config_path)

        if not self.config.has_section('account'):
            raise ValueError('Must add account section to config.ini')
        if not self.config.has_option('account', 'access_token'):
            raise ValueError('Must add access_token option to account section in config.ini')
        if not self.config.has_option('account', 'refresh_token'):
            raise ValueError('Must add refresh_token option to account section in config.ini')

        self._access_token = self.config.get('account', 'access_token')
        self._refresh_token = self.config.get('account', 'refresh_token')
        self._drive_id = self.config.get('account', 'drive_id', fallback=None)

    @property
    def access_token(self):
        """获取 access_token"""
        return self._access_token

    @property
    def refresh_token(self):
        """获取 refresh_token"""
        return self._refresh_token

    @property
    def drive_id(self):
        """获取 drive_id"""
        return self._drive_id

    def update_access_token(self, access_token):
        """
        更新 access_token
        :param access_token: 新的 access_token
        """
        self._access_token = access_token
        self.config.set('account', 'access_token', access_token)
        self._save_config()

    def update_drive_id(self, drive_id):
        """
        更新 drive_id
        :param drive_id: 新的 drive_id
        """
        self._drive_id = drive_id
        self.config.set('account', 'drive_id', drive_id)
        self._save_config()

    def _save_config(self):
        """保存配置到文件"""
        with open(self.config_path, 'w') as f:
            self.config.write(f) 