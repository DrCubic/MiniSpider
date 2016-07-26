#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: html_parser.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/09 10:37:33
"""
import urlparse
import logging

import bs4
import chardet

class HtmlParser(object):
    """
    This class is used for parsing html to extract urls 

    Attributes:
        content       : 带解析的html源码
        link_tag_dict : 待解析的标签
        url           : 带解析页面所处的url
    """

    def __init__(self, content, link_tag_dict, url):
        self.link_tag_dict = link_tag_dict
        self.content = content
        self.url = url

    def extract_url(self):
        """
        extract urls from html according to link_tag_dict

        Returns:
            extract_url_list : urls extracted from html
        """
        extract_url_list = []
        if not self.enc_to_utf8():
            return extract_url_list

        host_name = urlparse.urlparse(self.url).netloc
        soup = bs4.BeautifulSoup(self.content, 'html5lib')

        for tag, attr in self.link_tag_dict.iteritems():
            all_found_tags = soup.find_all(tag)
            for found_tag in all_found_tags:
                if found_tag.has_attr(attr):
                    extract_url = found_tag.get(attr).strip()

                    if extract_url.startswith("javascript") or len(extract_url) > 256:
                        continue

                    if not (extract_url.startswith('http:') or extract_url.startswith('https:')):
                        extract_url = urlparse.urljoin(self.url, extract_url)

                    extract_url_list.append(extract_url)

        return extract_url_list

    def detect_encoding(self):
        """
        检测html文本编码

        Returns:
            encode_name / None :能检测出来返回编码名字，否则返回None 
        """
        if isinstance(self.content, unicode):
            return 'unicode'

        try:
            encode_dict = chardet.detect(self.content)
            encode_name = encode_dict['encoding']
            return encode_name
        except Exception as e:
            logging.error(' * Error coding-detect: %s' % e)
            return None

    def enc_to_utf8(self):
        """
        将文本编码转为utf8

        Returns:
            True / False : 能正常转为utf-8则返回True，否则返回False
        """
        encoding = self.detect_encoding()
        try:
            if encoding is None:
                return False

            elif encoding.lower() == 'unicode':
                self.content = self.content.encode('utf-8')
                return True

            elif encoding.lower() == 'utf-8':
                return True

            else:
                self.content = self.content.decode(encoding, 'ignore').encode('utf-8')
                return True
        except UnicodeError as e:
            logging.warn(' * EncodingError - %s - %s:' % (self.url, e))
            return False
        except UnicodeEncodeError as e:
            logging.warn(' * EncodingError - %s - %s:' % (self.url, e))
            return False
        except UnicodeDecodeError as e:
            logging.warn(' * EncodingError - %s - %s:' % (self.url, e))
            return False
        except Exception as e:
            logging.warn(' * EncodingError - %s - %s:' % (self.url, e))
            return False
