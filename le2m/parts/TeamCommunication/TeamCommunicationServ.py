# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import logging
from collections import OrderedDict
from twisted.internet import defer
from util import utiltools, utili18n
import TeamCommunicationParams as pms
from TeamCommunicationGui import DConfiguration, Wlist, DGains
from time import strftime
from parts.Dictator import DictatorParams
from server.servgest import servgestgroups

logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen
        actions = OrderedDict()
        actions[u"Configurer"] = self._configure
        actions[u"Afficher les paramètres"] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), u"Paramètres")
        actions[u"Démarrer"] = lambda _: self._demarrer()
        actions[u"Former groupes dictator"] = self._prepare_dictator
        actions[u"Afficher question après Dictator"] = \
            lambda _: self._run_questionapresdictator()
        actions[u"Afficher les gains"] = self._display_payoffs

        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Team Communication", actions)

        # ajout d'onglets
        self._onglet_looks = Wlist()
        self._onglet_essais = Wlist()
        self._onglet_messages = Wlist()
        self._le2mserv.gestionnaire_graphique.screen.ui.onglets.addTab(
            self._onglet_looks, u"Ouvertures grilles")
        self._le2mserv.gestionnaire_graphique.screen.ui.onglets.addTab(
            self._onglet_essais, u"Essais")
        self._le2mserv.gestionnaire_graphique.screen.ui.onglets.addTab(
            self._onglet_messages, u"Messages")

        self._currentsequence = -1

    @property
    def onglet_looks(self):
        return self._onglet_looks

    @property
    def onglet_essais(self):
        return self._onglet_essais

    @property
    def onglet_messages(self):
        return self._onglet_messages

    def _configure(self):
        """
        To make changes in the parameters
        :return:
        """
        dconfig = DConfiguration(self._le2mserv.gestionnaire_graphique.screen)
        if dconfig.exec_():
            pms.TEMPS_PARTIE, pms.TREATMENT, pms.GRILLES = dconfig.get_config()
            self._le2mserv.gestionnaire_graphique.infoserv(
                [u"Temps partie: {}".format(pms.TEMPS_PARTIE),
                 u"Traitement: {}".format(pms.treatmentcodes[pms.TREATMENT]),
                 u"Grilles: {}".format(len(pms.GRILLES))])

    @defer.inlineCallbacks
    def _demarrer(self):
        # checks of consistency
        if (divmod(len(self._le2mserv.gestionnaire_joueurs.get_players()),
                pms.TAILLE_GROUPES)[1] != 0):
            self._le2mserv.gestionnaire_graphique.display_error(
                u"Impossible de former des groupes de {} avec {} "
                u"joueurs".format(
                    pms.TAILLE_GROUPES,
                    self._le2mserv.gestionnaire_joueurs.nombre_joueurs))
            return
        if not pms.GRILLES:
            self._le2mserv.gestionnaire_graphique.display_error(
                u"Il faut charger les grilles")
            return

        # confirmation start
        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(u"Démarrer TeamCommunication?")
        if not confirmation:
            return

        # init part
        if not self._le2mserv.gestionnaire_experience.has_part(
                "TeamCommunication"):  # init part
            yield (self._le2mserv.gestionnaire_experience.init_part(
                "TeamCommunication", "PartieTC", "RemoteTC", pms))
            self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
                'TeamCommunication')
        else:  # uniquement affichage
            self._le2mserv.gestionnaire_graphique.infoserv(None)
            self._le2mserv.gestionnaire_graphique.infoserv(
                "TeamCommunication".upper(), fg="white", bg="blue")
            self._le2mserv.gestionnaire_graphique.infoclt(None)
            self._le2mserv.gestionnaire_graphique.infoclt(
                "TeamCommunication".upper(), fg="white", bg="blue")
            self._le2mserv.gestionnaire_graphique.infoserv(
                utili18n.le2mtrans(u"Start time: {st}").format(
                    st=strftime("%H:%M:%S")))

        self._currentsequence += 1
        self._le2mserv.gestionnaire_graphique.infoserv(u"Sequence {}".format(
            self._currentsequence))
        self.onglet_looks.clear()
        self.onglet_essais.clear()
        self.onglet_messages.clear()

        # groups formation
        if self._currentsequence == 0:
            try:
                self._le2mserv.gestionnaire_groupes.former_groupes(
                    liste_joueurs=self._le2mserv.gestionnaire_joueurs.get_players(),
                    taille_groupes=pms.TAILLE_GROUPES, roundrobin=True)
            except ValueError as e:
                self._le2mserv.gestionnaire_graphique.display_error(e.message)
                return
        else:
            self._le2mserv.gestionnaire_groupes.roundrobinnext()
    
        # configuration of players and remote
        yield (self._le2mserv.gestionnaire_experience.run_step(
            u"Configure", self._tous, "configure", self, self._currentsequence))
        for j in self._tous:
            j.othergroupmembers = [
                k.get_part("TeamCommunication") for k in
                self._le2mserv.gestionnaire_groupes.get_autres_membres_groupe(
                    j.joueur)]

        # Start of repetitions -------------------------------------------------
        for period in xrange(1 if pms.NOMBRE_PERIODES else 0,
                             pms.NOMBRE_PERIODES + 1):

            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # init period
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, u"Période {}".format(period)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, u"Période {}".format(period)], fg="white", bg="gray")
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))
            
            # decision
            yield (self._le2mserv.gestionnaire_experience.run_step(
                u"Décision", self._tous, "display_decision"))

            # computation of good answers in each group
            self._le2mserv.gestionnaire_graphique.infoserv(u"Good answers")
            for g, m in self._le2mserv.gestionnaire_groupes.get_groupes(
                    "TeamCommunication").viewitems():
                nbbonnesrep = sum([j.currentperiod.TC_goodanswers for j in m])
                for j in m:
                    j.currentperiod.TC_goodanswers_group = nbbonnesrep
                self._le2mserv.gestionnaire_graphique.infoserv(
                    u"G{}: {}".format(g.split("_")[2], nbbonnesrep))

            # period payoffs
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "TeamCommunication")

            # questions about self confidence and satisfaction
            yield (self._le2mserv.gestionnaire_experience.run_step(
                u"Questions additionnelles", self._tous,
                "display_additionnalquestions"))
        
            # period summary
            yield (self._le2mserv.gestionnaire_experience.run_step(
                u"Récapitulatif", self._tous, "display_summary"))
        
        # End of part ----------------------------------------------------------
        self._le2mserv.gestionnaire_experience.finalize_part(
            "TeamCommunication")

    def _display_payoffs(self):
        gains_txt = []
        gains, textes_finaux = {}, {}
        if self._currentsequence >= 0:
            sequence, ok = QtGui.QInputDialog.getInt(
                self._le2mserv.gestionnaire_graphique.screen, u"Choix séquence",
                u"Choisir la séquence", min=0, max=self._currentsequence,
                step=1, value=0)
            if ok:
                for j in self._tous:
                    gains[j.joueur] = \
                        j.sequences[sequence]["gain_euros"]
                    gains_txt.append([str(j.joueur), u"{}".format(
                        gains[j.joueur])])
                    textes_finaux[j.joueur] = j.sequences[sequence]["texte_final"]
                self._ecran_gains = DGains(
                    self._le2mserv, gains_txt, textes_finaux, gains)
                self._ecran_gains.show()

    def _prepare_dictator(self):
        if self._currentsequence == -1:
            self._le2mserv.gestionnaire_graphique.display_error(
                u"Il faut au moins avoir lancé une séquence de "
                u"TeamCommunication")
            return
        if not self._le2mserv.gestionnaire_graphique.question(
                u"Préparer les groupes de Dictator?"):
            return

        DictatorParams.TAILLE_GROUPES = 0
        self._le2mserv.gestionnaire_groupes.roundrobinnext()
        groups = self._le2mserv.gestionnaire_groupes.get_groupes()
        newgroups = {}
        for v in groups.viewvalues():
            newgroups["{}_g_{}".format(
                self._le2mserv.nom_session, servgestgroups.compteur_groupe)] = \
                [v[0], v[1]]
            servgestgroups.compteur_groupe += 1
            newgroups["{}_g_{}".format(
                self._le2mserv.nom_session, servgestgroups.compteur_groupe)] = \
                [v[2], v[3]]
            servgestgroups.compteur_groupe += 1
        self._le2mserv.gestionnaire_groupes.set_groupes(newgroups)
        self._le2mserv.gestionnaire_groupes.set_attributes()
        self._le2mserv.gestionnaire_graphique.infoserv(
            self._le2mserv.gestionnaire_groupes.get_groupes_string())

    @defer.inlineCallbacks
    def _run_questionapresdictator(self):
        if self._currentsequence == -1 or \
                not self._le2mserv.gestionnaire_joueurs.get_players()[0].\
                        get_part("Dictator"):
            self._le2mserv.gestionnaire_graphique.display_error(
                u"Il faut avoir fait au moins une séquence de "
                u"TeamCommunication et la partie Dictator")
            return
        if not self._le2mserv.gestionnaire_graphique.question(
                u"Lancer la question d'après Dictator?"):
            return
        yield (self._le2mserv.gestionnaire_experience.run_step(
            step_name=u"Question après Dictator", step_participants=self._tous,
            step_function="display_questionapresdictator"))
