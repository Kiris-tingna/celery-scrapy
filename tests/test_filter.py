#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from spider.filter import BloomFilter


class TestFilter(unittest.TestCase):
    """
    TestCase
    """

    def test_filter(self):
        bf = BloomFilter(host='localhost', port=6379, db=3)
        if bf.isContains('http://www.baidu.com/2'):  # 判断字符串是否存在
            print('exists!')
        else:
            print('not exists!')
            bf.insert('http://www.baidu.com')
            bf.insert('http://www.baidu.com/2')
            bf.insert('http://www.baidu.com/3')
