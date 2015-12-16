# -*- coding: utf-8 -*-

import scrapy
from votes import items
from scrapy.loader import ItemLoader
import re

__author__ = 'Arthur Cheysson <arthur.cheysson@opusline.fr>'

RE_VOTE = r'([0-9]+)(\*?)'
RE_SCRUTIN_URL = r'\(legislature\)/(?P<legislature>[0-9]+)/\(num\)/(?P<scrutin>[0-9]+)$'
RE_SCRUTIN_DATE = r'[0-9]{2}/[0-9]{2}/[0-9]{4}$'
RE_GROUPE_MEMBRES = r'\(([0-9]+) membres\)$'


class VotesSpider(scrapy.Spider):
    name = "votes"
    allowed_domains = ['assemblee-nationale.fr']

    start_urls = ['http://www2.assemblee-nationale.fr/scrutins/liste/(legislature)/14']

    def __init__(self):
        super(VotesSpider, self).__init__()

        self.re_vote = re.compile(RE_VOTE)
        self.re_scrutin_url = re.compile(RE_SCRUTIN_URL)
        self.re_scrutin_date = re.compile(RE_SCRUTIN_DATE)
        self.re_groupe_membres = re.compile(RE_GROUPE_MEMBRES)

    def parse(self, response):
        for analyse in response.xpath('//table[@id="listeScrutins"]/tbody/tr/td[3]/a[contains(., "analyse")]/@href').extract():
            yield scrapy.Request(response.urljoin(analyse), self.parse_analyse)

        # next_link = response.xpath('//div[@id="contenu-page"]//div[contains(@class, "pagination")]/ul/li[last()]'
        #                            '/a[contains(., "Suivant")]/@href').extract_first()
        # if next_link:
        #     yield scrapy.Request(response.urljoin(next_link), self.parse)

    def parse_analyse(self, response):
        url_match = self.re_scrutin_url.search(response.url)

        legislature = url_match.group('legislature')
        identifiant = url_match.group('scrutin')

        scrutin = self.extraire_scrutin(response)
        scrutin['legislature'] = legislature
        scrutin['identifiant'] = identifiant
        yield scrutin

        for position in self.extraire_positions(response):
            position['legislature'] = legislature
            position['identifiant'] = identifiant
            yield position

        # for vote in self.extraires_votes(response):
        #     vote.legislature = legislature
        #     vote.identifiant = identifiant
        #     yield vote

    def extraire_scrutin(self, response):
        s = items.Scrutin()

        titre_page = response.xpath('//h1/text()[last()]').extract_first()
        titre_page_match = self.re_scrutin_date.search(titre_page)

        s["date"] = titre_page_match.group(0)

        sujet_scrutin = response.xpath('//h3[@class="president-title"]//text()').extract_first()

        s["intitule"] = sujet_scrutin[len('Scrutin public sur '):]

        elements_votes = response.css('.interieur-media-moyenne-colonne-scrutin')
        nombre_votes = map(int, elements_votes.xpath('p/b/text()').extract())

        if len(nombre_votes) == 1:
            # motion de censure
            s['votes_pour'] = nombre_votes
        else:
            s["nombres_votants"], s["nombres_exprimes"], s["nombres_majorite"], s["votes_pour"], s["votes_contre"] = nombre_votes
            s["abstention"] = s["nombres_votants"] - s["nombres_exprimes"]

        s["resultat"] = elements_votes.css('.annoncevote::text').extract_first()

        return s

    def extraire_positions(self, response):
        elem_groupes = response.css('#index-groupe li > a')
        noms_groupe_avec_nombre = response.css('#analyse .TTgroupe .nomgroupe::text').extract()

        for groupe, nb_membres in zip(elem_groupes, noms_groupe_avec_nombre):
            p = items.Position()
            p['parti'] = groupe.css('.nom-groupe::text').extract_first()

            p['membres'] = self.re_groupe_membres.search(nb_membres).group(1)

            for res_groupe in groupe.css('.res-groupe'):
                position = res_groupe.xpath('text()[1]').extract_first().split(':')[0].lower()
                if position in ['non-votant', 'non-votants']:
                    position = 'nonvotants'

                p[position] = int(res_groupe.xpath('b/text()').extract_first())

            yield p
