"""
阿里云盘 API Python SDK
~~~~~~~~~~~~~~~~~~~~~

一个简单的阿里云盘 API Python 实现。

基本用法:

    >>> from aliyundrive import AliyunDriveApi
    >>> api = AliyunDriveApi()
    >>> api.upload_file("./test.txt")

:copyright: (c) 2024 by __LittleQ__
:license: MIT, see LICENSE for more details.
"""

from .api import AliyunDriveApi

__title__ = 'aliyundrive'
__version__ = '0.1.0'
__author__ = '__LittleQ__' 