#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: test_htmlparse.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/10 00:04:01
"""
import unittest
import sys
import os

sys.path.append('../')
import htmlParse

class TestHtmlParse(unittest.TestCase):
    """
    对 htmlParse.HtmlParse 类进行单元测试
    """
    
    def setUp(self):
        content = """
            <html>
                <a class="dropdown-menu" style="width:45px" title="腾 讯" href="http://www.qq.com/" _hover-ignore="1">腾 讯</a>
                <img class="" src="http://img.firefoxchina.cn/2016/07/4/201607010831530.jpg">
            </html>
        """
        ddict = {'a':'href', 'img':'src', 'link':'href', 'script':'src'}
        self.htmlparse = htmlParse.HtmlParser(content, 'html5lib', ddict, 'www.baidu.com')

    def test_extract_url(self):
        """
        test In for extract_url function
        """
        self.assertIn('http://img.firefoxchina.cn/2016/07/4/201607010831530.jpg', 
                       self.htmlparse.extract_url()
                       )

    def tearDown(self):
        self.htmlparse = None

if __name__ == '__main__':
    unittest.main()
