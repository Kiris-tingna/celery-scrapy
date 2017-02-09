#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import random
import requests
from spider.settings import USER_AGENT


class Fetcher(object):
    def __init__(self, header, max_repeat=3, sleep_time=0):
        """
        constructor
        :param max_repeat:
        :param sleep_time:
        """
        self._header = header
        self._max_repeat = max_repeat  # default: 3, maximum repeat fetching time for a url
        self._sleep_time = sleep_time  # default: 0, sleeping time after a fetching for a url
        return

    def run(self, url: str, repeat: int) -> (int, object):

        """
        main fuc
        :type header:
        :param url:
        :param keys:
        :param repeat:
        :return:
        """
        # logging.debug("%s start: keys=%s, repeat=%s, url=%s", self.__class__.__name__, keys, repeat, url)
        time.sleep(random.randint(0, self._sleep_time))

        # 尝试抓取
        try:
            fetch_result, content = self.url_fetch(url, repeat, self._header)
        except Exception as ex:
            # print(ex)
            # 大于最大重复次数
            if repeat >= self._max_repeat:

                fetch_result, content = -1, None
                # logging.error("%s error: %s, keys=%s, repeat=%s, url=%s", self.__class__.__name__, ex, keys, repeat,
                #               url)
            # 其他错误
            else:
                fetch_result, content = 0, None
                # logging.debug("%s repeat: %s, keys=%s, repeat=%s, url=%s", self.__class__.__name__, ex, keys, repeat,
                #               url)

        # 抓取结束
        # logging.debug("%s end: fetch_result=%s, url=%s", self.__class__.__name__, fetch_result, url)
        return fetch_result, content

    def url_fetch(self, url: str, repeat: int, header: dict) -> (int, str, str):
        # 请求参数
        response = requests.get(url, params=None, data=None, headers=header, cookies=None, timeout=(2, 10))

        # if response.history:
        #     logging.debug("%s redirect: keys=%s, repeat=%s, url=%s", self.__class__.__name__, keys, repeat, url)

        # 内容
        return response.status_code, response.text
