# -*- coding: utf-8 -*-

import scrapy


class Scrutin(scrapy.Item):
    """Représente les méta-données d'un scrutin

    :param legislature: le numéro de la législature concernée (14 uniquement pour le moment)
    :param identifiant: le numéro identifiant le scrutin (unique pour cette législature)
    :param date: la date du scrutin
    :param intitule: l'intitulé du scrutin
    :param nombres_votants: le nombre de députés votants
    :param nombres_exprimes: le nombre de députés ayant exprimés leur suffrage
    :param votes_pour: le nombre de députés ayant adopté la position *pour* au cours de ce scrutin
    :param votes_contre: le nombre de députés ayant adopté la position *contre* au cours de ce scrutin
    :param abstention: le nombre de députés s'étant abstenu (ils ne comptent pas au nombre des suffrages exprimés
    :param resultat: le résultat du scrutin : soit *adopté*, soit *non adopté*, soit "Inconnu : " suivi du texte brut
    """
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
    """Représente la position individuelle d'un député au cours d'un scrutin

    Pour les scrutins solennels, et pour les scrutins postérieurs au DD/MM/2014, la position individuelle
    des députés est toujours disponible. Antérieurement à cette date, seuls les députés qui avaient voté contrairement
    à la position de leur groupe se voyaient mentionnés dans le rapport de vote. Pour ces scrutins, il n'est donc
    pas possible de distinguer les députés absents de ceux ayant votés conformément à leur groupe.

    Les positions possibles sont les suivantes :

    * *pour* : le député a voté pour au cours de ce scrutin
    * *contre* : le député a voté contre au cours de ce scrutin
    * *abstention* : le député était présent mais s'est abstenu au cours du scrutin
    * *non-votant* : le député était présent, mais ne pouvait pas voter (car il présidait la séance par exemple)

    :param legislature: le numéro de la législature concernée (14 uniquement pour le moment)
    :param identifiant: le numéro identifiant le scrutin (unique pour cette législature)
    :param groupe: le groupe parlementaire auquel appartenait le député votant au moment du scrutin
    :param prenom: le prénom du député votant
    :param nom: le nom de famille du député votant
    :param position: la position adoptée par le député, parmi ``['pour', 'contre', 'abstention', 'non-votant']``
    """
    legislature = scrapy.Field()
    identifiant = scrapy.Field()

    groupe = scrapy.Field()

    prenom = scrapy.Field()
    nom = scrapy.Field()

    position = scrapy.Field()


class Position(scrapy.Item):
    """Représente la position d'un groupe parlementaire au cours d'un scrutin

    :param legislature: le numéro de la législature concernée (14 uniquement pour le moment)
    :param identifiant: le numéro identifiant le scrutin (unique pour cette législature)
    :param groupe: le nom du groupe parlementaire au moment du scrutin
    :param membres: le nombre de membres du groupe parlementaire au moment du scrutin
    :param pour: le nombre de membres du groupe ayant voté *pour* au moment du scrutin
    :param contre: le nombre de membres du groupe ayant voté *contre* au moment du scrutin
    :param absention: le nombre de membres du groupe présents au cours du scrutin et s'étant abstenu
    :param nonvotants: le nombre de membres du groupes présents au cours du scrutin mais dans l'impossibilité de voter
    """
    legislature = scrapy.Field()
    identifiant = scrapy.Field()

    groupe = scrapy.Field()

    membres = scrapy.Field()

    pour = scrapy.Field()
    contre = scrapy.Field()
    abstention = scrapy.Field()
    nonvotants = scrapy.Field()


class Depute(scrapy.Item):
    nom = scrapy.Field()

    circonscription = scrapy.Field()
    mandat_en_cours = scrapy.Field()
