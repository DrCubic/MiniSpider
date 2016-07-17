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
import miniSpider
import configArgs

class TestMiniSpider(unittest.TestCase):
    """
    对 miniSpider.MiniSpider 类进行单元测试
    """

    def setUp(self):
        self.minispider = miniSpider.MiniSpider('spider.conf')

    def test_initialize(self):
        """
        test True for conf_is_exist() function
        """
        os.chdir('../')
        self.assertTrue(self.minispider.Initialize())

    def tearDown(self):
        self.minispider = None


if __name__ == '__main__':
    unittest.main()