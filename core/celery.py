#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery import Celery

# create app to use task
app = Celery('celery_crawler', include=[
    'core.tasks',
])

app.config_from_object('core.config')
