#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: test_configargs.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/12 14:42:30
"""
import unittest
import sys

sys.path.append('../')
import config_args

class TestConfigArgs(unittest.TestCase):
    """
    对 configArgs.ConfigArgs 类进行单元测试
    """

    def setUp(self):
        self.configargs = config_args.ConfigArgs('../spider.conf')

    def test_load_from_file_success(self):
        """
        test True for function load_from_file()
        """
        self.assertTrue(self.configargs.initialize())

    def test_load_from_file_fail(self):
        """
        test False for function load_from_file()
        """
        self.configargs.file_path = 'spider.conf_'
        self.assertFalse(self.configargs.initialize())

    def tearDown(self):
        self.configargs = None
    
if __name__ == '__main__':
    unittest.main()
