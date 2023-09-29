import os,time,sys,traceback,json

from yandex_music import Client as YandexMusicClient
from vkaudiotoken import supported_clients

import re
import stagger
import requests
import urllib

import yt_dlp as youtube_dl

from eyed3 import id3
from eyed3 import load
from MSMPstream.lib.Native.GibridPlayer import GibridPlayer
#from threading import Thread

version=0.1


class YtLogger:
    def __init__(self,FullInfo):
        self.FullInfo=FullInfo
        
    def debug(self, msg):
        if msg.startswith('[debug] '):
            print(msg) 
        else:
            print(msg)

    def info(self, msg):  
        if(self.FullInfo):print(msg)

    def warning(self, msg):
        print(msg)
        
    def error(self, msg):
        print(msg)



 
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
                  logger=None,PlayInThread=False,TOKENvkMusic=None,TOKENYandexMusicClient="",CDcase=True,forceIpv4=False,MyYTLogger=None):
          global version
          print("Starting Core MSMP")
          self.logger=logger
          self.ydl_opts = {
                         'forceurl':True,
                         'ignoreerrors': True,
                         'ignore-config':True,
                         'extract_flat':True
                         }
          if not(MyYTLogger==None):
              self.ydl_opts['logger']=MyYTLogger(FullInfo,logger=self.logger),
          else:
              self.ydl_opts['logger']=YtLogger(FullInfo)
              
          if(forceIpv4):
               self.ydl_opts["force-ipv4"]=True
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
          if(versionCs==None):self.version="0.7"
          else:
               self.version=versionCs
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
          self.CDcase=CDcase

          if not(TOKENYandexMusicClient==None):
               self.YandexMusicClient = YandexMusicClient(TOKENYandexMusicClient).init()
          else:
               self.YandexMusicClient=None

          if not(TOKENvkMusic==None):
               self.vkMusicSess = requests.session()
               self.TOKENvkMusic=TOKENvkMusic
               Vkuser_agent = supported_clients.KATE.user_agent
               self.vkMusicSess.headers.update({'User-Agent': Vkuser_agent})
          else:
               self.vkMusicSess=None

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
          self.VersionContinuePlay="v0.1.3-beta"
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
                        if(self.CDcase):
                             self.msmp_streamIconYouTube='https://pybms.tk/Server/DiscordRPC/imgRPC/cdCase?type=Yt&img=https://img.youtube.com/vi/'+self.playlist[Num]["url"]+'/hqdefault.jpg'
                        else:
                             self.msmp_streamIconYouTube='https://pybms.tk/Server/DiscordRPC/imgRPC?type=Yt&img=https://img.youtube.com/vi/'+self.playlist[Num]["url"]+'/hqdefault.jpg'
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
                            
                            self.PlayNowMusicDataBox["like_count"]=r.get('like_count')
                            if(r.get('like_count')==None):
                                 self.PlayNowMusicDataBox["like_count"]=-1
                            self.PlayNowMusicDataBox["view_count"]=r.get("view_count")
                            self.PlayNowMusicDataBox["availability"]=r.get('availability')
                            self.PlayNowMusicDataBox["upload_date"]=r.get('upload_date')
                            try:
                                 self.CoverUrlPlayNow=self.playlist[Num]["cover"]
                                 if(self.CDcase):
                                      self.msmp_streamIconYouTube='https://pybms.tk/Server/DiscordRPC/imgRPC/cdCase?img='+self.playlist[Num]["cover"]
                                 else:
                                      self.msmp_streamIconYouTube='https://pybms.tk/Server/DiscordRPC/imgRPC?img='+self.playlist[Num]["cover"]
                            except:
                                self.CoverUrlPlayNow='https://img.youtube.com/vi/'+self.playlist[Num]["url"]+'/hqdefault.jpg'
                                if(self.CDcase):
                                     self.msmp_streamIconYouTube='https://pybms.tk/Server/DiscordRPC/imgRPC/cdCase?type=Yt&img=https://img.youtube.com/vi/'+self.playlist[Num]["url"]+'/hqdefault.jpg'#https://i.ytimg.com/vi/'+self.playlist[Num]["url"]+'/maxresdefault.jpg'
                                else:
                                     self.msmp_streamIconYouTube='https://pybms.tk/Server/DiscordRPC/imgRPC?type=Yt&img=https://img.youtube.com/vi/'+self.playlist[Num]["url"]+'/hqdefault.jpg'#https://i.ytimg.com/vi/'+self.playlist[Num]["url"]+'/maxresdefault.jpg'
                                
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
                                             #buttons=[{"label":"Открыть в MSMP Stream","url":r'fox-msmp-stream://?foxdata={"ytvideo":"'+self.PlayNowMusicDataBox["TrekPlayNowID"]+'"}'}],
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
                                if(self.CDcase):
                                      self.msmp_streamIconSoundCloud='https://pybms.tk/Server/DiscordRPC/imgRPC/cdCase?img='+img
                                else:
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
                                if(self.CDcase):
                                      self.msmp_streamIconSoundCloud='https://pybms.tk/Server/DiscordRPC/imgRPC/cdCase?img='+img
                                else:
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
               elif("VkMusic"==self.playlist[Num]["ID"]):
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
                          if not(self.vkMusicSess==None):  
                                r = json.loads((self.vkMusicSess.get("https://api.vk.com/method/audio.getById",params=[('access_token', self.TOKENvkMusic),('audios', self.playlist[Num]["vkIDaudio"]),('v', '5.95')])).content.decode('utf-8'))
                                if(r.get('error')):
                                     print("VK MUSIC Error:")
                                     print(r['error']['error_msg'])
                                else:
                                     r = r['response'][0]

                                print("firk")
                                if(self.FullInfo):print(r['duration'])
                                self.PlayNowMusicDataBox["titleTrekPlayNow"]=r['title']
                                self.PlayNowMusicDataBox["artistTrekPlayNow"]=r['artist']
                                self.PlayNowMusicDataBox["albumTrekPlayNow"]=""

                                self.PlayNowMusicDataBox["like_count"]=-1
                                self.PlayNowMusicDataBox["view_count"]=-1
                                self.PlayNowMusicDataBox["availability"]=None
                                self.PlayNowMusicDataBox["upload_date"]=-1

                                
                                castUrl=r['url']
                                #print(castUrl)
            
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
                                
                                img="https://msmp.maxsspeaker.tk/static/img/Missing.png"

                                try:
                                     img=self.playlist[Num]["cover"]
                                except:pass
                                self.CoverUrlPlayNow=img
                                if(self.CDcase):
                                      self.msmp_streamIconSoundCloud='https://pybms.tk/Server/DiscordRPC/imgRPC/cdCase?img='+img
                                else:
                                      self.msmp_streamIconSoundCloud='https://pybms.tk/Server/DiscordRPC/imgRPC?img='+img
                                
                                #viseon="  ["+r['formats'][castViseon]['format_note']+"]"
                                i=0
                                self.PlayNowMusicDataBox["albumImgTrekPlayNowID"]=str(self.playlist[Num]["vkIDaudio"])+"VkMusicAlbumImg"
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
                            self.LoadImg(IDasset=str(self.playlist[Num]["vkIDaudio"])+"VkMusicAlbumImg",IDtype=self.playlist[Num]["ID"],rID=str(self.playlist[Num]["vkIDaudio"]),CoverUrlPlayNow=self.CoverUrlPlayNow)
                            super().play(castUrl)
                            if(self.PlayNowMusicDataBox["artistTrekPlayNow"]==None):
                                  self.PlayNowMusicDataBox["artistTrekPlayNow"]=""
                            if not(self.discord_rpc==None):
                             if(os.path.isfile(self.downloadMusicFolder+(str(self.playlist[Num]["vkIDaudio"])+"vkAudio.mp3"))): 
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
                                  if(self.CDcase):
                                       MSMPNetServerImg='https://pybms.tk/Server/DiscordRPC/imgRPC/cdCase?img='+self.CoverUrlPlayNow
                                  else:
                                       MSMPNetServerImg='https://pybms.tk/Server/DiscordRPC/imgRPC?img='+self.CoverUrlPlayNow
                                  self.discord_rpc.updatePlayerNow(PlayNowMusicDataBox=self.PlayNowMusicDataBox,
                                             durationTreak=self.durationTreak,
                                             PlLen=len(self.playlist),
                                             Num=self.Num,
                                             NowPlayIconRPC="msmp_serverplay",
                                             ImgUrl=MSMPNetServerImg,firstPlay=True)
                   #print(self.CoverUrlPlayNow)
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
