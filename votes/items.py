# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrutin(scrapy.Item):
    legislature = scrapy.Field()
    identifiant = scrapy.Field()

    intitule = scrapy.Field()

    votes_pour = scrapy.Field()
    votes_contre = scrapy.Field()
    abstention = scrapy.Field()


class Depute(scrapy.Item):
    prenom = scrapy.Field()
    nom = scrapy.Field()

    parti = scrapy.Field()


class Parti(scrapy.Item):
    nom = scrapy.Field()


class Vote(scrapy.Item):
    depute = scrapy.Field()
    scrutin = scrapy.Field()

    position = scrapy.Field()


class Position(scrapy.Item):
    scrutin = scrapy.Field()

    position = scrapy.Field()
    decompte = scrapy.Field()
