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

import log
import Url
import configArgs
import crawlThread

class MiniSpider(object):
    """
    This class is a crawler-master-class for operating serveral crawling threads

    Attributes:
        checking_url : 存放待爬URL的队列
        checked_url  : 存放已经爬取过URL的队列
        dead_thread  : 存放已死的线程名字
        error_url    : 存放访问出错URL的队列
        config_args   : 存放配置参数的参数对象
    """

    def __init__(self, config_file_path='spider.conf',):
        """
        Initialize variables
        """
        self.checking_url = Queue.Queue(0)
        self.checked_url = []
        self.error_url = []
        self.dead_thread = Queue.Queue(0)
        self.config_file_path = config_file_path   

    def Initialize(self):
        """
        Initialize ConfigArgs parameters

        Returns:
            True / False : 相关配置文件正常返回True，否则返回False
        """
        config_args = configArgs.ConfigArgs(self.config_file_path)
        is_load = config_args.load_from_file()
        if not is_load:
            self.program_end('there is no conf file !')
            return False
        self.config_args = config_args

        seedfile_is_exist = self.get_seed_url()
        return seedfile_is_exist

    def pre_print(self):
        """
        MiniSpider 创建时显示配置信息

        Args:
            none

        Returns:
            none
        """
        print termcolor.colored('* MiniSpider Configurations list as follows:', 'green')
        print termcolor.colored('* %-25s : %s' % ('url_list_file   :', 
                                                   self.config_args.get_url_list_file()), 
                                                   'green'
                                                   )

        print termcolor.colored('* %-25s : %s' % ('output_directory:', 
                                                   self.config_args.get_output_dir()), 
                                                   'green'
                                                   )

        print termcolor.colored('* %-25s : %s' % ('max_depth       :', 
                                                  self.config_args.get_max_depth()), 
                                                  'green'
                                                  )

        print termcolor.colored('* %-25s : %s' % ('crawl_interval  :', 
                                                  self.config_args.get_crawl_interval()), 
                                                  'green'
                                                  )

        print termcolor.colored('* %-25s : %s' % ('crawl_timeout   :', 
                                                  self.config_args.get_crawl_timeout()), 
                                                  'green'
                                                  )

        print termcolor.colored('* %-25s : %s' % ('target_url      :', 
                                                   self.config_args.get_target_url()), 
                                                   'green'
                                                   )

        print termcolor.colored('* %-25s : %s' % ('thread_count    :', 
                                                  self.config_args.get_thread_count()), 
                                                  'green'
                                                  )

        print termcolor.colored('* %-25s : %s' % ('try_times       :', 
                                                  self.config_args.get_try_times()), 
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
        if not os.path.isfile(self.config_args.get_url_list_file()):
            logging.error(' * seedfile is not existing !!!')
            self.program_end('there is no seedfile !')
            return False

        with open(self.config_args.get_url_list_file(), 'rb') as f:
            lines = f.readlines()

        for line in lines:
            url_obj = Url.Url(line.strip(), 0)
            self.checking_url.put_nowait(url_obj)
            self.checking_url.task_done()
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

        Args:
            none

        Returns:
            none
        """
        threads_pools = []
        for index in xrange(self.config_args.get_thread_count()):
            thread = crawlThread.CrawlerThread('thread - %d' % index, 
                                                self.checking_url,
                                                self.dead_thread, 
                                                self.checked_url, 
                                                self.error_url, 
                                                self.config_args,)
            thread.setDaemon(True)
            thread.start()
            print termcolor.colored(("第%s个线程开始工作") % index, 'yellow')
            logging.info(("第%s个线程开始工作") % index)
            threads_pools.append(thread)

        while 1:
            if threading.activeCount() <= 1:
                break

        self.checking_url.join()
        self.program_end('normal exits ')