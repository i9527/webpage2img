    #!/usr/bin/python

# -*- coding: utf-8 -*-

from selenium import webdriver
import unittest
import fileutil
import sys
import time
import os
import pictureutil


filelist = []

def save_url(driver, url, dir):
    index = 0
    driver.get(url)
    title_element = driver.find_element_by_xpath("//div//h2[@class='rich_media_title']")
    if title_element == None:
        return 
    title = title_element.text
    pic_path = os.path.join(dir, title)
    fileutil.mkdirs_if_not_exist(pic_path)

    

    all_height = driver.execute_script("return document.body.scrollHeight")
    screen_height = driver.execute_script("return window.innerHeight")
    num = int(all_height / (screen_height))

    for i in range(0, num):
        time.sleep(1)
        pic_name = str(i) + '.png'
        driver.save_screenshot(os.path.join(pic_path,pic_name))
        height = screen_height * (i + 1)
        js = "window.scrollTo(0,%d)" % (height)
        driver.execute_script(js)
    return os.path.abspath(pic_path),title
    
    
def package_picture(dir, save_path, pic_name):
    
    
    list = os.listdir(dir)
    list.sort()
    pic_dir = dir
    pic_list = os.listdir(pic_dir)
    pic_list.sort()
    save_file = os.path.join(save_path, pic_name + '.png')
    pictureutil.merge_pic(pic_dir, pic_list, os.path.abspath(save_file))

def init_filelist():
    f = open('./test.txt', 'r')
    for line in open('./test.txt'):
        line = f.readline()
        if line == '' or line == '\n':
            continue
        filelist.append(line)


if __name__ == '__main__':
    init_filelist()
    driver = webdriver.Chrome()
    dir = './result'
    
    for item in filelist:
        try:
            pic_path,title = save_url(driver, item, dir)
            package_picture(pic_path, os.path.abspath(dir), title)
        except Exception as e :
            print(e)
            
    
           

    