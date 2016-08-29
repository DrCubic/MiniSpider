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
import re

sys.path.append('../')
import crawl_thread
import mini_spider

class TestCrawlThread(unittest.TestCase):
    """
    对 crawl_thread.CrawlerThread 类进行单元测试
    """

    def setUp(self):

        mini_spider_ = mini_spider.MiniSpider('../spider.conf')
        url_pattern = re.compile('.*.jpg')
        args_dict = {}
        args_dict['output_dir'] = './urls'
        args_dict['crawl_interval'] = 1
        args_dict['crawl_timeout'] = 1
        args_dict['url_pattern'] = url_pattern
        args_dict['max_depth'] = 1
        args_dict['tag_dict'] = {}

        self.crawlthread = crawl_thread.CrawlerThread('thread - 0',
                                                mini_spider_.process_request,
                                                mini_spider_.process_response,
                                                args_dict)

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

    def test_save_target(self):
        """
        test True for save_target() function
        """
        url = 'http://img.firefoxchina.cn/2016/07/4/201607010831530.jpg'
        self.assertTrue(self.crawlthread.save_target(url))

    def tearDown(self):
        self.crawlthread = None
        self.configargs = None

if __name__ == '__main__':
    unittest.main()
