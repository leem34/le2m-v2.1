# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'globalPublicGood_gui_decision.ui'
#
# Created: Tue Apr  1 09:56:26 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1024, 768)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(1024, 768))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_periode = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_periode.setFont(font)
        self.label_periode.setObjectName(_fromUtf8("label_periode"))
        self.horizontalLayout.addWidget(self.label_periode)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_historique = QtGui.QPushButton(Form)
        self.pushButton_historique.setObjectName(_fromUtf8("pushButton_historique"))
        self.horizontalLayout.addWidget(self.pushButton_historique)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.textEdit_explication = QtGui.QTextEdit(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_explication.sizePolicy().hasHeightForWidth())
        self.textEdit_explication.setSizePolicy(sizePolicy)
        self.textEdit_explication.setMinimumSize(QtCore.QSize(850, 100))
        self.textEdit_explication.setMaximumSize(QtCore.QSize(850, 100))
        self.textEdit_explication.setReadOnly(True)
        self.textEdit_explication.setObjectName(_fromUtf8("textEdit_explication"))
        self.horizontalLayout_2.addWidget(self.textEdit_explication)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_decision_individuel = QtGui.QLabel(Form)
        self.label_decision_individuel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_decision_individuel.setObjectName(_fromUtf8("label_decision_individuel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_decision_individuel)
        self.spinBox_individuel = QtGui.QSpinBox(Form)
        self.spinBox_individuel.setObjectName(_fromUtf8("spinBox_individuel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.spinBox_individuel)
        self.label_decision_local = QtGui.QLabel(Form)
        self.label_decision_local.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_decision_local.setObjectName(_fromUtf8("label_decision_local"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_decision_local)
        self.spinBox_local = QtGui.QSpinBox(Form)
        self.spinBox_local.setObjectName(_fromUtf8("spinBox_local"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBox_local)
        self.label_decision_global = QtGui.QLabel(Form)
        self.label_decision_global.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_decision_global.setObjectName(_fromUtf8("label_decision_global"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_decision_global)
        self.spinBox_global = QtGui.QSpinBox(Form)
        self.spinBox_global.setObjectName(_fromUtf8("spinBox_global"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.spinBox_global)
        self.horizontalLayout_3.addLayout(self.formLayout)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.pushButton_valider = QtGui.QPushButton(Form)
        self.pushButton_valider.setObjectName(_fromUtf8("pushButton_valider"))
        self.horizontalLayout_6.addWidget(self.pushButton_valider)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        spacerItem7 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem7)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_periode.setText(QtGui.QApplication.translate("Form", "Période", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_historique.setText(QtGui.QApplication.translate("Form", "Historique", None, QtGui.QApplication.UnicodeUTF8))
        self.label_decision_individuel.setText(QtGui.QApplication.translate("Form", "Nombre de jetons que vous placez sur votre compte individuel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_decision_local.setText(QtGui.QApplication.translate("Form", "Nombre de jetons que vous placez sur le compte collectif local", None, QtGui.QApplication.UnicodeUTF8))
        self.label_decision_global.setText(QtGui.QApplication.translate("Form", "Nombre de jetons que vous placez sur le compte collectif global", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_valider.setText(QtGui.QApplication.translate("Form", "Valider", None, QtGui.QApplication.UnicodeUTF8))

