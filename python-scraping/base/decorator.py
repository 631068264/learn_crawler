#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

from base import smartpool


def db_conn(db_name):
    def deco(old_handler):
        @wraps(old_handler)
        def new_handler(*args, **kwargs):
            kwargs[db_name] = smartpool.ConnectionProxy(db_name)
            return old_handler(*args, **kwargs)

        return new_handler

    return deco
