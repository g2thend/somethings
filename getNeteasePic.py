#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/1/31 下午9:15  

from selenium import webdriver
from PIL import Image
import time, random


def get_small_pic(url):
    driver = webdriver.PhantomJS()
    # driver.get('https://music.163.com/#/song?id=521784134')
    driver.get(url)
    driver.switch_to.frame('g_iframe')
    time.sleep(random.randint(3, 5))
    for i in range(1, 7):
        src_pic_save = "/home/xxx/桌面/netease/"
        src_pic_target = "{}src{}.png".format(src_pic_save, i)
        # print(src_pic_target)
        if i < 6:
            button = driver.find_elements_by_class_name("zpg{}".format(i))
            button[0].click()
        else:
            button = driver.find_elements_by_class_name("zpg5")
            button[0].click()
        time.sleep(random.randint(3, 5))
        driver.save_screenshot(src_pic_target)
        # element = driver.find_elements_by_class_name("itm")
        element = driver.find_elements_by_class_name("itm")
        cut_every_pic(src_pic_target, element, src_pic_save, i)


def cut_every_pic(sourcepath, elments, savepath, src_index):
    i = 1
    for index, cut_element in enumerate(elments):
        # small_pic_path = "{}pic{}x{}.png".format(savepath, src_index, index)
        n = "%02d" % i
        small_pic_path = "{}pic{}{}.png".format(savepath, src_index, n)
        left = cut_element.location['x'] + 53
        top = cut_element.location['y']
        right = cut_element.location['x'] + cut_element.size['width'] + 62
        bottom = cut_element.location['y'] + cut_element.size['height']
        # print(left, top, right, bottom)
        im = Image.open(sourcepath)
        im = im.crop((left, top, right, bottom))
        im.save(small_pic_path)
        i = i + 1


if __name__ == '__main__':
    # get_small_pic("https://music.163.com/#/song?id=521784134")
    get_small_pic("https://music.163.com/#/song?id=521784134")









