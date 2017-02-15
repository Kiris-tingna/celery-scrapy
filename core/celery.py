#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery import Celery

# create app to use task
app = Celery('celery_crawler', include=[
    'jd_crawler.jd_tasks',
])

app.config_from_object('core.config')
