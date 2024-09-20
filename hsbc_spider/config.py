# -*- coding:utf-8
# __author__ : funny
# __create_time__ : 16/11/6 10:41

import configparser

import pymysql

profile_config = configparser.ConfigParser()
profile_config.read('./profile/product.ini')

dbconfig = {
    'host': profile_config.get('mysql', 'host'),
    'port': profile_config.getint('mysql', 'port'),
    'user': profile_config.get('mysql', 'user'),
    'password': profile_config.get('mysql', 'password'),
    'db': profile_config.get('mysql', 'db'),
    'charset': profile_config.get('mysql', 'charset'),
    'cursorclass': pymysql.cursors.DictCursor
}