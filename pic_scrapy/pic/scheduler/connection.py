#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/11/3 14:27
@annotation = '' 
"""

import redis


def get_redis(redis_config):
    DEFAULT_PARAMS = {
        'socket_timeout': 30,
        'socket_connect_timeout': 30,
        'retry_on_timeout': True,
    }
    redis_config.update(DEFAULT_PARAMS)
    return redis.StrictRedis(**redis_config)
