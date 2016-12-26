#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/11/3 13:50
@annotation = '' 
"""
from pic.scheduler import connection
from pic.scheduler.dupefilter import RedisDupeFilter
from pic.scheduler.queue import SpiderPriorityQueue
from scrapy.utils.misc import load_object

PERSIST = True
FLUSH_ON_START = False

QUEUE_KEY = '%(spider)s:requests'
DUPEFILTER_KEY = '%(spider)s:dupefilter'


class RedisScheduler(object):
    """Redis-based scheduler"""

    def __init__(self, server, persist, flush_on_start, queue_key,
                 queue_cls, dupefilter_key, dupefilter_cls, stats):
        self.server = server
        self.persist = persist
        self.flush_on_start = flush_on_start

        self.queue_key = queue_key
        self.queue_cls = queue_cls
        self.dupefilter_key = dupefilter_key
        self.dupefilter_cls = dupefilter_cls

        self.stats = stats

    def __len__(self):
        return len(self.queue)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        kwargs = {
            'persist': settings.getbool('SCHEDULER_PERSIST', PERSIST),
            'flush_on_start': settings.getbool('SCHEDULER_FLUSH_ON_START', FLUSH_ON_START),
            'queue_key': settings.get('SCHEDULER_QUEUE_KEY', QUEUE_KEY),
            'queue_cls': load_object(settings.get('SCHEDULER_QUEUE_CLASS')) if settings.get(
                'SCHEDULER_QUEUE_CLASS') else SpiderPriorityQueue,
            'dupefilter_key': settings.get('DUPEFILTER_KEY', DUPEFILTER_KEY),
            'dupefilter_cls': RedisDupeFilter,
            'stats': crawler.stats,
        }
        server = connection.get_redis(settings.getdict("REDIS_CONFIG"))
        return cls(server=server, **kwargs)

    def open(self, spider):
        """
            execute this function when open one spider
        """
        self.spider = spider

        self.queue = self.queue_cls(
            server=self.server,
            spider=self.spider,
            key=self.queue_key % {'spider': spider.name},
        )

        self.df = self.dupefilter_cls(
            server=self.server,
            key=self.dupefilter_key % {'spider': spider.name},
        )

        if self.flush_on_start:
            self.flush()
        # notice if there are requests already in the queue to resume the crawl
        if len(self.queue):
            spider.log("Resuming crawl (%d requests scheduled)" % len(self.queue))

    def close(self, reason):
        if not self.persist:
            self.flush()

    def flush(self):
        self.df.clear()
        self.queue.clear()

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            return False
        if self.stats:
            self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        self.queue.push(request)
        return True

    def next_request(self):
        request = self.queue.pop()
        if request and self.stats:
            self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
        return request

    def has_pending_requests(self):
        return len(self) > 0
