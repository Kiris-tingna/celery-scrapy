#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import csv
from core.tasks import add, crawler, mongo_pipeline


class TestCelery(unittest.TestCase):
    """
    TestCase
    """

    # def test_celery(self):
    #     add.delay(1, 2)

    def test_run(self):
        _u = 'https://www.douyu.com/directory/game/DOTA2'
        s = crawler.delay(_u)

        # In Python 3 csv takes the input in text mode, whereas in Python 2 it took it in binary mode.
        with open('data.csv', 'w') as f:
            writer = csv.writer(f, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerows([(_u, r) for r in s.get()])

    def test_store(self):
        data = [
            {'test1': 'sda', 'test2': 'ada'}, {'test1': 'sda', 'test2': 'ada'},
            {'test1': 'sda', 'test2': 'ada'}, {'test1': 'sda', 'test2': 'ada'},
            {'test1': 'sda', 'test2': 'ada'}, {'test1': 'sda', 'test2': 'ada'},
            {'test1': 'sda', 'test2': 'ada'}, {'test1': 'sda', 'test2': 'ada'}
        ]

        mongo_pipeline.delay(data)
