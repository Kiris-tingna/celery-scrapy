#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from spider import Spider, settings


class TestSpider(unittest.TestCase):
    def setUp(self):
        self._spider = Spider()

    def tearDown(self):
        pass

    """
    TestCase
    """

    def test_fetch(self):
        status_code, content = self._spider.run('http://jandan.net/ooxx')
        print(status_code)
        print(content)
        # self.assertNotEquals(status_code, -1, 'test fetch fail')
        # self.assertNotEquals(status_code, 0, 'test fetch fail')

    def test_useragent(self):
        headers = settings.DEFAULT_REQUEST_HEADERS
        headers.update({'User-Agent': settings.USER_AGENT})
        print(headers)
