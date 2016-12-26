#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/10/24 11:27
@annotation = '' 
"""
import base64
import random
import re
import urlparse

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class ProxyMiddleware(object):
    def __init__(self, settings=None):
        self.settings = settings
        self.proxies = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('PROXIES'))

    def process_request(self, request, spider):
        if 'proxy' in request.meta or not self.settings:
            return

        for proxy in self.settings:
            scheme, user_pass, hostport = re.match(r'(\w+)://(\w+:\w+@)?(.+)', proxy).groups()
            proxy_url = "%s://%s" % (scheme, hostport)
            creds = base64.encodestring(user_pass[:-1]) if user_pass else None
            self.proxies[scheme] = (creds, proxy_url)

        scheme = urlparse.urlsplit(request.url).scheme
        if scheme in self.proxies:
            self._set_proxy(request, scheme)

    def _set_proxy(self, request, scheme):
        creds, proxy = self.proxies[scheme]
        request.meta['proxy'] = proxy
        if creds:
            request.headers['Proxy-Authorization'] = 'Basic ' + creds


class RandomUserAgent(UserAgentMiddleware):
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


if __name__ == '__main__':
    url = "https://www.baidu.com/s?wd=python%20url%20%E6%8B%86%E5%88%86&rsv_spt=1&rsv_iqid=0xca1d3ec10000e603&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=30&rsv_sug1=24&rsv_sug7=100&rsv_t=47b3%2BQSYxo1ImHj9ZcEzKmoffA7fq1YgKZXATXAVw58inA%2FFdpEIpIUWZm1VyJWT3%2FgV"
    print urlparse.urlsplit(url).scheme
    proxy = "http://USERNAME:PASSWORD@PROXYIP:PROXYPORT"
    # proxy = "http://PROXYIP:PROXYPORT"
    scheme, user_pass, hostport = re.match(r'(\w+)://(\w+:\w+@)?(.+)', proxy).groups()
    print user_pass[:-1]
