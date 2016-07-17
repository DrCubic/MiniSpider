#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: htmlParse.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/09 10:37:33
"""
import urlparse

import bs4

class HtmlParser(bs4.BeautifulSoup):
    """
    This class is used for parsing html to extract urls 

    Attributes:
        content       : 带解析的html源码
        parser        : 解析器
        link_tag_dict : 待解析的标签
        host_name     : html 对应URL-域名
    """

    def __init__(self, content, parser, link_tag_dict, host_name):
        super(HtmlParser, self).__init__(content, parser)
        self.link_tag_dict = link_tag_dict
        self.host_name = host_name

    def extract_url(self):
        """
        extract urls from html according to link_tag_dict

        Returns:
            extract_url_list : urls extracted from html
        """
        extract_url_list = []
        for tag, attr in self.link_tag_dict.iteritems():
            res_list = self.find_all(tag)
            for i in res_list:
                if i.has_attr(attr):
                    extract_url = i.get(attr).strip()

                    if 'javascript' in extract_url or len(extract_url) > 256:
                        continue
                    if not extract_url.startswith('http'):
                        extract_url = urlparse.urljoin('http://' + self.host_name, extract_url)

                    extract_url_list.append(extract_url)

        return extract_url_list