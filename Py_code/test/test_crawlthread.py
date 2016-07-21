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
import crawl_thread
import mini_spider

class TestCrawlThread(unittest.TestCase):
    """
    对 crawl_thread.CrawlerThread 类进行单元测试
    """
    
    def setUp(self):
        
        mini_spider_ = mini_spider.MiniSpider('../spider.conf')
        mini_spider_.output_dir = './urls'
        mini_spider_.crawl_interval = 1
        mini_spider_.crawl_timeout = 1
        mini_spider_.target_url = '.*.jpg'
        mini_spider_.tag_dict = {}

        self.crawlthread = crawl_thread.CrawlerThread('thread - 0', 
                                                mini_spider_.process_request,
                                                mini_spider_.process_response, 
                                                mini_spider_.output_dir,
                                                mini_spider_.crawl_interval,
                                                mini_spider_.crawl_timeout,
                                                mini_spider_.target_url,
                                                mini_spider_.tag_dict)

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

    def tearDown(self):
        self.crawlthread = None
        self.configargs = None

if __name__ == '__main__':
    unittest.main()
