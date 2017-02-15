#!/usr/bin/env python
# -*- coding: utf-8 -*-

BROKER_URL = 'redis://127.0.0.1:6379/1'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'
CELERY_TASK_SERIALIZER = 'json'

# CELERY_ANNOTATIONS = {
#     'tasks.crawler': {'rate_limit': '600/m'}
# }
