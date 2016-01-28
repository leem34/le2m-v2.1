# -*- coding: utf-8 -*-

from twisted.internet import defer
from twisted.spread import pb
import logging
import random
from client.cltgui.cltguidialogs import GuiRecapitulatif
import PublicGoodGameParams as pms
from PublicGoodGameGui import GuiDecision


logger = logging.getLogger("le2m")


class RemotePGG(pb.Referenceable):
    """
    Class remote, remote_ methods can be called by the server
    """
    def __init__(self, le2mclt):
        self._le2mclt = le2mclt
        self._periode_courante = 0
        self._historique = []

    def remote_configure(self, *args):
        """
        Appelé au démarrage de la partie, permet de configure le remote
        par exemple: traitement, séquence ...
        :param args:
        :return:
        """
        logger.info(u"{} Configure".format(self._le2mclt.uid))
        pass

    def remote_newperiod(self, periode):
        """
        Appelé au début de chaque période.
        L'historique est "vidé" s'il s'agit de la première période de la partie
        Si c'est un jeu one-shot appeler cette méthode en mettant 0
        :param periode: le numéro de la période courante
        :return:
        """
        logger.info(u"{} Period {}".format(self._le2mclt.uid, periode))
        self._periode_courante = periode
        if self._periode_courante == 1:
            del self._historique[:]

    def remote_display_decision(self):
        """
        Display the decision screen
        :return: deferred
        """
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            decision = \
                random.randrange(
                    pms.DECISION_MIN,
                    pms.DECISION_MAX + pms.DECISION_STEP,
                    pms.DECISION_STEP)
            logger.info(u"{} Send back {}".format(self._le2mclt.uid, decision))
            return decision
        else: 
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered, self._le2mclt.automatique,
                self._le2mclt.screen, self._periode_courante, self._historique)
            ecran_decision.show()
            return defered

    def remote_display_summary(self, texte_recap, historique):
        """
        Display the summary screen
        :param texte_recap:
        :param historique:
        :return: deferred
        """
        logger.info(u"{} Summary".format(self._le2mclt.uid))
        self._historique = historique
        if self._le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = GuiRecapitulatif(
                defered, self._le2mclt.automatique, self._le2mclt.screen,
                self._periode_courante, self._historique, texte_recap)
            ecran_recap.show()
            return defered
