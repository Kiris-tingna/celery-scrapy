#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
import datetime


class MongoPipeline(object):
    """Pushes serialized item into mongodb"""

    def __init__(self, address='localhost', port=27017, database='PythonScrapy', collection='jd_spider'):
        self.db = pymongo.MongoClient(address, port).connection[database]
        self.collection = self.db[collection]

    def process_item(self, data: dict):
        for i in data:
            i.update({'created_at': datetime.datetime.utcnow()})

        self.collection.insert_many(data)
        return True


class PicturePipeline(object):
    def __init__(self):
        pass

    def process_item(self, path, data):
        if data.status_code == 200:
            with open('./data/{}'.format(path), 'wb') as f:
                for chunk in data:
                    f.write(chunk)
