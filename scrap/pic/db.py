#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/16 17:39
@annotation = '' 
"""
import redis
from base import config
from playhouse.pool import PooledMySQLDatabase

redis_conn = redis.StrictRedis(
    connection_pool=redis.ConnectionPool(
        **config.redis_config
    )
)

db = PooledMySQLDatabase("pic", **config.db_config)
