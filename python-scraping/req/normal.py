#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/10 12:00
@annotation = '' 
"""
import json

import requests

r = requests.get('http://cuiqingcai.com')
print type(r)
print r.status_code
print r.encoding
# print r.text html源码
print r.cookies

payload = {'key1': 'value1', 'key2': 'value2'}
headers = {'content-type': 'application/json'}
r = requests.get("http://httpbin.org/get", params=payload, headers=headers)
print r.url

payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post("http://httpbin.org/post", data=payload)
print r.text

url = 'http://httpbin.org/post'
payload = {'some': 'data'}
r = requests.post(url, data=json.dumps(payload))
print r.json()

# url = 'http://httpbin.org/post'
# files = {'file': open('test.txt', 'rb')}
# r = requests.post(url, files=files)
# print r.text

# with open('massive-body') as f:
#     requests.post('http://some.url/streamed', data=f)



cookies = dict(cookies_are='working')
r = requests.get('http://httpbin.org/cookies', cookies=cookies)
print r.text

s = requests.Session()
s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get("http://httpbin.org/cookies")
print(r.text)

s = requests.Session()
s.headers.update({'x-test': 'true'})
r = s.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
print r.text
