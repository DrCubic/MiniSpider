#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
File: test_minispider.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/09 13:57:19
"""
import unittest
import sys
import os

sys.path.append('../')
import mini_spider
import url_object

class TestMiniSpider(unittest.TestCase):
    """
    对 miniSpider.MiniSpider 类进行单元测试
    """

    def setUp(self):
        self.minispider = mini_spider.MiniSpider('spider.conf')

    def test_initialize(self):
        """
        test True for conf_is_exist() function
        """
        os.chdir('../')
        self.assertTrue(self.minispider.initialize())

    def test_not_visited(self):
        """
        test False for func - is_visited()
        """
        url = url_object.Url("http://www.baidu.com")
        self.assertFalse(self.minispider.is_visited(url))

    def test_has_visited(self):
        """
        test True for func - is_visited()
        """
        url = url_object.Url("http://www.baidu.com")
        self.minispider.checked_url.add(url)
        self.assertTrue(self.minispider.is_visited(url))

    def test_has_visited_(self):
        """
        test True for func - is_visited()
        """
        url = url_object.Url("http://www.baidu.com")
        self.minispider.error_url.add(url)
        self.assertTrue(self.minispider.is_visited(url))

    def tearDown(self):
        self.minispider = None


if __name__ == '__main__':
    unittest.main()
