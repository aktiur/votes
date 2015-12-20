# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrutin(scrapy.Item):
    legislature = scrapy.Field()
    identifiant = scrapy.Field()
    date = scrapy.Field()

    intitule = scrapy.Field()

    nombres_votants = scrapy.Field()
    nombres_exprimes = scrapy.Field()
    nombres_majorite = scrapy.Field()
    votes_pour = scrapy.Field()
    votes_contre = scrapy.Field()
    abstention = scrapy.Field()
    resultat = scrapy.Field()


class Vote(scrapy.Item):
    legislature = scrapy.Field()
    identifiant = scrapy.Field()

    parti = scrapy.Field()

    prenom = scrapy.Field()
    nom = scrapy.Field()

    position = scrapy.Field()


class Position(scrapy.Item):
    legislature = scrapy.Field()
    identifiant = scrapy.Field()

    parti = scrapy.Field()

    membres = scrapy.Field()

    pour = scrapy.Field()
    contre = scrapy.Field()
    abstention = scrapy.Field()
    nonvotants = scrapy.Field()
