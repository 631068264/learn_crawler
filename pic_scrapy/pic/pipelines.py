# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import scrapy
from pic.items import ProxyItem, PhotoItem
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
from util.smartsql import QS, T


class MysqlPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8',
            use_unicode=True,
        )
        dbargs.update(settings.getdict("MYSQL_CONFIG"))
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._insert, item)
        d.addErrback(self._handle_error, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _exexcute(self, txn, sql, params):
        txn.execute(sql, params)

    def _insert(self, txn, item):
        if isinstance(item, ProxyItem):
            self._handle_proxy(txn, item)
        elif isinstance(item, PhotoItem):
            self._handle_photo(txn, item)

    def _handle_photo(self, txn, item):
        self._exexcute(txn, *QS(T.photo).insert(item))

    def _handle_proxy(self, txn, item):
        self._exexcute(txn, *QS(T.proxy).insert(item, ignore=True))

    def _handle_error(self, failure, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        spider.log.err(failure)


class ImageDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item.get("img_url", None) is not None:
            yield scrapy.Request(item["img_url"], meta={'item': item})

    def item_completed(self, results, item, info):
        if not isinstance(item, (PhotoItem)):
            return item
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta["item"]
        image_guid = request.url.split("/")[-1]
        filename = "%s/%s/%s" % (item["photo_name"], item["charter_name"], image_guid)
        item["img_url"] = filename
        return filename
