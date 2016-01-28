# -*- coding: utf-8 -*-

from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
import logging
from datetime import datetime
from util.utiltools import get_module_attributes
from server.servbase import Base
from server.servparties import Partie
import DictatorParams as pms
from DictatorTexts import _DIC
import DictatorTexts as textes


logger = logging.getLogger("le2m")


class PartieDIC(Partie):
    __tablename__ = "partie_Dictator"
    __mapper_args__ = {'polymorphic_identity': 'Dictator'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsDIC')

    def __init__(self, le2mserv, joueur):
        super(PartieDIC, self).__init__("Dictator", "DIC")
        self._le2mserv = le2mserv
        self.joueur = joueur
        self._texte_recapitulatif = u""
        self._texte_final = u""
        self.DIC_gain_ecus = 0
        self.DIC_gain_euros = 0
        self._histo_vars = []
        self._histo = []
        self.periodes = {}
        self.currentperiod = None
        self.role = None

    @defer.inlineCallbacks
    def configure(self):
        """
        permet de configure la partie (traitement ...)
        :param args:
        :return:
        """
        self._histo_vars = []
        self._histo = []
        logger.debug(u"{} Configure".format(self.joueur))
        # ici mettre en place la configuration
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))

    @defer.inlineCallbacks
    def display_role(self):
        yield (self.joueur.get_part("base").remote.callRemote(
            "display_information", textes.get_role(self.role)))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def newperiod(self, period):
        """
        Nouvelle période: création de la période et information du remote
        du numéro de cette période
        Vide l'historique si première période
        :param period:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        self.currentperiod = RepetitionsDIC(period)
        self.currentperiod.DIC_role = self.role
        self._le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (self.remote.callRemote("newperiod", period))
        logger.info(u"{} Ready for period {}".format(self.joueur, period))

    @defer.inlineCallbacks
    def display_decision(self):
        """
        Affiche l'écran de décision sur le remote.
        Récupère la ou les décisions, le temps de décision et enregistre
        le tout dans la base.
        :return:
        """
        logger.debug(u"{} Decision".format(self.joueur))
        debut = datetime.now()
        self.currentperiod.DIC_decision = \
            yield(self.remote.callRemote("display_decision"))
        self.currentperiod.DIC_decision_temps = \
            (datetime.now() - debut).seconds
        self.joueur.info(u"{}".format(self.currentperiod.DIC_decision))
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Calcul du gain de la période
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))

        if self.currentperiod.DIC_role == pms.PLAYER_A:
            self.currentperiod.DIC_periodpayoff = \
                pms.DOTATION - self.currentperiod.DIC_decision
        else:
            self.currentperiod.DIC_periodpayoff = self.currentperiod.DIC_recu

        # gain cumulé
        if self.currentperiod.DIC_period < 2:
            self.currentperiod.DIC_cumulativepayoff = \
                self.currentperiod.DIC_periodpayoff
        else: 
            previousperiod = self.periodes[
                self.currentperiod.DIC_period - 1]
            self.currentperiod.DIC_cumulativepayoff = \
                previousperiod.DIC_cumulativepayoff + \
                self.currentperiod.DIC_periodpayoff

        # periode courange dans dictionnaire des périodes passées
        self.periodes[self.currentperiod.DIC_period] = \
            self.currentperiod

        logger.info(u"{} Period Payoff {}".format(
            self.joueur, self.currentperiod.DIC_periodpayoff))

    @defer.inlineCallbacks
    def display_summary(self):
        """
        Création du texte du récapitulatif et de l'historique puis affichage
        sur le remote
        :param args:
        :return:
        """
        logger.debug(u"{} Summary".format(self.joueur))
        if not self._histo_vars:
            if self.currentperiod.DIC_role == pms.PLAYER_A:
                self._histo_vars = ["DIC_decision", "DIC_periodpayoff"]
                self._histo.append([_DIC(u"Decision"), _DIC(u"Payoff")])
            else:
                self._histo_vars = ["DIC_recu", "DIC_periodpayoff"]
                self._histo.append([_DIC(u"Received"), _DIC(u"Payoff")])

        self._texte_recapitulatif = textes.get_recapitulatif(self.currentperiod)
        self._histo.append(
            [getattr(self.currentperiod, e) for e in self._histo_vars])
        yield(self.remote.callRemote("display_summary",
                                     self._texte_recapitulatif, self._histo))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()
    
    def compute_partpayoff(self):
        """
        Cacul du gain de la partie.
        :return:
        """
        logger.debug(u"{} Part Payoff".format(self.joueur))
        # gain partie
        self.DIC_gain_ecus = \
            self.currentperiod.DIC_cumulativepayoff
        self.DIC_gain_euros = \
            float(self.DIC_gain_ecus) * \
            float(pms.TAUX_CONVERSION)

        # texte final
        self._texte_final = textes.get_texte_final(self.DIC_gain_euros)

        logger.debug(u"Texte final {}: {}".format(
            self.joueur, self._texte_final))
        logger.info(u'{} Payoff ecus {} Payoff euros {:.2f}'.format(
            self.joueur, self.DIC_gain_ecus, self.DIC_gain_euros))


class RepetitionsDIC(Base):
    __tablename__ = 'partie_Dictator_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_Dictator.partie_id"))

    DIC_period = Column(Integer)
    DIC_traitement = Column(Integer)
    DIC_role = Column(Integer)
    DIC_decision = Column(Integer)
    DIC_decision_temps = Column(Integer)
    DIC_recu = Column(Integer)
    DIC_periodpayoff = Column(Float)
    DIC_cumulativepayoff = Column(Float)

    def __init__(self, periode):
        self.DIC_traitement = pms.TRAITEMENT
        self.DIC_period = periode
        self.DIC_temps_decision = 0
        self.DIC_periodpayoff = 0
        self.DIC_cumulativepayoff = 0
        
    def todict(self, joueur):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        temp["joueur"] = joueur
        return temp
