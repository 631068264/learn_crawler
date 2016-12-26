#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/11/3 11:13
@annotation = '' 
"""
import time

import redis
from pic.scheduler import connection
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

DEFAULT_DUPEFILTER_KEY = "dupefilter:%(timestamp)s"


class RedisDupeFilter(BaseDupeFilter):
    """Redis-based request duplicates filter.
    This class can also be used with default Scrapy's scheduler.
    """

    def __init__(self, server, key):
        """Initialize the duplicates filter.
        Parameters
        ----------
        server : redis.StrictRedis
            The redis server instance.
        key : str
            Redis key Where to store fingerprints.
        debug : bool, optional
            Whether to log filtered requests.
        """
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, settings):
        """Returns an instance from given settings.
        This uses by default the key ``dupefilter:<timestamp>``. When using the
        ``scrapy_redis.scheduler.Scheduler`` class, this method is not used as
        it needs to pass the spider name in the key.
        Parameters
        ----------
        settings : scrapy.settings.Settings
        Returns
        -------
        RFPDupeFilter
            A RFPDupeFilter instance.
        """
        server = connection.get_redis(settings.getdict("REDIS_CONFIG"))
        # XXX: This creates one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        # TODO: Use SCRAPY_JOB env as default and fallback to timestamp.
        key = DEFAULT_DUPEFILTER_KEY % {'timestamp': int(time.time())}
        return cls(server, key=key)

    @classmethod
    def from_crawler(cls, crawler):
        """Returns instance from crawler.
        Parameters
        ----------
        crawler : scrapy.crawler.Crawler
        Returns
        -------
        RFPDupeFilter
            Instance of RFPDupeFilter.
        """
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        """Returns True if request was already seen.
        Parameters
        ----------
        request : scrapy.http.Request
        Returns
        -------
        bool
        """
        fp = request_fingerprint(request)
        # This returns the number of values added, zero if already exists.
        added = self.server.sadd(self.key, fp)
        return added == 0

    def close(self, reason=''):
        """Delete data on close. Called by Scrapy's scheduler.
        Parameters
        ----------
        reason : str, optional
        """
        self.clear()

    def clear(self):
        """Clears fingerprints data."""
        self.server.delete(self.key)
