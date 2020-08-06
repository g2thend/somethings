#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 下午8:47 6月/26日/2020年
# @Author  : yon
# @Email   : @qq.com
# @File    : sql.py


from collections import Counter

from sqlalchemy import func

from lagouSpider.creat_lagou_tables import Lagoutables
from lagouSpider.creat_lagou_tables import Session



# 这里是为了获取指定的格式,以便在高德地图上展示
def get_for():
    mysql_session = Session()
    query_result = mysql_session.query(Lagoutables).order_by(Lagoutables.id)
    for job in query_result:
        # print(job.longitude, job.latitude, job.companyShortName, job.salary)
        # {title: "名称：中通服", point: "116.432859,39.926202", address: "中同服", tel: "18500000000"}
        ll = '"{},{}"'.format(job.longitude, job.latitude)
        one = 'title: "{}", point: {}, company: "{}", workYear: "{}", salary: "{}"'.format(job.positionName, ll, job.companyShortName,job.workYear, job.salary)
        print('{' + one + '},')


if __name__ == '__main__':
    get_for()
