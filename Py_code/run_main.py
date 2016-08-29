#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
File: run_main.py
功能：启动mini_spider
Author: mijianhong(mijianhong@baidu.com)
Date: 2016/07/08 13:29:59
"""
import argparse
import logging

import termcolor

import mini_spider
import log

if __name__ == '__main__':
    """
    主程序,程序入口
    """

    log.init_log('./log/mini_spider')
    logging.info('%-35s' % ' * miniSpider is starting ... ')
    red_on_cyan = lambda x: termcolor.colored(x, 'red', 'on_cyan')
    # *********************************  start  ***********************
    # set args for the program
    parser = argparse.ArgumentParser(description = 'This is a mini spider program!')
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='%(prog)s 1.0.0')

    parser.add_argument('-c',
                        '--config_file',
                        action='store',
                        dest='CONF_PATH',
                        default='spider.conf',
                        help='Set configuration file path')

    args = parser.parse_args()

    # create an instance of miniSpider and start crawling
    print red_on_cyan('* MiniSpider is Staring ... ')
    mini_spider_inst = mini_spider.MiniSpider(args.CONF_PATH)
    init_success = mini_spider_inst.initialize()
    if init_success:
        mini_spider_inst.pre_print()
        mini_spider_inst.run_threads()

    # *********************************** end  **************************
    logging.info('%-35s' % ' * miniSpider is ending ...')
    print red_on_cyan('* MiniSpider is ending ... ')
