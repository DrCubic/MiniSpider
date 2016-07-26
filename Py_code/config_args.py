#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: config_args.py
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/08 13:53:12
"""
import ConfigParser
import logging

class ConfigArgs(object):
    """
    This class is used for get all configurations of configure_file   

     Attributes:
        file_path   :  存放配置的文件路径
        config_dict :  存放参数的字典
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.config_dict = {}

    def initialize(self):
        """
        load from configurations from conf_file
        """
        config = ConfigParser.ConfigParser()
        try:
            conf_res = config.read(self.file_path)
        except ConfigParser.MissingSectionHeaderError as e:
            logging.error(' * Config-file error: %s' % e)
            return False
        except Exception as e:
            logging.error(' * Config-file error: %s' % e)
            return False

        if len(conf_res) == 0:
            return False
        try:
            self.config_dict['url_list_file'] = config.get('spider', 'url_list_file').strip()
            self.config_dict['output_directory'] = config.get('spider', 'output_directory').strip()
            self.config_dict['max_depth'] = config.getint('spider', 'max_depth')
            self.config_dict['crawl_timeout'] = config.getfloat('spider', 'crawl_timeout')
            self.config_dict['crawl_interval'] = config.getfloat('spider', 'crawl_interval')
            self.config_dict['target_url'] = config.get('spider', 'target_url').strip()
            self.config_dict['thread_count'] = config.getint('spider', 'thread_count')
            self.config_dict['try_times'] = 3
            self.config_dict['tag_dict'] = {'a':'href', 'img':'src', 'link':'href', 'script':'src'}
        except ConfigParser.NoSectionError as e:
            logging.error(' * Config_File not exists error : No section: \'spider\', %s' % e)
            return False
        except ConfigParser.NoOptionError as e:
            logging.error(' * Config_File not exists error : No option, %s' % e)
            return False
        return True

    def get_url_list_file(self):
        """
        get path of 'seeds-url' file
        """
        return self.config_dict['url_list_file']

    def get_output_dir(self):
        """
        get output-dir for storing pages
        """
        return self.config_dict['output_directory']

    def get_max_depth(self):
        """
        get max-depth of breadth-first crawling
        """
        return self.config_dict['max_depth']

    def get_crawl_timeout(self):
        """
        get downloadings-timeout
        """
        return self.config_dict['crawl_timeout']

    def get_crawl_interval(self):
        """
        get time-interval between downloadings
        """
        return self.config_dict['crawl_interval']

    def get_target_url(self):
        """
        get pattern of target_url
        """
        return self.config_dict['target_url']

    def get_thread_count(self):
        """
        get thread-count for minispider
        """
        return self.config_dict['thread_count']

    def get_try_times(self):
        """
        get attempt times for downloading a web-page
        """
        return self.config_dict['try_times']

    def get_tag_dict(self):
        """
        get pic flag for Url-object
        """
        return self.config_dict['tag_dict']
