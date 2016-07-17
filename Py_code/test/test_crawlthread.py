#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: test_crawlthread.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/10 10:10:47
"""
import unittest
import Queue
import sys

sys.path.append('../')
import crawlThread
import configArgs
import Url

class TestCrawlThread(unittest.TestCase):
    """
    对 crawlThread.CrawlerThread 类进行单元测试
    """
    
    def setUp(self):
        self.checking_url = Queue.Queue(0)
        self.checked_url = []
        self.error_url = []
        self.dead_thread = Queue.Queue(0)
        self.configargs = configArgs.ConfigArgs('../spider.conf')
        self.configargs.load_from_file()
        self.crawlthread = crawlThread.CrawlerThread('thread', 
                                                    self.checking_url, 
                                                    self.dead_thread, 
                                                    self.checked_url, 
                                                    self.error_url, 
                                                    self.configargs,
                                                    )

    def test_test_is_visited(self):
        """
        test True for is_visited() function
        """
        url_obj = Url.Url('http://www.baidu.com')
        self.checked_url.append(url_obj)
        self.assertTrue(self.crawlthread.is_visited(url_obj))

    def test_test_is_not_visited(self):
        """
        test False for is_visited() function
        """
        url_obj = Url.Url('http://www.baidu.com')
        url_obj_ = Url.Url('http://www.hupu.com')
        self.checked_url.append(url_obj)
        self.assertFalse(self.crawlthread.is_visited(url_obj_))

    def test_not_downloading(self):
        """
        test Equal for downloading() function
        """
        url_obj = Url.Url('http://mi.mi-minus.cn')
        self.assertEqual(self.crawlthread.downloading(url_obj), None)

    def test_downloading(self):
        """
        test NotEqual for downloading() function
        """
        url_obj = Url.Url('http://mi-minus.cn')
        self.assertNotEqual(self.crawlthread.downloading(url_obj), None)

    def test_is_targeturl(self):
        """
        test True fot is_target_url() function
        """
        url = 'http://img.firefoxchina.cn/2016/07/4/201607010831530.jpg'
        self.assertTrue(self.crawlthread.is_target_url(url))

    def test_is_not_targeturl(self):
        """
        test False for is_target_url() function 
        """
        url = 'http://www.baidu.com'
        self.assertFalse(self.crawlthread.is_target_url(url))

    def test_thread_is_end(self):
        """
        test True for thread_is_end() function
        """
        self.assertTrue(self.crawlthread.thread_is_end())

    def test_thread_not_end(self):
        """
        test False for thread_is_end() function
        """
        url_obj = Url.Url('http://www.baidu.com')
        self.crawlthread.checking_url.put(url_obj)
        self.assertFalse(self.crawlthread.thread_is_end())        

    def tearDown(self):
        self.crawlthread = None
        self.configargs = None

if __name__ == '__main__':
    unittest.main()
