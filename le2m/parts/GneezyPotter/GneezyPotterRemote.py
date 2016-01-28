# -*- coding: utf-8 -*-

from twisted.internet import defer
from twisted.spread import pb
import logging
import random
from client.cltgui.cltguidialogs import GuiRecapitulatif
import GneezyPotterParams as pms
from GneezyPotterGui import GuiDecision


logger = logging.getLogger("le2m")


class RemoteGP(pb.Referenceable):
    """
    Class remote, celle qui est contactée par le client (sur le serveur)
    """
    def __init__(self, le2mclt):
        self._le2mclt = le2mclt
        self.currentperiod = 0
        self._histo = []

    def remote_configure(self, params):
        logger.info(u"{} Configure".format(self._le2mclt.uid))
        for k, v in params.viewitems():
            setattr(pms, k, v)
        logger.debug(u"Display summary: {}".format(
            u"Yes" if pms.DISPLAY_SUMMARY else u"No"))

    def remote_newperiod(self, period):
        """
        Appelé au début de chaque période.
        L'historique est "vidé" s'il s'agit de la première période de la partie
        Si c'est un jeu one-shot appeler cette méthode en mettant 0
        :param period: le numéro de la période courante
        :return:
        """
        logger.info(u"{} Period {}".format(self._le2mclt.uid, period))
        self.currentperiod = period
        if self.currentperiod == 1:
            del self._histo[:]

    def remote_display_decision(self):
        """
        :return: deferred
        """
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            decision = \
                random.randrange(
                    pms.DECISION_MIN,
                    pms.DECISION_MAX + pms.DECISION_STEP,
                    pms.DECISION_STEP)
            logger.info(u"{} Send back: {}".format(self._le2mclt.uid, decision))
            return decision
        else: 
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered,
                self._le2mclt.automatique, self._le2mclt.screen,
                self.currentperiod, self._histo)
            ecran_decision.show()
            return defered

    def remote_display_summary(self, texte_recap, historique):
        """
        Affiche l'écran récapitulatif
        :param texte_recap: le texte affiché
        :param historique: l'historique de la partie
        :return: deferred
        """
        logger.info(u"{} Summary".format(self._le2mclt.uid))
        self._histo = historique
        if self._le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = GuiRecapitulatif(
                defered,
                self._le2mclt.automatique, self._le2mclt.screen,
                self.currentperiod, self._histo, texte_recap)
            ecran_recap.show()
            return defered
