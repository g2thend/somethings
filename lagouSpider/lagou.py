#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/4/15 下午9:07  
# @Author  : yon              
# @Email   : @qq.com
# @File    : lagou.py          


# https://github.com/KeerZhou/crawllagou/blob/master/lagouSpider/crawlTest.py
# https://blog.csdn.net/KeerZhou/article/details/99631869

import requests
import time
import json


def main():
    url_start = "https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput="
    url_parse = "https://www.lagou.com/jobs/positionAjax.json?city=北京&needAddtionalResult=false"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    for x in range(1, 2):
        data = {
            'first': 'true',
            'pn': str(x),
            'kd': '运维'
                }
        s = requests.Session()
        s.get(url_start, headers=headers, timeout=3)  # 请求首页获取cookies
        cookie = s.cookies  # 为此次获取的cookies
        response = s.post(url_parse, data=data, headers=headers, cookies=cookie, timeout=3)  # 获取此次文本
        time.sleep(5)
        response.encoding = response.apparent_encoding
        text = json.loads(response.text)
        info = text["content"]["positionResult"]["result"]
        crawltime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("打印\n")
        for i in info:
            job_desc = {
                        'city': i["city"],
                        'companyFullName': i["companyFullName"],
                        'companyId': i["companyId"],
                        'companyLabelList': i["companyLabelList"],
                        'companyShortName': i["companyShortName"],
                        'companySize': i["companySize"],
                        'district': i["district"],
                        'education': i["education"],
                        'financeStage': i["financeStage"],
                        'firstType': i["firstType"],
                        'industryField': i["industryField"],
                        'isSchoolJob': i["isSchoolJob"],
                        'jobNature': i["jobNature"],
                        'latitude': i["latitude"],
                        'linestaion': i["linestaion"],
                        'longitude': i["longitude"],
                        'positionAdvantage': i["positionAdvantage"],
                        'positionId': i["positionId"],
                        'positionLables': i["positionLables"],
                        'positionName': i["positionName"],
                        'salaryMonth': i["salaryMonth"],
                        'salary': i["salary"],
                        'score': i["score"],
                        'secondType': i["secondType"],
                        'skillLables': i["skillLables"],
                        'stationname': i["stationname"],
                        'subwayline': i["subwayline"],
                        'thirdType': i["thirdType"],
                        'workYear': i["workYear"],
                        'jobTempetation': "",
                        'jobDescribe': "",
                        'jobAddress': "",
                        'site': "https://www.lagou.com/gongsi/{}.html".format(i["companyId"]),
                        'jobSite': "https://www.lagou.com/jobs/{}.html".format(i["positionId"]),
                        'crawltime': crawltime
                        }
            print(job_desc)


if __name__ == '__main__':
    main()