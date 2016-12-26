#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/5/25 14:07
@annotation = '' 
"""
debug = True
encoding = 'utf8'
# MySQL配置
db_config = {
    "db_reader": {"host": "127.0.0.1", "port": 3306, "db": "test",
                  "user": "root", "passwd": "", "charset": encoding},
    "db_writer": {"host": "127.0.0.1", "port": 3306, "db": "test",
                  "user": "root", "passwd": "", "charset": encoding},
}

pool_coroutine_mode = True
pool_log = "pool-log"

db_conn_pool_size = (3, 10)
db_connection_idle = 60
db_pool_clean_interval = 1000
db_query_log = "query-log"

# log_config = [
#     ["pool-log", "pool.log", "debug"],
#     ["query-log", "query.log", "debug"],
# ]
