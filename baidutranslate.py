#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5:44 PM 3月/13日/2020年
# @Author  : yon
# @Email   : @qq.com
# @File    : baidutranslate


# 百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# coding=utf-8

import http.client
import hashlib
import urllib
import random
import json
from pyquery import PyQuery as pq
import time
import pdfkit


class baidu_Trans:
    def __init__(self):
        self.httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')

    def __del__(self):
        if self.httpClient:
            self.httpClient.close()

    def baidu_translate(self, word):
        appid = '20191207000'  # 填写你的appid
        secretKey = 'mLQDNfTGETpy'  # 填写你的密钥


        myurl = '/api/trans/vip/translate'

        fromLang = 'auto'  # 原文语种
        toLang = 'zh'  # 译文语种
        salt = random.randint(32768, 65536)
        sign = appid + word + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
            word) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

        try:
            time.sleep(1)

            self.httpClient.request('GET', myurl)

            # response是HTTPResponse对象
            response = self.httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            return result.get('trans_result')[0].get('dst')

        except Exception as e:
            return False

    def destory(self):
        if self.httpClient:
            self.httpClient.close()


def american_life(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://cn.bing.com/',
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    doc = pq(url=url, headers=headers)
    article = doc('article')
    title = doc('h1').text().strip().replace(" ", "-")
    sb_baidu = baidu_Trans()
    for i in range(len(article('p'))):
        print("开始翻译\n")
        text = article('p').eq(i).text()
        print(text)
        translate = sb_baidu.baidu_translate(text)
        taged_text = '<pre style="word-wrap:break-word;white-space: pre-wrap;">{}</pre>'.format(translate)
        print(translate)
        article('p').eq(i).append(taged_text)

    sb_baidu.destory()
    dic = {
        "title": title,
        "html": doc('article').html()
    }
    return dic


def create_to_pdf(url):
    html_to_pdf = american_life(url)
    ddoc = '<head><meta charset="UTF-8"></head>{}'.format(html_to_pdf['html'])
    pdfkit.from_string(str(ddoc), "/home/baixiaoxu/desk/{}.pdf".format(html_to_pdf['title']))


if __name__ == '__main__':
    create_to_pdf("https://www.thisamericanlife.org/692/transcript")
