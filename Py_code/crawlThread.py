#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: crawlThread.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/08 19:47:41
"""
import threading
import time
import Queue
import urllib2
import socket
import logging
import urlparse
import urllib
import re
import os

import termcolor

import log
import Url
import htmlParse

class CrawlerThread(threading.Thread):
    """
    This class is a crawler thread for crawling pages by breadth-first-crawling

    Attributes:
        checking_url : 存放待爬URL的队列
        checked_url  : 存放已经爬取过URL的队列
        dead_thread  : 存放已死的线程名字
        error_url    : 存放访问出错URL的队列
        config_args   : 存放配置参数的参数对象
    """

    def __init__(self, name, checking_url, dead_thread, checked_url, error_url, config_args):
        super(CrawlerThread, self).__init__(name=name)
        self.checking_url = checking_url
        self.dead_thread = dead_thread
        self.checked_url = checked_url
        self.error_url = error_url
        self.config_args = config_args

    def run(self):
        """
        线程执行的具体内容

        Args:
            none

        Returns:
            none
        """
        while 1:
            try:
                thread_name = threading.currentThread().getName()
                i = self.checking_url.get(timeout=self.config_args.get_crawl_timeout())
            except Queue.Empty as e:
                if self.thread_is_end():
                    self.dead_thread.put_nowait(threading.currentThread().getName())
                    self.dead_thread.task_done()
                    logging.info('%-15s Exited ...' % thread_name)
                    print '%-15s Exited ...' % thread_name
                    break
                else:
                    continue

            if self.is_visited(i):
                continue

            while not self.dead_thread.empty() and not self.thread_is_end():
                deaded_thread_name = self.dead_thread.get(0.5)
                thread = CrawlerThread(deaded_thread_name, 
                                        self.checking_url, 
                                        self.dead_thread, 
                                        self.checked_url, 
                                        self.error_url, 
                                        self.config_args
                                        )
                thread.setDaemon(True)
                thread.start()
                print ("第%s个线程开始工作") % deaded_thread_name
                logging.info(("第%s个线程开始工作") % deaded_thread_name)

            # print ('%-80s%-50s' % (i.get_url(), str(i.get_depth())))
            logging.info('%-12s  : get a url  in depth : ' % thread_name + str(i.get_depth()))
           
            response = self.downloading(i)
            self.get_next(response)

    def is_target_url(self, url):
        """
        判断url 是否符合TargetUrl的形式

        Args:
            url : 被用来判断的url

        Returns:
            True/False : 符合返回True 否则返回False
        """
        aim_pa = re.compile(self.config_args.get_target_url(), re.S)
        found_aims = re.findall(aim_pa, url)   
        if len(found_aims) > 0:
            return True
        return False      

    def thread_is_end(self):
        """
        判断线程是否运行完毕

        Args:
            None

        Returns:
            True/False - 所有线程爬取完毕返回True，否则返回False
        """
        if not self.checking_url.empty():
            return False

        return True  

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

    def save_target(self, response):
        """
        save targetUrl-page into outputDir

        Args:
            response : 页面返回file-object

        Returns:
            none
        """
        if not os.path.isdir(self.config_args.get_output_dir()):
            os.mkdir(self.config_args.get_output_dir())

        file_name = urllib.quote_plus(response.geturl())
        pic_path = "{}/{}".format(self.config_args.get_output_dir(), file_name)
        with open(pic_path, 'wb') as f:
            f.write(response.read())

    def downloading(self, url_obj):
        """
        检查url_obj 是否可以被访问，若能访问则放入Checked_Url , 若不能访问则放入Error_Url
        
        Args:
            url_obj : Url 实例

        Returns:
            response 对象  :   URL 访问成功
            None          :   URL 访问失败
        """
        if url_obj.get_depth() > self.config_args.get_max_depth():
            return None

        # starting downloading for try_times
        for i in range(self.config_args.get_try_times()):
            try:
                timeout = self.config_args.get_crawl_timeout()
                response = urllib2.urlopen(url_obj.get_url(), timeout=timeout)
                response.depth = url_obj.get_depth()
                self.checked_url.append(url_obj)        #  page visited put into Checked_Url
                return response

            except urllib2.URLError as e:
                if i == self.config_args.get_try_times() - 1:
                    error_info = '* Downloading failed for urllib2.URLError : ' \
                                                                    + url_obj.get_url()
                    
            except UnicodeEncodeError as e:
                if i == self.config_args.get_try_times() - 1:
                    error_info = '* Downloading failed for UnicodeEncodeError : ' \
                                                                    + url_obj.get_url()
                    
            except urllib2.HTTPError as e:
                if i == self.config_args.get_try_times() - 1:
                    error_info = '* Downloading failed for urllib2.HTTPError : ' \
                                                                    + url_obj.get_url()
            
            except socket.timeout as e:
                if i == self.config_args.get_try_times() - 1:
                    error_info = '* Downloading failed for socket.timeout : '\
                                                                    + url_obj.get_url()

            finally:
                # interval time between two download
                time.sleep(self.config_args.get_crawl_interval())

            logging.warn('try for {}th times'.format(i + 1))
            if i == self.config_args.get_try_times() - 1:
                self.error_url.append(url_obj)               #   page could not visited put into Error_Url
                logging.warn(error_info)
                return None

    def get_next(self, response):
        """
        解析HTML源码，获取下一层URLs 放入Checking_URL，并获取此页面的目标文件,
        抓取图片并保存到固定目录中

        Args:
            response : downloading 函数生成的 页面响应对象，其包含 源码、深度、...

        Returns:
            none
        """
        if response is None:
            return

        # if response url is matched for pattern, then save to local
        if self.is_target_url(response.geturl()):
            self.save_target(response)
            return

        host_name = urlparse.urlparse(response.geturl()).netloc
        next_depth = response.depth + 1

        # depth is beyond config, then stop it
        if next_depth > self.config_args.get_max_depth():
            return

        # parse html for extracting urls
        tag_dict = self.config_args.get_tag_dict()
        soup = htmlParse.HtmlParser(response.read(), 'html5lib', tag_dict, host_name)
        extract_url_list = soup.extract_url()

        # link add into Checking_Url
        for ex_url in extract_url_list:
            next_url_obj = Url.Url(ex_url, next_depth)
            self.checking_url.put_nowait(next_url_obj)
            self.checking_url.task_done()
