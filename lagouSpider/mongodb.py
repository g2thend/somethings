#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2/19/20 2:24 PM
# @Author  : yon
# @Email   : @qq.com
# @File    : mongodb.py

import pymongo
from lagouSpider.setting import DB_IP, DB_NAME, DB_COLLECTION


class HandleMongodb(object):
    def __init__(self):
        self.dbaddress = 'mongodb://{}:27017/'.format(DB_IP)
        self.dbname = DB_NAME
        self.dbcol = DB_COLLECTION
        self.doc = self.db_isexists()

    def db_isexists(self):
        try:
            my_client = pymongo.MongoClient(self.dbaddress)
            mydb = my_client[self.dbname]
            return mydb[self.dbcol]
        except Exception as e:
            raise Exception("ERROR :init db!")

    def insert_one(self, dic):
        try:
            result = self.doc.insert_one(dic)
            if result.inserted_id:
                return True
            else:
                return False
        except:
            return False

    def insert_many(self, dics):
        try:
            lens = len(dics)
            results = self.doc.insert_many(dics)
            if len(results.inserted_ids) == lens:
                return True
            else:
                return False
        except:
            return False

    def modify(self, query, tochange):
        # moodify one item
        newvalue = {"$set": tochange}
        modifyresult = self.doc.update_one(query, newvalue)
        if modifyresult.modified_count:
            return True
        else:
            return False

    def doc_isexists(self, dic_is_exists):
        if self.doc.find(dic_is_exists).count() > 0:
            return True
        else:
            return False

    def doccounts(self):
        return self.doc.count()

    def job_site(self):
        return self.doc.find({}, {"_id": 0, "jobSite": 1, "jobDescribe": 1})

    def company_site(self):
        return self.doc.find({}, {"_id": 0, "site": 1})

    def get_for_ditu(self):
        return self.doc.find({}, {
                                   '_id': 0,
                                   'companyShortName': 1,
                                   'latitude': 1,
                                   'longitude': 1,
                                   'salary': 1,
                                   'jobSite': 1,
                                   'positionAdvantage': 1,
                                   'companyLabelList': 1
                                  })


if __name__ == '__main__':
    db = HandleMongodb()
    # job = {'city': '北京', 'companyFullName': '北京金山云网络技术有限公司', 'companyId': 956, 'companyLabelList': ['技能培训', '节日礼物', '瑜伽房', '免费班车'], 'companyShortName': '金山云', 'companySize': '2000人以上', 'district': '海淀区', 'education': '本科', 'financeStage': 'D轮及以上', 'firstType': '开发|测试|运维类', 'industryField': '移动互联网,数据服务', 'isHotHire': 0, 'isSchoolJob': 0, 'jobNature': '全职', 'latitude': '40.03674', 'linestaion': '13号线_上地', 'longitude': '116.32274', 'positionAdvantage': '云服务平台', 'positionId': 7362008, 'positionLables': ['云计算'], 'positionName': '主机运维工程师', 'publisherId': 9431917, 'salary': '20k-40k', 'score': 23, 'secondType': '高端技术职位', 'skillLables': [], 'stationname': '上地', 'subwayline': '13号线', 'thirdType': '运维经理', 'workYear': '5-10年', 'jobTempetation': '', 'jobDescribe': '', 'jobAddress': '', 'site': 'https://www.lagou.com/gongsi/956.html', 'jobSite': 'https://www.lagou.com/jobs/7362008.html'}
    # # if db.insert_one(job):
    # #     print("save  data successful")
    #
    # for address in db.job_site():
    #     print(type(address))
    #     print(address['jobSite'])
    # # print(db.doccounts())
    for i in db.get_for_ditu():
        i['title'] = '{},{}'.format(i['longitude'], i['latitude'])
        print(i, ',')










