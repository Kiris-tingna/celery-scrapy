#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.celery import app
from celery import group
from spider import BloomFilter, Spider
import pymongo
import datetime

# url 去重装置
bf = BloomFilter(host='localhost', port=6379, db=3)

# 数据库存储
mg = pymongo.MongoClient('localhost', 27017)
mdb = mg.PythonScrapy
mcollection = mdb.jd_spider

# our spider
_spider = Spider()


@app.task
def add(x, y):
    return x + y


@app.task()
def crawler(url: str):
    """
    即是消费者也是产出者
    :param url:
    """
    wanted_urls = []
    need_store = []
    image_urls = []
    # print('crawling: {0}'.format(url))

    urls, need_store, images = _spider.run(url)

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
        wanted_urls.append(_url)

    # 数据库存储
    if need_store:
        mongo_pipeline.delay(need_store)

    # 图片下载
    image_tasks = group(image_pipeline.s(image) for image in image_urls)
    image_tasks()

    sub_tasks = group(crawler.s(url) for url in wanted_urls).skew(start=1)
    sub_tasks()


@app.task
def image_pipeline(url: str):
    _spider.download(url)


@app.task
def mongo_pipeline(data: list):
    for i in data:
        i.update({'created_at': datetime.datetime.utcnow()})
    mcollection.insert_many(data)
