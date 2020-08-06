# coding=gbk
import json
import re
import time
import requests
from lagouSpider.mongodb import HandleMongodb
from loguru import logger
from pyquery import PyQuery as pq

proxypool_url = 'http://127.0.0.1:5555/random'


class GetInfoFromProxy(object):
    def __init__(self):
        self.proxy = self.get_random_proxy()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }

    def get_random_proxy(self):
        return requests.get(proxypool_url).text.strip()

    def get_response_from_url(self, url):
        while True:
            proxies = {'http': 'http://' + self.proxy}
            # logger.info("使用代理获取职位细节")
            respon = requests.get(url, proxies=proxies, headers=self.header)
            respon.encoding = "utf8"
            if '页面加载中' in respon.text:
                time.sleep(5)
                print(respon.text)
                logger.debug("重新获取代理")
                self.proxy = self.get_random_proxy()
                continue
            return respon.text


class CrawlLaGou(object):
    def __init__(self):
        self.lagou_session = requests.session()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }
        self.city_list = ""
        self.save_data = HandleMongodb()

    def crawl_city(self):
        city_search = re.compile(r'www\.lagou\.com\/.*\/">(.*?)</a>')
        city_url = "https://www.lagou.com/jobs/allCity.html"
        city_result = self.crawl_request(method="GET", url=city_url)
        self.city_list = city_search.findall(city_result)
        self.lagou_session.cookies.clear()

    @logger.catch
    def crawl_city_job(self, city):
        logger.info(f"start crawl in city: {city}")
        first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput="%city
        first_response = self.crawl_request(method="GET", url=first_request_url)
        total_page_search = re.compile(r'class="span\stotalNum">(\d+)</span>')
        try:
            total_page = total_page_search.search(first_response).group(1)
        except:
            return
        else:
            for i in range(1, int(total_page) + 1):
                data = {
                    "pn": i,
                    "kd": "python"
                }
                logger.info(f'start get the position Ajax page: {i}')
                page_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false" % city
                referer_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput="% city
                self.header['Referer'] = referer_url.encode()
                time.sleep(3)
                get_response = self.crawl_request(method="POST", url=page_url, data=data, info=city)
                lagou_data = json.loads(get_response)
                job_list = lagou_data['content']['positionResult']['result']
                crawltime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                for job in job_list:
                    job_detail = {
                        '_id': job["positionId"],
                        'city': job["city"],
                        'companyFullName': job["companyFullName"],
                        'companyId': job["companyId"],
                        'companyLabelList': job["companyLabelList"],
                        'companyShortName': job["companyShortName"],
                        'companySize': job["companySize"],
                        'district': job["district"],
                        'education': job["education"],
                        'financeStage': job["financeStage"],
                        'firstType': job["firstType"],
                        'industryField': job["industryField"],
                        'isSchoolJob': job["isSchoolJob"],
                        'jobNature': job["jobNature"],
                        'latitude': job["latitude"],
                        'linestaion': job["linestaion"],
                        'longitude': job["longitude"],
                        'positionAdvantage': job["positionAdvantage"],
                        'positionId': job["positionId"],
                        'positionLables': job["positionLables"],
                        'positionName': job["positionName"],
                        'salaryMonth': job["salaryMonth"],
                        'salary': job["salary"],
                        'secondType': job["secondType"],
                        'skillLables': job["skillLables"],
                        'stationname': job["stationname"],
                        'subwayline': job["subwayline"],
                        'thirdType': job["thirdType"],
                        'workYear': job["workYear"],
                        'jobTempetation': "",
                        'jobDescribe': "",
                        'jobAddress': "",
                        'site': "https://www.lagou.com/gongsi/{}.html".format(job["companyId"]),
                        'jobSite': "https://www.lagou.com/jobs/{}.html".format(job["positionId"]),
                        'company_site': "",
                        'investors': "",
                        'crawltime': crawltime
                    }
                    if self.save_data.insert_one(job_detail):
                        logger.info(f'Success save to mongodb-->>job: {job["positionName"]} from company: {job["companyShortName"]}')
                    else:
                        logger.debug("Failed to save data!!!!")

    @logger.catch
    def optimize_job_detail(self):
        logger.info("start get job detail >>>")
        newcrawl = GetInfoFromProxy()
        for job_address in self.save_data.job_site():
            job_url = job_address['jobSite']
            if job_address['jobDescribe']:
                continue
            logger.info(f'get the job site: {job_url}')
            time.sleep(6)
            # referer = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
            # self.header['Referer'] = referer
            # proxy = requests.get("http://127.0.0.1:5555/random").text.strip()
            # proxies = {'http': 'http://' + proxy}
            # job_resp = requests.get(job_url, proxies=proxies, headers=self.header).text

            # new
            job_resp = newcrawl.get_response_from_url(job_url)
            doc = pq(job_resp)
            query_tmp = {
                'jobSite': job_url
            }
            # print(job_resp)
            try:
                job_tempetation = doc('.job-advantage').text().split('\n')[1] if doc('.job-advantage').text().split('\n')[1] else ""
            except:
                logger.debug(f"job_tempetation get wrong")
                print(job_resp)
                continue

            job_describe = doc('.job-detail').text()
            job_address = doc('.work_addr').text().replace('查看地图', '').replace(' ', '')
            company_site = doc('.c_feature_name').text().split(' ')[-1]
            job_detail = {
                'jobTempetation': job_tempetation,
                'jobDescribe': job_describe,
                'jobAddress': job_address,
                'company_site': company_site
            }
            if self.save_data.modify(query_tmp, job_detail):
                logger.info(f"Success job detail optimized from -->>> {job_url}")
            else:
                logger.debug(f"Failed job detail optimized from -->>> {job_url}")

    def crawl_request(self, method, url, data=None, info=None):
        while True:
            if method == "GET":
                response = self.lagou_session.get(url=url, headers=self.header)
            elif method == "POST":
                response = self.lagou_session.post(url=url, headers=self.header, data=data)
            response.encoding = "utf8"
            if '频繁' in response.text or '页面加载中' in response.text:
                print(response.text)
                logger.debug("session Failure, clear and get it again")
                self.lagou_session.cookies.clear()
                first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % info
                self.crawl_request(method="GET", url=first_request_url)
                time.sleep(6)
                logger.debug("jump the stuck page, start to crawl netx page")
                continue
            return response.text


if __name__ == '__main__':
    lagou = CrawlLaGou()
    # lagou.crawl_city_job("北京")
    lagou.optimize_job_detail()
    #lagou.crawl_city()
    #print(lagou.city_list)
    #city = "深圳"
    #lagou.crawl_city_job(city)
    #for city in lagou.city_list:
    #     lagou.crawl_city_job(city)
    #     break
