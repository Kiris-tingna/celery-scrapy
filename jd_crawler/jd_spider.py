#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from spider import Spider


class JdSpider(Spider):
    rules = ()

    start_urls = ['http://jandan.net/ooxx']

    def parse(self, response: BeautifulSoup):
        """
        需要解析的数据
        :param response:
        """
        for g in response.find_all('a', 'view_img_link'):
            my_url = 'http:{url}'.format(url=g.get('href'))
            yield my_url

    def db(self, response: BeautifulSoup):
        """
        需要存储的数据
        :param response:
        """
        # try:
        #     for g in response.find_all(''):
        #         yield g.get
        # except Exception as ex:
        #     self.log(ex.__str__())
        pass

    def exactor_links(self, response: BeautifulSoup):
        return ['{url}'.format(url=response.find('a', 'previous-comment-page').get('href'))]
