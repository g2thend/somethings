#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 上午9:46 7月/02日/2020年
# @Author  : yon
# @Email   :  @qq.com
# @File    : setting.py


# mongodb  info setting

from loguru import logger

logger.add('runtime.log', level='DEBUG', format="{time:YYYY-MM-DD HH:mm:ss} |  {name} | {line} | {message}", rotation='1 week', retention='20 days')
logger.add('error.log', level='ERROR', format="{time:YYYY-MM-DD HH:mm:ss} |  {name} | {line} | {message}", rotation='1 week')

DB_IP = "192.168.190.134"
DB_NAME = "jobcrawl"
DB_COLLECTION = "lagou"  # pyhon  运维
# DB_COLLECTION = "crawl"   #爬虫
# DB_COLLECTION = "python"   # job Python   test


