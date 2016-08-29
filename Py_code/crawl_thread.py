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
import time
import os

import downloader
import html_parser

class CrawlerThread(threading.Thread):
    """
    This class is a crawler thread for crawling pages by breadth-first-crawling

    Attributes:
        process_request : 前期回调函数
        process_response: 后期回调函数
        output_dir      : 存放target 目录
        crawl_interval  : 爬取间隔
        crawl_timeout   : 爬取时间延迟
        target_url      : 目标文件链接格式
        max_depth       : 爬取最大深度
        tag_dict        : 链接标签字典
    """
    def __init__(self, name, process_request, process_response, args_dict):

        super(CrawlerThread, self).__init__(name=name)
        self.process_request = process_request
        self.process_response = process_response
        self.output_dir = args_dict['output_dir']
        self.crawl_interval = args_dict['crawl_interval']
        self.crawl_timeout = args_dict['crawl_timeout']
        self.url_pattern = args_dict['url_pattern']
        self.max_depth = args_dict['max_depth']
        self.tag_dict = args_dict['tag_dict']

    def run(self):
        """
        线程执行的具体内容
        """
        while 1:
            url_obj = self.process_request()
            time.sleep(self.crawl_interval)

            logging.info('%-12s  : get a url  in depth : ' %
                         threading.currentThread().getName() + str(url_obj.get_depth()))

            if self.is_target_url(url_obj.get_url()):
                flag = -1
                if self.save_target(url_obj.get_url()):
                    flag = 1
                self.process_response(url_obj, flag)
                continue

            if url_obj.get_depth() < self.max_depth:
                downloader_obj = downloader.Downloader(url_obj, self.crawl_timeout)
                response, flag = downloader_obj.download() #flag = 0 or -1

                if flag == -1: # download failed
                    self.process_response(url_obj, flag)
                    continue

                if flag == 0: # download sucess
                    content = response.read()
                    url = url_obj.get_url()
                    soup = html_parser.HtmlParser(content, self.tag_dict, url)
                    extract_url_list = soup.extract_url()

                    self.process_response(url_obj, flag, extract_url_list)
            else:
                flag = 2  # depth > max_depth 的正常URL
                self.process_response(url_obj, flag)

    def is_target_url(self, url):
        """
        判断url 是否符合TargetUrl的形式

        Args:
            url : 被用来判断的url

        Returns:
            True/False : 符合返回True 否则返回False
        """
        found_aim =self.url_pattern.match(url)
        if found_aim:
            return True
        return False

    def save_target(self, url):
        """
        save targetUrl-page into outputDir

        Args:
            response : 页面返回file-object

        Returns:
            none
        """
        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

        file_name = urllib.quote_plus(url)
        if len(file_name) > 127:
            file_name = file_name[-127:]
        target_path = "{}/{}".format(self.output_dir, file_name)
        try:
            urllib.urlretrieve(url, target_path)
            return True
        except IOError as e:
            logging.warn(' * Save target Faild: %s - %s' % (url, e))
            return False
