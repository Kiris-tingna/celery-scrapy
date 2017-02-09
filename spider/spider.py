# !/usr/bin/env python
# -*- coding: utf-8 -*-
from spider.fetch import Fetcher
from spider.settings import DEFAULT_REQUEST_HEADERS, USER_AGENT
from bs4 import BeautifulSoup
import requests


class Spider(object):
    def __init__(self, retry=3, delay=2):
        """

        :type retry: integer    重试次数
        :type delay: integer    下载延时
        """
        self._header = DEFAULT_REQUEST_HEADERS
        self._header.update({'User-Agent': USER_AGENT})
        self._fetcher = Fetcher(self._header, retry, delay)

    def run(self, url: str) -> (list, list, list):
        status, content = self._fetcher.run(url, 1)

        if content is None:
            return [], []
        else:
            _bs = BeautifulSoup(content, "html.parser")

            try:
                parse_code, url_list, mongo_store, save_links = self.parse(_bs)

            except Exception as ex:
                print(ex)
                parse_code, url_list, save_links = -1, [], []

        return url_list, mongo_store, save_links

    def parse(self, beautiful: object) -> (int, list, list, list):
        try:
            next_page = beautiful.find('a', 'previous-comment-page').get('href')
            images = ['http:{url}'.format(url=g.get('href')) for g in beautiful.find_all('a', 'view_img_link')]
        except Exception as ex:
            print(ex)
            # print(beautiful.prettify())
        return 1, ['{next_page}'.format(next_page=next_page)], [], images

    def download(self, url):
        r = requests.get(url, headers=self._header, stream=True)
        if r.status_code == 200:
            with open('./data/{name}'.format(name=url[-15:]), 'wb') as f:
                for chunk in r:
                    f.write(chunk)
