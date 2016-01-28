# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""
__author__ = "Dimitri DUBOIS"


from collections import namedtuple
from util.utiltools import get_pluriel
import TeamCommunicationParams as pms

# pour i18n:
# 1)  décommenter les lignes ci-après,
# 2) entourer les expressions à traduire par _TC()
# 3) dans le projet créer les dossiers locale/fr_FR/LC_MESSAGES
# en remplaçant fr_FR par la langue souhaitée
# 4) créer le fichier TeamCommunication.po: dans invite de commande, taper:
# xgettext fichierTextes.py -p locale/fr_FR/LC_MESSAGES -d TeamCommunication
# 5) avec poedit, éditer le fichier TeamCommunication.po qui a été créé

# import os
# import configuration.configparam as params
# import gettext
# localedir = os.path.join(params.getp("PARTSDIR"), "TeamCommunication", "locale")
# _TC = gettext.translation(
#   "TeamCommunication", localedir, languages=[params.getp("LANG")]).ugettext


TITLE_MSG = namedtuple("TITLE_MSG", "titre message")


# ECRAN DECISION ===============================================================
DECISION_titre = u"Decision"
DECISION_explication = u"Veuillez compter le nombre de 1 dans les grilles"
DECISION_label = u"Decision label text"
DECISION_erreur = TITLE_MSG(
    u"Warning",
    u"Warning message")
DECISION_confirmation = TITLE_MSG(
    u"Confirmation",
    u"Confirmation message")


# ECRAN RECAPITULATIF ==========================================================
def get_recapitulatif(currentperiod):
    txt = u"Vous avez trouvé {}.<br />Au total votre groupe a trouvé {}." \
          u"<br />Le gain de chacun des membres du groupe est {}.".format(
        get_pluriel(currentperiod.TC_goodanswers, u"bonne réponse"),
        get_pluriel(currentperiod.TC_goodanswers_group, u"bonne réponse"),
        get_pluriel(currentperiod.TC_periodpayoff, u"ecu"))
    return txt


# TEXTE FINAL PARTIE ===========================================================
def get_texte_final(gain_ecus, gain_euros):
    txt = u"Vous avez gagné {gain_en_ecu}, soit {gain_en_euro}.".format(
        gain_en_ecu=get_pluriel(gain_ecus, u"ecu"),
        gain_en_euro=get_pluriel(gain_euros, u"euro"))
    return txt


# ADDITIONNAL QUESTIONS
def get_text_reponses(nbanswers):
    return u"Parmi vos {}, combien de réponses justes êtes-vous sûr(e) " \
           u"d'avoir?".format(get_pluriel(nbanswers, u"réponse"))


def get_text_infosatisfaction():
    return u"Sur une échelle de 1 (tout à fait insatisfait) à 7 " \
           u"(tout à fait satisfait), <br />où situez-vous votre niveau de " \
           u"satisfaction par rapport<br />aux informations échangées dans " \
           u"votre groupe?"


def get_text_jobsatisfaction():
    return u"Sur une échelle de 1 (tout à fait insatisfait) à 7 " \
           u"(tout à fait satisfait),<br />où situez-vous votre niveau de " \
           u"satisfaction par rapport à la tâche"


def get_textpredictiondictator():
    return u"A vote avis, en moyenne, quel montant a été envoyé au joueur B " \
           u"par les participants de la session?"