#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/5/25 13:59
@annotation = '' 
"""
import os


def deep_update(from_dict, to_dict):
    for (key, value) in from_dict.iteritems():
        if key in to_dict.keys() and \
                isinstance(to_dict[key], dict) and \
                isinstance(value, dict):
            deep_update(value, to_dict[key])
        else:
            to_dict[key] = value


modules = ("default", "my")
current = __name__
for module_name in modules:
    try:
        module = getattr(__import__(current, globals(), locals(),
                                    [module_name]), module_name)
    except AttributeError:
        continue

    module_fg = {}
    for fg in dir(module):
        if fg.startswith("__") and fg.endswith("__"):
            continue
        module_fg[fg] = getattr(module, fg)
    deep_update(module_fg, locals())
