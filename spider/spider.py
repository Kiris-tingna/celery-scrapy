# !/usr/bin/env python
# -*- coding: utf-8 -*-
from spider.settings import DEFAULT_REQUEST_HEADERS, USER_AGENT, LOG_FILE
from bs4 import BeautifulSoup
import requests
import logging


class Spider(object):
    # spider name
    name = None

    def __init__(self, name: str = 'default', **kwargs):
        """
        @method: construct
        @useage: Spider(name, config)
        """
        if name is not None:
            self.name = name  # every spider has aname

        elif not getattr(self, 'name', None):
            raise ValueError("{} must have a name".format(type(self).__name__))

        # configure
        self.__dict__.update(kwargs)

        # start_url
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

        self._header = DEFAULT_REQUEST_HEADERS
        self._header.update({'User-Agent': USER_AGENT})

        # logger setting
        logger = logging.getLogger(self.name)
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def __str__(self):
        return "<%s %r at 0x%0x>" % (type(self).__name__, self.name, id(self))

    @property
    def logger(self):
        """
        @method:spider logger
        @useage:Spider.logger.info(str)
        """
        logger = logging.getLogger(self.name)

        return logging.LoggerAdapter(logger, {'spider': self})

    def log(self, message: str, level: int = logging.INFO, **kw):
        """
        @method:Log the given message at the given log level

        This helper wraps a log call to the logger within the spider, but you
        can use it directly (e.g. Spider.logger.info('msg')) or use any other
        Python logger too.

        @useage:Spider.log(str)
        """
        self.logger.log(level, message, **kw)

    def start_requests(self):
        """
        from multi url produce multi request
        @useage: Spider.start_requests(url)
        """
        _items = []
        _data = []
        _links = []

        for url in self.start_urls:
            _i, _d, _l = self.single_requests(url)
            if _i:
                _items.extend(_i)
            if _d:
                _data.extend(_d)
            if _l:
                _links.extend(_l)
        return list(set(_items)), list(set(_data)), list(set(_links))

    def parse(self, response: BeautifulSoup):
        """
        every spdier must implement this method
        @useage:Spider.parse(bs)
        """
        raise NotImplementedError

    def db(self, response: BeautifulSoup):
        raise NotImplementedError

    def exactor_links(self, response: BeautifulSoup):
        """
        every spdier must implement this method
        @useage:Spider.exactor_links(bs)
        """
        raise NotImplementedError

    def single_requests(self, url: str):
        _response = requests.get(url, params=None, data=None, headers=self._header, cookies=None, timeout=(2, 10))

        _bs = BeautifulSoup(_response.text, "html.parser")

        # produce items
        _items = self.parse(_bs)
        _data = self.db(_bs)

        # produce more links
        _links = self.exactor_links(_bs)

        return _items, _data, _links

    def downloader(self, url: str) -> object:
        return requests.get(url, headers=self._header, stream=True)
