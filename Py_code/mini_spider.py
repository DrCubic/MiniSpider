#!/usr/bin/env python-2.7.3
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: mini_spider.py
功能 ：使用python开发一个迷你定向抓取器 mini_spider.py ，实现对种子链接的广度优先抓取，并把URL格式符合特定pattern的网页保存到磁盘上
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/05 12:04:33
"""
import Queue
import threading
import os
import logging

import termcolor

import html_parser
import url_object
import config_args
import crawl_thread

class MiniSpider(object):
    """
    This class is a crawler-master-class for operating serveral crawling threads

    Attributes:
        checking_url      : 存放待爬URL的队列
        checked_url       : 存放已经爬取过URL的队列
        config_file_path  : 配置文件路径
        error_url         : 存放访问出错URL的队列
        lock              : 线程锁
    """

    def __init__(self, config_file_path='spider.conf'):
        """
        Initialize variables
        """
        self.checking_url = Queue.Queue(0)
        self.checked_url = []
        self.error_url = []
        self.config_file_path = config_file_path
        self.lock = threading.Lock()

    def initialize(self):
        """
        Initialize ConfigArgs parameters

        Returns:
            True / False : 相关配置文件正常返回True，否则返回False
        """
        config_arg = config_args.ConfigArgs(self.config_file_path)
        is_load = config_arg.initialize()
        if not is_load:
            self.program_end('there is no conf file !')
            return False

        self.url_list_file = config_arg.get_url_list_file()
        self.output_dir = config_arg.get_output_dir()
        self.max_depth = config_arg.get_max_depth()
        self.crawl_interval = config_arg.get_crawl_interval()
        self.crawl_timeout = config_arg.get_crawl_timeout()
        self.target_url = config_arg.get_target_url()
        self.thread_count = config_arg.get_thread_count()
        self.tag_dict = config_arg.get_tag_dict()

        seedfile_is_exist = self.get_seed_url()
        return seedfile_is_exist

    def pre_print(self):
        """
        MiniSpider 创建时显示配置信息
        """
        print termcolor.colored('* MiniSpider Configurations list as follows:', 'green')
        print termcolor.colored('* %-25s : %s' % ('url_list_file   :', 
                                                   self.url_list_file), 
                                                   'green'
                                                   )

        print termcolor.colored('* %-25s : %s' % ('output_directory:', 
                                                   self.output_dir), 
                                                   'green'
                                                   )

        print termcolor.colored('* %-25s : %s' % ('max_depth       :', 
                                                  self.max_depth), 
                                                  'green'
                                                  )

        print termcolor.colored('* %-25s : %s' % ('crawl_interval  :', 
                                                  self.crawl_interval), 
                                                  'green'
                                                  )

        print termcolor.colored('* %-25s : %s' % ('crawl_timeout   :', 
                                                  self.crawl_timeout), 
                                                  'green'
                                                  )

        print termcolor.colored('* %-25s : %s' % ('target_url      :', 
                                                   self.target_url), 
                                                   'green'
                                                   )

        print termcolor.colored('* %-25s : %s' % ('thread_count    :', 
                                                  self.thread_count), 
                                                  'green'
                                                  )

    def get_seed_url(self):
        """
        get seed url from seedUrlFile

        Args:
            none

        Returns:
            True / False : 存在种子文件返回True, 否则返回 False
        """ 
        if not os.path.isfile(self.url_list_file):
            logging.error(' * seedfile is not existing !!!')
            self.program_end('there is no seedfile !')
            return False

        with open(self.url_list_file, 'rb') as f:
            lines = f.readlines()

        for line in lines:
            if line.strip() == '':
                continue
                
            url_obj = url_object.Url(line.strip(), 0)
            self.checking_url.put(url_obj)
        return True

    def program_end(self, info):
        """
        退出程序的后续信息输出函数

        Args:
            info : 退出原因信息

        Returns:
            none
        """
        print termcolor.colored('* crawled page num : {}'.format(len(self.checked_url)), 'green')
        logging.info('crawled  pages  num : {}'.format(len(self.checked_url)))
        print termcolor.colored('* error page num : {}'.format(len(self.error_url)), 'green')
        logging.info('error page num : {}'.format(len(self.error_url)))
        print termcolor.colored('* finish_reason  :' + info, 'green')
        logging.info('reason of ending :' + info)
        print termcolor.colored('* program is ended ... ', 'green')
        logging.info('program is ended ... ')
 
    def run_threads(self):
        """
        设置线程池，并启动线程
        """
        for index in xrange(self.thread_count):
            thread = crawl_thread.CrawlerThread('thread - %d' % index, 
                                                self.process_request,
                                                self.process_response, 
                                                self.output_dir,
                                                self.crawl_interval,
                                                self.crawl_timeout,
                                                self.target_url,
                                                self.tag_dict)

            thread.setDaemon(True)
            thread.start()
            print termcolor.colored(("第%s个线程开始工作") % index, 'yellow')
            logging.info(("第%s个线程开始工作") % index)

        self.checking_url.join()
        self.program_end('normal exits ')

    def is_visited(self, url_obj):
        """
        check new url_obj if visited (including Checked_Url and Error_Url)

        Args:
            url_obj : Url 对象

        Returns:
            True / False  -  若访问过则返回 True ，否则返回 False
        """
        checked_url_list = set()

        for url_o in self.checked_url:
            checked_url_list.add(url_o.get_url())
        for url_o in self.error_url:
            checked_url_list.add(url_o.get_url())

        if url_obj.get_url() in checked_url_list:
            return True

        return False  

    def process_request(self):
        """
        线程任务前期处理的回调函数：
            负责从任务队列checking_url中取出url对象

        Returns:
            url_obj : 取出的url-object 对象
        """
        url_obj = self.checking_url.get()
        return url_obj

    def process_response(self, response, url_obj, flag):
        """
        线程任务后期处理回调函数：
            解析HTML源码，获取下一层URLs 放入checking_url

        Args:
            response : downloading 函数生成的 页面响应对象，其包含 源码、深度、...
            url_obj  : 被下载页面所处的url链接对象
            flag     : 页面下载具体情况的返回标志 
                     - 0  : 表示下载成功且为非pattern页面
                     - 1  : 表示下载成功且为符合pattern的图片
                     - -1 : 表示页面下载失败
        """
        if self.lock.acquire():
            if flag == -1: 
                self.error_url.append(url_obj)

            elif flag == 0: 
                self.checked_url.append(url_obj)

                if response.depth < self.max_depth:
                    # parse html for extracting urls
                    content = response.read()
                    url = url_obj.get_url()

                    soup = html_parser.HtmlParser(content, self.tag_dict, url)
                    extract_url_list = soup.extract_url()

                    # link add into Checking_Url
                    for ex_url in extract_url_list:
                        next_url_obj = url_object.Url(ex_url, response.depth + 1)
                        if not self.is_visited(next_url_obj):
                            self.checking_url.put(next_url_obj)

            elif flag == 1: 
                self.checked_url.append(url_obj)
            self.checking_url.task_done()
        self.lock.release()