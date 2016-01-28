# -*- coding: utf-8 -*-
"""
Ce module contient les textes des écrans
"""
__author__ = "Dimitri DUBOIS"

import os
import configuration.configparam as params
import gettext
localedir = os.path.join(
    params.getp("PARTSDIR"), "CommonPoolResource", "locale")
_CPR = gettext.translation(
    "CommonPoolResource", localedir, languages=[params.getp("LANG")]).ugettext

from collections import namedtuple
from util.utiltools import get_pluriel
import CommonPoolResourceParams as pms


TITLE_MSG = namedtuple("TITLE_MSG", "titre message")

# MULTI-ECRANS =================================================================
PERIODE_label = lambda periode: _CPR(u"Period {}").format(periode)

# ECRAN DECISION ===============================================================
DECISION_explication = \
    _CPR(u"You have two accounts: a private account and a public account. "
         u"The public account has {}. Each group member can extract a maximum "
         u"of {} from the public account to put on his/her private account. "
         u"The payoff of each member depends on the number of tokens he/she "
         u"has put on his/her private account as well as on the total number "
         u"of tokens extracted by the group from the public account.").format(
        get_pluriel(pms.DECISION_MAX * pms.TAILLE_GROUPES, _CPR(u"token")),
        get_pluriel(pms.DECISION_MAX, _CPR(u"token")))

DECISION_label = _CPR(u"Please choose how much you want to extract from the "
                      u"public account")

DECISION_titre = _CPR(u"Decision")

DECISION_confirmation = TITLE_MSG(
    _CPR(u"Confirmation"), _CPR(u"Do you confirm your choice?"))


# ECRAN RECAPITULATIF ==========================================================
def get_recapitulatif(currentperiod):
    texte = _CPR(u"You extracted {} and you group extracted a total of {}.\n "
                 u"Your payoff is equal to {}").format(
        get_pluriel(currentperiod.CPR_decision, _CPR(u"token")),
        get_pluriel(currentperiod.CPR_decisiongroup, _CPR(u"token")),
        get_pluriel(currentperiod.CPR_periodpayoff, u"ecu"))
    return texte


def get_texte_final(gain_ecus, gain_euros):
    return _CPR(u"You have earned {}, which corresponds to {}.").format(
        get_pluriel(gain_ecus, u"ecu"), get_pluriel(gain_euros, u"euro"))
