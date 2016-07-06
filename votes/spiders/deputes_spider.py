# -*- coding: utf-8 -*-

import logging
import re

import scrapy

from votes import items

logger = logging.getLogger(__file__)

RE_DROP_TAGS = r'<[^>]*>'


class DeputesSpider(scrapy.Spider):
    name = "deputes"
    allowed_domains = ['assemblee-nationale.fr']

    start_urls = [
        'http://www2.assemblee-nationale.fr/deputes/liste/alphabetique',
        'http://www2.assemblee-nationale.fr/deputes/liste/clos',
    ]

    def __init__(self):
        super(DeputesSpider, self).__init__()
        self.re_drop_tags = re.compile(RE_DROP_TAGS)

    def parse(self, response):
        logger.info(u'Récupéré liste des députés (%d) <%s>', response.status, response.url)

        for page_depute in response.xpath('//div[@id="deputes-list"]//li/a/@href').extract():
            yield scrapy.Request(response.urljoin(page_depute), self.parse_depute)

        for page_depute in response.xpath('//table[@class="clos"]/tbody/tr/td[1]/a/@href').extract():
            yield scrapy.Request(response.urljoin(page_depute), self.parse_depute)

    def parse_depute(self, response):
        logger.info(u'Récupéré député (%d) <%s>', response.status, response.url)

        depute = items.Depute()

        nom_complet = response.xpath('//h1/text()').extract_first().split(' ')

        depute['titre'] = nom_complet[0]
        depute['nom'] = ' '.join(nom_complet[1:])

        fragments_circo = response.xpath('//p[@class="deputy-healine-sub-title"]/node()').extract() or \
                          response.xpath('//dt[starts-with(text(), "Circonscription")]/following::li[1]/node()').extract()
        fragments_circo[0] = fragments_circo[0].replace('&nbsp', ' ')
        fragments_circo[1] = self.re_drop_tags.sub('', fragments_circo[1])

        depute['circonscription'] = ''.join(fragments_circo)

        depute['mandat_en_cours'] = not bool(response.xpath('//p[@class="deputy-healine-sub-title rouge"]'))

        yield depute
