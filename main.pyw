import sys, time, os, traceback,random
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox 
from PyQt5.QtGui import QIcon,QFont 
from os.path import exists
from PyQt5.uic import loadUi as LoadStyleUI
from PIL import Image,ImageStat
from PIL.ImageQt import ImageQt
import io
import logging
from logging.handlers import QueueHandler
import pypresence
from datetime import date
import yaml

logging.basicConfig(filename="all.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

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
import NewMainUI as mainUI


import TrekBox as TrekBoxUi
import MSMPTrekBox as MSMPTrekBoxUi

from yandex_music import Client as YandexMusicClient

import re
import stagger
import requests
import urllib
import json
import pylast
import yt_dlp as youtube_dl
from eyed3 import id3
from eyed3 import load
#from threading import Thread
import vlc
from appdirs import user_config_dir
if(sys.platform=="linux"):
     try:
          from notifypy import Notify
     except:
          pass





class Slider(QtWidgets.QSlider):
    def mousePressEvent(self, event):
        super(Slider, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)

    def pixelPosToRangeValue(self, pos):
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QtWidgets.QStyle.CC_Slider, opt, QtWidgets.QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QtWidgets.QStyle.CC_Slider, opt, QtWidgets.QStyle.SC_SliderHandle, self)

        if self.orientation() == QtCore.Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1;
        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == QtCore.Qt.Horizontal else pr.y()
        return QtWidgets.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
                                               sliderMax - sliderMin, opt.upsideDown)

TrekBoxUi.QtWidgets.QSlider=Slider




def loadLocal(NameLocal):
     with open(NameLocal,"r") as f:
               localbox = yaml.safe_load(f)
     return localbox

def loadConfig():
     configFileName = "config.yml"
     MyPlaylists = "MyPlaylists"

     configDir = user_config_dir(appname="MSMP-Stream",appauthor="Maxsspeaker",version="5.0",roaming=True)
     #print(configDir)

     configFile = os.path.join(configDir,configFileName)
     MyPlaylistsPath = os.path.join(configDir,MyPlaylists)
     #print(configFile)
     
     if(os.path.isfile(configFile)):
          with open(configFile,"r") as f:
               config = yaml.safe_load(f)
          return config,configDir,MyPlaylistsPath
     else:
          cacheFolder = "cache"
          download_MusicFolder = "download_Music"
          cacheFolderPath = os.path.join(configDir,cacheFolder)
          download_MusicFolderPath = os.path.join(configDir,download_MusicFolder)
          config={
               'MSMP Stream': 
                    {'Discord_rpc':True,
                     'audioVisual': 'visual',
                     'cache': True,
                     'cacheimgpachfolder': cacheFolderPath+"/",
                     'downloadMusicFolder': download_MusicFolderPath+"/",
                     'localizationBox': 'lengboxs/ru.loclb',
                     'NowPlayningPlayBoxActive': False,
                     'VideoMode': False,
                     "last-fmAllowed":False,
                     'latest_playlist':""
                     },
               'MSMP Stream Equalizer':
                    {'EqualizerOnOff': False,
                     'EqualizerSettings': [7.5, 7.5, 3.9, 0.1, 0, 0, 0, 0, 1.6, 1.6, 7.0]
                     }
               }
          os.makedirs(os.path.dirname(configFile), exist_ok=True)
          os.makedirs(MyPlaylistsPath, exist_ok=True)
          os.makedirs(download_MusicFolderPath, exist_ok=True)
          os.makedirs(cacheFolderPath, exist_ok=True)
          
          print("firk")
          with open(configFile,"w") as f:
               yaml.dump(config,f)
          return config,configDir,MyPlaylistsPath


class notifiBox():
     def __init__(self,Disabled=False):
        if not(Disabled):
          if(sys.platform=="linux"):
               self.notification = Notify(
                    default_application_name="MSMP Stream",
                    default_notification_icon="icon.png",
                    )
               self.Notifiok=True
          else:
               print("Приложение не поддерживает уведомления на этой системе...")
               self.Notifiok=False
        else:
             self.Notifiok=False
     def ShowNotifi(self,summary,message,icon=""):
          if(self.Notifiok):
               self.notification.title = summary
               self.notification.message = message
               if not(icon==""):
                    self.notification.icon = icon
               self.notification.application_name='MSMP Stream'
               self.notification.send()
               
          

class MyYTLogger:
    def __init__(self,FullInfo,logger,QPlainTextEdit=None):
        self.FullInfo=FullInfo
        self.logger=logger
        self.QPlainTextEdit=QPlainTextEdit
        print(QPlainTextEdit)
        
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

    def info(self, msg):  
        if(self.FullInfo):self.logger.info(msg)
        if not(self.QPlainTextEdit==None):
             self.QPlainTextEdit.appendPlainText(msg)
             self.QPlainTextEdit.repaint()
        pass

    def warning(self, msg):
        self.logger.warning(msg)
        if not(self.QPlainTextEdit==None):
             self.QPlainTextEdit.appendPlainText(msg)
             self.QPlainTextEdit.repaint()

    def error(self, msg):
        self.logger.error(msg)
        if not(self.QPlainTextEdit==None):
             self.QPlainTextEdit.appendPlainText(msg)
             self.QPlainTextEdit.repaint()


def GetImgFile(PachFile):
    try:
         mp3 = stagger.read_tag(PachFile)
         by_data = mp3[stagger.id3.APIC][0].data
         im = io.BytesIO(by_data)
         return im
    except:
          print(traceback.format_exc())
          return None



class MSMP_RPC():
     def __init__(self,RPC,msmp_streamIconYouTube=None,
                  msmp_streamIconMain=None,
                  msmp_streamIconSoundCloud=None,
                  msmp_streamIcon="qmsmpstream",
                  version="None",LastFm=False,
                  logger=None,DirConfig=None,lengbox=None,ImgApiHostTOKEN=None,ImgApiHost=None):
          
          self.RPC=RPC
          if (lengbox==None):
               lengbox={"MSMP Stream":{"RPCmsmpOf":"of"}}
          self.lengbox=lengbox
          if not(RPC==None):
               try:
                    self.RPC=pypresence.Presence("811577404279619634")
                    self.RPC.connect()
               except pypresence.exceptions.DiscordNotFound:
                  self.RPC=None

          self.ImgApiHostTOKEN=ImgApiHostTOKEN
          self.ImgApiHost=ImgApiHost
          
          self.msmp_streamIcon=msmp_streamIcon
          if(msmp_streamIconMain==None):
              self.msmp_streamIconMain=self.msmp_streamIcon
          else:self.msmp_streamIconMain=msmp_streamIconMain
          
          if(msmp_streamIconSoundCloud==None):
              self.msmp_streamIconSoundCloud=self.msmp_streamIcon
          else:self.msmp_streamIconSoundCloud=msmp_streamIconSoundCloud
          
          if(msmp_streamIconYouTube==None):
              self.msmp_streamIconYouTube=self.msmp_streamIcon
          else:self.msmp_streamIconYouTube=msmp_streamIconYouTube

          self.lenPlayListStatus=""
          
          self.version=version

          self.DirConfig=DirConfig
          self.timebox=0

          if(LastFm):
               self.runLastFMapi()
          else:
               self.LastFM=None
     def runLastFMapi(self):
          APIlastFm_KEY = "4e0f10f934869a276690fcce533e4aa4"  # this is a sample key
          APIlastFm_SECRET = "10f3da1934b00eb62a9424f79a599350"

          if(self.DirConfig==None):
               self.DirConfig=os.path.join(os.path.expanduser("~"))
          
          SESSION_KEY_FILE = os.path.join(self.DirConfig, ".session_key")
          self.LastFM = pylast.LastFMNetwork(APIlastFm_KEY, APIlastFm_SECRET)
          if not os.path.exists(SESSION_KEY_FILE):
               skg = pylast.SessionKeyGenerator(self.LastFM )
               url = skg.get_web_auth_url()

               print(f"Please authorize this script to access your account: {url}\n")
               import time
               import webbrowser

               webbrowser.open(url)
               while True:
                    try:
                         session_key = skg.get_web_auth_session_key(url)
                         with open(SESSION_KEY_FILE, "w") as f:
                              f.write(session_key)
                              break
                    except pylast.WSError:
                         print(f"Please authorize this script to access your account: {url}\n")
                         time.sleep(10)
          else:
               session_key = open(SESSION_KEY_FILE).read()
          self.LastFM.session_key = session_key

          #self.LastFMUser=self.LastFM.get_authenticated_user()
          #print(self.LastFMUser)
          

          
     def updatePlayerPause(self,Audiolength,AudioTime,PlayNowMusicDataBox,PlayerState,ImgUrl=""):
      try:
        if not(ImgUrl==""):
               msmp_streamIcon=ImgUrl
               self.IconImgUrl=ImgUrl
        elif not(self.IconImgUrl==None):
               msmp_streamIcon=self.IconImgUrl
        else:
               msmp_streamIcon=self.msmp_streamIcon
        print(PlayerState)       
        if not(PlayerState=="State.Playing"):
          
           if not(self.RPC==None):
             if not(PlayNowMusicDataBox["albumTrekPlayNow"]==""):
                self.RPC.update(
              **{
                  'details': PlayNowMusicDataBox["titleTrekPlayNow"],
                  'state': PlayNowMusicDataBox["artistTrekPlayNow"]+self.lenPlayListStatus,
                  'large_text':PlayNowMusicDataBox["albumTrekPlayNow"],
                  'large_image':msmp_streamIcon,
                  'small_image':"pause",
                  #'large_text':self.PlayNowMusicDataBox["albumTrekPlayNow"],
                  'small_text':self.version
                  }
              )
             else:
                  self.RPC.update(
              **{
                  'details': PlayNowMusicDataBox["titleTrekPlayNow"],
                  'state': PlayNowMusicDataBox["artistTrekPlayNow"]+self.lenPlayListStatus,
                  'large_image':msmp_streamIcon,
                  'small_image':"pause",
                  #'large_text':self.PlayNowMusicDataBox["albumTrekPlayNow"],
                  'small_text':self.version
                  }
              )
##           updatePlayerNow(self,
##                           PlayNowMusicDataBox,
##                           Audiolength,
##                           AudioTime):
        else:
          if not(int(Audiolength)==0):
           self.updatePlayerNow(PlayNowMusicDataBox=PlayNowMusicDataBox,
                           durationTreak=self.durationTreak)     
           
          else:
            if not(self.RPC==None):
               if not(PlayNowMusicDataBox["albumTrekPlayNow"]==""):
                 self.RPC.update(
              **{
                  'details': PlayNowMusicDataBox["titleTrekPlayNow"],
                  'state': PlayNowMusicDataBox["artistTrekPlayNow"],
                  'large_text':PlayNowMusicDataBox["albumTrekPlayNow"],
                  'large_image':msmp_streamIcon,
                  'small_image':"play",
                  'small_text':self.version,
                }
              )
               else:
                 self.RPC.update(
              **{
                  'details': PlayNowMusicDataBox["titleTrekPlayNow"],
                  'state': PlayNowMusicDataBox["artistTrekPlayNow"],
                  'large_image':msmp_streamIcon,
                  'small_image':"play",
                  'small_text':self.version,
                }  )
      except:printError(traceback.format_exc())
      
     def updatePlayerNow(self,PlayNowMusicDataBox,durationTreak=None,PlLen=None,Num=None,NowPlayIconRPC=None,ImgUrl="",timebox=None,firstPlay=False):

          if not(durationTreak==None):
               self.durationTreak=durationTreak
          if(firstPlay):
               self.timebox=0
          elif not(timebox==None):
               self.timebox=timebox
          
          if not(NowPlayIconRPC==None): #,Audiolength,AudioTime
               self.NowPlayIconRPC=NowPlayIconRPC
          if not(PlLen==None):
               self.lenPlayListStatus=" ("+str(Num+1)+" "+self.lengbox["MSMP Stream"]["RPCmsmpOf"]+" "+str(PlLen)+")"
               
          if not(ImgUrl==""):
               msmp_streamIcon=ImgUrl
               self.IconImgUrl=ImgUrl
          elif not(self.IconImgUrl==None):
               msmp_streamIcon=self.IconImgUrl
          else:
               msmp_streamIcon=self.msmp_streamIcon
               
          if not(self.RPC==None):
            if not(PlayNowMusicDataBox["albumTrekPlayNow"]==""):
               self.RPC.update(
                   **{
                      'details': PlayNowMusicDataBox["titleTrekPlayNow"],
                      'state': PlayNowMusicDataBox["artistTrekPlayNow"]+self.lenPlayListStatus,
                      'large_text':PlayNowMusicDataBox["albumTrekPlayNow"],
                      'large_image':msmp_streamIcon,
                      'small_image':"play",
                      #'large_text':self.PlayNowMusicDataBox["albumTrekPlayNow"],
                      'small_text':self.version,
                      'end': time.time()+(self.durationTreak-self.timebox)#((AudioTime-Audiolength)/1000)-((AudioTime-Audiolength)/1000)-((AudioTime-Audiolength)/1000)
                    }
                   )
            else:
                self.RPC.update(
                   **{
                      'details': PlayNowMusicDataBox["titleTrekPlayNow"],
                      'state': PlayNowMusicDataBox["artistTrekPlayNow"]+self.lenPlayListStatus,
                      'large_image':msmp_streamIcon,
                      'small_image':"play",
                      #'large_text':self.PlayNowMusicDataBox["albumTrekPlayNow"],
                      'small_text':self.version,
                      'end': time.time()+(self.durationTreak-self.timebox)#((AudioTime-Audiolength)/1000)-((AudioTime-Audiolength)/1000)-((AudioTime-Audiolength)/1000)
                    }
                   ) 
                 
          if not(self.LastFM==None) and (firstPlay):
               self.scrobbleThread = ProcessRunnable(target=self.scrobbleLastFM, args=(PlayNowMusicDataBox,))
               self.scrobbleThread.start()
                    
     def scrobbleLastFM(self,PlayNowMusicDataBox):
          try:
               self.LastFM.scrobble(artist=PlayNowMusicDataBox["artistTrekPlayNow"],
                                         title=PlayNowMusicDataBox["titleTrekPlayNow"],
                                         timestamp=time.time(),
                                         album=PlayNowMusicDataBox["albumTrekPlayNow"],
                                         duration=self.durationTreak)
          except:
               printError(traceback.format_exc())
          
     def updatePlayerStop(self,LoadingMusicMeta):
          if(LoadingMusicMeta): #self.PlayNowMusicDataBox["LoadingMusicMeta"]
                 if not(self.RPC==None):self.RPC.update(
                     **{
                         'large_image':"missing_texture",
                    })
          else:
                 if not(self.RPC==None):self.RPC.update(
                     **{
                         'large_image':self.msmp_streamIcon,
                    })
     def UploadNewImg(self,PillowImg,ImgNameTreak):
        if not(self.ImgApiHost==None):
          byte_io = io.BytesIO()
          PillowImg.save(byte_io, 'png')
          byte_io.seek(0)
          cookies = {"TOKEN":self.ImgApiHostTOKEN}

          r = requests.post(self.ImgApiHost+ImgNameTreak, cookies=cookies, files={'upload_file': ('1.png',byte_io)})

          return self.ImgApiHost+ImgNameTreak
        return None



class GibridPlayer():
    def __init__(self,InstanceSettings):
          self.Instance = vlc.Instance(InstanceSettings)
          self.NewPlaerVLC = self.Instance.media_player_new()
          
    def play(self,url):
        print("Play Treak")
        self.media = self.Instance.media_new(url)
        self.NewPlaerVLC.set_media(self.media)
        self.NewPlaerVLC.play()
        print("Play ok")
    def pause(self):
        self.NewPlaerVLC.pause()
    def get_state(self):
        return self.NewPlaerVLC.get_state()
    def setpos(self,PosTime):
        try:self.NewPlaerVLC.set_position(int((100/int(self.NewPlaerVLC.get_length()/1000)*int(PosTime)))*0.01)
        except ZeroDivisionError:
               return "Loading"
    def stop(self):
        #if str(NewPlaerVLC.get_state())=="State.Playing":
         self.NewPlaerVLC.stop()
         if not(self.discord_rpc==None):
             #OldMusicDataBox["Play"]=0
             self.Error=0
        
        
version=0.1

class MSMPboxPlayer(GibridPlayer): 
     def __init__(self,ServerPlaer,
                  InstanceSettings,
                  downloadMusicFolder="",
                  localizationBox=None,
                  ImgAssets=None,
                  MSMP_RPC=None,
                  HostNamePybms="https://pybms.tk/",
                  versionCs=None,
                  FullInfo=False,
                  VideoMode=False,AutoSplitAuthorName=False,
                  logger=None,PlayInThread=False,TOKENYandexMusicClient=""):
          global version
          print("Starting Core MSMP")
          self.logger=logger
          self.ydl_opts = {
                         'forceurl':True,
                         'ignoreerrors': True,
                         'logger':MyYTLogger(FullInfo,logger=self.logger),
                         'ignore-config':True,
                         'extract_flat':True
                         }
          self.PlayNowMusicDataBox={"LoadingMusicMeta":False,
                                    "titleTrekPlayNow":"",
                                    "artistTrekPlayNow":"",
                                    "albumTrekPlayNow":"",
                                    "albumImgTrekPlayNowID":"",
                                    "TrekPlayNowID":""
                                    }
          super().__init__(InstanceSettings)
          self.Error=False
          self.PlayInThread=PlayInThread
          if(versionCs==None):self.version=version
          self.Num=0
          self.FullInfo=FullInfo
          self.iconPlayList=None
          self.castViseonYouTube=1
          self.downloadMusicFolder=downloadMusicFolder
          self.cookiesSoundCloud=""
          self.cookiesYouTube=""
          self.lenPlayListStatus=""
          self.msmp_streamIconDf="qmsmpstream"
          self.msmp_streamIcon=self.msmp_streamIconDf
          self.discord_rpc=MSMP_RPC

          if not(TOKENYandexMusicClient==None):
               self.YandexMusicClient = YandexMusicClient(TOKENYandexMusicClient).init()
          else:
               self.YandexMusicClient=None

          self.AutoSplitAuthorName=AutoSplitAuthorName
               
          self.ImgAssets=ImgAssets
          self.castViseonSoundCloud=-1
          self.Useyt_dlp=True
          self.VideoMode=VideoMode
          self.DownloadingSounds={}
          self.tagid3 = id3.Tag()
          self.ErrorLoadSound=[]
          self.ServerPlaer=ServerPlaer
          self.HostNamePybms=HostNamePybms
          self.VersionContinuePlay="v0.1.2-beta"
          self.PlayLocalFile=False
          
          if not(ServerPlaer):
              self.localizationBox=localizationBox
     def LoadImg(self,IDasset,IDtype,rID,CoverUrlPlayNow=None):
         if not(self.ImgAssets==None):
             if(IDtype=="YouTube"):
                 try: 
                   # self.CoverUrlPlayNow='https://i.ytimg.com/vi/'+rID+'/maxresdefault.jpg'
                    self.CoverUrlPlayNow='https://img.youtube.com/vi/'+rID+'/hqdefault.jpg'
                    self.ImgAssets[str(rID)+"AlbumImg"]
                 except:
                    self.CoverUrlPlayNow='https://img.youtube.com/vi/'+rID+'/hqdefault.jpg'
                    self.ImgAssets[str(self.playlist[self.Num]["ID"])+"AlbumImg"] = pygame.transform.scale(MSMP_Img, (140, 140))
                    try:self.CoverUrlPlayNow=playlist[self.Num]["cover"]
                    except:pass 
                    loaderUrlImg(self.CoverUrlPlayNow,rID+"AlbumImg")
                    time.sleep(0.2)
             elif(IDtype=="soundcloud"):
                 self.CoverUrlPlayNow=CoverUrlPlayNow
                 try: 
                    self.CoverUrlPlayNow=CoverUrlPlayNow
                    self.ImgAssets[rID+"SoundCloudAlbumImg"]
                 except:
                    self.CoverUrlPlayNow=CoverUrlPlayNow
                    #ImgAssets[str(IDSound)+"AlbumImg"] = pygame.transform.scale(MSMP_Img, (140, 140))
                    try:CoverUrlPlayNow=playlist[self.Num]["cover"]
                    except:pass 
                    loaderUrlImg(CoverUrlPlayNow,rID+"SoundCloudAlbumImg")
                    time.sleep(0.2)
         else:
             if(IDtype=="YouTube"):
                 self.CoverUrlPlayNow='https://img.youtube.com/vi/'+rID+'/hqdefault.jpg'
             elif(IDtype=="soundcloud"):
                 self.CoverUrlPlayNow=CoverUrlPlayNow
##          except:
##               CoverUrlPlayNow=CoverUrlPlayNow
##               #ImgAssets[str(IDSound)+"AlbumImg"] = pygame.transform.scale(MSMP_Img, (140, 140))
##               try:CoverUrlPlayNow=playlist[Num]["cover"]
##               except:pass
##               loaderUrlImg(CoverUrlPlayNow,str(r['id'])+"AlbumImg")
              # time.sleep(0.2)
             # 
     def pause(self):
      try:
          super().pause()
          time.sleep(0.2)
          if not(self.discord_rpc==None):
               self.discord_rpc.updatePlayerPause(self.NewPlaerVLC.get_length(),
                                           self.NewPlaerVLC.get_time(),
                                           PlayNowMusicDataBox=self.PlayNowMusicDataBox,
                                           PlayerState=str(self.get_state()))
      except:printError(traceback.format_exc())
     ######
     def LoadPlaylist(self,PlObj,autoPlay=False,ContinuePlay=False): 
         if not(PlObj.get("playlist")==None):
             self.playlist=PlObj.get("playlist")
             self.Num=0
             self.PlayNowMusicDataBox["TrekPlayNowID"]=self.playlist[self.Num]["ID"] 
         else:
             return "Error"
         self.iconPlayList=PlObj.get("iconPlayList")
         ContinuePlayData=PlObj.get("ContinuePlayData")
         if not(ContinuePlayData==None):
             if(ContinuePlayData.get("VersionContinuePlay")==None):ContinuePlayData=None
         if not(ContinuePlayData==None):
             if not(ContinuePlayData["VersionContinuePlay"]==self.VersionContinuePlay):ContinuePlay=None

         if not(ContinuePlayData==None) and (ContinuePlay):
                 self.Num=ContinuePlayData.get("PlayNumber")
                 ContinuePlayPos=ContinuePlayData.get("PlayPos")
                 PlayPuase=ContinuePlayData.get("PlayPuase")
                 i=0
                 if not (PlayPuase==None) and not (ContinuePlayPos==None) and not (PlayPuase==None):
                    self.play(self.Num)
                    time.sleep(1)
                    while (int(self.NewPlaerVLC.get_length())==0):
                        if(i==30):break
                        i=i+1
                        time.sleep(0.1)
                        if not(int(self.NewPlaerVLC.get_length())==0):self.setpos(ContinuePlayPos)
                    if(PlayPuase):self.pause()
                    procrutca=ContinuePlayData.get("Procrutca")
                    TreakModeNum=ContinuePlayData.get("TreakModeNum")
                    if(TreakModeNum==None):TreakModeNum=0
                    if(procrutca==None):procrutca=0
                    return {"AutoPlayProcrutca":procrutca,"TreakModeNum":TreakModeNum}
                 else:
                     ContinuePlay=False
         else:
             if(autoPlay):
                 self.play(self.Num)
                 return {"AutoPlayProcrutca":0,"TreakModeNum":0}
             else:
                 self.stop()
                 return {"AutoPlayProcrutca":0,"TreakModeNum":0}
                
         #if (ContinuePlayData==None):MSMPboxPlayer.Num=0
         #MSMPboxPlayer.PlayNowMusicDataBox["TrekPlayNowID"]=MSMPboxPlayer.playlist[MSMPboxPlayer.Num]["ID"] 
     #time.sleep(1)
     #OldMusicDataBox["Play"]=1
     #if(Vizual==1):StreamVizualWindow.update()
     
##     print("Loading..")
##     analazePlayList=False
##     time.sleep(0.5)
##     if not(ContinuePlayData==None):
##            i=0
##            while (int(MSMPboxPlayer.NewPlaerVLC.get_length())==0):
##                if(i==30):break
##                i=i+1
##                time.sleep(0.1)
##            if not(int(MSMPboxPlayer.NewPlaerVLC.get_length())==0):MSMPboxPlayer.setpos(ContinuePlayPos)
##            if(PlayPuase):MSMPboxPlayer.pause()
##     else:
##         MainStyle.procrutca=0
         
##     cacheMetaBoxPotoc = Thread(target=cacheMetaBoxDef)
##     cacheMetaBoxPotoc.setDaemon(True)
##     cacheMetaBoxPotoc.start()


     ######
     def setpos(self,PosTime):
         return super().setpos(PosTime) 
     def stop(self): 
         super().stop()
         
     def nextTreak(self):
        if not (self.PlayNowMusicDataBox["LoadingMusicMeta"]): 
          self.Num=self.Num+1
          if(len(self.playlist)==self.Num):
               self.Num=0
          if(self.PlayInThread):
              self.PlayThreadBox = Thread(target=self.play,args=(self.Num,))
              self.PlayThreadBox.setDaemon(True)
              self.PlayThreadBox.start()
          else:
              self.play(self.Num)
     def previousTreak(self):
        if not (self.PlayNowMusicDataBox["LoadingMusicMeta"]): 
          self.Num=self.Num-1
          if(-1==self.Num):
               self.Num=len(self.playlist)-1
          if(self.PlayInThread):
              self.PlayThreadBox = Thread(target=self.play,args=(self.Num,))
              self.PlayThreadBox.setDaemon(True)
              self.PlayThreadBox.start()
          else:
              self.play(self.Num)
     def play(self,Num=None): #
        if not (self.PlayNowMusicDataBox["LoadingMusicMeta"]): 
          self.PlayNowMusicDataBox["LoadingMusicMeta"]=True
          super().stop()
          self.Error=False #
          if(Num==None):
              Num=self.Num
          IDSound=self.playlist[Num]["ID"]
          self.PlayLocalFile=False
          self.PlayNowMusicDataBox["like_count"]=-1
          self.PlayNowMusicDataBox["view_count"]=-1
          self.PlayNowMusicDataBox["availability"]=None
          self.PlayNowMusicDataBox["upload_date"]=-1
          if not(self.ServerPlaer):
              try:self.lenPlayListStatus=" ("+str(Num+1)+self.localizationBox["iz"]+str(len(self.playlist))+")"
              except:printError(traceback.format_exc())
          try:
               if("MyFiles"==self.playlist[Num]["ID"]):
                  MyFilePl=self.playlist[Num]
                  self.PlayLocalFile=True
                  self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]=str(self.playlist[Num]["ID"])+"AlbumImg"
                  try:self.tagid3.parse(MyFilePl["url"])
                  except:pass
                  if not(self.ImgAssets==None):
                      self.ImgAssets[str(IDSound)+"AlbumImg"]  = GetImgFile(MyFilePl["url"])
                  self.Num=Num
                  self.CoverUrlPlayNow="MyFiles"
                  super().play(MyFilePl["url"])
                  self.msmp_streamIcon=self.msmp_streamIconDf
                  self.PlayNowMusicDataBox["titleTrekPlayNow"] = self.tagid3.title
                  if(self.PlayNowMusicDataBox["titleTrekPlayNow"]==None):
                      try:self.PlayNowMusicDataBox["titleTrekPlayNow"] = MyFilePl["name"]
                      except:pass
                  try:
                      self.PlayNowMusicDataBox["artistTrekPlayNow"] = self.tagid3.artist
                      self.PlayNowMusicDataBox["albumTrekPlayNow"] = self.tagid3.album
                  except:pass
                  Error=0
                  print("[NowPlayningPlayBox]: "+MyFilePl["name"])
                  #while ("0.0"==str((NewPlaerVLC.get_time()-NewPlaerVLC.get_length())/1000)):
                      #pass
                  time.sleep(0.1)
                  msmp_streamIcon=self.msmp_streamIcon
                  self.durationTreak=((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)

                  if(self.PlayNowMusicDataBox["artistTrekPlayNow"]==None):
                      self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                  
                   
               elif("UserMusicServer"==self.playlist[Num]["ID"]):
                  MusicServerData=self.playlist[Num]
                  if(os.path.isfile(self.downloadMusicFolder+(str(MusicServerData[Num]["url"])+"Audio.m4a")) and(DownloadingAudio)):
                     pass
      
               elif("YouTube"==self.playlist[Num]["ID"]):
                    self.Error=0
                    castViseon=self.castViseonYouTube
                    try:DownloadingSounds[playlist[Num]["url"]];NODownloadingAudio=False
                    except:DownloadingAudio=True
                    #if(1==2):
                    if(self.FullInfo):print(self.downloadMusicFolder+(str(self.playlist[Num]["url"])+"YouTubeAudio.m4a"))
                    if(os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["url"])+"YouTubeAudio.m4a"))or os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["url"])+"YouTubeAudio.mp4"))) and(DownloadingAudio):
                        if(os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["url"])+"YouTubeAudio.mp4"))):
                           MyFilePl=str(self.downloadMusicFolder+(str(self.playlist[Num]["url"])+"YouTubeAudio.mp4"))
                        if(os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["url"])+"YouTubeAudio.m4a"))):
                           MyFilePl=str(self.downloadMusicFolder+(str(self.playlist[Num]["url"])+"YouTubeAudio.m4a"))
                        self.CoverUrlPlayNow=None
                        self.PlayLocalFile=True
                        castUrl=MyFilePl
                        self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]=str(self.playlist[Num]["url"])+"AlbumImg"
                        #/NowPlayningPlayBox/ImgAlbom/
                        self.CoverUrlPlayNow=''#'http://127.0.0.1:34679/NowPlayningPlayBox/ImgAlbom/'+self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]+".png"
                        self.msmp_streamIconYouTube='https://pybms.tk/Server/DiscordRPC/imgRPC?img=https://img.youtube.com/vi/'+self.playlist[Num]["url"]+'/hqdefault.jpg'
                        castUrl=MyFilePl
                                  
                        try: 
                            if not (self.playlist[Num]["title"]==None):
                                self.PlayNowMusicDataBox["titleTrekPlayNow"]=self.playlist[Num]["title"]
                            else:
                                self.PlayNowMusicDataBox["titleTrekPlayNow"]=self.playlist[Num]["Name"]
                        except:
                            try: self.PlayNowMusicDataBox["titleTrekPlayNow"]=self.playlist[Num]["Name"]
                            except:self.PlayNowMusicDataBox["titleTrekPlayNow"]=self.playlist[Num]["name"]
                        try:
                            if not (self.playlist[Num]["artist"]==None):
                                self.PlayNowMusicDataBox["artistTrekPlayNow"]=self.playlist[Num]['artist']
                            else:
                                self.PlayNowMusicDataBox["artistTrekPlayNow"]=self.playlist[Num]["uploader"].replace(" - Topic","")
                        except:
                            try:self.PlayNowMusicDataBox["artistTrekPlayNow"]=self.playlist[Num]["uploader"].replace(" - Topic","")
                            except:self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                        try:
                            if not (playlist[Num]["album"]==None):
                                self.PlayNowMusicDataBox["albumTrekPlayNow"]=self.playlist[Num]['album']
                            else:
                                self.PlayNowMusicDataBox["albumTrekPlayNow"]=""
                        except:self.PlayNowMusicDataBox["albumTrekPlayNow"]=""
                        
                              
                        if(self.PlayNowMusicDataBox["titleTrekPlayNow"]==""):
                           try:self.PlayNowMusicDataBox["titleTrekPlayNow"] = (str(str(self.playlist[Num]["url"])+"YouTubeAudio.m4a"))
                           except:pass
                        self.Error=0
                        print("[NowPlayningPlayBox]: "+(str(str(self.playlist[Num]["url"])+"YouTubeAudio.m4a")))
                        #while ("0.0"==str((NewPlaerVLC.get_time()-NewPlaerVLC.get_length())/1000)):
                                        #pass
                    else:
                     ydl_opts=self.ydl_opts
                     if not(self.cookiesYouTube==None) and (not (self.cookiesYouTube=="")) :
                         ydl_opts['cookiefile']=self.cookiesYouTube
                     with youtube_dl.YoutubeDL(ydl_opts) as ydl: #
                        r = ydl.extract_info(self.playlist[Num]["url"], download=False)
                        castUrl = ""
                        if r != None:
                            castUrl = r['formats'][castViseon]['url']
                            if(self.FullInfo):print(r['duration'])
                            self.PlayNowMusicDataBox["titleTrekPlayNow"]=r['title']
                            self.PlayNowMusicDataBox["artistTrekPlayNow"]=r['uploader'].replace(" - Topic","")
                            self.PlayNowMusicDataBox["albumTrekPlayNow"]=""
                            self.PlayNowMusicDataBox["TrekPlayNowID"]=r['id']
                            
                            self.PlayNowMusicDataBox["like_count"]=r['like_count']
                            self.PlayNowMusicDataBox["view_count"]=r["view_count"]
                            self.PlayNowMusicDataBox["availability"]=r['availability']
                            self.PlayNowMusicDataBox["upload_date"]=r['upload_date']
                            try:
                                 self.CoverUrlPlayNow=self.playlist[Num]["cover"]
                                 self.msmp_streamIconYouTube='https://pybms.tk/Server/DiscordRPC/imgRPC?img='+self.playlist[Num]["cover"]
                            except:
                                self.CoverUrlPlayNow='https://img.youtube.com/vi/'+self.playlist[Num]["url"]+'/hqdefault.jpg'
                                self.msmp_streamIconYouTube='https://pybms.tk/Server/DiscordRPC/imgRPC?img=https://img.youtube.com/vi/'+self.playlist[Num]["url"]+'/hqdefault.jpg'#https://i.ytimg.com/vi/'+self.playlist[Num]["url"]+'/maxresdefault.jpg'
                            #https://img.youtube.com/vi/N-V3zqvtbCM/hqdefault.jpg
                            
                            try: 
                                if not (self.playlist[Num]["title"]==None):
                                    self.PlayNowMusicDataBox["titleTrekPlayNow"]=self.playlist[Num]["title"]
                            except:pass
                            try:
                                if not (self.playlist[Num]["artist"]==None):
                                    self.PlayNowMusicDataBox["artistTrekPlayNow"]=self.playlist[Num]['artist']
                            except:pass
                            try:
                                if not (self.playlist[Num]["album"]==None):
                                    self.PlayNowMusicDataBox["albumTrekPlayNow"]=self.playlist[Num]['album']
                            except:pass
                            
                            self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]=str(r['id'])+"AlbumImg"
                            self.durationTreak=r['duration']
                            try:
                                #print(r['formats'][castViseon]['url'])
                                if not(self.Useyt_dlp):
                                    print("[YouTube-dl] "+r"curent viseon\/")
                                    print("[YouTube-dl] "+r['formats'][castViseon]['format_note'])
                                    print("[YouTube-dl] "+r['formats'][castViseon]['format'])
                                    viseon="  ["+r['formats'][castViseon]['format_note']+"]"
                                i=0
                                if(self.FullInfo):print(r"===all viseon\/====")
                                while not(len(r['formats'])==i):
                                    if(self.Useyt_dlp):
                                        if(self.FullInfo):print(r['formats'][i]["format_id"]+":   "+r['formats'][i]["format"]+"         :"+r['formats'][i]['acodec'])
                                        if(self.VideoMode):
                                            if(r['formats'][i]["format_id"]=="22"):
                                                castUrl = r['formats'][i]['url']
                                                castViseonNow=i
                                        else:
                                            if(r['formats'][i]["format_id"]=="251"):
                                                castUrl = r['formats'][i]['url']
                                                castViseonNow=i
                                        
                                    else:
                                            print(r['formats'][i]['format_note'])
                                    #print(r['formats'][i]['acodec'])
                                    i=i+1
                                if(self.FullInfo):print(r"===================")
                                if(self.Useyt_dlp):
                                    if(self.FullInfo):
                                        print("[YouTube-dl] "+r"curent viseon\/")
                                        print("[YouTube-dl] "+r['formats'][castViseonNow]['format_note'])
                                        print("[YouTube-dl] "+r['formats'][castViseonNow]['format'])
                                    viseon="  ["+r['formats'][castViseon]['format_note']+"]"
                            except:
                                print("===================\nErorr: Stream detect!")
                                printError(traceback.format_exc())
                                #ErrorSound.play()
                                #ErrorLoadSound="Stream detect!"
                                OldMusicDataBox["Play"]=0
                                Error=1
                                ErrorLoadSoundStatus={"ErrorType":"ErrorLoadSoundPlay","ErrorLog":(traceback.format_exc()).split("\n")}
                        else:
                            Error=1
                            ErrorLoadSoundStatus={"ErrorType":"ErrorLoadSoundPlay","ErrorLog":(traceback.format_exc()).split("\n")} 
                    self.Num=Num
                    #LoadImg(r['id'])
                    if(self.Error==0):
                            #if(os.path.isfile(downloadMusicFolder+(str(self.playlist[Num]["url"])+"YouTubeAudio.m4a"))):
                            #    pass
                            self.LoadImg(IDasset=self.playlist[Num]["url"]+"AlbumImg",IDtype=self.playlist[Num]["ID"],rID=self.playlist[Num]["url"])
                            if(self.AutoSplitAuthorName):
                             try:
                                  temp=self.PlayNowMusicDataBox["titleTrekPlayNow"]
                                  self.PlayNowMusicDataBox["titleTrekPlayNow"]=temp.split(" - ")[1] 
                                  self.PlayNowMusicDataBox["artistTrekPlayNow"]=temp.split(" - ")[0] 
                             except:
                                  try:
                                       temp=self.PlayNowMusicDataBox["titleTrekPlayNow"]
                                       self.PlayNowMusicDataBox["titleTrekPlayNow"]=temp.split(" — ")[1]
                                       self.PlayNowMusicDataBox["artistTrekPlayNow"]=temp.split(" — ")[0]
                                  except:pass
                              
                            super().play(castUrl)
                            
                            if(self.PlayNowMusicDataBox["artistTrekPlayNow"]==None):
                                  self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                            if not(self.discord_rpc==None):
                             if(os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["url"])+"YouTubeAudio.m4a"))):
                                 time.sleep(0.1)
                                 self.durationTreak=((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)

                            if not(self.discord_rpc==None):
                                  self.discord_rpc.updatePlayerNow(PlayNowMusicDataBox=self.PlayNowMusicDataBox,
                                             durationTreak=self.durationTreak,
                                             PlLen=len(self.playlist),
                                             Num=self.Num,
                                             NowPlayIconRPC="YouTube",
                                             ImgUrl=self.msmp_streamIconYouTube,firstPlay=True)
                             
               elif("soundcloud"==self.playlist[Num]["ID"]): 
                        self.Error=0
                        castViseon=self.castViseonSoundCloud
                        try:DownloadingSounds[playlist[Num]["url"]];NODownloadingAudio=False
                        except:DownloadingAudio=True
                        #if(1==2):
                        if(os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["IDSoundcloud"])+"SoundCloudAudio.mp3"))) and(DownloadingAudio):
                            MyFilePl=str(self.downloadMusicFolder+(str(self.playlist[Num]["IDSoundcloud"])+"SoundCloudAudio.mp3"))
                            self.PlayLocalFile=True
                            try:self.tagid3.parse(MyFilePl)
                            except:pass
                            
                            self.PlayNowMusicDataBox["like_count"]=-1
                            self.PlayNowMusicDataBox["view_count"]=-1
                            self.PlayNowMusicDataBox["availability"]=None
                            self.PlayNowMusicDataBox["upload_date"]=-1
                            
                            CoverUrlPlayNow=None
                            castUrl=MyFilePl
                            self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]=str(self.playlist[Num]["IDSoundcloud"])+"SoundCloudAlbumImg"
                            self.CoverUrlPlayNow='http://127.0.0.1:34679/NowPlayningPlayBox/ImgAlbom/'+self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]+".png"
                            castUrl=MyFilePl
                            self.PlayNowMusicDataBox["titleTrekPlayNow"] = self.tagid3.title
                            if(self.PlayNowMusicDataBox["titleTrekPlayNow"]==None):
                               try:self.PlayNowMusicDataBox["titleTrekPlayNow"] = (str(str(self.playlist[Num]["IDSoundcloud"])+"SoundCloudAudio.mp3"))
                               except:pass
                            try:
                               self.PlayNowMusicDataBox["artistTrekPlayNow"] = self.tagid3.artist
                               self.PlayNowMusicDataBox["albumTrekPlayNow"] = self.tagid3.album
                            except:pass
                            self.Error=0
                            self.msmp_streamIconSoundCloud=self.msmp_streamIcon
                            print("[NowPlayningPlayBox]: "+(str(str(self.playlist[Num]["IDSoundcloud"])+"SoundCloudAudio.mp3")))
                            #while ("0.0"==str((NewPlaerVLC.get_time()-NewPlaerVLC.get_length())/1000)):
                                            #pass
            
                        else:
                            ydl_opts=self.ydl_opts
                            if not(self.cookiesSoundCloud==None):
                             if not(self.cookiesSoundCloud==""):
                                ydl_opts['cookiefile']=self.cookiesSoundCloud

                            with youtube_dl.YoutubeDL(ydl_opts) as ydl: 
                                r = ydl.extract_info(self.playlist[Num]["url"], download=False)
                                castUrl = r['formats'][castViseon]['url']
                                if(self.FullInfo):print(r['duration'])
                                self.PlayNowMusicDataBox["titleTrekPlayNow"]=r['title']
                                self.PlayNowMusicDataBox["artistTrekPlayNow"]=r['uploader']
                                self.PlayNowMusicDataBox["albumTrekPlayNow"]=""

                                self.PlayNowMusicDataBox["like_count"]=r['like_count']
                                self.PlayNowMusicDataBox["view_count"]=r["view_count"]
                                self.PlayNowMusicDataBox["availability"]=None
                                self.PlayNowMusicDataBox["upload_date"]=r['upload_date']

                                
            
                                try:
                                    if not (self.playlist[Num]["title"]==None):
                                        self.PlayNowMusicDataBox["titleTrekPlayNow"]=self.playlist[Num]["title"]
                                except:pass
                                try:
                                    if not (playlist[Num]["artist"]==None):
                                        self.PlayNowMusicDataBox["artistTrekPlayNow"]=self.playlist[Num]['artist']
                                except:pass
                                try:
                                    if not (playlist[Num]["album"]==None):
                                        self.PlayNowMusicDataBox["albumTrekPlayNow"]=self.playlist[Num]['album']
                                except:pass
                                self.durationTreak=r['duration']
                                
                                try:
                                    img=r['thumbnails'][-2]['url']
                                except:
                                    try:
                                        img=r['thumbnails'][-1]['url']
                                    except:
                                        try:
                                            img=r['thumbnails'][0]['url']
                                        except:
                                            img=HostNamePybms+"static/assets/MSMP.png"


                                try:
                                     img=self.playlist[Num]["cover"]
                                except:pass
                                self.CoverUrlPlayNow=img
                                self.msmp_streamIconSoundCloud='https://pybms.tk/Server/DiscordRPC/imgRPC?img='+img
                                
                                if(self.FullInfo):
                                    print(img)
                                    print("[SoundCloud] "+r"curent viseon\/")
                                    #print("[YouTube-dl] "+r['formats'][castViseon]['format_note'])
                                    print("[SoundCloud] "+r['formats'][castViseon]['format'])
                                #viseon="  ["+r['formats'][castViseon]['format_note']+"]"
                                i=0
                                if(self.FullInfo):print(r"===all viseon\/====")
                                while not(len(r['formats'])==i):
                                    if(self.FullInfo):print(r['formats'][i]["format"])
                                    #print(r['formats'][i]['acodec'])
                                    i=i+1
                                if(self.FullInfo):print(r"===================")
                                self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]=str(r['id'])+"SoundCloudAlbumImg"
##                                except:
##                                    printError(traceback.format_exc())
##                                    
##                                    #ImgAssets[str(IDSound)+"AlbumImg"] = pygame.transform.scale(MSMP_Img, (140, 140))
##                                    
##                                    
##                                    #loaderUrlImg(CoverUrlPlayNow,str(r['id'])+"SoundCloudAlbumImg")
##                                    time.sleep(0.2)
                        self.Num=Num
                        #LoadImg(r['id'])
                        if(self.Error==0):
                            self.LoadImg(IDasset=self.playlist[Num]["IDSoundcloud"]+"SoundCloudAlbumImg",IDtype=self.playlist[Num]["ID"],rID=self.playlist[Num]["IDSoundcloud"],CoverUrlPlayNow=self.CoverUrlPlayNow)
                            super().play(castUrl)
                            if(self.PlayNowMusicDataBox["artistTrekPlayNow"]==None):
                                  self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                            if not(self.discord_rpc==None):
                             if(os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["IDSoundcloud"])+"SoundCloudAudio.mp3"))):
                                 time.sleep(0.1)
                                 self.durationTreak=((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)
                             self.NowPlayIconRPC="SoundCloud"
                             print(self.msmp_streamIconSoundCloud)
                             if not(self.discord_rpc==None):
                                  self.discord_rpc.updatePlayerNow(PlayNowMusicDataBox=self.PlayNowMusicDataBox,
                                             durationTreak=self.durationTreak,
                                             PlLen=len(self.playlist),
                                             Num=self.Num,
                                             NowPlayIconRPC="SoundCloud",
                                             ImgUrl=self.msmp_streamIconSoundCloud,firstPlay=True)
                                  
               elif("YandexMusic"==self.playlist[Num]["ID"]): 
                        self.Error=0
                        castViseon=self.castViseonSoundCloud
                        try:DownloadingSounds[playlist[Num]["url"]];NODownloadingAudio=False
                        except:DownloadingAudio=True
                        #if(1==2):
                        if(False):
                             pass
                        #if(os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["IDSoundcloud"])+"SoundCloudAudio.mp3"))) and(DownloadingAudio):
##                            MyFilePl=str(self.downloadMusicFolder+(str(self.playlist[Num]["IDSoundcloud"])+"SoundCloudAudio.mp3"))
##                            self.PlayLocalFile=True
##                            try:self.tagid3.parse(MyFilePl)
##                            except:pass
##                            
##                            self.PlayNowMusicDataBox["like_count"]=-1
##                            self.PlayNowMusicDataBox["view_count"]=-1
##                            self.PlayNowMusicDataBox["availability"]=None
##                            self.PlayNowMusicDataBox["upload_date"]=-1
##                            
##                            CoverUrlPlayNow=None
##                            castUrl=MyFilePl
##                            self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]=str(self.playlist[Num]["IDSoundcloud"])+"SoundCloudAlbumImg"
##                            self.CoverUrlPlayNow='http://127.0.0.1:34679/NowPlayningPlayBox/ImgAlbom/'+self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]+".png"
##                            castUrl=MyFilePl
##                            self.PlayNowMusicDataBox["titleTrekPlayNow"] = self.tagid3.title
##                            if(self.PlayNowMusicDataBox["titleTrekPlayNow"]==None):
##                               try:self.PlayNowMusicDataBox["titleTrekPlayNow"] = (str(str(self.playlist[Num]["IDSoundcloud"])+"SoundCloudAudio.mp3"))
##                               except:pass
##                            try:
##                               self.PlayNowMusicDataBox["artistTrekPlayNow"] = self.tagid3.artist
##                               self.PlayNowMusicDataBox["albumTrekPlayNow"] = self.tagid3.album
##                            except:pass
##                            self.Error=0
##                            self.msmp_streamIconSoundCloud=self.msmp_streamIcon
##                            print("[NowPlayningPlayBox]: "+(str(str(self.playlist[Num]["IDSoundcloud"])+"SoundCloudAudio.mp3")))
##                            #while ("0.0"==str((NewPlaerVLC.get_time()-NewPlaerVLC.get_length())/1000)):
##                                            #pass
##            
                        else:
                          if not(self.YandexMusicClient==None):
                            ydl_opts=self.ydl_opts

                            with youtube_dl.YoutubeDL(ydl_opts) as ydl: 
                                r = ydl.extract_info(self.playlist[Num]["url"], download=False)
                                if(self.FullInfo):print(r['duration'])
                                self.PlayNowMusicDataBox["titleTrekPlayNow"]=r["track"]
                                self.PlayNowMusicDataBox["artistTrekPlayNow"]=r["album_artist"]
                                self.PlayNowMusicDataBox["albumTrekPlayNow"]=r["album"]

                                self.PlayNowMusicDataBox["like_count"]=-1
                                self.PlayNowMusicDataBox["view_count"]=-1
                                self.PlayNowMusicDataBox["availability"]=None
                                self.PlayNowMusicDataBox["upload_date"]=-1

                                regex = "album/(\w+)/"
                                self.AlbumIDYandexMusic=re.findall(regex, r["original_url"])[0]

                                Trak=self.YandexMusicClient.tracks([r['display_id']+":"+self.AlbumIDYandexMusic])[0]
                                
                                castUrl=Trak.get_download_info(get_direct_links=True)[0]["direct_link"]
            
                                try:
                                    if not (self.playlist[Num]["title"]==None):
                                        self.PlayNowMusicDataBox["titleTrekPlayNow"]=self.playlist[Num]["title"]
                                except:pass
                                try:
                                    if not (playlist[Num]["artist"]==None):
                                        self.PlayNowMusicDataBox["artistTrekPlayNow"]=self.playlist[Num]['artist']
                                except:pass
                                try:
                                    if not (playlist[Num]["album"]==None):
                                        self.PlayNowMusicDataBox["albumTrekPlayNow"]=self.playlist[Num]['album']
                                except:pass
                                self.durationTreak=r['duration']
                                
                                img=r['thumbnail']

                                try:
                                     img=self.playlist[Num]["cover"]
                                except:pass
                                self.CoverUrlPlayNow=img
                                self.msmp_streamIconSoundCloud='https://pybms.tk/Server/DiscordRPC/imgRPC?img='+img
                                
                                #viseon="  ["+r['formats'][castViseon]['format_note']+"]"
                                i=0
                                self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]=str(r['display_id'])+"YandexMusicAlbumImg"
##                                except:
##                                    printError(traceback.format_exc())
##                                    
##                                    #ImgAssets[str(IDSound)+"AlbumImg"] = pygame.transform.scale(MSMP_Img, (140, 140))
##                                    
##                                    
##                                    #loaderUrlImg(CoverUrlPlayNow,str(r['id'])+"SoundCloudAlbumImg")
##                                    time.sleep(0.2)
                          else:
                               self.Error=1
                               self.ErrorLoadSoundStatus={"ErrorType":"ErrorYandexMusicToken","ErrorLog":["Нету YandexMusic токена","Для загрузки трека из YandexMusic требуеться авторизация! \nhttps://github.com/MarshalX/yandex-music-api/discussions/513#discussioncomment-2729781"]}
                        self.Num=Num
                        #LoadImg(r['id'])
                        if(self.Error==0):
                            self.LoadImg(IDasset=self.playlist[Num]["YandexMusicID"]+"YandexMusicAlbumImg",IDtype=self.playlist[Num]["ID"],rID=self.playlist[Num]["YandexMusicID"],CoverUrlPlayNow=self.CoverUrlPlayNow)
                            super().play(castUrl)
                            if(self.PlayNowMusicDataBox["artistTrekPlayNow"]==None):
                                  self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                            if not(self.discord_rpc==None):
                             if(os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["YandexMusicID"])+"YandexMusicAudio.mp3"))): 
                                 time.sleep(0.1)
                                 self.durationTreak=((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)
                             self.NowPlayIconRPC="YandexMusic"
                             print(self.msmp_streamIconSoundCloud)
                             if not(self.discord_rpc==None):
                                  self.discord_rpc.updatePlayerNow(PlayNowMusicDataBox=self.PlayNowMusicDataBox,
                                             durationTreak=self.durationTreak,
                                             PlLen=len(self.playlist),
                                             Num=self.Num,
                                             NowPlayIconRPC="YandexMusic",
                                             ImgUrl=self.msmp_streamIconSoundCloud,firstPlay=True)
                                  
               elif("MSMPNetServer"==self.playlist[Num]["ID"]): 
                  data = {"version":self.version,"appName":"qMSMP Stream"}
                  IDSound=str(self.playlist[Num]["idSoundName"])
                  response = requests.get(self.playlist[Num]["hostUrlName"]+self.playlist[Num]["HostUrlPatch"]+self.playlist[Num]["idSoundName"], timeout=10, json=data)
                  dataBox = json.loads(response.text)
                  if(dataBox["status"]=="OK"):
                   self.CoverUrlPlayNow=self.playlist[Num]["hostUrlName"]+dataBox["AlbumImg"]
                   CoverUrlPlayNow=self.playlist[Num]["hostUrlName"]+dataBox["AlbumImg"]
                   self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]=str(self.playlist[Num]["idSoundName"])+"AlbumImg"
                   super().play(self.playlist[Num]["hostUrlName"]+dataBox["urlAudio"])
                   self.PlayNowMusicDataBox["titleTrekPlayNow"]=dataBox['Name'] 
                   self.PlayNowMusicDataBox["artistTrekPlayNow"]=dataBox['artist']
                   self.PlayNowMusicDataBox["albumTrekPlayNow"]=dataBox['album']
                   self.PlayNowMusicDataBox["Uploader"]=dataBox['Uploader']

                   self.Num=Num

                   self.PlayNowMusicDataBox["like_count"]=dataBox['like_count']
                   self.PlayNowMusicDataBox["view_count"]=dataBox["view_count"]
                   self.PlayNowMusicDataBox["availability"]=dataBox['availability']
                   self.PlayNowMusicDataBox["upload_date"]=dataBox['upload_date']
                            
                   self.Error=0
                   time.sleep(0.3)
                   self.durationTreak= dataBox["duration"]
                   print("[NowPlayningPlayBox]: "+dataBox["Name"])
                   #if not(self.discord_rpc==None):self.msmp_streamIcon=self.msmp_streamIconMain
                   if(self.PlayNowMusicDataBox["artistTrekPlayNow"]==None):
                       self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                   self.NowPlayIconRPC="msmp_serverplay"
                   if not(self.discord_rpc==None):
                                  self.discord_rpc.updatePlayerNow(PlayNowMusicDataBox=self.PlayNowMusicDataBox,
                                             durationTreak=self.durationTreak,
                                             PlLen=len(self.playlist),
                                             Num=self.Num,
                                             NowPlayIconRPC="msmp_serverplay",
                                             ImgUrl='https://pybms.tk/Server/DiscordRPC/imgRPC?img='+self.CoverUrlPlayNow,firstPlay=True)
                   print(self.CoverUrlPlayNow)
##                    
                   #print(datajson_server)
                  elif(datajson_server["status"]=="Error"):
                   #ErrorSound.play()
                   self.ErrorLoadSound = ["Не верный ID трека","Возможно у вас усторевшая версия MSMP Stream"]
                   self.ErrorLoadSoundStatus={"ErrorType":"ErrorLoadSoundPlay","ErrorLog":["Не верный ID трека","Возможно у вас усторевшая версия MSMP Stream"]}
                   self.Error=1
                    
               elif("GlobalServerUpload"==self.playlist[Num]["ID"]):
                 if(os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["IDSound"])+"GlobalServerUpload.mp3"))):
                   print("firk2")
                   MyFilePl=str(self.downloadMusicFolder+(str(self.playlist[Num]["IDSound"])+"GlobalServerUpload.mp3"))
                   self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]=str(self.playlist[Num]["IDSound"])+"AlbumImg"
                   self.Num=Num
                   IDSound=str(self.playlist[Num]["IDSound"])
                   self.PlayLocalFile=True
                   try:self.tagid3.parse(MyFilePl)
                   except:pass
                   #self.ImgAssets[str(playlist[Num]["IDSound"])+"AlbumImg"]  = GetImgFile(MyFilePl)
                   self.CoverUrlPlayNow=str(IDSound)+"AlbumImg.png"
                   super().play(MyFilePl)
                   self.PlayNowMusicDataBox["titleTrekPlayNow"] = self.tagid3.title
                   if(self.PlayNowMusicDataBox["titleTrekPlayNow"]==None):
                       try:self.PlayNowMusicDataBox["titleTrekPlayNow"] = (str(IDSound)+"GlobalServerUpload.mp3")
                       except:pass
                   try:
                       self.PlayNowMusicDataBox["artistTrekPlayNow"] = self.tagid3.artist
                       self.PlayNowMusicDataBox["albumTrekPlayNow"] = self.tagid3.album
                   except:pass
                   
                   self.Error=0
                   print("[NowPlayningPlayBox]: "+(str(IDSound)+"GlobalServerUpload.mp3"))
                   #while ("0.0"==str((NewPlaerVLC.get_time()-NewPlaerVLC.get_length())/1000)):
                       #pass
                   time.sleep(0.1)
                   self.durationTreak=((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)
                   
                   #if not(self.discord_rpc==None):self.msmp_streamIcon=self.msmp_streamIconMain
                   if(self.PlayNowMusicDataBox["artistTrekPlayNow"]==None):
                       self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                   if not(self.discord_rpc==None):
                    self.NowPlayIconRPC=self.msmp_streamIcon  
                    self.discord_rpc.updatePlayerNow(PlayNowMusicDataBox=self.PlayNowMusicDataBox,
                                             durationTreak=self.durationTreak,
                                             PlLen=len(self.playlist),
                                             Num=self.Num,
                                             NowPlayIconRPC="GlobalServerUpload",
                                             ImgUrl=self.msmp_streamIcon,firstPlay=True)
                    
                 else:
                  print("firk")
                  data = {"apikey":"BmCastMusicSreamV2","idsound":str(self.playlist[Num]["IDSound"])}
                  IDSound=str(self.playlist[Num]["IDSound"])
                  if not(self.ServerPlaer): imgAlbum = pygame.transform.scale(MSMP_Img, (140, 140))
                  response = requests.post(self.HostNamePybms+"Server/bmCastStream/MusicApi/", timeout=10, json=data)
                  datajson_server = (json.loads(response.text))
                  self.Num=Num
                  if(datajson_server["status"]=="OK"):
                   if not(self.ImgAssets==None):
                       LoaderAlbumT=Thread(target=loaderAlbumImg,args=())
                       LoaderAlbumT.start()
                       try:
                           CoverUrlPlayNow=datajson_server["img"]
                           ImgAssets[str(IDSound)+"AlbumImg"]
                       except:
                           CoverUrlPlayNow=datajson_server["img"]
                           #ImgAssets[str(IDSound)+"AlbumImg"] = pygame.transform.scale(MSMP_Img, (140, 140))
                           #loaderUrlImg(datajson_server["img"],str(self.playlist[Num]["IDSound"])+"AlbumImg")
                           time.sleep(0.2)
                   self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]=str(self.playlist[Num]["IDSound"])+"AlbumImg"
                   self.CoverUrlPlayNow=datajson_server['img']
                   super().play(datajson_server["url"])
                   self.PlayNowMusicDataBox["titleTrekPlayNow"]=datajson_server['title'] 
                   self.PlayNowMusicDataBox["artistTrekPlayNow"]=datajson_server['artist']
                   self.PlayNowMusicDataBox["albumTrekPlayNow"]=datajson_server['album']
                   self.Error=0
                   time.sleep(0.3)
                   self.durationTreak=((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)
                   print("[NowPlayningPlayBox]: "+datajson_server["name"])
                   #if not(self.discord_rpc==None):self.msmp_streamIcon=self.msmp_streamIconMain
                   if(self.PlayNowMusicDataBox["artistTrekPlayNow"]==None):
                       self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                   self.NowPlayIconRPC="GlobalServerUpload"
                   if not(self.discord_rpc==None):
                                  self.discord_rpc.updatePlayerNow(PlayNowMusicDataBox=self.PlayNowMusicDataBox,
                                             durationTreak=self.durationTreak,
                                             PlLen=len(self.playlist),
                                             Num=self.Num,
                                             NowPlayIconRPC="GlobalServerUpload",
                                             ImgUrl='https://pybms.tk/Server/DiscordRPC/imgRPC?img='+self.CoverUrlPlayNow,firstPlay=True)
#                   if not(self.discord_rpc==None):
##                    self.NowPlayIconRPC=self.msmp_streamIcon   
##                    self.discord_rpc.update(
##                    **{
##                       'details': datajson_server['title'],
##                       'state': datajson_server['artist']+self.lenPlayListStatus,
##                       'large_image':self.msmp_streamIcon,
##                       'small_image':"play",
##                       'large_text':datajson_server['album'],
##                       #'small_image':self.version,
##                       'end': time.time()+datajson_server["duration"]
##                     }
##                    )
##                    
                   #print(datajson_server)
                  elif(datajson_server["status"]=="Error"):
                   #ErrorSound.play()
                   self.ErrorLoadSound = ["Не верный ID трека","Возможно у вас усторевшая версия MSMP Stream"]
                   self.ErrorLoadSoundStatus={"ErrorType":"ErrorLoadSoundPlay","ErrorLog":["Не верный ID трека","Возможно у вас усторевшая версия MSMP Stream"]}
                   self.Error=1
               else:
                   #ErrorSound.play()
                   self.ErrorLoadSound = ["Не верный тип Аудио","Возможно у вас усторевшая версия ядра MSMP Stream"]
                   self.ErrorLoadSoundStatus={"ErrorType":"UnknownAudioTypeFormat","ErrorLog":["Не верный тип Аудио","Возможно у вас усторевшая версия ядра MSMP Stream","Либо открыт усторевший плейлист, или не устоновлен плагин?..."]}
                   self.Error=1                     
                        
          except:
              #if not(ServerPlaer): ErrorSound.play()
              #if("YouTube"==IDSound):
              with open("Error.txt", "w") as file:
                  file.write(traceback.format_exc())
              print("")
              print(traceback.format_exc())
              #ErrorLoadSound = sys.exc_info()
              #ErrorLoadSound.append("")
              # print(ErrorLoadSound)
              self.PlayNowMusicDataBox["LoadingMusicMeta"]=False
              self.ErrorLoadSoundStatus={"ErrorType":"ErrorLoadSoundPlay","ErrorLog":(traceback.format_exc()).split("\n")}
              self.Error=1
          self.PlayNowMusicDataBox["LoadingMusicMeta"]=False
          #finally:
              #self.PlayNowMusicDataBox["LoadingMusicMeta"]=False
              #if(self.Error):
                 # return "Error"
              #else:
                  #return




#InstanceSettings=[r' --projectm-preset-path='+sys.argv[0].replace(os.path.basename(sys.argv[0]), '')+r'assets/visualizations',r'--soundfont='+sys.argv[0].replace(os.path.basename(sys.argv[0]), '')+r'assets/soundfonts/8bitsf.SF2']

def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    #Функция для обрезки изображения по центру.
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

  
class ProcessRunnable(QtCore.QRunnable):
    def __init__(self, target, args):
        QtCore.QRunnable.__init__(self)
        self.t = target
        self.args = args

    def run(self):
        self.t(*self.args)

    def start(self):
        QtCore.QThreadPool.globalInstance().start(self)
        
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

def hhmmss(second):
    # s = 1000
    # m = 60000
    # h = 360000
    s = second

    
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return ("%d:%02d:%02d" % (h, m, s)) if h else ("%d:%02d" % (m, s))
class MSMPTrekBoxUi(QtWidgets.QDialog,MSMPTrekBoxUi.Ui_Dialog): 
     def __init__(self,MainWindow,cookiesFile=None):
          super().__init__()
          self.setupUi(self)
          self.MainWindow=MainWindow
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
                         'logger':MyYTLogger(False,logger=self.MainWindow.MSMPboxPlayer.logger,QPlainTextEdit=self.LogBoxYT_dlp),
                         'ignore-config':True,
                         'extract_flat':True,
                         }
          if(self.NoPlayListMode):
               ydl_opts['no-playlist']=self.NoPlayListMode
          else:
               ydl_opts['yes-playlist']=True
               
          print(ydl_opts.get('no-playlist'))     
          if not(self.cookiesFile==None):
               ydl_opts['cookiefile']=self.cookiesFile
          with youtube_dl.YoutubeDL(ydl_opts) as ydl: #
               r = ydl.extract_info(url, download=False)
               print(r['extractor'])
               if(r['extractor']=="yandexmusic:track"):
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
          self.MainWindow.MSMPboxPlayer.play(0)
          self.MainWindow.PlayButton.setEnabled(True)
          self.MainWindow.NextTreakButton.setEnabled(True)
          self.MainWindow.PauseButton.setEnabled(True)
          self.MainWindow.StopButton.setEnabled(True)
          self.MainWindow.PreviousTreakButton.setEnabled(True)
          try:self.MainWindow.ReloadInformation()
          except:pass
          self.hide()
          
               
def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    ex.TrekBoxUi.hide()
    print("error catched!:")
    print("error message:\n", tb)
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText("MSMP CRASH:")
    msg.setInformativeText(str(tb))
    msg.setWindowTitle("Error")
    retval = msg.exec_()
    ex.close()


class NameDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if isinstance(index.model(), QtWidgets.QFileSystemModel):
            if not index.model().isDir(index):
                option.text = index.model().fileInfo(index).baseName()

    def setEditorData(self, editor, index):
        if isinstance(index.model(), QtWidgets.QFileSystemModel):
            if not index.model().isDir(index):
                editor.setText(index.model().fileInfo(index).baseName())
            else:
                super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(model, QtWidgets.QFileSystemModel):
            fi = model.fileInfo(index)
            if not model.isDir(index):
                model.setData(index, editor.text() + "." + fi.suffix())
            else:
                super().setModelData(editor, model.index)




               
class MainWindow(QtWidgets.QMainWindow, mainUI.Ui_MainWindow): #

    def __init__(self): 
        super().__init__()
        InstanceSettings=[]

        self.config,self.ConfigDir,self.PlaylistsFolder=loadConfig()

        if(self.config['MSMP Stream'].get("mobileMode")==None):
             self.config['MSMP Stream']["mobileMode"]=False
             
        self.mobileMode=self.config['MSMP Stream']["mobileMode"]

        self.LocalImgCache={}

        if(self.mobileMode):
             LoadStyleUI("untitledMobile.ui",self)
        else:
             self.setupUi(self)

        if(self.config['MSMP Stream']["localizationBox"]=="assets/localizationBoxes/ru.localizationBox"):
             self.config['MSMP Stream']['localizationBox']='lengboxs/ru.loclb'

        self.show()
        
        self.PlayerBox.hide()
        self.PlaylistBox.hide()
        if not(self.mobileMode):
             self.NewMainUI=True
             self.NewMainUIb=self.NewMainUI
             self.LoadingLabel.show()
        else:
             self.NewMainUI=False
             self.NewMainUIb=self.NewMainUI

        self.update()

        print(self.config['MSMP Stream']['localizationBox'])
        self.lengbox=loadLocal(self.config['MSMP Stream']['localizationBox'])
        
##        if sys.platform == "win32":
##            InstanceSettings.append("--audio-visual="+"visual")
##            InstanceSettings.append("--effect-list=spectrum")
##            InstanceSettings.append("--effect-fft-window=none")

        self.CloseApp=False


        print(self.ConfigDir)

        if(self.config['MSMP Stream'].get("notifiDisabled")==None):
             self.config['MSMP Stream']["notifiDisabled"]=False

          
        
        if(self.config['MSMP Stream'].get("last-fmAllowed")==None):
             self.config['MSMP Stream']["last-fmAllowed"]=False
        
        OtherApiAlow=False
        if(self.config['MSMP Stream']['Discord_rpc']):
             Presence=True
             OtherApiAlow=True
        else:
             Presence=None
             
        if(self.config['MSMP Stream']["last-fmAllowed"]):
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
             self.RPC=MSMP_RPC(RPC=Presence,DirConfig=self.ConfigDir,LastFm=LastFm,version="QT0.6a",lengbox=self.lengbox,ImgApiHost=ImgApiHost,ImgApiHostTOKEN=ImgApiHostTOKEN)
        else:
            self.RPC=None 
        self.MSMPboxPlayer=MSMPboxPlayer(ServerPlaer=True,
                                         InstanceSettings=InstanceSettings,
                                         MSMP_RPC=self.RPC,
                                         logger=logger,
                                         AutoSplitAuthorName=True,
                                         downloadMusicFolder=self.config['MSMP Stream']['downloadMusicFolder'],
                                         TOKENYandexMusicClient=self.config['MSMP Stream']["YandexMusicTOKEN"])
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


        try:
             self.notifiBox=notifiBox(Disabled=self.config['MSMP Stream']["notifiDisabled"])
        except:
             self.notifiBox=notifiBox(Disabled=True)
             #LoadStyleUI("untitled.ui",self)

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
##            #it.setData(QtGui.QIcon(iconroot +'/images/flags'), QtCore.Qt.DecorationRole)
##            it.setData(cov,        # +++
##                                   QtCore.Qt.DecorationRole)
        
        self.PathImgsCache=self.config['MSMP Stream']['cacheimgpachfolder']

        
        self.add_functions()
        

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
                   self.showFullScreen()
        
        
        #it.setBackground(QtGui.QColor('red'))
        
        self.isPlayListSelectionChanged=False
        
        
        if(self.mobileMode):
             self.MSMPboxPlayer.NewPlaerVLC.audio_set_volume(100)
        else:
             self.VolumeSlider.setValue(self.MSMPboxPlayer.NewPlaerVLC.audio_get_volume())
        
        self.bufferNewPlaerVLCposition=0
        self.p = ProcessRunnable(target=self.updateBgGui, args=())
        self.p.start()
        
        self.EqualizerPlaerVLC=vlc.AudioEqualizer()
        self.setEqualizer()
        
    def FixScrollBlat(self):
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
        background-color: #B72E2B;         
        min-height: 5px;
}

QScrollBar::sub-line:vertical{
        margin: 3px 0px 3px 0px;
        border-image: url(img/SliderUp.png);
        height: 11px;
        width: 11px;
        subcontrol-position: top;
        subcontrol-origin: margin;
}

QScrollBar::add-line:vertical{
        margin: 3px 0px 3px 0px;
        border-image: url(img/SliderDown.png);
        height: 11px;
        width: 11px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on{
        border-image: url(img/SliderUpA.png);
        height: 11px;
        width: 11px;
        subcontrol-position: top;
        subcontrol-origin: margin;
}

QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on{
        border-image: url(img/SliderDownA.png);
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
""")
          
    def add_functions(self):

        self.model = self.get_file_tree_model(self.PlaylistsFolder)

        self.PlaylistsView.setModel(self.model)
        self.PlaylistsView.setRootIndex(self.model.index(self.PlaylistsFolder))

        

        self.PlaylistsViewShowed=True
        self.PlaylistsView.hideColumn(3)
        self.PlaylistsView.hideColumn(2)
        self.PlaylistsView.hideColumn(1)
        self.PlaylistsView.doubleClicked.connect(self.handle_double_click)
        delegate = NameDelegate(self.PlaylistsView)
        self.PlaylistsView.setItemDelegate(delegate)
        
        self.PlayListAddMenu = QtWidgets.QMenu()
        self.PlayListAddMenu.triggered.connect(lambda x: self.AddTrekOptions(x.data))
        self.AddTreakPlaylist.setMenu(self.PlayListAddMenu)

        self.RemoveTreakMenu = QtWidgets.QMenu()
        self.RemoveTreakMenu.triggered.connect(lambda x: print(x.data))
        self.RemoveTreakPlaylist.setMenu(self.RemoveTreakMenu)

        self.MenuPlaylistMenu = QtWidgets.QMenu()
        self.MenuPlaylistMenu.triggered.connect(lambda x: self.PlTrekOptions(x.data))
        self.MenuPlaylist.setMenu(self.MenuPlaylistMenu)

        self.MSMPqmenu = QtWidgets.QMenu()
        self.MSMPqmenu.triggered.connect(lambda x: self.SkinChanger(x.data))
        self.MSMPmenu.setMenu(self.MSMPqmenu)
        

        MSMPmenuData=[self.lengbox["MSMP Stream"].get("obu")+"#obu",self.lengbox["MSMP Stream"].get("Set")+"#Set"]
        

        if not(self.mobileMode):
             MSMPmenuData.append(self.lengbox["MSMP Stream"].get("PLshHd")+"#PLshHd")
             MSMPmenuData.append("SKIN TOP#st")
             MSMPmenuData.append("SKIN BOTTOM#sb")
             MSMPmenuData.append("SKIN OLD#OLDskin")
             MSMPmenuData.append("SKIN AIMPqt#AIMPskin")
             MSMPmenuData.append("mbMode#mbMode")

        MSMPmenuData.append("setEqualizer#sEq")
        MSMPmenuData.append(self.lengbox["MSMP Stream"].get("Cls")+"#Cls")
        
        if(self.mobileMode):
             self.PlSelector=False
             self.ButtonShowPlSelector.clicked.connect(lambda: self.ShowPlSelector())
        
        self.add_menu(MSMPmenuData, self.MSMPqmenu)
        self.add_menu([self.lengbox["MSMP Stream"].get("RT")+"#RT",self.lengbox["MSMP Stream"].get("CPL")+"#CPL"], self.RemoveTreakMenu)
        
        self.add_menu([self.lengbox["MSMP Stream"].get("addLF")+"#addLF",{self.lengbox["MSMP Stream"].get("addAS")+"#addAS": ["MSMP audio"+"#addAS-Ma",self.lengbox["MSMP Stream"].get("addAS-YV")+"#addAS-YV",self.lengbox["MSMP Stream"].get("addAS-ST")+"#addAS-ST"]}], self.PlayListAddMenu)

        self.add_menu([self.lengbox["MSMP Stream"].get("DwTr")+"#DwTr",self.lengbox["MSMP Stream"].get("SvPL")+"#SvPL",self.lengbox["MSMP Stream"].get("SvPLas")+"#SvPLas",self.lengbox["MSMP Stream"].get("PYtPl")+"#PYtPl"], self.MenuPlaylistMenu)
#https://msmp-audio.maxsspeaker.tk/msmp-audio/audio/Space%20Queen-Nglr2WV8mw0
        


        self.PlayListBox = QtGui.QStandardItemModel()
        self.PlaylistView.setModel(self.PlayListBox)
        self.PlaylistView.setSpacing(0)
            
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

        if not(self.mobileMode):self.VolumeSlider.valueChanged[int].connect(self.changeVolumeSlider)

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
        if not(self.mobileMode):self.statusBar.hide()

        if sys.platform.startswith("linux"):
            pass# for Linux using the X Server
            #self.MSMPboxPlayer.NewPlaerVLC.set_xwindow(self.Visualframe.winId())
        elif sys.platform == "win32":  # for Windows
            self.MSMPboxPlayer.NewPlaerVLC.set_hwnd(self.Visualframe.winId())
        #elif sys.platform == "darwin":  # for MacOS
        #    self.MSMPboxPlayer.NewPlaerVLC.set_nsobject(self.Visualframe.winId())

        if not(self.mobileMode):self.VolumeSlider.setValue(self.MSMPboxPlayer.NewPlaerVLC.audio_get_volume())
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
              self.ViewPlaylistBox.show()
              self.PlaylistsView.hide()
         else:
              self.PlSelector=True
              self.ViewPlaylistBox.hide()
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
              
    def ReloadInformation(self,ReloadInfoPlayer=True):
         
        
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
                       it.setData(QtGui.QIcon(pixmap),QtCore.Qt.DecorationRole)
                 else:
                       pixmap=QtGui.QPixmap("img/Missing_Texture.png")
                       it.setData(QtGui.QIcon(pixmap),QtCore.Qt.DecorationRole)
            elif (os.path.isfile(self.PathImgsCache+urlSoundID)): 
                 it.setData(QtGui.QIcon(self.PathImgsCache+urlSoundID),QtCore.Qt.DecorationRole)
            else:
                 it.setData(QtGui.QIcon("img/AlbumImgMini.png"),QtCore.Qt.DecorationRole)
                 
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
        model = QtWidgets.QFileSystemModel()
        model.setRootPath(root_path)
        model.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs | QtCore.QDir.Files)
        model.setNameFilters(['*'])
        model.setNameFilterDisables(False)
        return model
    def SkinChanger(self,Option):

         
         if(Option=="PLshHd"):
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
              LoadStyleUI("untitledStyleSpew3.ui",self)
              self.add_functions()
              self.show()
              self.showNormal()
              self.NewMainUI=False
              if not(self.MSMPboxPlayer.playlist==None):
                   self.ReloadInformation()
         elif(Option=="OLDskin"):
              self.DataPath=None
              LoadStyleUI("untitled.ui",self)
              self.add_functions()
              self.show()
              self.showNormal()
              self.NewMainUI=False
              if not(self.MSMPboxPlayer.playlist==None):
                   self.ReloadInformation()
                   
         elif(Option=="st"):
              self.DataPath=None
              self.setupUi(self)
              #LoadStyleUI("untitled.ui",self)
              self.add_functions()
              self.show()
              self.showNormal()
              self.NewMainUI=self.NewMainUIb
              self.FixScrollBlat()
              if not(self.MSMPboxPlayer.playlist==None):
                   self.ReloadInformation()
         elif(Option=="AIMPskin"):
              self.DataPath=None
              LoadStyleUI("untitledStyleSpew.ui",self)
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
              LoadStyleUI("untitledMobile.ui",self)
              self.add_functions()
              self.show()
              self.showFullScreen()
              if(self.mobileMode):
                   self.PlaylistsView.hide()
              if not(self.MSMPboxPlayer.playlist==None):
                   self.ReloadInformation()
                   
    def PlTrekOptions(self,Option):
         if(Option=="PYtPl"):
              self.TrekBoxUi.NoPlayListMode=False
              self.TrekBoxUi.show()
         if(Option=="SvPL"):
              self.SavePLmsmp(self.MSMPboxPlayer.OpenedplaylistPath)

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
    def SavePLmsmp(self,path):
       if not (self.MSMPboxPlayer.OpenedplaylistPath==None):  
         plToSave={"playlist":self.MSMPboxPlayer.playlist,"iconPlayList": None, "ContinuePlayData": None,"VerisonCore":2}
         with open(path, 'w') as f:
              json.dump(plToSave, f, indent=2)
              
    def OpenPLmsmp(self,path,AutoPlay=True):
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
                     
                     it.setData(QtGui.QIcon(pixmap),QtCore.Qt.DecorationRole)
                    else:
                       pixmap=QtGui.QPixmap("img/Missing_Texture.png")
                       it.setData(QtGui.QIcon(pixmap),QtCore.Qt.DecorationRole)
            elif (os.path.isfile(self.PathImgsCache+urlSoundID)): 
                 it.setData(QtGui.QIcon(self.PathImgsCache+urlSoundID),QtCore.Qt.DecorationRole)
            else:
                 it.setData(QtGui.QIcon("img/AlbumImgMini.png"),QtCore.Qt.DecorationRole)
        if not(len(self.MSMPboxPlayer.playlist)==0):
             self.PlayButton.setEnabled(True)
             self.NextTreakButton.setEnabled(True)
             self.PauseButton.setEnabled(True)
             self.StopButton.setEnabled(True)
             self.PreviousTreakButton.setEnabled(True)
             if(AutoPlay):self.UpdateInfoTreakPL(self.MSMPboxPlayer.play(0))
             
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
##              if("State.Opening"==str(MediaBoxStatus)):
##                        if not (self.OpeingVaribleBuffer):
##                                  self.OpeingVaribleBuffer=True
##                                  self.statusBar.show()
##                                  self.statusBar.showMessage("Loading Treak",0)
##              else:
##                        if (self.OpeingVaribleBuffer):
##                                  self.statusBar.hide()
##                                  self.OpeingVaribleBuffer=False   
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
         if not(Invert):
              PlayModeTreak.setStyleSheet("""
QPushButton{
  background-color: rgb(50, 50, 50,0);
  border: none;
  border-image: url(img/"""+IconName+"""New.png);
}
QPushButton:hover{
  background-color: rgb(100,100, 100,0);
  border: none;
  border-image: url(img/"""+IconName+"""NewA.png);
}

QPushButton:pressed{
  background-color: rgb(50, 50, 50,255);
  border: none;
  border-image: url(img/"""+IconName+"""NewA.png);

}
""")
         else:
              PlayModeTreak.setStyleSheet("""
QPushButton{
  background-color: rgb(50, 50, 50,0);
  border: none;
  border-image: url(img/"""+IconName+"""NewA.png);
}
QPushButton:hover{
  background-color: rgb(100,100, 100,0);
  border: none;
  border-image: url(img/"""+IconName+"""New.png);
}

QPushButton:pressed{
  background-color: rgb(50, 50, 50,255);
  border: none;
  border-image: url(img/"""+IconName+"""New.png);

}
""")

    def UpdateBg(self,RGBdata):
         self.ContorlPanel.setStyleSheet("QGroupBox{\n"
"   background-color:qlineargradient(spread:pad, x1:0.278, y1:1, x2:0, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba("+RGBdata+", 255));\n"
"   color:rgb(0,0,0);\n"
"   border:none;\n"
"   border-bottom: 1px solid;\n"
"}")
    def UpdateInfoTreakPL(self,fun):
         
        self.TreakName.setText(self.MSMPboxPlayer.PlayNowMusicDataBox["titleTrekPlayNow"])
        self.AuthorName.setText(self.MSMPboxPlayer.PlayNowMusicDataBox["artistTrekPlayNow"])
        self.AlbumName.setText(self.MSMPboxPlayer.PlayNowMusicDataBox["albumTrekPlayNow"])
        if not(self.LestNum==-1):
             self.PlayListBox.itemFromIndex(self.PlayListBox.index(self.LestNum,0)).setBackground(QtGui.QColor('rgb(0,0,0,0)'))
        self.LestNum=self.MSMPboxPlayer.Num
        try:self.PlayListBox.itemFromIndex(self.PlayListBox.index(self.LestNum,0)).setBackground(QtGui.QColor('red'))
        except:
             self.LestNum=-1
             return
        print("Firk1")  
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
                     try:self.PlayListBox.itemFromIndex(self.PlayListBox.index(self.LestNum,0)).setData(QtGui.QIcon(pixmap),QtCore.Qt.DecorationRole)
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
                       try:self.PlayListBox.itemFromIndex(self.PlayListBox.index(self.LestNum,0)).setData(QtGui.QIcon(pixmap),QtCore.Qt.DecorationRole)
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
                     try:self.PlayListBox.itemFromIndex(self.PlayListBox.index(self.LestNum,0)).setData(QtGui.QIcon(pixmap),QtCore.Qt.DecorationRole)
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
                except:pass
                if not(self.NewMainUI):self.UpdateBg(str(int(RGBbg[0]))+", "+str(int(RGBbg[1]))+", "+str(int(RGBbg[2])))
                else:
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
            self.AlbumImg.setPixmap(QtGui.QPixmap("img/X9at37tsrY8AlbumImg.png"))
            self.notifiBox.ShowNotifi(self.MSMPboxPlayer.PlayNowMusicDataBox["titleTrekPlayNow"],
                        self.MSMPboxPlayer.PlayNowMusicDataBox["artistTrekPlayNow"])
        if not(self.DataPath==None):
             if("soundcloud"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                     self.DataPath.setText(r"SoundCloud/"+str(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["IDSoundcloud"]))
             elif("YouTube"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                     self.DataPath.setText(r"YouTube/"+str(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"]))
             elif("YandexMusic"==self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]):
                   self.DataPath.setText(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"]) #self.MSMPboxPlayer.self.AlbumIDYandexMusic
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
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.CloseApp=True
            if not(self.RPC==None):self.RPC.RPC.close()
            self.MSMPboxPlayer.stop() 
            event.accept()
            #self.close()
            
        else:
            event.ignore()
       except:
                print('\n',traceback.format_exc())

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
            

if __name__ == '__main__':
     
    app = QtWidgets.QApplication(sys.argv)
    sys.excepthook = excepthook
    ex = MainWindow()
    
    sys.exit(app.exec_())
    firkbbb
