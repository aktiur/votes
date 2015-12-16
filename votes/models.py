# -*- coding: utf-8 -*-
__author__ = 'Arthur Cheysson <arthur.cheysson@opusline.fr>'

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, String


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)

