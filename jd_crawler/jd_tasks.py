#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery import group

from core.celery import app
from jd_crawler.jd_spider import JdSpider
from spider import BloomFilter, MongoPipeline, PicturePipeline

# url 去重装置
bf = BloomFilter(host='localhost', port=6379, db=3)

mp = MongoPipeline('localhost', 27017, 'PythonScrapy', 'jd_spider')
pp = PicturePipeline()

# our spider
_spider = JdSpider('jdspider')


@app.task()
def bootstrap():
    # place our wanted url
    wanted_urls = []
    image_urls = []

    images, datas, urls = _spider.start_requests()

    # filter not repeated url
    for _im in images:
        if not bf.isContains(_im):
            bf.insert(_im)
            image_urls.append(_im)

    # filter not repeated url
    for _url in urls:
        if not bf.isContains(_url):
            bf.insert(_url)
            wanted_urls.append(_url)

    sub_tasks = group(crawler.s(url) for url in wanted_urls).skew(start=1)
    sub_tasks()


@app.task()
def crawler(url: str):
    """
    即是消费者也是产出者
    :param url:
    """
    wanted_urls = []
    image_urls = []

    images, datas, urls = _spider.single_requests(url)

    # filter not repeated url
    for _im in images:
        if not bf.isContains(_im):
            bf.insert(_im)
            image_urls.append(_im)

    # filter not repeated url
    for _url in urls:
        if not bf.isContains(_url):
            bf.insert(_url)
            wanted_urls.append(_url)

    # 数据库存储
    if datas:
        mongo_tasks = group(mongo_pipeline.s(data) for data in datas)
        mongo_tasks()

    # 图片下载
    image_tasks = group(image_pipeline.s(image) for image in image_urls)
    image_tasks()

    # 下一个子任务
    sub_tasks = group(crawler.s(url) for url in wanted_urls).skew(start=1)
    sub_tasks()


@app.task()
def image_pipeline(url: str):
    _spider.log('fetched {} success'.format(url))
    pp.process_item(url[-15:], _spider.downloader(url))


@app.task()
def mongo_pipeline(data: dict):
    mp.process_item(data)
