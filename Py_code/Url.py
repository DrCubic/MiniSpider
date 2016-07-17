#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: Url.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/08 13:38:05
"""

class Url(object):
    """
    this class is used for encapsulating url and depth

    Attributes:
        url   : string of url 
        depth : depth of the url
    """

    def __init__(self, url, depth=0):
        self.__url = url
        self.__depth = depth

    def get_url(self):
        """
        get Url-object's url
        """
        return self.__url

    def get_depth(self):
        """
        get Url-object's depth
        """
        return self.__depth