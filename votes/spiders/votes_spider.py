# -*- coding: utf-8 -*-

import scrapy
import re

__author__ = 'Arthur Cheysson <arthur.cheysson@opusline.fr>'

RE_VOTE = r'([0-9]+)(\*?)'

class VotesSpider(scrapy.Spider):
    name = "votes"
    allowed_domains = ['assemblee-nationale.fr']

    start_urls = ['http://www2.assemblee-nationale.fr/scrutins/liste/(legislature)/14']

    def __init__(self):
        super(VotesSpider, self).__init__()

        self.re_vote = re.compile(RE_VOTE)

    def parse(self, response):
        for ligne in response.css('table.scrutins tbody tr'):
            denom = ligne.css('.denom::text').extract_first()
            desc = ligne.css('.desc::text').extract_first()

            score_pour = int(ligne.css('.pour::text').extract_first())
            score_contre = int(ligne.css('.contre::text').extract_first())
            score_abs = int(ligne.css('.abs::text').extract_first())

            match = self.re_vote.match(denom)
            identifiant_vote = match.group(1)
            solennel = match.group(2) != ''

            yield {
                'identifiant': identifiant_vote,
                'solennel': solennel,
                'desc': desc,
                'pour': score_pour,
                'contre': score_contre,
                'abstention': score_abs
            }
