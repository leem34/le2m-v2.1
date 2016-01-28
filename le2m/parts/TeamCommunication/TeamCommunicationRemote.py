# -*- coding: utf-8 -*-

import logging
import random
from twisted.internet import defer
from twisted.spread import pb
import TeamCommunicationParams as pms
from TeamCommunicationGui import GuiDecision, DAdditionnalquestions, \
    DQuestionDictator


logger = logging.getLogger("le2m")


class RemoteTC(pb.Referenceable):
    """
    Class remote, remote_ methods can be called by the server
    """
    def __init__(self, le2mclt):
        self._le2mclt = le2mclt
        self._currentperiod = 0
        self._histo = []
        self._tcremoteplayer = None  # to send message
        self._ecran_decision = None

    @property
    def tcremoteplayer(self):
        return self._tcremoteplayer

    def remote_configure(self, tcremoteplayer, params):
        """
        Appelé au démarrage de la partie, permet de configure le remote
        par exemple: traitement, séquence ...
        :param tcremoteplayer:
        :param treatment:
        :param grilles:
        :param tempspartie:
        :return:
        """
        logger.info(u"{} configure".format(self._le2mclt.uid))
        self._tcremoteplayer = tcremoteplayer
        for k, v in params.viewitems():
            setattr(pms, k, v)

    def remote_newperiod(self, periode):
        """
        Appelé au début de chaque période.
        L'historique est "vidé" s'il s'agit de la première période de la partie
        Si c'est un jeu one-shot appeler cette méthode en mettant 0
        :param periode: le numéro de la période courante
        :return:
        """
        logger.info(u"{} Period {}".format(self._le2mclt.uid, periode))
        self._currentperiod = periode
        if self._currentperiod == 1:
            del self._histo[:]

    def remote_display_decision(self):
        """
        Display the decision screen
        :return: deferred
        """
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        defered = defer.Deferred()
        if self._le2mclt.simulation:
            self._ecran_decision = GuiDecision(
                defered, True, self._le2mclt.screen, self)
            return defered
        else:
            self._ecran_decision = GuiDecision(
                defered, self._le2mclt.automatique, self._le2mclt.screen, self)
            self._ecran_decision.show()
            return defered

    @defer.inlineCallbacks
    def send_look(self, grille):
        logger.info(u"{} send_look grille {}".format(self._le2mclt.uid, grille))
        yield (self.tcremoteplayer.callRemote("send_look", grille))

    @defer.inlineCallbacks
    def send_try(self, grille, valeur):
        logger.info(u"{} send_try grille {} valeur {}".format(
            self._le2mclt.uid, grille, valeur))
        yield (self.tcremoteplayer.callRemote("send_try", grille, valeur))

    @defer.inlineCallbacks
    def send_message(self, message):
        logger.info(u"{} send_message {}".format(self._le2mclt.uid, message))
        yield (self.tcremoteplayer.callRemote("send_message", message))

    def remote_display_message(self, message):
        logger.info(u"{} display_message {}".format(self._le2mclt.uid, message))
        if self._le2mclt.simulation:
            pass
        else:
            self._ecran_decision.add_message(message)

    def remote_display_additionnalquestions(self, nbanswers):
        logger.info(u"{} display_additionnalquestions".format(
            self._le2mclt.uid))
        if self._le2mclt.simulation:
            rep = {"TC_confidence": random.randint(0, nbanswers),
                   "TC_jobsatifaction": random.randint(0, 7)}
            if pms.TREATMENT == pms.AVEC_COMMUNICATION:
                rep["TC_infosatisfaction"] = random.randint(0, 7)
            logger.info(u"{} renvoi {}".format(self._le2mclt.uid, rep))
            return rep
        else:
            defered = defer.Deferred()
            ecran_additionnalquestions = DAdditionnalquestions(
                defered, self._le2mclt.automatique, self._le2mclt.screen,
                nbanswers)
            ecran_additionnalquestions.show()
            return defered

    def remote_display_questionapresdictator(self):
        logger.info(u"{} remote_display_questionapresdictator".format(
            self._le2mclt.uid))
        if self._le2mclt.simulation:
            rep = random.randint(0, 10)
            logger.info(u"{} renvoi {}".format(self._le2mclt.uid, rep))
            return rep
        else:
            defered = defer.Deferred()
            screen = DQuestionDictator(
                defered, self._le2mclt.automatique, self._le2mclt.screen)
            screen.show()
            return defered
