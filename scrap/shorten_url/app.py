#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/19 14:30
@annotation = '' 
"""
base_list = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
base = len(base_list)


def encode(num: int):
    result = []
    if num == 0:
        result.append(base_list[0])

    while num > 0:
        result.append(base_list[num % base])
        num //= base

    print("".join(reversed(result)))


def decode(code: str):
    num = 0
    code_list = list(code)
    for index, code in enumerate(reversed(code_list)):
        num += base_list.index(code) * base ** index
    print(num)


if __name__ == '__main__':
    encode(341413134141)
    decode("60FoItT")
