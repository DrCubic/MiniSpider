#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: crawl_thread.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/08 19:47:41
"""
import threading
import logging
import urllib
import re
import os

import downloader

class CrawlerThread(threading.Thread):
    """
    This class is a crawler thread for crawling pages by breadth-first-crawling

    Attributes:
        checking_url : 存放待爬URL的队列
        checked_url  : 存放已经爬取过URL的队列
        dead_thread  : 存放已死的线程名字
        error_url    : 存放访问出错URL的队列
        config_arg   : 存放配置参数的参数对象
    """
    def __init__(self, name, process_request, process_response, output_dir, crawl_interval, 
                                                                            crawl_timeout, 
                                                                            target_url, 
                                                                            tag_dict):

        super(CrawlerThread, self).__init__(name=name)
        self.process_request = process_request
        self.process_response = process_response
        self.output_dir = output_dir
        self.crawl_interval = crawl_interval
        self.crawl_timeout = crawl_timeout
        self.target_url = target_url
        self.tag_dict = tag_dict    

    def run(self):
        """
        线程执行的具体内容
        """
        while 1:
            url_obj = self.process_request()

            logging.info('%-12s  : get a url  in depth : ' % 
                         threading.currentThread().getName() + str(url_obj.get_depth()))
            print ('%-12s  : get a url  in depth : ' % 
                         threading.currentThread().getName() + str(url_obj.get_depth()))
           
            downloader_obj = downloader.Downloader(url_obj,
                                                   self.crawl_timeout,
                                                   self.crawl_interval)

            response, flag = downloader_obj.downloading() #flag = 0 or -1

            if flag == 0 and self.is_target_url(response.geturl()):
                self.save_target(response)
                flag = 1

            self.process_response(response, url_obj, flag)

    def is_target_url(self, url):
        """
        判断url 是否符合TargetUrl的形式

        Args:
            url : 被用来判断的url

        Returns:
            True/False : 符合返回True 否则返回False
        """
        aim_pa = re.compile(self.target_url, re.S)
        found_aims = re.findall(aim_pa, url)
        if len(found_aims) > 0:
            return True
        return False

    def save_target(self, response):
        """
        save targetUrl-page into outputDir

        Args:
            response : 页面返回file-object

        Returns:
            none
        """
        if response is None:
            return

        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

        file_name = urllib.quote_plus(response.geturl())
        if len(file_name) > 127:
            file_name = file_name[::-1][:127][::-1]
        pic_path = "{}/{}".format(self.output_dir, file_name)
        with open(pic_path, 'wb') as f:
            f.write(response.read())