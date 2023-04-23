# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitledTrek.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(600, 196)
        Dialog.setMaximumSize(QtCore.QSize(1000, 196))
        Dialog.setSizeIncrement(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setLocale(QtCore.QLocale(QtCore.QLocale.Russian, QtCore.QLocale.Belarus))
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.UrlText = QtWidgets.QLineEdit(Dialog)
        self.UrlText.setObjectName("UrlText")
        self.horizontalLayout_4.addWidget(self.UrlText)
        self.LoadTrek = QtWidgets.QPushButton(Dialog)
        self.LoadTrek.setObjectName("LoadTrek")
        self.horizontalLayout_4.addWidget(self.LoadTrek)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AlbumImg = QtWidgets.QLabel(Dialog)
        self.AlbumImg.setMinimumSize(QtCore.QSize(140, 140))
        self.AlbumImg.setMaximumSize(QtCore.QSize(140, 140))
        self.AlbumImg.setText("")
        self.AlbumImg.setPixmap(QtGui.QPixmap("img/Missing_Texture2.png"))
        self.AlbumImg.setAlignment(QtCore.Qt.AlignCenter)
        self.AlbumImg.setObjectName("AlbumImg")
        self.horizontalLayout.addWidget(self.AlbumImg)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(6, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.NameTrek = QtWidgets.QLabel(Dialog)
        self.NameTrek.setObjectName("NameTrek")
        self.verticalLayout.addWidget(self.NameTrek)
        self.NameUploader = QtWidgets.QLabel(Dialog)
        self.NameUploader.setObjectName("NameUploader")
        self.verticalLayout.addWidget(self.NameUploader)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Добавить Трек"))
        self.UrlText.setText(_translate("Dialog", "https://youtube.com"))
        self.LoadTrek.setText(_translate("Dialog", "Загрузить"))
        self.NameTrek.setText(_translate("Dialog", "-"))
        self.NameUploader.setText(_translate("Dialog", "-"))