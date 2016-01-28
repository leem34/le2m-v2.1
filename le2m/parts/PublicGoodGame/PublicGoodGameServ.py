# -*- coding: utf-8 -*-

from twisted.internet import defer
import pandas as pd
import matplotlib.pyplot as plt
import logging
from collections import OrderedDict
from util import utiltools
import PublicGoodGameParams as pms
from PublicGoodGameTexts import _PGG
import PublicGoodGamePart  # for sqlalchemy


logger = logging.getLogger("le2m".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen
        actions = OrderedDict()
        actions[_PGG(u"Configure")] = self._configure
        actions[_PGG(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), u"Paramètres")
        actions[_PGG(u"Start")] = lambda _: self._demarrer()
        actions[_PGG(u"Display payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs("PublicGoodGame")
        actions[_PGG(u"Show graph")] = self._show_fig
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Public Good Game", actions)

        self._fig = None

    def _configure(self):
        """
        To make changes in the parameters
        :return:
        """
        pass

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(u"Démarrer PublicGoodGame?")
        if not confirmation:
            return
        
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "PublicGoodGame", "PartiePGG", "RemotePGG", pms))
        self._fig = None
        
        # formation des groupes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if pms.TAILLE_GROUPES > 0:
            try:
                self._le2mserv.gestionnaire_groupes.former_groupes(
                    self._le2mserv.gestionnaire_joueurs.get_players(),
                    pms.TAILLE_GROUPES, forcer_nouveaux=True)
            except ValueError as e:
                self._le2mserv.gestionnaire_graphique.display_error(
                    e.message)
                return
    
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'PublicGoodGame')

        # pour configure les clients et les remotes ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        yield (self._le2mserv.gestionnaire_experience.run_func(
            self._tous, "configure"))
    
        # DEBUT DES RÉPÉTITIONS ================================================
        for period in xrange(1 if pms.NOMBRE_PERIODES else 0,
                        pms.NOMBRE_PERIODES + 1):

            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # initialisation période ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, u"Période {}".format(period)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, u"Période {}".format(period)], fg="white", bg="gray")
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))
            
            # décision ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Décision", self._tous, "display_decision"))

            # compute total amount in the public account by group
            self._le2mserv.gestionnaire_graphique.infoserv(
                _PGG(u"Total amount by group"))
            for g, m in self._le2mserv.gestionnaire_groupes.get_groupes(
                    "PublicGoodGame").iteritems():
                total = sum([p.currentperiod.PGG_public for p in m])
                for p in m:
                    p.currentperiod.PGG_publicgroup = total
                self._le2mserv.gestionnaire_graphique.infoserv(
                    u"G{}: {}".format(g.split("_")[2], total))
            
            # calcul des gains de la période ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "PublicGoodGame")
        
            # summary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            yield(self._le2mserv.gestionnaire_experience.run_step(
                u"Summary", self._tous, "display_summary"))

            # stats period
            self._le2mserv.gestionnaire_graphique.infoserv(
                u"Av. for the period")
            dataperiod = []
            for part in self._tous:
                dataperiod.append(part.currentperiod.todict(part.joueur))
            df_dataperiod = pd.DataFrame(dataperiod)
            df_dataperiod = df_dataperiod.groupby(df_dataperiod.PGG_group).mean()
            self._le2mserv.gestionnaire_graphique.infoserv(
                df_dataperiod["PGG_public"].to_string())

            # graph period
            if self._fig is None:
                self._fig, self._graph = plt.subplots()
                self._graph.set_ylim(0, pms.DOTATION)
                self._graph.set_xlim(1, pms.NOMBRE_PERIODES)
                self._graph.set_ylabel("Amount put in the public account")
                self._graph.set_xlabel("Periods")
                self._dataall = []
                self._groups = df_dataperiod.index
                colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
                xval, yval = range(len(self._groups)), range(len(self._groups))
                for g in range(len(self._groups)):
                    xval[g] = []
                    yval[g] = []
            del self._graph.lines[:]
            for c, g in enumerate(self._groups):
                xval[c].append(period)
                yval[c].append(df_dataperiod["PGG_public"].ix[g])
                self._graph.plot(xval[c], yval[c], color=colors[c],
                                 label="G{}".format(g.split("_")[2]))
            if len(xval[0]) == 1:
                self._graph.legend(loc=9, ncol=len(self._groups), frameon=False,
                                   fontsize=10)
            self._fig.canvas.draw()

            self._dataall.extend(dataperiod)


        self._le2mserv.gestionnaire_graphique.infoserv(
            [None, u"Av. for the whole game"])
        datapandall = pd.DataFrame(self._dataall)
        datapandall = datapandall.groupby(datapandall.PGG_group)
        self._le2mserv.gestionnaire_graphique.infoserv(
            datapandall.mean()["PGG_public"].to_string())
        
        # FIN DE LA PARTIE =====================================================
        self._le2mserv.gestionnaire_experience.finalize_part(
            "PublicGoodGame")

    def _show_fig(self):
        if not self._fig:
            return
        self._fig.show()