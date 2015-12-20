# -*- coding: utf-8 -*-

import os
from csv import DictWriter


def type_item(item):
    """Identifie l'item émis par le spider

    :param item: l'item émis par le spider
    :return: le nom de classe de l'item, en minuscules
    """
    return type(item).__name__.lower()


def champs_item(item):
    """Liste les champs de l'item émis par le spider

    :param item: l'item émis par le spider
    :return: la liste des champs de l'item
    """
    return item.fields.keys()


class MultiCsvPipeline(object):
    """Ce pipeline enregistre les items renvoyés par le spider au format CSV

    Ce pipeline génère un fichier CSV par type d'item.

    Il est paramétré par les variables suivantes dans le module :mod:`votes.settings` :

    * ``VOTES_CSV_OUTPUT_DIR`` : le dossier dans lequel seront enregistrés les fichiers CSV
    * ``VOTES_CSV_ENCODING`` : le jeu de caractères utilisés pour écrire les fichiers CSV
    * ``VOTES_CSV_DELIMITER`` : le séparateur utilisé pour séparer les colonnes dans le fichier CSV
    """
    @classmethod
    def from_crawler(cls, crawler):
        """Génère une instance du pipeline en utilisant les paramètres définis dans les settings.

        :param crawler: l'objet crawler - non utilisé dans cette implémentation
        :return: l'instance pipeline
        """
        return cls(
            output_dir=crawler.settings.get('VOTES_CSV_OUTPUT_DIR'),
            encoding=crawler.settings.get('VOTES_CSV_ENCODING'),
            csv_params={
                'delimiter': crawler.settings.get('VOTES_CSV_DELIMITER')
            }
        )

    def __init__(self, output_dir, encoding, csv_params=None):
        """Constructeur pour une instance du pipeline

        Pour créer manuellement un pipeline, il faut renseigner les trois arguments. Par défaut, le pipeline est créé
        par le crawler et les arguments récupérés du fichier de paramétrage.

        :param output_dir: le dossier dans lequel seront enregistrés les fichiers CSV
        :param encoding: le jeu de caractères utilisés pour écrire les fichiers CSV
        :param csv_params: le séparateur utilisé pour séparer les colonnes dans le fichier CSV
        """
        if csv_params is None:
            csv_params = {}

        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.encoding = encoding

        self.csv_params = csv_params

        self.fichiers_sortie = None
        self.spider_count = 0

    def process_item(self, item, spider):

        item_type = type_item(item)
        champs = champs_item(item)

        if item_type not in self.fichiers_sortie:
            f = open(os.path.join(self.output_dir, item_type + '.csv'), 'wb')
            w = DictWriter(f, champs, **self.csv_params)
            w.writeheader()
            self.fichiers_sortie[item_type] = (f, w)

        res = {nom: (field.encode(self.encoding) if isinstance(field, unicode) else field)
               for nom, field in item.iteritems()}
        self.fichiers_sortie[item_type][1].writerow(res)

        # Renvoie l'objet pour d'éventuels autres pipelines
        return item

    def open_spider(self, spider):
        self.spider_count += 1
        if self.fichiers_sortie is None:
            self.fichiers_sortie = {}

    def close_spider(self, spider):
        self.spider_count -= 1

        if self.spider_count == 0:
            for file, _ in self.fichiers_sortie.values():
                file.close()

            self.fichiers_sortie = None
