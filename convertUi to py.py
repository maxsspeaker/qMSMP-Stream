import os


os.system("pyuic6 untitledNewBoxpyqt6.ui -o NewMainUI2.py")


f = open('NewMainUI2.py', 'r')
f2 = open('NewMainUI.py', 'w')

firk=f.read().replace("A:/YandexDisk/python-projects/MSMPstream/MSMPstreamGit/",'"+workingDir+"').replace("def setupUi(self, MainWindow):","def setupUi(self, MainWindow,workingDir,AccentColor=(183,46,43)):")# (183,46,43)

firk=firk.replace("rgb(183,46,43)",'rgb("+str(AccentColor[0])+","+str(AccentColor[1])+","+str(AccentColor[2])+")')
firk=firk.replace("#B72E2B",'rgb("+str(AccentColor[0])+","+str(AccentColor[1])+","+str(AccentColor[2])+")')


f2.write(firk)
