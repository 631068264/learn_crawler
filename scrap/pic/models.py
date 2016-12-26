#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/9/15 18:06
@annotation = '' 
"""
from peewee import Model, CharField, IntegerField, DateField
from pic.db import db


class BaseModel(Model):
    class Meta:
        database = db


class Manga(BaseModel):
    manga_id = IntegerField(unique=True, help_text="漫画id")
    cover_url = CharField(help_text="封面链接")
    view_page = CharField(help_text="漫画链接")
    title = CharField(help_text="漫画标题")
    date = DateField(help_text="发布日期")


class Page(BaseModel):
    manga_id = IntegerField(help_text="漫画id", index=True)
    page_num = IntegerField(help_text="页数")
    img_url = CharField(help_text="图片链接")


def init_db():
    db.drop_tables([Page, Manga], safe=True)
    db.create_tables([Page, Manga], safe=True)


if __name__ == '__main__':
    init_db()
