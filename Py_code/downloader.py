#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: downloader.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/18 20:58:17
"""
import urllib2
import time
import socket
import logging

class Downloader(object):
    """
    这个类作为下载器，下载响应url_obj的HTML源码

    Attributes：
        url_obj    : 下载器必需的URL对象
        try_times  : 下载尝试次数
        timeout    : 下载时间延迟
        inteval    : 下载时间间隔
    """
    def __init__(self, url_obj, timeout, interval, try_times=3):
        self.url_obj = url_obj
        self.try_times = try_times
        self.timeout = timeout
        self.interval = interval

    def downloading(self):
        """
        检查url_obj 是否可以被访问，若能访问则放入Checked_Url , 若不能访问则放入Error_Url
        
        Args:
            url_obj : Url 实例

        Returns:
            response 对象  :   URL 访问成功
            None          :   URL 访问失败
        """
        # starting downloading for try_times
        for i in range(self.try_times):
            try:
                response = urllib2.urlopen(self.url_obj.get_url(), timeout=self.timeout)
                response.depth = self.url_obj.get_depth()
                return (response, 0)

            except urllib2.URLError as e:
                if i == self.try_times - 1:
                    error_info = \
                        '* Downloading failed for urllib2.URLError : ' + self.url_obj.get_url()
                    
            except UnicodeEncodeError as e:
                if i == self.try_times - 1:
                    error_info = \
                        '* Downloading failed for UnicodeEncodeError : ' + self.url_obj.get_url()
                    
            except urllib2.HTTPError as e:
                if i == self.try_times - 1:
                    error_info = \
                        '* Downloading failed for urllib2.HTTPError : ' + self.url_obj.get_url()
            
            except socket.timeout as e:
                if i == self.try_times - 1:
                    error_info = \
                        '* Downloading failed for socket.timeout : ' + self.url_obj.get_url()

            except Exception as e:
                if i == self.try_times - 1:
                    error_info = \
                        '* Downloading failed for OtherError : ' + self.url_obj.get_url()

            finally:
                time.sleep(self.interval)

            logging.warn('try for {}th times'.format(i + 1))
            if i == self.try_times - 1:
                logging.warn(error_info)
                return (None, -1)