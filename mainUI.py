# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet("QMainWindown{\n"
"  background-color: rgb(0, 0, 0,255);\n"
" color: rgb(0, 0, 0);\n"
"}\n"
"")
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Russian, QtCore.QLocale.Belarus))
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMouseTracking(True)
        self.centralwidget.setTabletTracking(False)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("QWidget{\n"
"  background-color: rgb(0, 0, 0,0.1);\n"
"\n"
"\n"
"}\n"
"\n"
"QMainWindow > QWidget {\n"
"    border-image : url(img/bg.png);\n"
"    background-color: rgb(0, 0, 0,255);\n"
"\n"
"   /* background-image: url(img/Missing_Texture2.png); 0 0 0 0 stretch stretch;;*/\n"
"    background-size: 10px auto;\n"
"    background-attachment: fixed;\n"
"    /*background-repeat: no-repeat;*/\n"
"}\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.PlayerBox = QtWidgets.QGroupBox(self.centralwidget)
        self.PlayerBox.setMinimumSize(QtCore.QSize(0, 140))
        self.PlayerBox.setMaximumSize(QtCore.QSize(16777215, 140))
        self.PlayerBox.setStyleSheet("QGroupBox{\n"
"   border:1px solid;\n"
"   border-color:rgb(0,0,0);\n"
"   border-top:0; \n"
"   border-bottom:0;\n"
"   backgorund-color:rgb(100, 100, 100,1);\n"
"}")
        self.PlayerBox.setObjectName("PlayerBox")
        self.PlayerBoxFirk = QtWidgets.QHBoxLayout(self.PlayerBox)
        self.PlayerBoxFirk.setContentsMargins(0, 0, 0, 0)
        self.PlayerBoxFirk.setSpacing(0)
        self.PlayerBoxFirk.setObjectName("PlayerBoxFirk")
        self.Visualframe = QtWidgets.QFrame(self.PlayerBox)
        self.Visualframe.setEnabled(True)
        self.Visualframe.setMinimumSize(QtCore.QSize(140, 140))
        self.Visualframe.setMaximumSize(QtCore.QSize(140, 140))
        self.Visualframe.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Visualframe.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Visualframe.setObjectName("Visualframe")
        self.AlbumImg = QtWidgets.QLabel(self.Visualframe)
        self.AlbumImg.setGeometry(QtCore.QRect(0, 0, 140, 140))
        self.AlbumImg.setMinimumSize(QtCore.QSize(140, 140))
        self.AlbumImg.setMaximumSize(QtCore.QSize(140, 140))
        self.AlbumImg.setText("")
        self.AlbumImg.setPixmap(QtGui.QPixmap("img/Missing_Texture2.png"))
        self.AlbumImg.setScaledContents(False)
        self.AlbumImg.setAlignment(QtCore.Qt.AlignCenter)
        self.AlbumImg.setObjectName("AlbumImg")
        self.MSMPmenu = QtWidgets.QPushButton(self.Visualframe)
        self.MSMPmenu.setGeometry(QtCore.QRect(0, 0, 30, 30))
        self.MSMPmenu.setStyleSheet(" \n"
"QPushButton{\n"
"  background-color: rgba(18, 18, 18,0);\n"
"  color: rgba(18, 18, 18,0);\n"
"  border: none;\n"
"}\n"
"QPushButton:hover{\n"
"  background-color: rgb(100,100, 100);\n"
"  color: rgb(100,100, 100);\n"
"  border: none;\n"
"  border-image : url(icon.png);\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"  background-color: rgb(200,200, 200);\n"
"  color:  rgb(200,200, 200);\n"
"  border: none;\n"
"  border-image : url(icon.png);\n"
"}\n"
"")
        self.MSMPmenu.setText("")
        self.MSMPmenu.setIconSize(QtCore.QSize(30, 30))
        self.MSMPmenu.setShortcut("")
        self.MSMPmenu.setAutoRepeat(False)
        self.MSMPmenu.setAutoExclusive(False)
        self.MSMPmenu.setFlat(True)
        self.MSMPmenu.setObjectName("MSMPmenu")
        self.PlayerBoxFirk.addWidget(self.Visualframe)
        self.ContorlPanel = QtWidgets.QGroupBox(self.PlayerBox)
        self.ContorlPanel.setMinimumSize(QtCore.QSize(0, 142))
        self.ContorlPanel.setMaximumSize(QtCore.QSize(16777215, 142))
        self.ContorlPanel.setStyleSheet("QGroupBox{\n"
"   background-color:qlineargradient(spread:pad, x1:0.278, y1:1, x2:0, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"   color:rgb(0,0,0);\n"
"   border:none;\n"
"   border-bottom: 1px solid;\n"
"}")
        self.ContorlPanel.setObjectName("ContorlPanel")
        self.ControlPanelFirk = QtWidgets.QVBoxLayout(self.ContorlPanel)
        self.ControlPanelFirk.setContentsMargins(0, 0, 0, 0)
        self.ControlPanelFirk.setSpacing(0)
        self.ControlPanelFirk.setObjectName("ControlPanelFirk")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(5, -1, -1, -1)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.TreakName = QtWidgets.QLabel(self.ContorlPanel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TreakName.sizePolicy().hasHeightForWidth())
        self.TreakName.setSizePolicy(sizePolicy)
        self.TreakName.setMinimumSize(QtCore.QSize(0, 0))
        self.TreakName.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.TreakName.setFont(font)
        self.TreakName.setStyleSheet("QLabel{\n"
"background-color: rgba(0,0,0,0);\n"
"color:rgba(255, 0, 0)\n"
"}")
        self.TreakName.setObjectName("TreakName")
        self.verticalLayout_3.addWidget(self.TreakName)
        self.AuthorName = QtWidgets.QLabel(self.ContorlPanel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AuthorName.sizePolicy().hasHeightForWidth())
        self.AuthorName.setSizePolicy(sizePolicy)
        self.AuthorName.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Chicago")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.AuthorName.setFont(font)
        self.AuthorName.setStyleSheet("QLabel{\n"
"background-color: rgba(0,0,0,0);\n"
"color:rgba(255, 0, 0)\n"
"}")
        self.AuthorName.setObjectName("AuthorName")
        self.verticalLayout_3.addWidget(self.AuthorName)
        self.AlbumName = QtWidgets.QLabel(self.ContorlPanel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AlbumName.sizePolicy().hasHeightForWidth())
        self.AlbumName.setSizePolicy(sizePolicy)
        self.AlbumName.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setFamily("Chicago")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.AlbumName.setFont(font)
        self.AlbumName.setMouseTracking(False)
        self.AlbumName.setStyleSheet("QLabel{\n"
"background-color: rgba(0,0,0,0);\n"
"color:rgba(255, 0, 0)\n"
"}")
        self.AlbumName.setObjectName("AlbumName")
        self.verticalLayout_3.addWidget(self.AlbumName)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.ControlPanelFirk.addLayout(self.horizontalLayout_3)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(5, -1, -1, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.DataPath = QtWidgets.QLabel(self.ContorlPanel)
        font = QtGui.QFont()
        font.setFamily("Chicago")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.DataPath.setFont(font)
        self.DataPath.setStyleSheet("QLabel{\n"
"background-color: rgba(0,0,0,0);\n"
"color:rgba(255, 0, 0)\n"
"}")
        self.DataPath.setObjectName("DataPath")
        self.horizontalLayout_4.addWidget(self.DataPath)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.TimePlayCounter = QtWidgets.QLabel(self.ContorlPanel)
        font = QtGui.QFont()
        font.setFamily("Chicago")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.TimePlayCounter.setFont(font)
        self.TimePlayCounter.setStyleSheet("QLabel{\n"
"background-color: rgba(0,0,0,0);\n"
"color:rgba(255, 0, 0)\n"
"}")
        self.TimePlayCounter.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.TimePlayCounter.setObjectName("TimePlayCounter")
        self.horizontalLayout_4.addWidget(self.TimePlayCounter)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.ProgressBarTreakSlider = QtWidgets.QSlider(self.ContorlPanel)
        self.ProgressBarTreakSlider.setAutoFillBackground(False)
        self.ProgressBarTreakSlider.setStyleSheet("\n"
"QSlider{\n"
"background-color: rgba(0,0,0,0);\n"
"border: 1px solid;\n"
" border-color:rgb(128, 128, 128);\n"
"}\n"
"/*\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid;\n"
"    height: 22px;\n"
"    margin: 0px;\n"
"    border-color:rgb(128, 128, 128);\n"
"    }\n"
"QSlider::handle:horizontal {\n"
"    background-color: white;\n"
"    height: 40px;\n"
"    width: 5px;\n"
"    margin: -15px 0px;\n"
"   \n"
"    }\n"
"*/\n"
"\n"
"QSlider{\n"
"            }\n"
"            QSlider::groove:horizontal {  \n"
"                 height: 22px;\n"
"                margin: 0px;\n"
"                border-radius: 0px;\n"
"                background: rgba(0,0,0,0);\n"
"            }\n"
"            QSlider::handle:horizontal {\n"
"                background: #b00;\n"
"                width: 8px;\n"
"                border-radius: 0px;\n"
"            }\n"
"            QSlider::sub-page:qlineargradient {\n"
"                background: #fff;\n"
"                border-radius: 0px;\n"
"            }")
        self.ProgressBarTreakSlider.setMaximum(1000)
        self.ProgressBarTreakSlider.setSingleStep(300)
        self.ProgressBarTreakSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ProgressBarTreakSlider.setObjectName("ProgressBarTreakSlider")
        self.verticalLayout_6.addWidget(self.ProgressBarTreakSlider)
        self.ControlPanelFirk.addLayout(self.verticalLayout_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(5, 5, -1, 5)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.PreviousTreakButton = QtWidgets.QPushButton(self.ContorlPanel)
        self.PreviousTreakButton.setMinimumSize(QtCore.QSize(35, 35))
        self.PreviousTreakButton.setMaximumSize(QtCore.QSize(35, 35))
        self.PreviousTreakButton.setStyleSheet("QPushButton{\n"
"  background-color: rgb(50, 50, 50,0.6);\n"
"  border: none;\n"
"}\n"
"QPushButton:hover{\n"
"  background-color: rgb(100,100, 100);\n"
"  border: none;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"  background-color: rgb(200,200, 200);\n"
"  border: none;\n"
"\n"
"}")
        self.PreviousTreakButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PreviousTreakButton.setIcon(icon1)
        self.PreviousTreakButton.setIconSize(QtCore.QSize(30, 30))
        self.PreviousTreakButton.setObjectName("PreviousTreakButton")
        self.horizontalLayout_2.addWidget(self.PreviousTreakButton)
        self.PlayButton = QtWidgets.QPushButton(self.ContorlPanel)
        self.PlayButton.setMinimumSize(QtCore.QSize(35, 35))
        self.PlayButton.setMaximumSize(QtCore.QSize(35, 35))
        self.PlayButton.setStyleSheet("QPushButton{\n"
"  background-color: rgb(50, 50, 50,0.6);\n"
"  border: none;\n"
"}\n"
"QPushButton:hover{\n"
"  background-color: rgb(100,100, 100);\n"
"  border: none;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"  background-color: rgb(200,200, 200);\n"
"  border: none;\n"
"\n"
"}")
        self.PlayButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlayButton.setIcon(icon2)
        self.PlayButton.setIconSize(QtCore.QSize(30, 30))
        self.PlayButton.setObjectName("PlayButton")
        self.horizontalLayout_2.addWidget(self.PlayButton)
        self.NextTreakButton = QtWidgets.QPushButton(self.ContorlPanel)
        self.NextTreakButton.setMinimumSize(QtCore.QSize(35, 35))
        self.NextTreakButton.setMaximumSize(QtCore.QSize(35, 35))
        self.NextTreakButton.setStyleSheet("QPushButton{\n"
"  background-color: rgb(50, 50, 50,0.6);\n"
"  border: none;\n"
"}\n"
"QPushButton:hover{\n"
"  background-color: rgb(100,100, 100);\n"
"  border: none;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"  background-color: rgb(200,200, 200);\n"
"  border: none;\n"
"\n"
"}")
        self.NextTreakButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("img/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.NextTreakButton.setIcon(icon3)
        self.NextTreakButton.setIconSize(QtCore.QSize(30, 30))
        self.NextTreakButton.setObjectName("NextTreakButton")
        self.horizontalLayout_2.addWidget(self.NextTreakButton)
        self.PauseButton = QtWidgets.QPushButton(self.ContorlPanel)
        self.PauseButton.setMinimumSize(QtCore.QSize(35, 35))
        self.PauseButton.setMaximumSize(QtCore.QSize(35, 35))
        self.PauseButton.setStyleSheet("QPushButton{\n"
"  background-color: rgb(50, 50, 50,0.6);\n"
"  border: none;\n"
"}\n"
"QPushButton:hover{\n"
"  background-color: rgb(100,100, 100);\n"
"  border: none;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"  background-color: rgb(200,200, 200);\n"
"  border: none;\n"
"\n"
"}")
        self.PauseButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("img/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PauseButton.setIcon(icon4)
        self.PauseButton.setIconSize(QtCore.QSize(30, 30))
        self.PauseButton.setObjectName("PauseButton")
        self.horizontalLayout_2.addWidget(self.PauseButton)
        self.StopButton = QtWidgets.QPushButton(self.ContorlPanel)
        self.StopButton.setMinimumSize(QtCore.QSize(35, 35))
        self.StopButton.setMaximumSize(QtCore.QSize(35, 35))
        self.StopButton.setStyleSheet("QPushButton{\n"
"  background-color: rgb(50, 50, 50,0.6);\n"
"  border: none;\n"
"}\n"
"QPushButton:hover{\n"
"  background-color: rgb(100,100, 100);\n"
"  border: none;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"  background-color: rgb(200,200, 200);\n"
"  border: none;\n"
"\n"
"}")
        self.StopButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("img/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.StopButton.setIcon(icon5)
        self.StopButton.setIconSize(QtCore.QSize(30, 30))
        self.StopButton.setObjectName("StopButton")
        self.horizontalLayout_2.addWidget(self.StopButton)
        spacerItem1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.VolumeSlider = QtWidgets.QSlider(self.ContorlPanel)
        self.VolumeSlider.setMinimumSize(QtCore.QSize(50, 0))
        self.VolumeSlider.setMaximumSize(QtCore.QSize(150, 16777215))
        self.VolumeSlider.setStyleSheet("\n"
"QSlider{\n"
"background-color: rgba(0,0,0,0);\n"
"border: 1px solid;\n"
" border-color:rgb(128, 128, 128);\n"
"}\n"
"/*\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid;\n"
"    height: 22px;\n"
"    margin: 0px;\n"
"    border-color:rgb(128, 128, 128);\n"
"    }\n"
"QSlider::handle:horizontal {\n"
"    background-color: white;\n"
"    height: 40px;\n"
"    width: 5px;\n"
"    margin: -15px 0px;\n"
"   \n"
"    }\n"
"*/\n"
"\n"
"QSlider{\n"
"            }\n"
"            QSlider::groove:horizontal {  \n"
"                 height: 22px;\n"
"                margin: 0px;\n"
"                border-radius: 0px;\n"
"                background: rgba(0,0,0,0);\n"
"            }\n"
"            QSlider::handle:horizontal {\n"
"                background: #b00;\n"
"                width: 8px;\n"
"                border-radius: 0px;\n"
"            }\n"
"            QSlider::sub-page:qlineargradient {\n"
"                background: #fff;\n"
"                border-radius: 0px;\n"
"            }")
        self.VolumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.VolumeSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.VolumeSlider.setObjectName("VolumeSlider")
        self.horizontalLayout_2.addWidget(self.VolumeSlider)
        self.PlayModeTreak = QtWidgets.QPushButton(self.ContorlPanel)
        self.PlayModeTreak.setMinimumSize(QtCore.QSize(35, 35))
        self.PlayModeTreak.setMaximumSize(QtCore.QSize(35, 35))
        self.PlayModeTreak.setStyleSheet("QPushButton{\n"
"  background-color: rgb(50, 50, 50,0.6);\n"
"  border: none;\n"
"}\n"
"QPushButton:hover{\n"
"  background-color: rgb(100,100, 100);\n"
"  border: none;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"  background-color: rgb(200,200, 200);\n"
"  border: none;\n"
"\n"
"}")
        self.PlayModeTreak.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("img/nexttreak.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlayModeTreak.setIcon(icon6)
        self.PlayModeTreak.setIconSize(QtCore.QSize(30, 30))
        self.PlayModeTreak.setObjectName("PlayModeTreak")
        self.horizontalLayout_2.addWidget(self.PlayModeTreak)
        self.VisualMode = QtWidgets.QPushButton(self.ContorlPanel)
        self.VisualMode.setMinimumSize(QtCore.QSize(35, 35))
        self.VisualMode.setMaximumSize(QtCore.QSize(35, 35))
        self.VisualMode.setStyleSheet("QPushButton{\n"
"  background-color: rgb(50, 50, 50,0.6);\n"
"  border: none;\n"
"}\n"
"QPushButton:hover{\n"
"  background-color: rgb(100,100, 100);\n"
"  border: none;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"  background-color: rgb(200,200, 200);\n"
"  border: none;\n"
"\n"
"}")
        self.VisualMode.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("img/Vizual.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.VisualMode.setIcon(icon7)
        self.VisualMode.setIconSize(QtCore.QSize(30, 30))
        self.VisualMode.setObjectName("VisualMode")
        self.horizontalLayout_2.addWidget(self.VisualMode)
        self.ControlPanelFirk.addLayout(self.horizontalLayout_2)
        self.PlayerBoxFirk.addWidget(self.ContorlPanel)
        self.verticalLayout.addWidget(self.PlayerBox)
        self.PlaylistBox = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PlaylistBox.sizePolicy().hasHeightForWidth())
        self.PlaylistBox.setSizePolicy(sizePolicy)
        self.PlaylistBox.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.PlaylistBox.setObjectName("PlaylistBox")
        self.PlaylistBoxFirk = QtWidgets.QHBoxLayout(self.PlaylistBox)
        self.PlaylistBoxFirk.setContentsMargins(0, 0, 0, 0)
        self.PlaylistBoxFirk.setSpacing(0)
        self.PlaylistBoxFirk.setObjectName("PlaylistBoxFirk")
        self.PlaylistsView = QtWidgets.QTreeView(self.PlaylistBox)
        self.PlaylistsView.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PlaylistsView.sizePolicy().hasHeightForWidth())
        self.PlaylistsView.setSizePolicy(sizePolicy)
        self.PlaylistsView.setMinimumSize(QtCore.QSize(1, 0))
        self.PlaylistsView.setMaximumSize(QtCore.QSize(500, 16777215))
        self.PlaylistsView.setSizeIncrement(QtCore.QSize(0, 0))
        self.PlaylistsView.setMouseTracking(False)
        self.PlaylistsView.setAcceptDrops(False)
        self.PlaylistsView.setStyleSheet("QTreeView{\n"
"color:rgb(255, 255, 255);\n"
"\n"
"}\n"
"\n"
"QTreeView::branch:has-siblings:!adjoins-item {\n"
"    border-image: url(img/stylesheet-vline.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:has-siblings:adjoins-item {\n"
"    border-image: url(img/stylesheet-branch-more.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:!has-children:!has-siblings:adjoins-item {\n"
"    border-image: url(img/stylesheet-branch-end.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:has-children:!has-siblings:closed,\n"
"QTreeView::branch:closed:has-children:has-siblings {\n"
"        border-image: none;\n"
"        image: url(img/stylesheet-branch-closed.png);\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:!has-siblings,\n"
"QTreeView::branch:open:has-children:has-siblings  {\n"
"        border-image: none;\n"
"        image: url(img/stylesheet-branch-open.png);\n"
"}")
        self.PlaylistsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.PlaylistsView.setAnimated(True)
        self.PlaylistsView.setHeaderHidden(True)
        self.PlaylistsView.setObjectName("PlaylistsView")
        self.PlaylistBoxFirk.addWidget(self.PlaylistsView)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.PlaylistView = QtWidgets.QListView(self.PlaylistBox)
        self.PlaylistView.setMinimumSize(QtCore.QSize(500, 0))
        font = QtGui.QFont()
        font.setFamily("Chicago")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PlaylistView.setFont(font)
        self.PlaylistView.setAcceptDrops(False)
        self.PlaylistView.setStyleSheet("QListView{\n"
"  background-color: rgb(50, 50, 50,0.2);\n"
"  color:rgb(255, 255, 255);\n"
"  border: 1px solid;\n"
"}\n"
"\n"
"QListView {\n"
"    show-decoration-selected: 1; /* make the selection span the entire width of the view */\n"
"}\n"
"/*\n"
"QListView::item:alternate {\n"
"    background: #EEEEEE;\n"
"}\n"
"\n"
"QListView::item:selected {\n"
"    border: 1px solid #6a6ea9;\n"
"}\n"
"\n"
"QListView::item:selected:!active {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #ABAFE5, stop: 1 #8588B2);\n"
"}\n"
"\n"
"QListView::item:selected:active {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #6a6ea9, stop: 1 #888dd9);\n"
"}\n"
"\n"
"QListView::item:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #FAFBFE, stop: 1 #DCDEF1);\n"
"}\n"
"\n"
"*/\n"
"QListWidget {padding: 0px;}\n"
"QListWidget::item { margin: 0px; }")
        self.PlaylistView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.PlaylistView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.PlaylistView.setAutoScrollMargin(0)
        self.PlaylistView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.PlaylistView.setDragEnabled(True)
        self.PlaylistView.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.PlaylistView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.PlaylistView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.PlaylistView.setObjectName("PlaylistView")
        self.verticalLayout_5.addWidget(self.PlaylistView)
        self.PlaylistCommandBar = QtWidgets.QGroupBox(self.PlaylistBox)
        self.PlaylistCommandBar.setStyleSheet("QGroupBox{\n"
"   background-color:rgb(50, 50, 50);\n"
"\n"
"}")
        self.PlaylistCommandBar.setObjectName("PlaylistCommandBar")
        self.PlaylistCommandBarFirk = QtWidgets.QHBoxLayout(self.PlaylistCommandBar)
        self.PlaylistCommandBarFirk.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.PlaylistCommandBarFirk.setContentsMargins(0, 0, 0, 2)
        self.PlaylistCommandBarFirk.setSpacing(2)
        self.PlaylistCommandBarFirk.setObjectName("PlaylistCommandBarFirk")
        self.AddTreakPlaylist = QtWidgets.QPushButton(self.PlaylistCommandBar)
        self.AddTreakPlaylist.setMinimumSize(QtCore.QSize(30, 30))
        self.AddTreakPlaylist.setMaximumSize(QtCore.QSize(30, 30))
        self.AddTreakPlaylist.setAutoFillBackground(False)
        self.AddTreakPlaylist.setStyleSheet("QPushButton{\n"
"  background-color: rgba(18, 18, 18);\n"
"  color: rgba(18, 18, 18,0);\n"
"  border: none;\n"
"}\n"
"QPushButton:hover{\n"
"  background-color: rgb(100,100, 100);\n"
"  color: rgb(100,100, 100);\n"
"  border: none;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"  background-color: rgb(200,200, 200);\n"
"  color:  rgb(200,200, 200);\n"
"  border: none;\n"
"}")
        self.AddTreakPlaylist.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("img/add-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AddTreakPlaylist.setIcon(icon8)
        self.AddTreakPlaylist.setIconSize(QtCore.QSize(30, 30))
        self.AddTreakPlaylist.setShortcut("")
        self.AddTreakPlaylist.setObjectName("AddTreakPlaylist")
        self.PlaylistCommandBarFirk.addWidget(self.AddTreakPlaylist)
        self.RemoveTreakPlaylist = QtWidgets.QPushButton(self.PlaylistCommandBar)
        self.RemoveTreakPlaylist.setMinimumSize(QtCore.QSize(30, 30))
        self.RemoveTreakPlaylist.setMaximumSize(QtCore.QSize(30, 30))
        self.RemoveTreakPlaylist.setStyleSheet("QPushButton{\n"
"  background-color: rgb(18, 18, 18);\n"
"  color: rgba(18, 18, 18,0);\n"
"  border: none;\n"
"}\n"
"QPushButton:hover{\n"
"  background-color: rgb(100,100, 100);\n"
"  border: none;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"  background-color: rgb(200,200, 200);\n"
"  border: none;\n"
"\n"
"}")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("img/remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RemoveTreakPlaylist.setIcon(icon9)
        self.RemoveTreakPlaylist.setIconSize(QtCore.QSize(30, 30))
        self.RemoveTreakPlaylist.setShortcut("")
        self.RemoveTreakPlaylist.setObjectName("RemoveTreakPlaylist")
        self.PlaylistCommandBarFirk.addWidget(self.RemoveTreakPlaylist)
        self.MenuPlaylist = QtWidgets.QPushButton(self.PlaylistCommandBar)
        self.MenuPlaylist.setMinimumSize(QtCore.QSize(30, 30))
        self.MenuPlaylist.setMaximumSize(QtCore.QSize(30, 30))
        self.MenuPlaylist.setStyleSheet("QPushButton{\n"
"  background-color: rgb(18, 18, 18);\n"
"  color: rgba(18, 18, 18,0);\n"
"  border: none;\n"
"}\n"
"QPushButton:hover{\n"
"  background-color: rgb(100,100, 100);\n"
"  border: none;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"  background-color: rgb(200,200, 200);\n"
"  border: none;\n"
"\n"
"}")
        self.MenuPlaylist.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("img/menuplaylist.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MenuPlaylist.setIcon(icon10)
        self.MenuPlaylist.setIconSize(QtCore.QSize(30, 30))
        self.MenuPlaylist.setShortcut("")
        self.MenuPlaylist.setObjectName("MenuPlaylist")
        self.PlaylistCommandBarFirk.addWidget(self.MenuPlaylist)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.PlaylistCommandBarFirk.addItem(spacerItem2)
        self.verticalLayout_5.addWidget(self.PlaylistCommandBar)
        self.PlaylistBoxFirk.addLayout(self.verticalLayout_5)
        self.verticalLayout.addWidget(self.PlaylistBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MSMP Stream"))
        self.TreakName.setText(_translate("MainWindow", "TestNameTreak"))
        self.AuthorName.setText(_translate("MainWindow", "NameAuthor"))
        self.AlbumName.setText(_translate("MainWindow", "NameAlbum"))
        self.DataPath.setText(_translate("MainWindow", "YouTube/zr0kiRdU0M8"))
        self.TimePlayCounter.setText(_translate("MainWindow", "2:52/5:21"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
