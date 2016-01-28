# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""
__author__ = "Dimitri DUBOIS"

import os
import configuration.configparam as params
import gettext
localedir = os.path.join(params.getp("PARTSDIR"), "Dictator", "locale")
_DIC = gettext.translation(
    "Dictator", localedir, languages=[params.getp("LANG")]).ugettext
from collections import namedtuple
from util.utiltools import get_pluriel
from parts.Dictator import DictatorParams as pms

TITLE_MSG = namedtuple("TITLE_MSG", "titre message")


# ROLE =========================================================================
def get_role(role):
    return _DIC(u"You are player {}").format(
        u"A" if role == pms.PLAYER_A else u"B")

# ECRAN DECISION ===============================================================
DECISION_titre = _DIC(u"Decision")
DECISION_explication = _DIC(u"You have an endowment of {}. You can send any "
                            u"amount you want to player B").format(
    get_pluriel(pms.DOTATION, pms.MONNAIE))
DECISION_label = _DIC(u"Choose the amount you want to send to player B")
DECISION_erreur = TITLE_MSG(
    _DIC(u"Warning"),
    _DIC(u"Warning message"))
DECISION_confirmation = TITLE_MSG(
    _DIC(u"Confirmation"),
    _DIC(u"Do you confirm you choice?"))


# ECRAN RECAPITULATIF ==========================================================
def get_recapitulatif(currentperiod):
    txt = _DIC(u"You were player {}.").format(
        u"A" if currentperiod.DIC_role == pms.PLAYER_A else u"B")
    if currentperiod.DIC_role == pms.PLAYER_A:
        txt += _DIC(u" You sent {} to player B.").format(
            get_pluriel(currentperiod.DIC_decision, pms.MONNAIE))
    else:
        txt += _DIC(u" Player A sent {} to you.").format(
            get_pluriel(currentperiod.DIC_recu, pms.MONNAIE))
    txt += _DIC(u" Your payoff is equal to {}.").format(
        get_pluriel(currentperiod.DIC_periodpayoff, pms.MONNAIE))
    return txt


# TEXTE FINAL PARTIE ===========================================================
def get_texte_final(gain_euros):
    txt = _DIC(u"You've won {gain_en_euro}.").format(
        gain_en_euro=get_pluriel(gain_euros, u"euro"))
    return txt