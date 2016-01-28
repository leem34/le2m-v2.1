# -*- coding: utf-8 -*-
"""
Ce module contient les boites de dialogue du programme.
"""

from PyQt4 import QtGui, QtCore
import logging
import random
from client.cltgui.cltguidialogs import GuiHistorique
from util.utili18n import le2mtrans
from client import clttexts as textes_main
import PublicGoodGameParams as parametres
import PublicGoodGameTexts as textes
from PublicGoodGameGuiSrc import PublicGoodGameDecision


logger = logging.getLogger("le2m")


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, periode, historique):
        super(GuiDecision, self).__init__(parent)

        # variables
        self._defered = defered
        self._automatique = automatique
        self._historique = GuiHistorique(self, historique)

        # gui
        self.ui = PublicGoodGameDecision.Ui_Dialog()
        self.ui.setupUi(self)

        # period and history
        if periode:
            self.ui.label_periode.setText(textes_main.PERIODE_label(periode))
            self.ui.pushButton_historique.setText(
                le2mtrans(u"History"))
            self.ui.pushButton_historique.clicked.connect(
                self._historique.show)
        else:
            self.ui.label_periode.setVisible(False)
            self.ui.pushButton_historique.setVisible(False)

        # Explanation
        self.ui.textEdit_explication.setText(textes.DECISION_explication)
        self.ui.textEdit_explication.setReadOnly(True)
        self.ui.textEdit_explication.setFixedSize(400, 80)

        # Decision
        self.ui.label_decision.setText(textes.DECISION_label)
        self.ui.spinBox_decision.setButtonSymbols(
            QtGui.QAbstractSpinBox.NoButtons)
        self.ui.spinBox_decision.setMinimum(parametres.DECISION_MIN)
        self.ui.spinBox_decision.setMaximum(parametres.DECISION_MAX)
        self.ui.spinBox_decision.setSingleStep(parametres.DECISION_STEP)
        self.ui.spinBox_decision.setValue(self.ui.spinBox_decision.minimum())

        # bouton box
        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Cancel).setVisible(
            False)

        # title and size
        self.setWindowTitle(textes.DECISION_titre)
        self.setFixedSize(520, 320)

        # automatic
        if self._automatique:
            self.ui.spinBox_decision.setValue(
                random.randrange(
                    self.ui.spinBox_decision.minimum(),
                    self.ui.spinBox_decision.maximum() +
                    self.ui.spinBox_decision.singleStep(),
                    self.ui.spinBox_decision.singleStep()))
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(self._accept)
            self._timer_automatique.start(7000)
                
    def reject(self):
        pass
    
    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        decision = self.ui.spinBox_decision.value()
        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, textes.DECISION_confirmation.titre,
                textes.DECISION_confirmation.message,
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes
            )
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        logger.info(u"Decision callback {}".format(decision))
        self._defered.callback(decision)
        self.accept()
