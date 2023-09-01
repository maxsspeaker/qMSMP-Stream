import os


os.system("pyuic6 untitledNewBoxpyqt6.ui -o NewMainUI2.py")
os.system("pyuic6 YtDownloader.ui -o NewMainUIDownloader.py")



f = open('NewMainUI2.py', 'r')
f2 = open('NewMainUI.py', 'w')

firk=f.read().replace("/media/maxsspeaker/HDD_gamesWin/YandexDisk/python-projects/MSMPstream/MSMPstreamGit/",'"+workingDir+"').replace("def setupUi(self, MainWindow):","def setupUi(self, MainWindow,workingDir,AccentColor=(183,46,43),NormalColor=(16,16,16)):")# (183,46,43)

firk=firk.replace("rgb(183,46,43)",'rgb("+str(AccentColor[0])+","+str(AccentColor[1])+","+str(AccentColor[2])+")')
firk=firk.replace("#B72E2B",'rgb("+str(AccentColor[0])+","+str(AccentColor[1])+","+str(AccentColor[2])+")')
firk=firk.replace("rgb(25, 255,25)",'rgb("+str(NormalColor[0])+","+str(NormalColor[1])+","+str(NormalColor[2])+")')

f2.write(firk)




os.system("pyuic6 untitledNewBoxMb.ui -o NewMainUI2mb.py")




f = open('NewMainUI2mb.py', 'r')
f2 = open('NewMainUImb.py', 'w')

firk=f.read().replace("/media/maxsspeaker/HDD_gamesWin/YandexDisk/python-projects/MSMPstream/MSMPstreamGit/",'"+workingDir+"').replace("def setupUi(self, MainWindow):","def setupUimb(self, MainWindow,workingDir,AccentColor=(183,46,43),NormalColor=(16,16,16)):")# (183,46,43)

firk=firk.replace("rgb(183,46,43)",'rgb("+str(AccentColor[0])+","+str(AccentColor[1])+","+str(AccentColor[2])+")')
firk=firk.replace("#B72E2B",'rgb("+str(AccentColor[0])+","+str(AccentColor[1])+","+str(AccentColor[2])+")')
firk=firk.replace("rgb(25, 255,25)",'rgb("+str(NormalColor[0])+","+str(NormalColor[1])+","+str(NormalColor[2])+")')

firk=firk.replace("def retranslateUi","def retranslateUimb")
firk=firk.replace("self.retranslateUi(MainWindow)","self.retranslateUimb(MainWindow)")



f2.write(firk)
