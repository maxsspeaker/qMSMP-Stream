import sys,socket, time, os, traceback,random
import json, yaml

import MSMPstream
print(sys.argv)
os.chdir(MSMPstream.__file__.replace(os.path.basename(MSMPstream.__file__),"")) 

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox , QFileSystemModel
from PyQt5.QtGui import QIcon,QFont,QPalette
from os.path import exists
from PyQt5.uic import loadUi as LoadStyleUI
from PIL import Image,ImageStat
from PIL.ImageQt import ImageQt
import io
import logging
from logging.handlers import QueueHandler
import pypresence
from datetime import date



##logging.basicConfig(filename="all.log",
##                            filemode='a',
##                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
##                            datefmt='%H:%M:%S',
##                            level=logging.DEBUG)

#printError
logger = logging.getLogger()


#print=logger.info
printError=logger.error
    
logger.addHandler(logging.StreamHandler())
logger.info("starting...")


#today = date.today()
##handler = logging.FileHandler(
##    filename='logs/discord-'+str(today)+'.log',
##    encoding='utf-8',
##    mode="w"
##)
#logger.addHandler(logging.StreamHandler())

#import mainUI
from MSMPstream.AppUi import NewMainUI as mainUI
from MSMPstream.AppUi import NewMainUIDownloader as mainUIDownloader
from MSMPstream.AppUi import NewMainUImb as mainUimb


from MSMPstream.AppUi import TrekBox as TrekBoxUi
from MSMPstream.AppUi import MSMPTrekBox as MSMPTrekBoxUi

from yandex_music import Client as YandexMusicClient
from vkaudiotoken import supported_clients

import re
import stagger
import requests
import urllib

import yt_dlp as youtube_dl

from eyed3 import id3
from eyed3 import load
#from threading import Thread
import vlc


from MSMPstream.lib.MSMPcore import MSMPboxPlayer
from MSMPstream.lib.qtHelpers import *
from MSMPstream.lib.configLoader import *
from MSMPstream.lib.MSMP_RPC import MSMP_RPC
from MSMPstream.lib.ProcessRunnable import ProcessRunnable
from MSMPstream.lib.notifiBox import notifiBox
import MSMPstream.lib.TermuxHelpers


TrekBoxUi.QtWidgets.QSlider=Slider

               
class MyYTLogger:
    def __init__(self,FullInfo,logger,QPlainTextEdit=None,RenderWindow=None):
        self.FullInfo=FullInfo
        self.logger=logger
        self.QPlainTextEdit=QPlainTextEdit
        self.RenderWindow=RenderWindow
        #print(QPlainTextEdit) 
        
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            self.logger.debug(msg) 
        else:
            self.logger.debug(msg)
        if not(self.QPlainTextEdit==None):
             self.QPlainTextEdit.appendPlainText(msg)
             self.QPlainTextEdit.repaint()
             self.RenderWindow.update()

    def info(self, msg):  
        if(self.FullInfo):self.logger.info(msg)
        if not(self.QPlainTextEdit==None):
             self.QPlainTextEdit.appendPlainText(msg)
             self.QPlainTextEdit.repaint()
             self.RenderWindow.update()
        pass

    def warning(self, msg):
        self.logger.warning(msg)
        if not(self.QPlainTextEdit==None):
             self.QPlainTextEdit.appendPlainText(msg)
             self.QPlainTextEdit.repaint()
             self.RenderWindow.update()

    def error(self, msg):
        self.logger.error(msg)
        if not(self.QPlainTextEdit==None):
             self.QPlainTextEdit.appendPlainText(msg)
             self.QPlainTextEdit.repaint()
             self.RenderWindow.update()




#InstanceSettings=[r' --projectm-preset-path='+sys.argv[0].replace(os.path.basename(sys.argv[0]), '')+r'assets/visualizations',r'--soundfont='+sys.argv[0].replace(os.path.basename(sys.argv[0]), '')+r'assets/soundfonts/8bitsf.SF2']

  

        
##class MySpinBox(QtWidgets.QSpinBox):
##    valueHasChanged = pyqtSignal(int)
##
##    def changeProgressBarTreakSlider(self, value):
##        pass
##    
##    def __init__(self, *args, **kwargs):
##        super().__init__(*args, **kwargs)
##        self.valueChanged.connect(self.changeProgressBarTreakSlider)
##
##    def setValue(self, value, emit=False):
##        if not emit:
##            self.valueChanged.disconnect(self.changeProgressBarTreakSlider)
##        super().setValue(value)
##        if not emit:
##            self.valueChanged.connect(self.valueHasChanged)



class MSMPTrekBoxUi(QtWidgets.QDialog,MSMPTrekBoxUi.Ui_Dialog): 
     def __init__(self,MainWindow,cookiesFile=None):
          super().__init__()
          self.setupUi(self)
          self.MainWindow=MainWindow
          self.ContinePlay=False
     def add_functions(self):
          self.buttonBox.accepted.connect(self.AddTrek)
          self.buttonBox.rejected.connect(lambda: self.hide())
          self.LoadTrek.clicked.connect(lambda: self.FindTrek(self.UrlText.text()))
     def LoadImgTrek(self):
          #LogBoxYT_dlp
          urlSoundID=self.hostUrlName.replace("https://","").replace("http://","")+self.idSoundName+"AlbumImg.png"
          if not(os.path.isfile(self.MainWindow.PathImgsCache+urlSoundID)):
                     r = requests.get(self.Urlimg, stream=True)
                     r.raw.decode_content = True # Content-Encoding
                     ImgAlbum = Image.open(r.raw).convert("RGBA")
                     ImgAlbum=crop_center(ImgAlbum,ImgAlbum.size[1],ImgAlbum.size[1])
                     ImgAlbum.thumbnail((140,140)) #SoundCloudAlbumImg.png #270
          else:
                     ImgAlbum = Image.open(self.MainWindow.PathImgsCache+urlSoundID).convert("RGBA")
          ImgAlbum =ImageQt(ImgAlbum)

          print("Update icon")
          
          pixmap=QtGui.QPixmap.fromImage(ImgAlbum)
          self.AlbumImg.setPixmap(pixmap)
          
                     
     def FindTrek(self,url):
             print("firk")
             data = {"version":self.MainWindow.MSMPboxPlayer.version,"appName":"qMSMP Stream"}
             response = requests.get(url, timeout=10, json=data)
             dataBox = json.loads(response.text)
             if(dataBox["status"]=="OK"):
                   
                   self.Treaktitle=dataBox['Name'] 
                   self.ArtistTrek=dataBox['artist']
                   self.AlbumTrek=dataBox['album']

                   self.dataBox=dataBox

                   hostBox=url.replace("://",":||").split("/")

                   self.hostUrlName=hostBox[0].replace(":||","://")
                   hostBox[0]=""
                   self.idSoundName=hostBox[-1]
                   hostBox[-1]=""

                   self.HostUrlPatch="/".join(hostBox)
                   print(self.HostUrlPatch)
                   print(self.hostUrlName)
                   print(self.idSoundName)
                   
                   
                   self.TreakUploader=dataBox['Uploader']


                   self.durationTreak = dataBox['duration']
                    
                   self.NameTrek.setText(self.Treaktitle)
                   self.NameUploader.setText(self.ArtistTrek)
                   self.NameAlbum.setText(self.AlbumTrek)
                    
                   self.Urlimg=self.hostUrlName+"/"+dataBox["AlbumImg"]
                   self.LoadImgTrek()
             else:
                  if(dataBox["status"]=="OK"):
                       if(dataBox["code"]==404):
                            self.NameTrek.setText("Ошибка: файл не найден")
                    
     def AddTrek(self):
          self.MainWindow.MSMPboxPlayer.playlist.append({
                    "ID": "MSMPNetServer",
                    "HostUrlPatch": self.HostUrlPatch,
                    "hostUrlName": self.hostUrlName,
                    "idSoundName":self.idSoundName,
                    "Name": self.Treaktitle,
                    "AlbumImg": self.dataBox["AlbumImg"],
                    "album": self.AlbumTrek,
                    "artist": self.dataBox["artist"],
                    "Uploader": self.dataBox["Uploader"],
                    "duration": self.durationTreak,
                    "upload_date":self.dataBox["upload_date"],
                    "availability":self.dataBox['availability'],
                    "urlAudio":self.dataBox["urlAudio"]
                    })
          self.MainWindow.PlayButton.setEnabled(True)
          self.MainWindow.NextTreakButton.setEnabled(True)
          self.MainWindow.PauseButton.setEnabled(True)
          self.MainWindow.StopButton.setEnabled(True)
          self.MainWindow.PreviousTreakButton.setEnabled(True)
          try:self.MainWindow.ReloadInformation(False)
          except:pass
          self.hide()


class TrekBoxUi(QtWidgets.QDialog,TrekBoxUi.Ui_Dialog): 
     def __init__(self,MainWindow,cookiesFile=None):
          super().__init__()
          self.setupUi(self)
          self.MainWindow=MainWindow
          self.cookiesFile=cookiesFile
          self.NoPlayListMode=True
          self.BufferUrlFox=""
     def add_functions(self):
          self.buttonBox.accepted.connect(self.AddTrek)
          self.buttonBox.rejected.connect(lambda: self.hide())
          self.LoadTrek.clicked.connect(lambda: self.FindTrek(self.UrlText.text()))
     def LoadImgTrek(self,rYT):
          #LogBoxYT_dlp
          if(rYT['extractor']=="youtube"):
                     urlSoundID=self.IdTreak+"SoundCloudAlbumImg.png"
          elif(rYT['extractor']=="soundcloud"):
                     urlSoundID=self.IdTreak+"AlbumImg.png"
          elif("yandexmusic:track"==rYT['extractor']):
                     urlSoundID=str(self.IdTreakYandexMusic)+"YandexMusicAlbumImg.png"
          #elif("GlobalServerUpload"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                     #urlSoundID=str(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["IDSound"])+"AlbumImg.png"
          else:
               pass
                
          if not(os.path.isfile(self.MainWindow.PathImgsCache+urlSoundID)):
                     r = requests.get(self.Urlimg, stream=True)
                     r.raw.decode_content = True # Content-Encoding
                     ImgAlbum = Image.open(r.raw).convert("RGBA")
                     ImgAlbum=crop_center(ImgAlbum,270,270)
                     if(rYT['id']=="YouTube"):
                          ImgAlbum=crop_center(ImgAlbum,270,270)
                     else:
                          ImgAlbum=crop_center(ImgAlbum,ImgAlbum.size[1],ImgAlbum.size[1])
                     ImgAlbum.thumbnail((140,140)) #SoundCloudAlbumImg.png #270
          else:
                     ImgAlbum = Image.open(self.MainWindow.PathImgsCache+urlSoundID).convert("RGBA")
          ImgAlbum =ImageQt(ImgAlbum)

          print("Update icon")
          
          pixmap=QtGui.QPixmap.fromImage(ImgAlbum)
          self.AlbumImg.setPixmap(pixmap)
          
     def FindTrek(self,url):
          ydl_opts = {
                         'forceurl':True,
                         'ignoreerrors': True,
                         'logger':MyYTLogger(False,logger=self.MainWindow.MSMPboxPlayer.logger,QPlainTextEdit=self.LogBoxYT_dlp,RenderWindow=self),
                         'ignore-config':True,
                         'extract_flat':True,
                         }
          self.TypeTreak=None
          if(self.NoPlayListMode):
               ydl_opts['no-playlist']=self.NoPlayListMode
          else:
               ydl_opts['yes-playlist']=True
               
          print(ydl_opts.get('no-playlist'))     
          if not(self.cookiesFile==None):
               ydl_opts['cookiefile']=self.cookiesFile
          with youtube_dl.YoutubeDL(ydl_opts) as ydl: #
              r = ydl.extract_info(url, download=False)
              if(r):
               print(r['extractor'])
               if(r['extractor']=="soundcloud"):
                    self.durationTreak=r['duration']
                    self.Treaktitle=r['title']
                    self.TreakUploader=r['uploader']
                    self.IdTreak=r['id']
                    self.TypeTreak="soundcloud"
                    self.UrlSc=r["original_url"]
                    
                    self.NameTrek.setText(self.Treaktitle)
                    self.NameUploader.setText(self.TreakUploader)
                    
                    self.Urlimg='https://img.youtube.com/vi/'+r['id']+'/hqdefault.jpg'
                    self.LoadImgTrek(r)
               elif(r['extractor']=="yandexmusic:track"):
                    self.durationTreak=r['duration']
                    self.Treaktitle=r['track']
                    self.TreakUploader=r['album_artist']
                    self.IdTreak=r["original_url"]
                    self.IdTreakYandexMusic=r["id"]
                    
                    regex = "album/(\w+)/"
                    self.AlbumIDYandexMusic=re.findall(regex, r["original_url"])[0]
                    
                    self.TypeTreak="YandexMusic"
                    self.Urlimg=r["thumbnail"]
                    self.LoadImgTrek(r)

                    self.NameTrek.setText(self.Treaktitle)
                    self.NameUploader.setText(self.TreakUploader)
                    
               elif(r['extractor']=="youtube"):
                    self.durationTreak=r['duration']
                    self.Treaktitle=r['title']
                    self.TreakUploader=r['uploader']
                    self.IdTreak=r['id']
                    self.TypeTreak="YouTube"
                    
                    self.NameTrek.setText(self.Treaktitle)
                    self.NameUploader.setText(self.TreakUploader)
                    
                    self.Urlimg='https://img.youtube.com/vi/'+r['id']+'/hqdefault.jpg'
                    self.LoadImgTrek(r)
               elif(r['extractor']=="youtube:tab"):
                  self.TypeTreak="YouTube:pl"
                  self.Treaktitle=r['title']
                  self.TreakUploader="???"
                  self.NameTrek.setText(self.Treaktitle)
                  self.NameUploader.setText(self.TreakUploader)
                  playlist_dict=r
                  #self.LogBoxYT_dlp.appendPlainText(str(playlist_dict))
                  playlist=[]
                  for r in playlist_dict['entries']:
                    if not r:
                        self.LogBoxYT_dlp.appendPlainText('ERROR: Unable to get info. Continuing...')
                        self.LogBoxYT_dlp.repaint() 
                        continue
                    if("[Deleted video]"==str(r['title'])) or ("[Private video]"==str(r['title'])):
                         self.LogBoxYT_dlp.appendPlainText('ERROR: Unable to get info. Continuing...')
                         self.LogBoxYT_dlp.repaint() 
                         continue
                    self.LogBoxYT_dlp.appendPlainText("выбран: "+str(r['title']))
                    self.LogBoxYT_dlp.repaint()
                    self.update()
                    try:
                         playlist.append({"ID":"YouTube","url":r["id"],"name":r['title'],"uploader":r['uploader'],"duration":int(r['duration']),"Publis":False})
                    except KeyError:
                         try:
                              playlist.append({"ID":"YouTube","url":r["id"],"name":r['title'],"uploader":r["channel"],"duration":int(r['duration']),"Publis":False})
                         except KeyError:
                              playlist.append({"ID":"YouTube","url":r["id"],"name":r['title'],"uploader":'???',"duration":int(r['duration']),"Publis":False})
                  self.PltoAdd=playlist
               elif(r['extractor']=="soundcloud"):
                    pass
     def AddTrek(self):
        if not("YouTube:pl"==self.TypeTreak):
          MusicInfoPars={
                    "ID": self.TypeTreak,
                    "url": self.IdTreak,
                    "name": self.Treaktitle,
                    "uploader": self.TreakUploader,
                    "duration": self.durationTreak,
                    "Publis": False
                    }
          if(self.TypeTreak=="YandexMusic"):
               MusicInfoPars["YandexMusicIDalbum"]=self.AlbumIDYandexMusic 
               MusicInfoPars["YandexMusicID"]=self.IdTreakYandexMusic
          elif(self.TypeTreak=="soundcloud"):
               MusicInfoPars["IDSoundcloud"]=self.IdTreak
               MusicInfoPars["url"]=self.UrlSc
          self.MainWindow.MSMPboxPlayer.playlist.append(MusicInfoPars)
          self.MainWindow.PlayButton.setEnabled(True)
          self.MainWindow.NextTreakButton.setEnabled(True)
          self.MainWindow.PauseButton.setEnabled(True)
          self.MainWindow.StopButton.setEnabled(True)
          self.MainWindow.PreviousTreakButton.setEnabled(True)
          try:self.MainWindow.ReloadInformation(False)
          except:pass
          self.hide()
        else:
          self.MainWindow.MSMPboxPlayer.playlist=self.PltoAdd
          if not(self.BufferUrlFox==self.UrlText.text()):
               self.MainWindow.MSMPboxPlayer.play(0)
          else:
               self.MainWindow.MSMPboxPlayer.Num=0
               self.MainWindow.LestNum=0
          self.MainWindow.MSMPboxPlayer.OpenedplaylistPath=self.MainWindow.PlaylistsFolder+"/"+self.Treaktitle+".plmsmpsbox" 
          self.MainWindow.PlayButton.setEnabled(True)
          self.MainWindow.NextTreakButton.setEnabled(True)
          self.MainWindow.PauseButton.setEnabled(True)
          self.MainWindow.StopButton.setEnabled(True)
          self.MainWindow.PreviousTreakButton.setEnabled(True)
          try:self.MainWindow.ReloadInformation()
          except:pass
          self.hide()
          
               
def excepthook(exc_type, exc_value, exc_tb):
  if not(exc_type==KeyboardInterrupt):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    ex.TrekBoxUi.hide()
    print("error catched!")
    print("error message:\n", tb)
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
    msg.setText("MSMP CRASH:")
    msg.setInformativeText(str(tb))
    msg.setWindowTitle("Error")
    retval = msg.exec()
    ex.close()
  else:
       ex.close()


class NameDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if isinstance(index.model(), QFileSystemModel):
            if not index.model().isDir(index):
                option.text = index.model().fileInfo(index).baseName()

    def setEditorData(self, editor, index):
        if isinstance(index.model(), QFileSystemModel):
            if not index.model().isDir(index):
                editor.setText(index.model().fileInfo(index).baseName())
            else:
                super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(model, QFileSystemModel):
            fi = model.fileInfo(index)
            if not model.isDir(index):
                model.setData(index, editor.text() + "." + fi.suffix())
            else:
                super().setModelData(editor, model.index)





               
class MainWindow(QtWidgets.QMainWindow, mainUI.Ui_MainWindow,mainUimb.Ui_MainWindow): #

    def __init__(self,RunAPPEventHandler): 
        super().__init__()

        self.RunAPPEventHandler=RunAPPEventHandler
        self.RunAPPEventHandler.MainWindow = self
        

        InstanceSettings=[]

        self.mobileNewMode=False
        self.mobileMode=False



        #print(color)

        
        QtGui.QFontDatabase.addApplicationFont('img/Chicago Regular.ttf')

        self.config,self.ConfigDir,self.PlaylistsFolder=loadConfig()

        if(self.config['MSMP Stream'].get("mobileMode")==None):
             self.config['MSMP Stream']["mobileMode"]=False

        if(self.config['MSMP Stream'].get('force-ipv4')==None):
             self.config['MSMP Stream']['force-ipv4']=False
             
        self.mobileNewMode=self.config['MSMP Stream']['TermuxMbMode']

        #self.mobileNewMode=True
        #showFullScreen=False

        self.AccentColor=(166, 40, 153)
        self.QAccentColor=QtGui.QColor('rgba(166, 40, 153,255)')
        self.QAccentColor.setRed(self.AccentColor[0])
        self.QAccentColor.setGreen(self.AccentColor[1])
        self.QAccentColor.setBlue(self.AccentColor[2])

        self.NormalColor=(16,16,16)
        self.QNormalColor=QtGui.QColor('rgba(16,16,16,255)')
        self.QNormalColor.setRed(self.AccentColor[0])
        self.QNormalColor.setGreen(self.AccentColor[1])
        self.QNormalColor.setBlue(self.AccentColor[2])
        
        if sys.platform.startswith("linux"):
             palette = app.palette()
             
             self.QAccentColor = palette.color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Highlight)
             self.AccentColor=self.QAccentColor.getRgb()

             self.QNormalColor = palette.color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Window)
             self.NormalColor =self.QNormalColor.getRgb()
             print(self.NormalColor)

        #print(self.QAccentColor.getRgb())
        

        self.Forceipv4=True

        if(self.Forceipv4):
             InstanceSettings.append("--ipv4")

        self.LocalImgCache={}

        if(self.mobileNewMode):
             self.NewMainUI=False
             self.setupUimb(self,workingDir=MSMPstream.__file__.replace(os.path.basename(MSMPstream.__file__),""),AccentColor=self.AccentColor,NormalColor=self.NormalColor)
        else:
             self.NewMainUI=True
             self.setupUi(self,workingDir=MSMPstream.__file__.replace(os.path.basename(MSMPstream.__file__),""),AccentColor=self.AccentColor,NormalColor=self.NormalColor)
#  #os.path.dirname(sys.argv[0]).replace("\\","/")+"/"
        #self.FixScrollBlat()
        if(self.config['MSMP Stream']["localizationBox"]=="assets/localizationBoxes/ru.localizationBox"):
             self.config['MSMP Stream']['localizationBox']='lengboxs/ru.loclb'

        self.show()
        
        self.PlayerBox.hide()
        self.PlaylistBox.hide()
        self.NewMainUI=True
        if not(self.mobileNewMode):
             #self.NewMainUI=True
             self.NewMainUIb=self.NewMainUI
             self.LoadingLabel.show()
        else:
             #self.NewMainUI=False
             self.LoadingLabel.hide()
             self.NewMainUIb=self.NewMainUI

        self.update()

        

        print(self.config['MSMP Stream']['localizationBox'])
        self.lengbox=loadLocal(self.config['MSMP Stream']['localizationBox'])
        
##        if sys.platform == "win32":
##            InstanceSettings.append("--audio-visual="+"visual")
##            InstanceSettings.append("--effect-list=spectrum")
##            InstanceSettings.append("--effect-fft-window=none")

        self.CloseApp=False
        self.CloseAppFox=0

        self.UpdateBgAllowed=False


        print(self.ConfigDir)

        if(self.config['MSMP Stream'].get("notifiDisabled")==None):
             self.config['MSMP Stream']["notifiDisabled"]=False 

        if(self.config['MSMP Stream'].get('CDcaseImgRPC')==None):
             self.config['MSMP Stream']['CDcaseImgRPC']=False

        if(self.config['MSMP Stream'].get('TOKENvkMusic')==None):
             self.config['MSMP Stream']['TOKENvkMusic']=None
         
        
        if(self.config['MSMP Stream RPC'].get("last-fmAllowed")==None):
             self.config['MSMP Stream RPC']["last-fmAllowed"]=False
        
        OtherApiAlow=False
        if(self.config['MSMP Stream RPC']['Discord_rpc']):
             Presence=True
             OtherApiAlow=True
        else:
             Presence=None
             
        if(self.config['MSMP Stream RPC']["last-fmAllowed"]):
             LastFm=True
             OtherApiAlow=True
        else:
             LastFm=False

        if (self.config.get('MSMP API')):
             ImgApiHostTOKEN=self.config['MSMP API']["TOKEN"]
             ImgApiHost=self.config['MSMP API']["ImgApiHost"]
        else:
             ImgApiHostTOKEN=None
             ImgApiHost=None

        if(self.config['MSMP Stream'].get("YandexMusicTOKEN")==None):
             self.config['MSMP Stream']["YandexMusicTOKEN"]=""
             
        if(OtherApiAlow):
             self.RPC=MSMP_RPC(RPC=Presence,DirConfig=self.ConfigDir,LastFm=LastFm,version="QT0.7.8a",lengbox=self.lengbox,ImgApiHost=ImgApiHost,ImgApiHostTOKEN=ImgApiHostTOKEN,RPCbuttons=self.config['MSMP Stream RPC']['Discord_Buttons'])
        else:
            self.RPC=None 
        self.MSMPboxPlayer=MSMPboxPlayer(ServerPlaer=True,
                                         InstanceSettings=InstanceSettings,
                                         MSMP_RPC=self.RPC,
                                         logger=logger,
                                         AutoSplitAuthorName=True,
                                         downloadMusicFolder=self.config['MSMP Stream']['downloadMusicFolder'],TOKENvkMusic=self.config['MSMP Stream']['TOKENvkMusic'],
                                         TOKENYandexMusicClient=self.config['MSMP Stream']["YandexMusicTOKEN"],
                                         CDcase=self.config['MSMP Stream']['CDcaseImgRPC'],forceIpv4=self.config['MSMP Stream']['force-ipv4']) #,MyYTLogger=MyYTLogger
        self.MSMPboxPlayer.playlist=[] #

        #self.cookiesSoundCloud=""
        #  self.cookiesYouTube=""
        #  self.cookiesYandexMusic=""

        
        #self.initUI()
        #self.MSMPboxPlayer.playlist=[{"ID": "YouTube", "url": "Q52GzsGmRuk", "name": "Hold", "uploader": "Home", "duration": 210, "Publis": False},
        #                             {"ID": "YouTube", "url": "5py6E6yo7wk", "name": "Siberian (BGM)", "uploader": "LEMMiNO", "duration": 210, "Publis": False},
        #                             {"ID": "YouTube", "url": "XeiR1w236yo", "name": "Sunshower", "uploader": "Home", "duration": 210, "Publis": False},
        #                             {"ID": "YouTube", "url": "d6SQb0WTrlA", "name": "Glimmer", "uploader": "AGST", "duration": 210, "Publis": False}]

        #mainUI.QtWidgets.QSpinBox=MySpinBox
        

        self.TrekBoxUi=TrekBoxUi(self,cookiesFile=self.config['MSMP Stream'].get("cookiesFile"))
        self.TrekBoxUi.add_functions()
        self.MSMPTrekBoxUi=MSMPTrekBoxUi(self)
        self.MSMPTrekBoxUi.add_functions()

        self.MSMPboxPlayer.OpenedplaylistPath=None
        

        #self.statusBar = self.statusBar()

        #PlAnalizequeue={}


        try:
             self.notifiBox=notifiBox(Disabled=self.config['MSMP Stream']["notifiDisabled"])
        except:
             self.notifiBox=notifiBox(Disabled=True)
             #LoadStyleUI("ui/untitled.ui",self)

        #self.PlaylistsFolder=r"../../bmCastMusic/myPlaylists"
        

        
        

        
        
##        self.PlaylistWidget.insertItem(0, "test")
##        self.PlaylistWidget.insertItem(1, "test1")
##        self.PlaylistWidget.insertItem(2, "test2")
##        self.PlaylistWidget.insertItem(3, "test3")
##        self.PlaylistWidget.insertItem(4, "test4")
##        self.PlaylistWidget.insertItem(5, "test5")
##        
        
            #cov = None
            
            #self.MSMPboxPlayer.LoadImg(None,ItemP['ID'],ItemP['url'])
            
            #covurl = self.MSMPboxPlayer.CoverUrlPlayNow

##            print(ItemP["name"]+"\n"+ItemP["uploader"])
##            print(i,'/',len(self.MSMPboxPlayer.playlist))
##            
##            imgurl = '.msmpcache/'+ItemP['url']+".jpg"
##
##            if False: #not exists(imgurl):
##                if covurl:
##                    try:
##                        data = urllib.request.urlopen(covurl).read()
##                        im = Image.open(io.BytesIO(data))
##                        im.thumbnail((140,140))
##                        im.save(imgurl)
##                        cov = QtGui.QIcon(imgurl)
##                        #com = im.tobytes()
##                        #pixmap = QtGui.QPixmap()
##                        #pixmap.loadFromData(com)
##                        #cov = QtGui.QIcon(pixmap)
##                        print('loaded')
##                        
##                    except urllib.error.HTTPError:
##                        cov = QtGui.QIcon("img/X9at37tsrY8AlbumImg.png")
##                        print('err, default')
##                else:
##                    cov = QtGui.QIcon("img/X9at37tsrY8AlbumImg.png")
##                    print('nocov, default')
##            else:
##                cov = QtGui.QIcon("img/X9at37tsrY8AlbumImg.png")
##                print('cached, loaded')
##                
##
##            #it.setData(QtGui.QIcon(iconroot +'/images/flags'), QtCore.Qt.ItemDataRole.DecorationRole)
##            it.setData(cov,        # +++
##                                   QtCore.Qt.ItemDataRole.DecorationRole)
        
        self.PathImgsCache=self.config['MSMP Stream']['cacheimgpachfolder']

        self.DownloaderProcess=None
        self.add_functions()

        if(self.NewMainUI):
             self.FoxStatusBar.setText("")
        

        self.ProgressUpdate=False
        self.LestNum=-1

        self.PlayModeMSMP="nexttreak"
        self.PlayModeMSMPNum=0
        self.PlayModeMSMPModes=["nexttreak","looptreak","randomtreak"]

        self.PlayerBox.show()
        self.PlaylistBox.show()
        
        if not(self.mobileMode):self.LoadingLabel.hide()
        
        if(self.mobileMode):
                   self.PlaylistsView.hide()
                   #self.showFullScreen()
                   TermuxHelpers.setWindowFullScreen(self,app)
                   
        if(self.mobileNewMode):
             self.PlaylistsView.hide()
             #if(showFullScreen):
                  #self.showFullScreen()
        
        #it.setBackground(QtGui.QColor('red'))
        
        self.isPlayListSelectionChanged=False
        
        
        if(self.mobileNewMode):
             self.MSMPboxPlayer.NewPlaerVLC.audio_set_volume(100)
        else:
             self.VolumeSlider.setValue(self.MSMPboxPlayer.NewPlaerVLC.audio_get_volume())
        
        self.bufferNewPlaerVLCposition=0
        self.p = ProcessRunnable(target=self.updateBgGui, args=())
        self.p.start()


        self.pEvent = ProcessRunnable(target=self.RunAPPEventHandler.RunEventServer, args=())
        self.pEvent.start()
        
        self.EqualizerPlaerVLC=vlc.AudioEqualizer()
        self.setEqualizer()

        
        self.ContinePlay=False
        self.NoAlbumImgs=False

        qr=self.frameGeometry()           
        cp=app.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        print(app.primaryScreen().availableGeometry())

        size=app.primaryScreen().availableGeometry()

        if(self.mobileNewMode):
             self.resize(size.width(), size.height() )


        if(self.ContinePlay):
             pass
             #self.PathToPlMSMPbox=""
             #self.OpenPlmsmpThread()
    def ContextMenuRemoveTreak(self):
         selections=self.PlaylistView.selectedIndexes()
         if(len(selections)==1):
                self.PlayListContextMenuItem=self.PlaylistView.model().itemFromIndex(selections[0])
                
                del self.MSMPboxPlayer.playlist[self.PlayListContextMenuItem.row()]
                self.PlaylistView.model().removeRow(self.PlayListContextMenuItem.row())
         else:
              FirkItems=len(selections)
              i=0
              self.PlayListContextMenuItem=self.PlaylistView.model().itemFromIndex(selections[0]).row()

              while not (i==FirkItems):
                   del self.MSMPboxPlayer.playlist[self.PlayListContextMenuItem]
                   self.PlaylistView.model().removeRow(self.PlayListContextMenuItem)
                   
                   i=i+1
    def ContextMenuLoadMix(self):
         selections=self.PlaylistView.selectedIndexes()
         
         self.PlayListContextMenuItem=self.PlaylistView.model().itemFromIndex(selections[0]).row()

         VideoId=self.MSMPboxPlayer.playlist[self.PlayListContextMenuItem]["url"]
              
         self.TrekBoxUi.NoPlayListMode=False
         self.TrekBoxUi.ContinePlay=True
         self.TrekBoxUi.UrlText.setText(f"https://www.youtube.com/watch?v={VideoId}&list=RD{VideoId}&start_radio=1")
         self.TrekBoxUi.BufferUrlFox=f"https://www.youtube.com/watch?v={VideoId}&list=RD{VideoId}&start_radio=1"
         self.TrekBoxUi.show()

              
    def PlayListContextMenu(self, position):
      try:
        styleColorFox=str(self.AccentColor[0])+","+str(self.AccentColor[1])+","+str(self.AccentColor[2])
        menu = QtWidgets.QMenu(self)

        selections=self.PlaylistView.selectedIndexes()
        #print(position)

        # Создание действий для меню
        self.PlayListContextMenuItem=self.PlaylistView.model().itemFromIndex(selections[0]).row()
        
                                        
        if(len(selections)==1):
             if(self.MSMPboxPlayer.playlist[self.PlayListContextMenuItem]["ID"]=="YouTube"):
                  action1 = QtWidgets.QAction("Загрузить Микс", self)
                  action1.triggered.connect(self.ContextMenuLoadMix)
                  menu.addAction(action1)
             action2 = QtWidgets.QAction("Удалить трек", self)
        else:
             action2 = QtWidgets.QAction("Удалить треки", self)
             
        action2.triggered.connect(self.ContextMenuRemoveTreak)
        menu.addAction(action2)
        

        # Добавление действий в меню
        

        # Показ контекстного меню в указанной позиции
        
        
        menu.setStyleSheet("""QMenu {
    background-color: rgb(50,50,50); /* sets background of the menu */
    border: 1px solid black;
}

QMenu::item {
    /* sets background of menu item. set this to something non-transparent
        if you want menu color and menu item color to be different */
    background-color: transparent;
    color:white;
}

QMenu::item:selected { /* when user selects item using mouse or keyboard */
    background-color: rgb("""+styleColorFox+""");
}""")
        menu.exec(self.PlaylistView.viewport().mapToGlobal(position))
      except IndexError:
          pass
    def FixScrollBlat(self):
          styleColorFox=str(self.AccentColor[0])+","+str(self.AccentColor[1])+","+str(self.AccentColor[2])
          self.setStyleSheet("""
QScrollBar:vertical{
        background-color: #2A2929;
        width: 17px;
        margin: 14px 3px 14px 3px;
        border: 0px transparent;
        border-radius: 0px;
}

QScrollBar::handle:vertical{
        background-color: #181818;         /* #605F5F; */  
        min-height: 5px;
}
QScrollBar::handle:vertical:hover{
        background-color: rgb("""+styleColorFox+""");         
        min-height: 5px;
}


QScrollBar::sub-line:vertical{
        margin: 3px 0px 3px 0px;
        border-image: url(A:/YandexDisk/python-projects/MSMPstream/MSMPstreamGit/img/SliderUp.png);
        background-color: rgb(80, 80, 80);
        height: 11px;
        width: 11px;
        subcontrol-position: top;
        subcontrol-origin: margin;
}

QScrollBar::add-line:vertical{
        margin: 3px 0px 3px 0px;
        border-image: url(A:/YandexDisk/python-projects/MSMPstream/MSMPstreamGit/img/SliderDown.png);
        background-color: rgb(80, 80, 80);
        height: 11px;
        width: 11px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on{
        border-image: url(A:/YandexDisk/python-projects/MSMPstream/MSMPstreamGit/img/SliderUp.png);
        background-color: rgb("""+styleColorFox+""");  
        height: 11px;
        width: 11px;
        subcontrol-position: top;
        subcontrol-origin: margin;
}

QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on{
        border-image: url(A:/YandexDisk/python-projects/MSMPstream/MSMPstreamGit/img/SliderDown.png);
        background-color: rgb("""+styleColorFox+""");  
        height: 11px;
        width: 11px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{
        background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{
        background: none;
}




QMenu {
    background-color: rgb(50,50,50); /* sets background of the menu */
    border: 1px solid black;
}

QMenu::item {
    /* sets background of menu item. set this to something non-transparent
        if you want menu color and menu item color to be different */
    background-color: transparent;
    color:white;
}

QMenu::item:selected { /* when user selects item using mouse or keyboard */
    background-color:  rgb("""+styleColorFox+""");  
}
""")
          self.qMenuStylesheetFix="""
QMenu {
    background-color: rgb(50,50,50); /* sets background of the menu */
    border: 1px solid black;
}

QMenu::item {
    /* sets background of menu item. set this to something non-transparent
        if you want menu color and menu item color to be different */
    background-color: transparent;
    color:white;
}

QMenu::item:selected { /* when user selects item using mouse or keyboard */
    background-color: rgb("""+styleColorFox+"""); 
}
"""
    def add_functions(self):

        self.model = self.get_file_tree_model(self.PlaylistsFolder)

        self.PlaylistsView.setModel(self.model)
        self.PlaylistsView.setRootIndex(self.model.index(self.PlaylistsFolder))

        self.FixScrollBlat()

        self.PlaylistsViewShowed=True
        self.PlaylistsView.hideColumn(3)
        self.PlaylistsView.hideColumn(2)
        self.PlaylistsView.hideColumn(1)
        self.PlaylistsView.doubleClicked.connect(self.handle_double_click)
        delegate = NameDelegate(self.PlaylistsView)
        self.PlaylistsView.setItemDelegate(delegate)
        
        self.PlayListAddMenu = QtWidgets.QMenu()
        self.PlayListAddMenu.setStyleSheet(self.qMenuStylesheetFix)
        self.PlayListAddMenu.triggered.connect(lambda x: self.AddTrekOptions(x.data))
        self.AddTreakPlaylist.setMenu(self.PlayListAddMenu)

        self.RemoveTreakMenu = QtWidgets.QMenu()
        self.RemoveTreakMenu.setStyleSheet(self.qMenuStylesheetFix)
        self.RemoveTreakMenu.triggered.connect(lambda x: print(x.data))
        self.RemoveTreakPlaylist.setMenu(self.RemoveTreakMenu)

        self.MenuPlaylistMenu = QtWidgets.QMenu()
        self.MenuPlaylistMenu.setStyleSheet(self.qMenuStylesheetFix)
        self.MenuPlaylistMenu.triggered.connect(lambda x: self.PlTrekOptions(x.data))
        self.MenuPlaylist.setMenu(self.MenuPlaylistMenu)

        self.MSMPqmenu = QtWidgets.QMenu()
        self.MSMPqmenu.setStyleSheet(self.qMenuStylesheetFix)
        self.MSMPqmenu.triggered.connect(lambda x: self.SkinChanger(x.data))
        self.MSMPmenu.setMenu(self.MSMPqmenu)
        

        MSMPmenuData=[self.lengbox["MSMP Stream"].get("obu")+"#obu",self.lengbox["MSMP Stream"].get("Set")+"#Set"]
        

        if not(self.mobileMode):
             MSMPmenuData.append(self.lengbox["MSMP Stream"].get("PLshHd")+"#PLshHd")
##             MSMPmenuData.append("SKIN TOP#st")
             MSMPmenuData.append("SKIN BOTTOM#sb")
             MSMPmenuData.append("changeColor#ColorFox")
             #MSMPmenuData.append("RunDownloader#RuDown") 
##             MSMPmenuData.append("SKIN OLD#OLDskin")
##             MSMPmenuData.append("SKIN AIMPqt#AIMPskin")
##             MSMPmenuData.append("mbMode#mbMode")

        MSMPmenuData.append("setEqualizer#sEq")
        MSMPmenuData.append(self.lengbox["MSMP Stream"].get("Cls")+"#Cls")
        
        if(self.mobileNewMode):
             self.PlSelector=False
             self.ButtonShowPlSelector.clicked.connect(lambda: self.ShowPlSelector())
        
        self.add_menu(MSMPmenuData, self.MSMPqmenu)
        self.add_menu([self.lengbox["MSMP Stream"].get("RT")+"#RT",self.lengbox["MSMP Stream"].get("CPL")+"#CPL"], self.RemoveTreakMenu)
        
        self.add_menu([self.lengbox["MSMP Stream"].get("addLF")+"#addLF",{self.lengbox["MSMP Stream"].get("addAS")+"#addAS": ["MSMP audio"+"#addAS-Ma",self.lengbox["MSMP Stream"].get("addAS-YV")+"#addAS-YV",self.lengbox["MSMP Stream"].get("addAS-ST")+"#addAS-ST"]}], self.PlayListAddMenu)

        self.add_menu([self.lengbox["MSMP Stream"].get("DwTr")+"#DwTr",self.lengbox["MSMP Stream"].get("SvPL")+"#SvPL",self.lengbox["MSMP Stream"].get("SvPLas")+"#SvPLas",self.lengbox["MSMP Stream"].get("OpPL")+"#OpPL",self.lengbox["MSMP Stream"].get("PYtPl")+"#PYtPl"], self.MenuPlaylistMenu)
#https://msmp-audio.maxsspeaker.tk/msmp-audio/audio/Space%20Queen-Nglr2WV8mw0
        


        self.PlayListBox = QtGui.QStandardItemModel()
        self.PlaylistView.setModel(self.PlayListBox)
        self.PlaylistView.setSpacing(0)

        self.PlaylistView.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.PlaylistView.customContextMenuRequested.connect(self.PlayListContextMenu)
            
        self.PlaylistView.setIconSize(QtCore.QSize(25,25))
        
        self.StopButton.clicked.connect(lambda: self.UpdateInfoTreakPL(self.MSMPboxPlayer.stop()))

        self.PlayButton.clicked.connect(lambda: self.UpdateInfoTreakPL(self.MSMPboxPlayer.play()))
        if not(self.NewMainUI):
             self.PauseButton.clicked.connect(lambda: self.MSMPboxPlayer.pause())
        else:
             self.FixScrollBlat()
             self.ChangePlayIcon("play",self.PlayButton,Invert=False)
             self.PauseButton.clicked.connect(lambda: self.CustomPauseButton())

        self.PlayModeTreak.clicked.connect(self.PlayModeTreakChange)

        #self.AddTreakPlaylist.connect(self.contextMenuPlayList)
        
        self.PreviousTreakButton.clicked.connect(lambda: self.UpdateInfoTreakPL(self.MSMPboxPlayer.previousTreak()))   
        self.NextTreakButton.clicked.connect(lambda: self.UpdateInfoTreakPL(self.MSMPboxPlayer.nextTreak()))
        
        self.ProgressBarTreakSlider.valueChanged[int].connect(self.changeProgressBarTreakSlider)
        self.ProgressBarTreakSlider.IsMoveToPointEnabled=True

        if not(self.mobileNewMode):self.VolumeSlider.valueChanged[int].connect(self.changeVolumeSlider)

        self.PlaylistView.selectionModel().selectionChanged.connect(
            self.PlayListSelectionChanged
        )
        self.PlaylistView.doubleClicked.connect(
            lambda: self.PlayListClickPL()
        )
                #self.OpenPLmsmp("../Понравившиеся.plmsmpsbox",AutoPlay=False)
        self.PlayButton.setEnabled(False)
        self.NextTreakButton.setEnabled(False)
        self.PauseButton.setEnabled(False)
        self.StopButton.setEnabled(False)
        self.PreviousTreakButton.setEnabled(False)

        self.TreakName.setText(self.MSMPboxPlayer.PlayNowMusicDataBox["titleTrekPlayNow"])
        self.AuthorName.setText(self.MSMPboxPlayer.PlayNowMusicDataBox["artistTrekPlayNow"])
        self.AlbumName.setText(self.MSMPboxPlayer.PlayNowMusicDataBox["albumTrekPlayNow"])
        if not(self.mobileMode):
             try:self.InfoLabel.setText("")
             except:pass

        self.OpeingVaribleBuffer=False
        #if not(self.mobileMode):self.statusBar.hide()

        if sys.platform.startswith("linux"):
            pass# for Linux using the X Server
            #self.MSMPboxPlayer.NewPlaerVLC.set_xwindow(self.Visualframe.winId())
        elif sys.platform == "win32":  # for Windows
            self.MSMPboxPlayer.NewPlaerVLC.set_hwnd(self.Visualframe.winId())
        #elif sys.platform == "darwin":  # for MacOS
        #    self.MSMPboxPlayer.NewPlaerVLC.set_nsobject(self.Visualframe.winId())

        if not(self.mobileNewMode):self.VolumeSlider.setValue(self.MSMPboxPlayer.NewPlaerVLC.audio_get_volume())
    def CustomPauseButton(self):
         self.MSMPboxPlayer.pause()
         
         if(str(self.MSMPboxPlayer.get_state())=="State.Playing"): 
              self.ChangePlayIcon("play",self.PlayButton,Invert=True)
         else:
              self.ChangePlayIcon("play",self.PlayButton,Invert=False)
              
    def PlayModeTreakChange(self):
         self.PlayModeMSMPNum=self.PlayModeMSMPNum+1
         if(len(self.PlayModeMSMPModes)==self.PlayModeMSMPNum):
              self.PlayModeMSMPNum=0
              #self.PlayModeMSMPModes=["nexttreak","looptreak","randomtreak"]
              #self.PlayModeMSMPNum=0
         self.PlayModeMSMP=self.PlayModeMSMPModes[self.PlayModeMSMPNum]
         if(self.NewMainUI):
              self.ChangePlayIcon(self.PlayModeMSMP,self.PlayModeTreak)
         else:
              icon6 = QtGui.QIcon()
              icon6.addPixmap(QtGui.QPixmap("img/"+self.PlayModeMSMP+".png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
              self.PlayModeTreak.setIcon(icon6)
         
    def setEqualizer(self,EqualizerSettings=None,Custom=False):
         #self.EqualizerSettings=[7.2,7.2,0,0,0,0,0,0,0,7.2,7.2] #[-9.6,-9.6,-9.6,-4,2.4,11.2,16.0,16.0,16.0,16.7,0]
         if not(Custom):
              print("equalizer firk")
              if(self.config['MSMP Stream Equalizer']["EqualizerOnOff"]):
                   self.setEqualizer(self.config['MSMP Stream Equalizer']["EqualizerSettings"],Custom=True)
                   print("equalizer set")
              else:
                  self.MSMPboxPlayer.NewPlaerVLC.set_equalizer(None)
                  print("equalizer disabled")
              return
         SetSettings=0
         i=0
         while not -1==SetSettings:
              SetSettings=self.EqualizerPlaerVLC.set_amp_at_index(EqualizerSettings[i],i)
              i=i+1
         self.MSMPboxPlayer.NewPlaerVLC.set_equalizer(self.EqualizerPlaerVLC)     
         
    def ShowPlSelector(self):
         if(self.PlSelector):
              self.PlSelector=False
              self.PlaylistView.show()
              self.PlaylistsView.hide()
              self.LoadingLabel.hide()
              self.PlaylistCommandBar.show()
              self.LoadingLabel.show()
         else:
              self.PlSelector=True
              self.PlaylistCommandBar.hide()
              self.LoadingLabel.hide()
              self.PlaylistView.hide()
              self.PlaylistsView.show()

    def UpdateInfoBoxLabel(self):
        InfoTextBox=""
        if not(self.MSMPboxPlayer.PlayNowMusicDataBox['like_count']==-1):
             if(self.NewMainUI):
                  InfoTextBox=InfoTextBox+str(self.MSMPboxPlayer.PlayNowMusicDataBox['like_count'])+" :Likes"+"\n"
             else:
                  InfoTextBox=InfoTextBox+"Likes: "+str(self.MSMPboxPlayer.PlayNowMusicDataBox['like_count'])+"\n"
        if not(self.MSMPboxPlayer.PlayNowMusicDataBox["view_count"]==-1):
             if(self.NewMainUI):
                  InfoTextBox=InfoTextBox+str(self.MSMPboxPlayer.PlayNowMusicDataBox["view_count"])+" :Views"
             else:
                  InfoTextBox=InfoTextBox+"Views: "+str(self.MSMPboxPlayer.PlayNowMusicDataBox["view_count"])
        self.InfoLabel.setText(InfoTextBox)

        #self.PlayNowMusicDataBox["like_count"]=r[]
        #self.PlayNowMusicDataBox["view_count"]=r[]
        ##self.PlayNowMusicDataBox["availability"]=r['availability']
        #self.PlayNowMusicDataBox["upload_date"]=r['upload_date']
              
    def ReloadInformation(self,ReloadInfoPlayer=True,reloadView=True):
         
        self.PlayListBox = QtGui.QStandardItemModel()
        self.PlaylistView.setModel(self.PlayListBox)
        self.PlaylistView.setSpacing(0)
        
        for i, ItemP in enumerate(self.MSMPboxPlayer.playlist):
            uploader=ItemP.get("uploader")
            if(uploader==None):
                uploader=ItemP.get("artist")
                if(uploader==None):uploader=" "
                
            try:it = QtGui.QStandardItem(ItemP["name"]+"\n"+uploader)
            except KeyError:it = QtGui.QStandardItem(ItemP["Name"]+"\n"+uploader)
            self.PlayListBox.appendRow(it)

            if("soundcloud"==ItemP["ID"]):
                     urlSoundID=ItemP["IDSoundcloud"]+"SoundCloudAlbumImg.png"
            elif("YouTube"==ItemP["ID"]):
                     urlSoundID=ItemP["url"]+"AlbumImg.png"
            elif("GlobalServerUpload"==ItemP["ID"]):
                 urlSoundID=str(ItemP["IDSound"])+"AlbumImg.png"
            elif("YandexMusic"==ItemP["ID"]):
                     urlSoundID=str(ItemP["YandexMusicID"])+"YandexMusicAlbumImg.png"
            elif("VkMusic"==ItemP["ID"]):
                     urlSoundID=str(ItemP["vkIDaudio"])+"VkMusicAlbumImg.png"
            elif("MSMPNetServer"==ItemP["ID"]):
                 urlSoundID=ItemP["hostUrlName"].replace("https://","").replace("http://","")+ItemP["idSoundName"]+"AlbumImg.png"  
            elif ("MyFiles"==ItemP["ID"]) and(os.path.isfile(ItemP["url"])):
                 pass
            else:
                 continue
                 #urlSoundID=str(ItemP["IDSound"])+"AlbumImg.png" 
            if ("MyFiles"==ItemP["ID"]) and(os.path.isfile(ItemP["url"])):
                 if not(self.LocalImgCache.get(ItemP["url"])==None):
                       ImgAlbum=self.LocalImgCache.get(ItemP["url"])
                       ImgAlbum =ImageQt(ImgAlbum)
                       
                       pixmap=QtGui.QPixmap.fromImage(ImgAlbum)
                       it.setData(QtGui.QIcon(pixmap),QtCore.Qt.ItemDataRole.DecorationRole)
                 else:
                       pixmap=QtGui.QPixmap("img/Missing_Texture.png")
                       it.setData(QtGui.QIcon(pixmap),QtCore.Qt.ItemDataRole.DecorationRole)
            elif (os.path.isfile(self.PathImgsCache+urlSoundID)): 
                 it.setData(QtGui.QIcon(self.PathImgsCache+urlSoundID),QtCore.Qt.ItemDataRole.DecorationRole)
            else:
                 it.setData(QtGui.QIcon("img/AlbumImgMini.png"),QtCore.Qt.ItemDataRole.DecorationRole)
              
        self.PlayButton.setEnabled(True)
        self.NextTreakButton.setEnabled(True)
        self.PauseButton.setEnabled(True)
        self.StopButton.setEnabled(True)
        self.PreviousTreakButton.setEnabled(True)

        try:self.UpdateInfoBoxLabel()
        except:pass

        if(ReloadInfoPlayer):
             self.UpdateInfoTreakPL(None) 
        
    def get_file_tree_model(self, root_path):
        model = QFileSystemModel()
        model.setRootPath(root_path)
        model.setFilter(QtCore.QDir.Filter.NoDotAndDotDot | QtCore.QDir.Filter.AllDirs | QtCore.QDir.Filter.Files)
        model.setNameFilters(['*'])
        model.setNameFilterDisables(False)
        return model

    def RunDownloaderBox(self):
            if not(self.MSMPboxPlayer.PlayLocalFile):
              if (self.DownloaderProcess==None):
                   print("Run Downloader")
                   self.DownloaderProcess = QtCore.QProcess()
                   self.DownloaderProcess.finished.connect(self.DownloaderClosedProcess)
                   downloadParam=json.dumps({'YtUrl':self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"],'filePatch':self.config['MSMP Stream']["downloadMusicFolder"]+self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"]+'YouTubeAudio.m4a'})
                        
                   if(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]=="YouTube"):
                        if(os.path.basename(sys.argv[0]).split(".")[1]=="exe"):
                             self.DownloaderProcess.start(sys.argv[0], ["--downloader",downloadParam.replace('"',"'")])
                        else:
                             self.DownloaderProcess.start("python", [sys.argv[0],"--downloader",downloadParam.replace('"',"'")])
                             
                        self.DownloaderProcess.start(sys.argv[0], ["--downloader",downloadParam.replace('"',"'")])
                        self.MSMPboxPlayer.PlayLocalFile=True
                        
                        print(sys.argv[0], "--downloader",downloadParam.replace('"',"'")) #"{'YtUrl':'jIgD_xSY0YA','filePatch':'jIgD_xSY0YA.m4a'}"  
              else:
                   pass
    
    def DownloaderClosedProcess(self):
         print(self.DownloaderProcess.exitCode())
         if(str(self.DownloaderProcess.exitCode())=="-52"):
              self.DownloaderAppProcess = QtCore.QProcess()
              if(os.path.basename(sys.argv[0]).split(".")[1]=="exe"):
                   self.DownloaderAppProcess.start(sys.argv[0], ["--downloader"])
              else:
                   self.DownloaderAppProcess.start("python", [sys.argv[0],"--downloader"])
              print("running Downloader")
              time.sleep(5)
              self.DownloaderProcess=None
              self.RunDownloaderBox()
         else:
              print("DownloaderClosedProcess")
              self.DownloaderProcess=None
         
         
    def SkinChanger(self,Option):

         if(Option=="obu"):
              msg = QMessageBox(self)
              msg.setIcon(QMessageBox.Icon.Information)
              msg.setText("""
Maxs-Speaker Media-Player Stream
свободный стриминговый медиа плеер с поддержкой: YouTube, SoundCloud, YandexMusic и MSMP-AUDIO Server

автор дс: maxsspeaker
автор мобильной версии: Kelk
github: https://github.com/maxsspeaker/qMSMP-Stream
""")
              msg.setWindowTitle("info")
              button = msg.exec()
         elif(Option=="PLshHd"):
              if(self.PlaylistsViewShowed):
                   self.PlaylistsViewShowed=False
                   self.PlaylistsView.hide()
              else:
                   self.PlaylistsViewShowed=True
                   self.PlaylistsView.show()
         elif(Option=="Cls"):
              self.close()
         elif(Option=="sb"):
              self.DataPath=None
              LoadStyleUI("untitledNewBoxpyqt6.ui",self)
              self.add_functions()
              self.show()
              self.showNormal()
              self.NewMainUI=False
              self.mobileMode=False
              if not(self.MSMPboxPlayer.playlist==None):
                   self.ReloadInformation()
         elif(Option=="OLDskin"):
              self.DataPath=None
              LoadStyleUI("ui/untitled.ui",self)
              self.add_functions()
              self.show()
              self.showNormal()
              self.NewMainUI=False
              if not(self.MSMPboxPlayer.playlist==None):
                   self.ReloadInformation()
         elif(Option=="RuDown"):
              self.RunDownloaderBox()
                   #self.DownloaderProcessFox = QtCore.QProcess()
         elif(Option=="st"):
              self.DataPath=None
              self.setupUi(self)
              #LoadStyleUI("ui/untitled.ui",self)
              self.NewMainUI=False
              self.add_functions()
              self.show()
              self.showNormal()
              self.NewMainUI=self.NewMainUIb
              self.FixScrollBlat()
              self.NewMainUI=True
              self.FoxStatusBar.setText("")
              if not(self.MSMPboxPlayer.playlist==None):
                   self.ReloadInformation()
         elif(Option=="ColorFox"):
              color = QtWidgets.QColorDialog.getColor()
              if color.isValid():
                   self.QAccentColor=color
                   self.AccentColor=self.QAccentColor.getRgb()
                   self.DataPath=None
                   self.setupUi(self,workingDir=os.path.dirname(sys.argv[0]).replace("\\","/")+"/",AccentColor=self.AccentColor,NormalColor=self.NormalColor)
                   self.add_functions()
                   self.FoxStatusBar.setText("")
                   self.show()
                   self.showNormal()
                   self.NewMainUI=True
                   self.mobileMode=False
                   if not(self.MSMPboxPlayer.playlist==None):
                        self.ReloadInformation()
         elif(Option=="AIMPskin"):
              self.DataPath=None
              LoadStyleUI("ui/untitledStyleSpew.ui",self)
              self.add_functions()
              self.show()
              self.showNormal()
              self.NewMainUI=False
              if not(self.MSMPboxPlayer.playlist==None):
                   self.ReloadInformation()
         elif(Option=="sEq"):
              self.config,self.ConfigDir,self.PlaylistsFolder=loadConfig()
              self.setEqualizer()

         elif(Option=="mbMode"):
              self.DataPath=None
              LoadStyleUI("ui/untitledNewBoxMb.ui",self)
              self.mobileNewMode=True
              self.NewMainUI=True
              self.FoxStatusBar.setText("")
              self.add_functions()
              self.show()
              #self.mobileMode=True
              #self.showFullScreen()
              if(self.mobileNewMode):
                   self.PlaylistsView.hide()
              if not(self.MSMPboxPlayer.playlist==None):
                   self.ReloadInformation()
                   
    def PlTrekOptions(self,Option):
         if(Option=="DwTr"):
              self.RunDownloaderBox()
         elif(Option=="PYtPl"):
              self.TrekBoxUi.ContinePlay=True
              self.TrekBoxUi.NoPlayListMode=False
              self.TrekBoxUi.show()
         elif(Option=="OpPL"):
              self.OpenPLmsmp(path=None,AutoPlay=False)
         elif(Option=="SvPL"):
              self.SavePLmsmp(self.MSMPboxPlayer.OpenedplaylistPath)
         elif(Option=="SvPLas"):
              self.SavePLmsmp(path=None)

    def GibridPausePlay(self):
         pass
                   
    def AddTrekOptions(self,Option):
         if(Option=="addAS-YV"):
              self.TrekBoxUi.NoPlayListMode=True
              self.TrekBoxUi.show()
         if(Option=="addAS-Ma"):
              self.MSMPTrekBoxUi.show() 
              
              
    def handle_double_click(self, index): 
        path = self.model.filePath(index)
        if self.model.isDir(index):
            if not self.model.canFetchMore(index):
                self.model.fetchMore(index)
            if self.model.rowCount(index) > 0:
                self.tree.setExpanded(index, True)
        else:
            self.OpenPLmsmp(path)
    def SavePLmsmp(self,path=None):
       if(path==None):
            path , check = QtWidgets.QFileDialog.getSaveFileName(None, "QFileDialog.getOpenFileName()",
                                               "", "PlayList File files (*.plmsmpsbox);;All Files (*)")
       else:
            check=True
            
       if check:
            print("saving "+path)
            plToSave={"playlist":self.MSMPboxPlayer.playlist,"iconPlayList": None, "ContinuePlayData": None,"VerisonCore":2}
            with open(path, 'w') as f:
                 json.dump(plToSave, f, indent=2)
            print("saving ok")
              
    def OpenPLmsmp(self,path=None,AutoPlay=False):
        if(path==None):
              path , check = QtWidgets.QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                               "", "PlayList File files (*.plmsmpsbox);;All Files (*)")
        else:
              check=True

        if check:     
         self.StopParsePL=True
         time.sleep(0.5)
         self.PathToPlMSMPbox=path
         self.StopParsePL=False
         self.OpenPLThread = ProcessRunnable(target=self.OpenPlmsmpThread, args=())
         self.OpenPLThread.start()
         
         time.sleep(0.5)
         if not(len(self.MSMPboxPlayer.playlist)==0):
             self.PlayButton.setEnabled(True)
             self.NextTreakButton.setEnabled(True)
             self.PauseButton.setEnabled(True)
             self.StopButton.setEnabled(True)
             self.PreviousTreakButton.setEnabled(True)
             if(AutoPlay):self.UpdateInfoTreakPL(self.MSMPboxPlayer.play(0))

     
             
    def OpenPlmsmpThread(self):
      path=self.PathToPlMSMPbox   
      try:
        with open(path, 'r') as fr:
                    playlistFile = json.load(fr)
                    self.MSMPboxPlayer.playlist=playlistFile["playlist"]

        self.MSMPboxPlayer.OpenedplaylistPath=path 
        self.LestNum=-1            
        self.PlayListBox = QtGui.QStandardItemModel()
        self.PlaylistView.setModel(self.PlayListBox)
        self.PlaylistView.setSpacing(0)

        self.LocalImgCache={}
        
        
        for i, ItemP in enumerate(self.MSMPboxPlayer.playlist):
            uploader=ItemP.get("uploader")
            if(self.NewMainUI):self.FoxStatusBar.setText("Loading PL: "+str(i)+"/"+str(len(self.MSMPboxPlayer.playlist)))
            if(uploader==None):
                uploader=ItemP.get("artist")
                if(uploader==None):uploader=" "
            try:it = QtGui.QStandardItem(ItemP["name"]+"\n"+uploader)
            except KeyError:it = QtGui.QStandardItem(ItemP["Name"]+"\n"+uploader)
            self.PlayListBox.appendRow(it)
            if not(self.NoAlbumImgs):
             if("soundcloud"==ItemP["ID"]):
                     urlSoundID=ItemP["IDSoundcloud"]+"SoundCloudAlbumImg.png"
             elif("YouTube"==ItemP["ID"]):
                     urlSoundID=ItemP["url"]+"AlbumImg.png"
             elif("GlobalServerUpload"==ItemP["ID"]):
                 urlSoundID=str(ItemP["IDSound"])+"AlbumImg.png"
             elif("YandexMusic"==ItemP["ID"]):
                     urlSoundID=str(ItemP["YandexMusicID"])+"YandexMusicAlbumImg.png"
             elif("VkMusic"==ItemP["ID"]):
                     urlSoundID=str(ItemP["vkIDaudio"])+"VkMusicAlbumImg.png"
             elif ("MyFiles"==ItemP["ID"]) and(os.path.isfile(ItemP["url"])):
                 pass
             elif("MSMPNetServer"==ItemP["ID"]):
                 urlSoundID=ItemP["hostUrlName"].replace("https://","").replace("http://","")+ItemP["idSoundName"]+"AlbumImg.png"  
             else:
                 continue
                 #urlSoundID=str(ItemP["IDSound"])+"AlbumImg.png"
             if ("MyFiles"==ItemP["ID"]) and(os.path.isfile(ItemP["url"])):
                    DataImg=GetImgFile(ItemP["url"])
                    if not(DataImg==None): 
                     ImgAlbum = Image.open(DataImg).convert("RGBA")
                     ImgAlbum=crop_center(ImgAlbum,ImgAlbum.size[1],ImgAlbum.size[1])
                     ImgAlbum.thumbnail((140,140)) #SoundCloudAlbumImg.png #270
                     
                     self.LocalImgCache[ItemP["url"]]=ImgAlbum
                     
                     ImgAlbum =ImageQt(ImgAlbum)
                     pixmap=QtGui.QPixmap.fromImage(ImgAlbum)
                     
                     it.setData(QtGui.QIcon(pixmap),QtCore.Qt.ItemDataRole.DecorationRole)
                    else:
                       pixmap=QtGui.QPixmap("img/Missing_Texture.png")
                       it.setData(QtGui.QIcon(pixmap),QtCore.Qt.ItemDataRole.DecorationRole)
             elif (os.path.isfile(self.PathImgsCache+urlSoundID)): 
                 it.setData(QtGui.QIcon(self.PathImgsCache+urlSoundID),QtCore.Qt.ItemDataRole.DecorationRole)
             else:
                 it.setData(QtGui.QIcon("img/AlbumImgMini.png"),QtCore.Qt.ItemDataRole.DecorationRole)
            if(self.StopParsePL):
                 if(self.NewMainUI):self.FoxStatusBar.setText("")
                 return
        if(self.NewMainUI):self.FoxStatusBar.setText("")     
      except:print(traceback.format_exc())

    def expand_all(self):
        self.tree.expandAll()

    def collapse_all(self):
        self.tree.collapseAll()
            
    def updateBgGui(self):
        while not self.CloseApp:
            #print("fox")
            try:
                      
              MediaBoxStatus=self.MSMPboxPlayer.get_state()
              if not(self.mobileMode):
                   if("State.Opening"==str(MediaBoxStatus)):
                        if not (self.OpeingVaribleBuffer):
                                  self.OpeingVaribleBuffer=True
                                  if(self.NewMainUI):self.FoxStatusBar.setText("Loading Treak")
                   else:
                        if (self.OpeingVaribleBuffer):
                                  if(self.NewMainUI):self.FoxStatusBar.setText("")
                                  self.OpeingVaribleBuffer=False   
              #print(self.PlaylistView.indexAt())
              if not(self.bufferNewPlaerVLCposition==self.MSMPboxPlayer.NewPlaerVLC.get_position()*1000):
                self.bufferNewPlaerVLCposition=self.MSMPboxPlayer.NewPlaerVLC.get_position()*1000
                #print(self.MSMPboxPlayer.NewPlaerVLC.get_position()*100)
                #print(self.MSMPboxPlayer.NewPlaerVLC.get_length()/1000)
                self.ProgressBarTreakSlider.valueChanged[int].disconnect(self.changeProgressBarTreakSlider)
                self.ProgressBarTreakSlider.setValue(int(self.MSMPboxPlayer.NewPlaerVLC.get_position()*1000))
                self.ProgressBarTreakSlider.valueChanged[int].connect(self.changeProgressBarTreakSlider)
                self.TimePlayCounter.setText(hhmmss(self.MSMPboxPlayer.NewPlaerVLC.get_time()/1000)+"/"+hhmmss(self.MSMPboxPlayer.durationTreak))
                time.sleep(1)
              else:
                   time.sleep(0.1)
                   if(str(MediaBoxStatus)=="State.Ended"):
                       if(self.PlayModeMSMP=="nexttreak"):
                            self.UpdateInfoTreakPL(self.MSMPboxPlayer.nextTreak())
                       elif(self.PlayModeMSMP=="looptreak"):
                            self.UpdateInfoTreakPL(self.MSMPboxPlayer.play())
                       elif(self.PlayModeMSMP=="randomtreak"):
                            self.UpdateInfoTreakPL(self.MSMPboxPlayer.play(random.randint(0,len(self.MSMPboxPlayer.playlist)-1)))
            #except AttributeError:
            #    pass
            except:
                print('\n',traceback.format_exc())
        
    def changeProgressBarTreakSlider(self, value):
            #self.MSMPboxPlayer.setpos(int(value))
            self.MSMPboxPlayer.NewPlaerVLC.set_position(int(value)/1000)
            if(str(self.MSMPboxPlayer.get_state())=="State.Playing"):
                 if not (self.RPC==None):
                      self.RPC.updatePlayerNow(self.MSMPboxPlayer.PlayNowMusicDataBox,timebox=self.MSMPboxPlayer.NewPlaerVLC.get_time()/1000)
            else:
                 self.RPC.timebox=self.MSMPboxPlayer.NewPlaerVLC.get_time()/1000
            #print(int(self.MSMPboxPlayer.NewPlaerVLC.get_position()*100))
            #print(value)
    def PlayListClickPL(self):
      try:
        if not(self.isPlayListSelectionChanged):
            selections=self.PlaylistView.selectedIndexes()
            if(len(selections)==1):
                item=self.PlaylistView.model().itemFromIndex(selections[0])
                self.UpdateInfoTreakPL(self.MSMPboxPlayer.play(item.row()))
                
        print(self.isPlayListSelectionChanged)
        self.isPlayListSelectionChanged=False
      except:
          print('\n',traceback.format_exc())
    def PlayListSelectionChanged(self):
      try:
        self.isPlayListSelectionChanged=True
        print("========")
        for index in self.PlaylistView.selectedIndexes():
            item = self.PlaylistView.model().itemFromIndex(index)
            print(item.text())
            print("==")
      except:
                print('\n',traceback.format_exc())

            
    def changeVolumeSlider(self, value):
        self.MSMPboxPlayer.NewPlaerVLC.audio_set_volume(value)

    def ChangePlayIcon(self,IconName,PlayModeTreak,Invert=False):
         styleColorFox=str(self.AccentColor[0])+","+str(self.AccentColor[1])+","+str(self.AccentColor[2])
         if not(Invert):
              PlayModeTreak.setStyleSheet("""
QPushButton{
  background-color: rgb(80,80, 80);
  border: none;
  border-image: url(img/"""+IconName+"""New.png);
}
QPushButton:hover{
  background-color: rgb("""+styleColorFox+""");
  border: none;
  border-image: url(img/"""+IconName+"""New.png);
}

QPushButton:pressed{
  background-color: rgb("""+styleColorFox+""");
  border: none;
  border-image: url(img/"""+IconName+"""NewA.png);

}
""")
         else:
              PlayModeTreak.setStyleSheet("""
QPushButton{
  background-color: rgb("""+styleColorFox+""");
  border: none;
  border-image: url(img/"""+IconName+"""New.png);
}
QPushButton:hover{
  background-color: rgb(100,100, 100);
  border: none;
  border-image: url(img/"""+IconName+"""New.png);
}

QPushButton:pressed{
  background-color: rgb("""+styleColorFox+""");
  border: none;
  border-image: url(img/"""+IconName+"""NewA.png);

}
""")

    def UpdateBg(self,RGBdata):
         self.ContorlPanel.setStyleSheet("QGroupBox{\n"
"   background-color:qlineargradient(spread:pad, x1:0.278, y1:1, x2:0, y2:1, stop:0 rgba(16,16,16, 255), stop:1 rgba("+RGBdata+", 255));\n"
"   color:rgb(0,0,0);\n"
"   border:none;\n"
"   border-bottom: 1px solid;\n"
"}")
    def UpdateInfoTreakPL(self,fun):
         
        self.TreakName.setText(self.MSMPboxPlayer.PlayNowMusicDataBox["titleTrekPlayNow"])
        self.AuthorName.setText(self.MSMPboxPlayer.PlayNowMusicDataBox["artistTrekPlayNow"])
        self.AlbumName.setText(self.MSMPboxPlayer.PlayNowMusicDataBox["albumTrekPlayNow"])
        if not(self.LestNum==-1):
             ColorFix=QtGui.QColor('rgba(0,0,0,0)')
             ColorFix.setAlpha(0)
             self.PlayListBox.itemFromIndex(self.PlayListBox.index(self.LestNum,0)).setBackground(ColorFix)
        self.LestNum=self.MSMPboxPlayer.Num
        
        try:self.PlayListBox.itemFromIndex(self.PlayListBox.index(self.LestNum,0)).setBackground(self.QAccentColor)
        except:
             print('\n',traceback.format_exc())
             self.LestNum=-1
             return
        print("Firk1")
        if (self.NoAlbumImgs):
             self.MSMPboxPlayer.CoverUrlPlayNow=None
             
        if self.MSMPboxPlayer.CoverUrlPlayNow:
            print("Loading Icon")
            try:
                #data = urllib.request.urlopen(self.MSMPboxPlayer.CoverUrlPlayNow).read()
                if("soundcloud"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                     urlSoundID=self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["IDSoundcloud"]+"SoundCloudAlbumImg.png"
                elif("MSMPNetServer"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                     urlSoundID=self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["hostUrlName"].replace("https://","").replace("http://","")+self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["idSoundName"]+"AlbumImg.png"  
                elif("YouTube"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                     urlSoundID=self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"]+"AlbumImg.png"
                elif("YandexMusic"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                     urlSoundID=str(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["YandexMusicID"])+"YandexMusicAlbumImg.png"
                elif("VkMusic"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                     urlSoundID=str(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["vkIDaudio"])+"VkMusicAlbumImg.png"
                elif("GlobalServerUpload"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                     urlSoundID=str(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["IDSound"])+"AlbumImg.png"
                else:
                     pass
                #print("==========================================1")

                #print(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"])
                #print(self.PathImgsCache+urlSoundID)
                #print(os.path.isfile(self.PathImgsCache+urlSoundID))
                if ("MyFiles"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]) and(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"]):
                  if(self.LocalImgCache.get(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"])==None):
                    DataImg=GetImgFile(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"])   
                    if not(DataImg==None): 
                     ImgAlbum = Image.open(DataImg).convert("RGBA")
                     ImgAlbum=crop_center(ImgAlbum,ImgAlbum.size[1],ImgAlbum.size[1])
                     ImgAlbum.thumbnail((140,140)) #SoundCloudAlbumImg.png #270
                     
                     self.LocalImgCache[self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"]]=ImgAlbum
                     
                     RGBbg=ImageStat.Stat(ImgAlbum).mean
                     ImgAlbumQt =ImageQt(ImgAlbum)
                     pixmap=QtGui.QPixmap.fromImage(ImgAlbum)
                     print("self.PlayListBox.itemFromIndex")
                     try:self.PlayListBox.itemFromIndex(self.PlayListBox.index(self.LestNum,0)).setData(QtGui.QIcon(pixmap),QtCore.Qt.ItemDataRole.DecorationRole)
                     except:pass
                     Mising=False
                    else:
                       pixmap=QtGui.QPixmap("img/Missing_Texture.png")
                       Mising=True
                  else:
                       ImgAlbum=self.LocalImgCache.get(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"])
                       RGBbg=ImageStat.Stat(ImgAlbum).mean
                       ImgAlbumQt =ImageQt(ImgAlbum)
                       
                       pixmap=QtGui.QPixmap.fromImage(ImgAlbumQt)
                       try:self.PlayListBox.itemFromIndex(self.PlayListBox.index(self.LestNum,0)).setData(QtGui.QIcon(pixmap),QtCore.Qt.ItemDataRole.DecorationRole)
                       except:pass
                       Mising=False
                  if not(self.RPC==None):
                       if not (Mising):
                                  CustomImgAlbum=self.RPC.UploadNewImg(ImgAlbum,str(self.MSMPboxPlayer.PlayNowMusicDataBox["artistTrekPlayNow"])+str(self.MSMPboxPlayer.PlayNowMusicDataBox["titleTrekPlayNow"]))
                                  if(CustomImgAlbum==None):
                                       CustomImgAlbum=self.MSMPboxPlayer.msmp_streamIcon
                                  print(CustomImgAlbum)
                                  self.RPC.updatePlayerNow(PlayNowMusicDataBox=self.MSMPboxPlayer.PlayNowMusicDataBox,
                                             durationTreak=self.MSMPboxPlayer.durationTreak,
                                             PlLen=len(self.MSMPboxPlayer.playlist),
                                             Num=self.MSMPboxPlayer.Num,
                                             NowPlayIconRPC="MyFiles",
                                             ImgUrl=CustomImgAlbum.replace(" ","%20"),firstPlay=True)
                       else:
                            self.RPC.updatePlayerNow(PlayNowMusicDataBox=self.MSMPboxPlayer.PlayNowMusicDataBox,
                                             durationTreak=self.MSMPboxPlayer.durationTreak,
                                             PlLen=len(self.MSMPboxPlayer.playlist),
                                             Num=self.MSMPboxPlayer.Num,
                                             NowPlayIconRPC="MyFiles",
                                             ImgUrl=self.MSMPboxPlayer.msmp_streamIcon,firstPlay=True)
                       
                elif not(os.path.isfile(self.PathImgsCache+urlSoundID)):
                     print("Loading")
                     print("==========================================")
                     r = requests.get(self.MSMPboxPlayer.CoverUrlPlayNow, stream=True)
                     r.raw.decode_content = True # Content-Encoding
                     ImgAlbum = Image.open(r.raw).convert("RGBA")
                     if(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]=="YouTube"):
                          ImgAlbum=crop_center(ImgAlbum,270,270)
                     else:
                          ImgAlbum=crop_center(ImgAlbum,ImgAlbum.size[1],ImgAlbum.size[1])
                     ImgAlbum.thumbnail((140,140)) #SoundCloudAlbumImg.png #270
                     try:ImgAlbum.save(self.PathImgsCache+urlSoundID)
                     except:print("ошибка сохронения изоброжения трека")
                     RGBbg=ImageStat.Stat(ImgAlbum).mean
                     ImgAlbum =ImageQt(ImgAlbum)
                     pixmap=QtGui.QPixmap.fromImage(ImgAlbum)
                     print("self.PlayListBox.itemFromIndex")
                     try:self.PlayListBox.itemFromIndex(self.PlayListBox.index(self.LestNum,0)).setData(QtGui.QIcon(pixmap),QtCore.Qt.ItemDataRole.DecorationRole)
                     except:pass
                else:
                     ImgAlbum = Image.open(self.PathImgsCache+urlSoundID).convert("RGBA")
                     pixmap=QtGui.QPixmap(self.PathImgsCache+urlSoundID)
                     RGBbg=ImageStat.Stat(ImgAlbum).mean
                     
                
                

                
                
                
                
                print("Update icon")
                print('QPixmap("img/Missing_Texture.png")')
                self.AlbumImg.setPixmap(QtGui.QPixmap("img/Missing_Texture.png"))
                
                #im = Image.open(io.BytesIO(data))
                #im.thumbnail((140,140))
                
                #pixmap.loadFromData(com)
                #self.AlbumImg.setPixmap(pixmap)
                print('QtGui.QPixmap.fromImage(ImgAlbum)')
                
                print('self.AlbumImg.setPixmap(pixmap)')
                self.AlbumImg.setPixmap(pixmap)
                print("self.UpdateBg")
                try:self.UpdateInfoBoxLabel()
                except:pass #if not(self.NewMainUI):
                if(self.UpdateBgAllowed):
                     self.UpdateBg(str(int(RGBbg[0]))+", "+str(int(RGBbg[1]))+", "+str(int(RGBbg[2])))
                if(self.NewMainUI):
                     self.ChangePlayIcon("play",self.PlayButton,Invert=True)
                
                #print(self.MSMPboxPlayer.CoverUrlPlayNow)
                print("self.notifiBox.ShowNotifi")
                if not("MyFiles"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                     self.notifiBox.ShowNotifi(self.MSMPboxPlayer.PlayNowMusicDataBox["titleTrekPlayNow"],
                        self.MSMPboxPlayer.PlayNowMusicDataBox["artistTrekPlayNow"],self.PathImgsCache+urlSoundID)
                else:
                     self.notifiBox.ShowNotifi(self.MSMPboxPlayer.PlayNowMusicDataBox["titleTrekPlayNow"],
                        self.MSMPboxPlayer.PlayNowMusicDataBox["artistTrekPlayNow"])
            except:
                print('\n',traceback.format_exc())
                self.AlbumImg.setPixmap(QtGui.QPixmap("img/Missing_Texture.png"))
            print("Update icon ok")
        else:
             try:self.UpdateInfoBoxLabel()
             except:pass #if not(self.NewMainUI):
             if(self.NewMainUI):
                     self.ChangePlayIcon("play",self.PlayButton,Invert=True)
            #self.AlbumImg.setPixmap(QtGui.QPixmap("img/X9at37tsrY8AlbumImg.png"))
            #self.notifiBox.ShowNotifi(self.MSMPboxPlayer.PlayNowMusicDataBox["titleTrekPlayNow"],
            #            self.MSMPboxPlayer.PlayNowMusicDataBox["artistTrekPlayNow"])
        if not(self.DataPath==None):
             if("soundcloud"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                     self.DataPath.setText(r"SoundCloud/"+str(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["IDSoundcloud"]))
             elif("YouTube"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                     self.DataPath.setText(r"YouTube/"+str(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"]))
             elif("YandexMusic"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                   self.DataPath.setText(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"]) #self.MSMPboxPlayer.self.AlbumIDYandexMusic
             elif("VkMusic"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                   self.DataPath.setText("vkAudio"+"/"+str(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["vkIDaudio"]))
             elif("GlobalServerUpload"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                  self.DataPath.setText("MSMPnet"+"/"+str(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["IDSound"]))
             elif("MSMPNetServer"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                  self.DataPath.setText(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["hostUrlName"].replace("https://","").replace("http://","")+"/audio/"+self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["idSoundName"]) 
             elif("MyFiles"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                   self.DataPath.setText(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"])

             
        
        #self.ProgressBarTreakSlider.setMaximum(self.MSMPboxPlayer.durationTreak)

    def keyPressEvent(self, event):
        try:
         key = event.key()
         #print(key)
         if key == QtCore.Qt.Key_MediaPrevious:
              self.UpdateInfoTreakPL(self.MSMPboxPlayer.previousTreak())
         elif str(key) == "16777344": # Qt.Key_MediaPause ? Qt.Key_MediaPlay  
              self.UpdateInfoTreakPL(self.MSMPboxPlayer.pause())
         elif key == QtCore.Qt.Key_MediaNext:
              self.UpdateInfoTreakPL(self.MSMPboxPlayer.nextTreak())
        except:print('\n',traceback.format_exc())

    def closeEvent(self, event):
       try:
        if not(self.ContinePlay):
             reply = QtWidgets.QMessageBox.question(self, "Exit?", "Are you sure to quit?")
        else:
          reply=None
        
        if (reply == QtWidgets.QMessageBox.StandardButton.Yes) or (self.ContinePlay):
            self.CloseApp=True
            if not(self.RPC.RPC==None):self.RPC.RPC.close()
            self.MSMPboxPlayer.stop()
            self.RunAPPEventHandler.ServerStarted=False
            self.RunAPPEventHandler.RunCommandBox()
            event.accept()
            #self.close()
            
        else:
            event.ignore()
       except:
                print('\n',traceback.format_exc())
                event.ignore()

    def add_menu(self, data, menu_obj):
        if isinstance(data, dict):
            for k, v in data.items():
                sub_menu = QtWidgets.QMenu(k.split("#")[0], menu_obj)
                menu_obj.addMenu(sub_menu)
                self.add_menu(v, sub_menu)
        elif isinstance(data, list):
            for element in data:
                self.add_menu(element, menu_obj)
        else:
            
            action = menu_obj.addAction(data.split("#")[0])
            action.setIconVisibleInMenu(False)
            action.data=data.split("#")[1]


class ProgressDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        progress = index.data(QtCore.Qt.ItemDataRole.UserRole + 1000)
        opt = QtWidgets.QStyleOptionProgressBar()
        opt.rect = option.rect
        opt.minimum = 0
        opt.maximum = 100
        opt.progress = progress
        opt.text = "{}%".format(progress)
        opt.textVisible = True
        style = ex.style()
        #print(style)
        if style:
            style.drawControl(QtWidgets.QStyle.ControlElement.CE_ProgressBar, opt, painter)


class MyYTLoggerNoOut:
    def __init__(self):
         self.firk=True
         pass

        
    def debug(self, msg):
         pass

    def info(self, msg):  
        pass

    def warning(self, msg):
         print(msg)

    def error(self, msg):
         print(msg)



class MainWindowDownloader(QtWidgets.QMainWindow, mainUIDownloader.Ui_MainWindow): #

    def __init__(self,RunAPPEventHandler,AppHidden):
        data = []
        super().__init__()
        self.RunAPPEventHandler=RunAPPEventHandler
        self.RunAPPEventHandler.MainWindow = self
        self.setupUi(self)
        
        self.trayIcon = QtWidgets.QSystemTrayIcon(self)
        icon = QtGui.QIcon("resources/icon.png")
        self.trayIcon.setIcon(icon)
        self.trayIcon.setVisible(True)

        self.firstClose=True

        
        self.trayMenu = QtWidgets.QMenu()
        
        if(sys.platform=="linux"):
             action = QtWidgets.QAction("Open Downloader", self)
             action.triggered.connect(self.OpenDownloader)
             self.trayMenu.addAction(action)
        
        action = QtWidgets.QAction("ShowMsg", self)
        action.triggered.connect(self.ShowMsg)
        self.trayMenu.addAction(action)
        
        quitAction = QtWidgets.QAction("Quit", self)
        quitAction.triggered.connect(self.CloseAction)
        
        self.trayMenu.addAction(quitAction)
        self.trayIcon.setContextMenu(self.trayMenu)#
        self.trayIcon.activated.connect(self.handleTrayIconActivated)

        self.trayIcon.setToolTip("MSMP Downloader")


        #self.pushButton.clicked.connect(self.testDownload)

        
        
        #self.trayIcon.activated.connect(self.eventClickTray)
        #self.trayIcon.setContextMenu(self.TrayMenu)


        #app.setQuitOnLastWindowClosed(False)
        
        self.CloseApp=False

        self.pEvent = ProcessRunnable(target=self.RunAPPEventHandler.RunEventServer, args=())
        self.pEvent.start()
        #
        self.delegate = ProgressDelegate(self.TreakDownloadList)
        self.TreakDownloadList.horizontalHeader().setStretchLastSection(True)
        self.TreakDownloadList.setItemDelegateForColumn(5, self.delegate)
        self.model = QtGui.QStandardItemModel(0, 4)
        self.model.setHorizontalHeaderLabels(["#", "Name","Type","Size","Speed", "Progress"])
        for r, (_id, _name,_type,_size,_speed, _progress) in enumerate(data):
             it_id = QtGui.QStandardItem(_id)
             it_name = QtGui.QStandardItem(_name)
             it_type = QtGui.QStandardItem(_type)
             it_size = QtGui.QStandardItem(_size)
             it_speed = QtGui.QStandardItem(_speed)
             it_progress = QtGui.QStandardItem()
             it_progress.setData( _progress,QtCore.Qt.ItemDataRole.UserRole+1000)
             
             self.model.appendRow([it_id, it_name,it_type,it_size,it_speed, it_progress])
        self.TreakDownloadList.setModel(self.model)
        self.TreakDownloadList.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.p = ProcessRunnable(target=self.updateBgGui, args=())
        self.p.start()
        if not(AppHidden):
             self.show()
        else:
             self.firstClose=False
        self.setStyleSheet('''
QProgressBar {
    border: 2px solid rgb(16, 16, 16);
}

QProgressBar::chunk {
    background-color: rgb(242, 128, 133); 
    width: 20px;
}

''')

        self.DownloadIndexList={}

        #showMessage(title, msg[, icon=QSystemTrayIcon.Information[, msecs=10000]])¶
    def OpenDownloader(self):
         self.show()
         
    def testDownload(self):
         self.DownloadYtFox("4rTMvyRJgLQ",r"A:\YandexDisk\python-projects\MSMPstream\MSMPstreamGit\files\Geming.m4a")
    def ShowMsg(self):
         self.trayIcon.showMessage("MSMP Downloader", "фыр!",icon=QtWidgets.QSystemTrayIcon.MessageIcon.Information)

    def my_hookDownload(self,d):
       try:
        if d['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(d['filename']))
            print("Done downloading {}".format(file_tuple[1]))
        if d['status'] == 'downloading':
            p = d['_percent_str'] #_total_bytes_str #_speed_str #_total_bytes_str
            p = p.replace('%','')
            #self.progress.setValue(float(p))
            #print(int(d["_speed_str"]))
            self.model.item(self.DownloadIndexList.get(d['info_dict']["id"])[0]-1, 3).setText(str(d["_total_bytes_str"]))
            self.model.item(self.DownloadIndexList.get(d['info_dict']["id"])[0]-1, 4).setText(str(d["_speed_str"].replace("\x1b[0;32m","").replace("\x1b[0m","")))
            self.model.item(self.DownloadIndexList.get(d['info_dict']["id"])[0]-1, 5).setData(int(float(p.replace("\x1b[0;94m","").replace("\x1b[0m",""))),QtCore.Qt.ItemDataRole.UserRole+1000)
            if(self.CloseApp):
                 sys.exit()
            #print("firk"+p)
            #print("firk"+p)
            #print("firk"+p)
            #print(d['filename'], d['_percent_str'], d['_eta_str'])
       except:
            print(traceback.format_exc())
            if(self.CloseApp):
                 sys.exit()
            
    def DownloadYtFox(self,url,filename):
         ydl_opts = {
              'forceurl':True,
              'ignoreerrors': True,
              'progress_hooks': [self.my_hookDownload],
              'logger':MyYTLoggerNoOut(),
              'ignore-config':True,
              'extract_flat':True,
              #'extractaudio': True,
              'format':"bestaudio[ext=m4a]/best[ext=m4a]",
              'outtmpl':str(filename)
              }
         #self.DownloadIndexList=
         with youtube_dl.YoutubeDL(ydl_opts) as ydl: #
              r = ydl.extract_info(url, download=False)
              
              it_id = QtGui.QStandardItem(str(len(self.DownloadIndexList)+1))
              it_name = QtGui.QStandardItem(str(r['title'])+" - "+str(r['uploader'].replace(" - Topic","")))
              it_type = QtGui.QStandardItem("YouTube")
              it_size = QtGui.QStandardItem("0")
              it_speed = QtGui.QStandardItem("0")
              it_progress = QtGui.QStandardItem()
              it_progress.setData(0,QtCore.Qt.ItemDataRole.UserRole+1000)

              self.model.appendRow([it_id, it_name,it_type,it_size,it_speed, it_progress])
              self.DownloadIndexList[url]=[len(self.DownloadIndexList)+1,False]
              
              self.DownloadP = ProcessRunnable(target=ydl.download, args=([url]))
              self.DownloadP.start()
              
         
              
    def updateBgGui(self):
        while not self.CloseApp:
             self.TreakDownloadList.update()
             #self.model.item(1, 5).setData(0,QtCore.Qt.ItemDataRole.UserRole+1000)#.text()
             time.sleep(0.1)
             
    def handleTrayIconActivated(self,reason):
         if(str(reason)=="ActivationReason.DoubleClick"):
              self.show()
          
    def CloseAction(self):
         if (True):
             reply = QtWidgets.QMessageBox.question(self, "Exit?", "Загрузка не завершина, выйти?")
         else:
              reply=None

         if (reply == QtWidgets.QMessageBox.StandardButton.Yes) or (False):
              print("close1")
              self.CloseApp=True
              self.show()
              print("close2")
              self.RunAPPEventHandler.ServerStarted=False
              self.RunAPPEventHandler.RunCommandBox()
              print("close3")
              time.sleep(0.5)
              self.close()
              print("close5")
         
    def closeEvent(self, event):
         print(self.CloseApp)
         if(self.CloseApp):
              event.accept()
              sys.exit()
         else:
              if(self.firstClose):
                   self.trayIcon.showMessage('MSMP Downloader', 'Программа свернута в системный лоток.')
                   self.firstClose=False
              self.hide()
              event.ignore()
         #self.CloseApp=True
         #event.accept() #event.ignore()

                
def main():
    from MSMPstream.lib.EventHandler import EventHandler as RunAPPEventHandler

    global RunAPPEventHandler
    global IsdownloaderNode
    global app
    global ex
    
    RunAPPEventHandler=RunAPPEventHandler(RunCommands=sys.argv)
    IsdownloaderNode=RunAPPEventHandler.downloaderNode

    if not(RunAPPEventHandler.FirstApp):
          sys.exit()
          
    app = QtWidgets.QApplication(sys.argv)
    
    sys.excepthook = excepthook
    if (IsdownloaderNode):
         ex = MainWindowDownloader(RunAPPEventHandler,AppHidden=False)
    else:
         ex = MainWindow(RunAPPEventHandler)

    sys.exit(app.exec())
    
def mainDownloader():
    from MSMPstream.lib.EventHandler import EventHandler as RunAPPEventHandler
    
    global RunAPPEventHandler
    global IsdownloaderNode
    global app
    global ex
    
    RunAPPEventHandler=RunAPPEventHandler(RunCommands=["","-d"],downloaderNodeF=True)
    RunAPPEventHandler.downloaderNode=True
    RunAPPEventHandler.PORT = 59716
    IsdownloaderNode=RunAPPEventHandler.downloaderNode

    if not(RunAPPEventHandler.FirstApp):
          sys.exit()
          
    app = QtWidgets.QApplication(sys.argv)
    
    sys.excepthook = excepthook
    
    ex = MainWindowDownloader(RunAPPEventHandler,AppHidden=True)
    
    sys.exit(app.exec())        

if __name__ == '__main__':
     #main()
    main()
