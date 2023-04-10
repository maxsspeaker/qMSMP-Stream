import sys, time, os, traceback
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox 
from PyQt5.QtGui import QIcon,QFont 
from os.path import exists
from PIL import Image
from PIL.ImageQt import ImageQt
import io
import logging
from logging.handlers import QueueHandler
from pypresence import Presence
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
#logger = logging.getLogger('discord')


#today = date.today()
##handler = logging.FileHandler(
##    filename='logs/discord-'+str(today)+'.log',
##    encoding='utf-8',
##    mode="w"
##)
#logger.addHandler(logging.StreamHandler())

import mainUI

import requests
import urllib
import json
import yt_dlp as youtube_dl
from eyed3 import id3
from eyed3 import load
from threading import Thread
import vlc
from appdirs import user_config_dir


def loadConfig():
     configFileName = "config.yml"

     configDir = user_config_dir(appname="MSMP-Stream",appauthor="Maxsspeaker",version="5.0",roaming=True)
     print(configDir)

     configFile = os.path.join(configDir,configFileName)
     print(configFile)
     if(os.path.isfile(configFile)):
          with open(configFile,"r") as f:
               config = yaml.safe_load(f)
          return config
     else:
          config={
               'MSMP Stream': 
                    {'Discord_rpc':True,
                     'audioVisual': 'visual',
                     'cache': True,
                     'cacheimgpachfolder': 'assets/cache/',
                     'downloadMusicFolder': 'download_Music/',
                     'localizationBox': 'assets/localizationBoxes/ru.localizationBox',
                     'NowPlayningPlayBoxActive': False,
                     'VideoMode': False,
                     'latest_playlist':""
                     },
               'MSMP Stream Equalizer':
                    {'EqualizerOnOff': False,
                     'EqualizerSettings': [7.5, 7.5, 3.9, 0.1, 0, 0, 0, 0, 1.6, 1.6, 7.0]
                     }
               }
          os.makedirs(os.path.dirname(configFile), exist_ok=True)
          print("firk")
          with open(configFile,"w") as f:
               yaml.dump(config,f)
          return config,UserPath

class MyYTLogger:
    def __init__(self,FullInfo,logger):
        self.FullInfo=FullInfo
        self.logger=logger
        
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            self.logger.debug(msg) 
        else:
            self.logger.debug(msg) 

    def info(self, msg):
        if(self.FullInfo):self.logger.info(msg)
        pass

    def warning(self, msg):
        self.logger.warning(msg) 

    def error(self, msg):
        self.logger.error(msg)



class Discord_RPC():
     def __init__(self,RPC,msmp_streamIconYouTube=None,
                  msmp_streamIconMain=None,
                  msmp_streamIconSoundCloud=None,
                  logger=None):
          self
     

class GibridPlayer():
    def __init__(self,InstanceSettings):
          self.Instance = vlc.Instance(InstanceSettings)
          self.NewPlaerVLC = self.Instance.media_player_new()
          
    def play(self,url):
        self.media = self.Instance.media_new(url)
        self.NewPlaerVLC.set_media(self.media)
        self.NewPlaerVLC.play()
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
             if(self.PlayNowMusicDataBox["LoadingMusicMeta"]):
                 self.discord_rpc.update(
                     **{
                         'large_image':"missing_texture",
                    })
             else:
                 self.discord_rpc.update(
                     **{
                         'large_image':msmp_streamIcon,
                    })
             
             #OldMusicDataBox["Play"]=0
             self.Error=0
        
        
version=0.1

class MSMPboxPlayer(GibridPlayer): 
     def __init__(self,ServerPlaer,
                  InstanceSettings,
                  downloadMusicFolder="",
                  localizationBox=None,
                  ImgAssets=None,
                  discord_rpc=None,
                  HostNamePybms="",
                  versionCs=None,
                  FullInfo=False,
                  msmp_streamIconYouTube=None,
                  msmp_streamIconMain=None,
                  msmp_streamIconSoundCloud=None,
                  VideoMode=False,
                  logger=None,PlayInThread=False):
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
          if not(discord_rpc==None):
           if(msmp_streamIconMain==None):
              self.msmp_streamIconMain=self.msmp_streamIcon
           else:self.msmp_streamIconMain=msmp_streamIconMain
           if(msmp_streamIconSoundCloud==None):
              self.msmp_streamIconSoundCloud=self.msmp_streamIcon
           else:self.msmp_streamIconSoundCloud=msmp_streamIconSoundCloud 
           if(msmp_streamIconYouTube==None):
              self.msmp_streamIconYouTube=self.msmp_streamIcon
           else:self.msmp_streamIconYouTube=msmp_streamIconYouTube
          self.ImgAssets=ImgAssets
          self.castViseonSoundCloud=-1
          self.Useyt_dlp=True
          self.VideoMode=VideoMode
          self.DownloadingSounds={}
          self.tagid3 = id3.Tag()
          self.ErrorLoadSound=[]
          self.ServerPlaer=ServerPlaer
          self.discord_rpc=discord_rpc
          self.HostNamePybms=HostNamePybms
          self.VersionContinuePlay="v0.1.2-beta"
          self.PlayLocalFile=False
          
          if not(ServerPlaer):
              self.localizationBox=localizationBox
     def LoadImg(self,IDasset,IDtype,rID,CoverUrlPlayNow=None):
         if not(self.ImgAssets==None):
             if(IDtype=="YouTube"):
                 try: 
                    self.CoverUrlPlayNow='https://i.ytimg.com/vi/'+rID+'/maxresdefault.jpg'
                    self.ImgAssets[str(rID)+"AlbumImg"]
                 except:
                    self.CoverUrlPlayNow='https://i.ytimg.com/vi/'+rID+'/maxresdefault.jpg'
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
                 self.CoverUrlPlayNow='https://i.ytimg.com/vi/'+rID+'/maxresdefault.jpg'
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
        if str(self.get_state())=="State.Playing": 
          if not(self.discord_rpc==None):
           self.discord_rpc.update(
              **{
                  'details': self.PlayNowMusicDataBox["titleTrekPlayNow"],
                  'state': self.PlayNowMusicDataBox["artistTrekPlayNow"]+self.lenPlayListStatus,
                  'large_image':self.NowPlayIconRPC,
                  'small_image':"pause",
                  #'large_text':self.PlayNowMusicDataBox["albumTrekPlayNow"],
                  #'small_image':self.version
                  }
              )
           
          #StepPause=cur_time
          super().pause()  
          #start_time = time.time()
          #cur_time = time.time() - start_time + cur_timeSet
          #cur_time = cur_timeSet
        else:
         super().pause()
         if not(self.discord_rpc==None):
          if not(int(self.NewPlaerVLC.get_length())==0):
          #print(NewPlaerVLC.get_time()/1000)
          #print(cur_timeSet)
          #start_time = time.time()
           self.discord_rpc.update(
              **{
                  'details': self.PlayNowMusicDataBox["titleTrekPlayNow"],
                  'state': self.PlayNowMusicDataBox["artistTrekPlayNow"]+self.lenPlayListStatus,
                  'large_image':self.NowPlayIconRPC,
                  'small_image':"play",
                  #'large_text':self.PlayNowMusicDataBox["albumTrekPlayNow"],
                  #'small_image':self.version,
                  'end': time.time()+((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)
                }
              )
           
          else:
            self.discord_rpc.update(
              **{
                  'details': self.PlayNowMusicDataBox["titleTrekPlayNow"],
                  'state': self.PlayNowMusicDataBox["artistTrekPlayNow"],
                  'large_image':self.msmp_streamIcon,
                  'small_image':"play",
                  #'small_image':self.version,
                }
              )
            
  
  
  
  
           
            if str(self.get_state())=="State.Playing":
                self.NewPlaerVLC.pause()
                if not(self.discord==None):
                     pass
                
            else:
                self.NewPlaerVLC.pause()
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
                  self.CoverUrlPlayNow=None
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
                  msmp_streamIcon=msmp_streamIconMain
                  if(self.PlayNowMusicDataBox["artistTrekPlayNow"]==None):
                      self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                  if not(self.discord_rpc==None):
                   self.discord_rpc.update(
                   **{
                      'details': self.PlayNowMusicDataBox["titleTrekPlayNow"],
                      'state': self.PlayNowMusicDataBox["artistTrekPlayNow"]+lenPlayListStatus,
                      'large_image':self.msmp_streamIcon,
                      'small_image':"play",
                      #'large_text':self.PlayNowMusicDataBox["albumTrekPlayNow"],
                      'small_image':version,
                      'end': time.time()+((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)
                    }
                   )
                   
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
                        self.CoverUrlPlayNow='http://127.0.0.1:34679/NowPlayningPlayBox/ImgAlbom/'+self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]+".png"
                        self.msmp_streamIconYouTube='https://pybms.tk/Server/DiscordRPC/imgRPC?img=https://i.ytimg.com/vi/'+self.playlist[Num]["url"]+'/maxresdefault.jpg'
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
                            self.msmp_streamIconYouTube='https://pybms.tk/Server/DiscordRPC/imgRPC?img=https://i.ytimg.com/vi/'+self.playlist[Num]["url"]+'/maxresdefault.jpg'
                            
                            
                            try: 
                                if not (playlist[Num]["title"]==None):
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
                            super().play(castUrl)
                            if not(self.discord_rpc==None):self.msmp_streamIcon=self.msmp_streamIconYouTube
                            if(self.PlayNowMusicDataBox["artistTrekPlayNow"]==None):
                                  self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                            if not(self.discord_rpc==None):
                             if(os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["url"])+"YouTubeAudio.m4a"))):
                                 time.sleep(0.1)
                                 self.durationTreak=((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)
                             self.NowPlayIconRPC=self.msmp_streamIconYouTube
                             self.discord_rpc.update(
                             **{
                                'details': self.PlayNowMusicDataBox["titleTrekPlayNow"],
                                'state':self.PlayNowMusicDataBox["artistTrekPlayNow"]+self.lenPlayListStatus,
                                'large_image':self.msmp_streamIconYouTube,
                                'small_image':"play",
                                #'large_text':self.PlayNowMusicDataBox["albumTrekPlayNow"],
                                #'small_image':self.version,
                                'end': time.time()+self.durationTreak
                             }
                             )
                             
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
                                CoverUrlPlayNow=img
                                try:CoverUrlPlayNow=playlist[Num]["cover"]
                                except:CoverUrlPlayNow=""
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
                            self.LoadImg(IDasset=self.playlist[Num]["IDSoundcloud"]+"SoundCloudAlbumImg",IDtype=self.playlist[Num]["ID"],rID=self.playlist[Num]["IDSoundcloud"],CoverUrlPlayNow=CoverUrlPlayNow)
                            super().play(castUrl)
                            if(self.PlayNowMusicDataBox["artistTrekPlayNow"]==None):
                                  self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                            if not(self.discord_rpc==None):
                             if(os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["IDSoundcloud"])+"SoundCloudAudio.mp3"))):
                                 time.sleep(0.1)
                                 self.durationTreak=((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)
                             self.NowPlayIconRPC=self.msmp_streamIconSoundCloud
                             self.discord_rpc.update(
                             **{
                                'details': self.PlayNowMusicDataBox["titleTrekPlayNow"],
                                'state':self.PlayNowMusicDataBox["artistTrekPlayNow"]+self.lenPlayListStatus,
                                'large_image':self.msmp_streamIconSoundCloud,
                                'small_image':"play",
                                #'large_text':self.PlayNowMusicDataBox["albumTrekPlayNow"],
                                #'small_image':self.version,
                                'end': time.time()+self.durationTreak
                             }
                             )
                             
               elif("GlobalServerUpload"==self.playlist[Num]["ID"]):
                 if(os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["IDSound"])+"GlobalServerUpload.mp3"))):
                   print("firk2")
                   MyFilePl=str(self10.downloadMusicFolder+(str(self.playlist[Num]["IDSound"])+"GlobalServerUpload.mp3"))
                   self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]=str(self.playlist[Num]["IDSound"])+"AlbumImg"
                   self.Num=Num
                   IDSound=str(self.playlist[Num]["IDSound"])
                   self.PlayLocalFile=True
                   try:self.tagid3.parse(MyFilePl)
                   except:pass
                   #self.ImgAssets[str(playlist[Num]["IDSound"])+"AlbumImg"]  = GetImgFile(MyFilePl)
                   self.CoverUrlPlayNow=None
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
                   if not(self.discord_rpc==None):self.msmp_streamIcon=self.msmp_streamIconMain
                   if(self.PlayNowMusicDataBox["artistTrekPlayNow"]==None):
                       self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                   if not(self.discord_rpc==None):
                    self.NowPlayIconRPC=self.msmp_streamIcon  
                    self.discord_rpc.update(
                    **{
                       'details': self.PlayNowMusicDataBox["titleTrekPlayNow"],
                       'state': self.PlayNowMusicDataBox["artistTrekPlayNow"]+self.lenPlayListStatus,
                       'large_image':self.msmp_streamIcon,
                       'small_image':"play",
                       #'large_text':self.PlayNowMusicDataBox["albumTrekPlayNow"],
                       #'small_image':self.version,
                       'end': time.time()+((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)-((self.NewPlaerVLC.get_time()-self.NewPlaerVLC.get_length())/1000)
                     }
                    )
                    
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
                   super().play(datajson_server["url"])
                   self.PlayNowMusicDataBox["titleTrekPlayNow"]=datajson_server['title'] 
                   self.PlayNowMusicDataBox["artistTrekPlayNow"]=datajson_server['artist']
                   self.PlayNowMusicDataBox["albumTrekPlayNow"]=datajson_server['album']
                   self.Error=0
                   print("[NowPlayningPlayBox]: "+datajson_server["name"])
                   if not(self.discord_rpc==None):self.msmp_streamIcon=self.msmp_streamIconMain
                   if(self.PlayNowMusicDataBox["artistTrekPlayNow"]==None):
                       self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                   if not(self.discord_rpc==None):
                    self.NowPlayIconRPC=self.msmp_streamIcon   
                    self.discord_rpc.update(
                    **{
                       'details': datajson_server['title'],
                       'state': datajson_server['artist']+self.lenPlayListStatus,
                       'large_image':self.msmp_streamIcon,
                       'small_image':"play",
                       'large_text':datajson_server['album'],
                       #'small_image':self.version,
                       'end': time.time()+datajson_server["duration"]
                     }
                    )
                    
                   #print(datajson_server)
                  elif(datajson_server["status"]=="Error"):
                   #ErrorSound.play()
                   self.ErrorLoadSound = ["Не верный ID трека","Возможно у вас усторевшая версия MSMP Stream"]
                   self.ErrorLoadSoundStatus={"ErrorType":"ErrorLoadSoundPlay","ErrorLog":["Не верный ID трека","Возможно у вас усторевшая версия MSMP Stream"]}
                   self.Error=1
               else:
                   #ErrorSound.play()
                   self.ErrorLoadSound = ["Не верный тип Аудио","Возможно у вас усторевшая версия MSMP Stream"]
                   self.ErrorLoadSoundStatus={"ErrorType":"UnknownAudioTypeFormat","ErrorLog":["Не верный тип Аудио","Возможно у вас усторевшая версия MSMP Stream","Либо открыт усторевший плейлист, или не устоновлен плагин?..."]}
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

class MainWindow(QtWidgets.QMainWindow, mainUI.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        InstanceSettings=[]
        if sys.platform == "win32":
            InstanceSettings.append("--audio-visual="+"visual")
            InstanceSettings.append("--effect-list=spectrum")
            InstanceSettings.append("--effect-fft-window=none")
        RPC = Presence("811577404279619634")
        RPC.connect()
        self.MSMPboxPlayer=MSMPboxPlayer(ServerPlaer=True,InstanceSettings=InstanceSettings,discord_rpc=RPC,logger=logger)
        self.config=loadConfig()
        
        #self.initUI()
        with open(r"../Понравившиеся.plmsmpsbox", 'r') as fr:
                    playlistFile = json.load(fr)
                    self.MSMPboxPlayer.playlist=playlistFile["playlist"]
        #self.MSMPboxPlayer.playlist=[{"ID": "YouTube", "url": "Q52GzsGmRuk", "name": "Hold", "uploader": "Home", "duration": 210, "Publis": False},
        #                             {"ID": "YouTube", "url": "5py6E6yo7wk", "name": "Siberian (BGM)", "uploader": "LEMMiNO", "duration": 210, "Publis": False},
        #                             {"ID": "YouTube", "url": "XeiR1w236yo", "name": "Sunshower", "uploader": "Home", "duration": 210, "Publis": False},
        #                             {"ID": "YouTube", "url": "d6SQb0WTrlA", "name": "Glimmer", "uploader": "AGST", "duration": 210, "Publis": False}]

        #mainUI.QtWidgets.QSpinBox=MySpinBox
        
        self.setupUi(self)
        self.PlayListAddMenu = QtWidgets.QMenu()
        self.PlayListAddMenu.triggered.connect(lambda x: print(x.data))

        self.RemoveTreakMenu = QtWidgets.QMenu()
        self.RemoveTreakMenu.triggered.connect(lambda x: print(x.data))
        

        self.AddTreakPlaylist.setMenu(self.PlayListAddMenu)
        self.RemoveTreakPlaylist.setMenu(self.RemoveTreakMenu)
        self.add_menu(["Remove Treak"+"#RT","Clear Playlist"+"#CPL"], self.RemoveTreakMenu)
        self.add_menu(['add Local File'+"#addLF",{'add AudioStream'+"#addAS": ['YouTube Video'+"#addAS-YV", 'soundcloud Treak'+"#addAS-ST"]}], self.PlayListAddMenu)
        
        if sys.platform.startswith("linux"):
            pass# for Linux using the X Server
            #self.MSMPboxPlayer.NewPlaerVLC.set_xwindow(self.Visualframe.winId())
        elif sys.platform == "win32":  # for Windows
            self.MSMPboxPlayer.NewPlaerVLC.set_hwnd(self.Visualframe.winId())
        #elif sys.platform == "darwin":  # for MacOS
        #    self.MSMPboxPlayer.NewPlaerVLC.set_nsobject(self.Visualframe.winId())

        self.PlayListBox = QtGui.QStandardItemModel()
        self.PlaylistView.setModel(self.PlayListBox)
        self.PlaylistView.setSpacing(0)
        
        
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
            
        self.PlaylistView.setIconSize(QtCore.QSize(25,25))

        
        self.add_functions()

        self.ProgressUpdate=False
        self.LestNum=-1
        self.show()
        for i, ItemP in enumerate(self.MSMPboxPlayer.playlist):
            uploader=ItemP.get("uploader")
            if(uploader==None):
                uploader=" "
            try:it = QtGui.QStandardItem(ItemP["name"]+"\n"+uploader)
            except KeyError:it = QtGui.QStandardItem(ItemP["Name"]+"\n"+uploader)
            self.PlayListBox.appendRow(it)
            it.setData(QtGui.QIcon("img/AlbumImgMini.png"),QtCore.Qt.DecorationRole)
        #it.setBackground(QtGui.QColor('red'))
        
        self.isPlayListSelectionChanged=False
        
        self.VolumeSlider.setValue(self.MSMPboxPlayer.NewPlaerVLC.audio_get_volume())
        
        self.bufferNewPlaerVLCposition=0
        self.p = ProcessRunnable(target=self.updateBgGui, args=())
        self.p.start()
        
    
    def updateBgGui(self):
        while True:
            #print("fox")
            try:
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
                   if(str(self.MSMPboxPlayer.get_state())=="State.Ended"):
                       self.UpdateInfoTreakPL(self.MSMPboxPlayer.nextTreak())
                   
            #except AttributeError:
            #    pass
            except:
                print('\n',traceback.format_exc())
        
    def changeProgressBarTreakSlider(self, value):
            #self.MSMPboxPlayer.setpos(int(value))
            self.MSMPboxPlayer.NewPlaerVLC.set_position(int(value)/1000)
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
        
    def UpdateInfoTreakPL(self,fun):
         
        self.TreakName.setText(self.MSMPboxPlayer.PlayNowMusicDataBox["titleTrekPlayNow"])
        self.AuthorName.setText(self.MSMPboxPlayer.PlayNowMusicDataBox["artistTrekPlayNow"])
        self.AlbumName.setText(self.MSMPboxPlayer.PlayNowMusicDataBox["albumTrekPlayNow"])
        if not(self.LestNum==-1):
             self.PlayListBox.itemFromIndex(self.PlayListBox.index(self.LestNum,0)).setBackground(QtGui.QColor('#1A1A1A'))
        self.LestNum=self.MSMPboxPlayer.Num
        self.PlayListBox.itemFromIndex(self.PlayListBox.index(self.LestNum,0)).setBackground(QtGui.QColor('red'))
         
        if self.MSMPboxPlayer.CoverUrlPlayNow:
            try:
                #data = urllib.request.urlopen(self.MSMPboxPlayer.CoverUrlPlayNow).read()
                r = requests.get(self.MSMPboxPlayer.CoverUrlPlayNow, stream=True)
                r.raw.decode_content = True # Content-Encoding
                ImgAlbum = Image.open(r.raw)
                
                ImgAlbum=crop_center(ImgAlbum,ImgAlbum.size[1],ImgAlbum.size[1])
                ImgAlbum.thumbnail((140,140))
                ImgAlbum =ImageQt(ImgAlbum)
                
                print("Update icon")
                #im = Image.open(io.BytesIO(data))
                #im.thumbnail((140,140))
                
                #pixmap.loadFromData(com)
                #self.AlbumImg.setPixmap(pixmap)
                pixmap=QtGui.QPixmap.fromImage(ImgAlbum)
                self.AlbumImg.setPixmap(pixmap)
                
                self.PlayListBox.itemFromIndex(self.PlayListBox.index(self.LestNum,0)).setData(QtGui.QIcon(pixmap),QtCore.Qt.DecorationRole)
                #print(self.MSMPboxPlayer.CoverUrlPlayNow)
            except:
                print('\n',traceback.format_exc())
                self.AlbumImg.setPixmap(QtGui.QPixmap("img/X9at37tsrY8AlbumImg.png"))
        else:
            self.AlbumImg.setPixmap(QtGui.QPixmap("img/X9at37tsrY8AlbumImg.png"))
        self.DataPath.setText(self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["ID"]+"/"+self.MSMPboxPlayer.playlist[self.MSMPboxPlayer.Num]["url"])
        
        #self.ProgressBarTreakSlider.setMaximum(self.MSMPboxPlayer.durationTreak)
    def add_functions(self):
        self.PlayButton.clicked.connect(lambda: self.UpdateInfoTreakPL(self.MSMPboxPlayer.play()))
        self.StopButton.clicked.connect(lambda: self.UpdateInfoTreakPL(self.MSMPboxPlayer.stop()))
        self.PauseButton.clicked.connect(lambda: self.MSMPboxPlayer.pause())

        #self.AddTreakPlaylist.connect(self.contextMenuPlayList)
        
        self.PreviousTreakButton.clicked.connect(lambda: self.UpdateInfoTreakPL(self.MSMPboxPlayer.previousTreak()))   
        self.NextTreakButton.clicked.connect(lambda: self.UpdateInfoTreakPL(self.MSMPboxPlayer.nextTreak()))
        
        self.ProgressBarTreakSlider.valueChanged[int].connect(self.changeProgressBarTreakSlider)

        self.VolumeSlider.valueChanged[int].connect(self.changeVolumeSlider)

        self.PlaylistView.selectionModel().selectionChanged.connect(
            self.PlayListSelectionChanged
        )
        self.PlaylistView.clicked.connect(
            lambda: self.PlayListClickPL()
        )
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

        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.MSMPboxPlayer.stop()
            event.accept()
            self.close()
        else:
            event.ignore()

    def add_menu(self, data, menu_obj):
        if isinstance(data, dict):
            for k, v in data.items():
                sub_menu = QtWidgets.QMenu(k, menu_obj)
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
    ex = MainWindow()
    sys.exit(app.exec_())
