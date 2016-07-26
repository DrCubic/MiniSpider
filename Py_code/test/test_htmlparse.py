#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################in
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
import html_parser

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
        self.htmlparser = html_parser.HtmlParser(content, ddict, 'www.baidu.com')

    def test_extract_url(self):
        """
        test In for extract_url function
        """
        url_example = 'http://img.firefoxchina.cn/2016/07/4/201607010831530.jpg'
        self.assertIn(url_example, 
                       self.htmlparser.extract_url()
                       )

    def test_unicode_to_utf8(self):
        """
        test True for func - enc_to_utf8() of unicode_to_utf8
        """
        self.htmlparser.content = u'没事的发水电费'
        self.assertTrue(self.htmlparser.enc_to_utf8())

    def test_gbk_to_utf8(self):
        """
        test True for func - enc_to_utf8() of gbk_to_utf8
        """
        self.htmlparser.content = u'苏打水地方'.encode('gbk')
        self.assertTrue(self.htmlparser.enc_to_utf8())

    def test_utf8_utf8(self):
        """
        test True for func - enc_to_utf8() of utf8_to_utf8
        """
        self.htmlparser.content = u"撒旦法撒旦法".encode('utf-8')
        self.assertTrue(self.htmlparser.enc_to_utf8())

    def tearDown(self):
        self.htmlparser = None

if __name__ == '__main__':
    unittest.main()
