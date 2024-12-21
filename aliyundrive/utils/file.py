#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件处理工具模块
"""


class ChunksIter:
    """文件分块迭代器"""

    def __init__(self, file, total_size, chunk_size=1024 * 1024):
        """
        初始化迭代器
        :param file: 文件对象
        :param total_size: 文件总大小
        :param chunk_size: 分块大小，默认1MB
        """
        self.file = file
        self.total_size = total_size
        self.chunk_size = chunk_size

    def __iter__(self):
        return self

    def __next__(self):
        data = self.file.read(self.chunk_size)
        if not data:
            raise StopIteration
        return data

    def __len__(self):
        return self.total_size 