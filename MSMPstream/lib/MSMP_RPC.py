import os,time
import pylast,pypresence
from PIL import Image
from MSMPstream.lib.ProcessRunnable import ProcessRunnable
 
class MSMP_RPC():
     def __init__(self,RPC,msmp_streamIconYouTube=None,
                  msmp_streamIconMain=None,
                  msmp_streamIconSoundCloud=None,
                  msmp_streamIcon="qmsmpstream",
                  version="None",LastFm=False,
                  logger=None,DirConfig=None,lengbox=None,ImgApiHostTOKEN=None,ImgApiHost=None,RPCbuttons=False):
          
          self.RPC=RPC
          self.buttons=None
          if (lengbox==None):
               lengbox={"MSMP Stream":{"RPCmsmpOf":"of"}}
          self.lengbox=lengbox
          if not(RPC==None):
               try:
                    self.RPC=pypresence.Presence("811577404279619634")
                    self.RPC.connect()
               except pypresence.exceptions.DiscordNotFound:
                  self.RPC=None
               except ConnectionRefusedError:
                  self.RPC=None
               except pypresence.exceptions.DiscordError:
                  self.RPC=None
          self.RpcDiscordQueue=None
          self.RPCupdateThread_stop=None
          
          self.ImgApiHostTOKEN=ImgApiHostTOKEN
          self.ImgApiHost=ImgApiHost

          if(self.ImgApiHostTOKEN):
               self.AlbumCaseImg = Image.open(r"img/LocalAlbumTreakBg.png").convert("RGB")
               self.AlbumCaseImgLi = Image.open(r"img/LocalAlbumTreakLi.png").convert("RGBA")
          
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
                self.RPCupdate(
              **{
                  'details': PlayNowMusicDataBox["titleTrekPlayNow"],
                  'state': PlayNowMusicDataBox["artistTrekPlayNow"]+self.lenPlayListStatus,
                  'large_text':PlayNowMusicDataBox["albumTrekPlayNow"],
                  'large_image':msmp_streamIcon,
                  'small_image':"pause",
                  'buttons':self.buttons,
                  #'large_text':self.PlayNowMusicDataBox["albumTrekPlayNow"],
                  'small_text':self.version
                  }
              )
             else:
                  self.RPCupdate(
              **{
                  'details': PlayNowMusicDataBox["titleTrekPlayNow"],
                  'state': PlayNowMusicDataBox["artistTrekPlayNow"]+self.lenPlayListStatus,
                  'large_image':msmp_streamIcon,
                  'small_image':"pause",
                  'buttons':self.buttons,
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
                 self.RPCupdate(
              **{
                  'details': PlayNowMusicDataBox["titleTrekPlayNow"],
                  'state': PlayNowMusicDataBox["artistTrekPlayNow"],
                  'large_text':PlayNowMusicDataBox["albumTrekPlayNow"],
                  'large_image':msmp_streamIcon,
                  'small_image':"play",
                  'buttons':self.buttons,
                  'small_text':self.version,
                }
              )
               else:
                 self.RPCupdate(
              **{
                  'details': PlayNowMusicDataBox["titleTrekPlayNow"],
                  'state': PlayNowMusicDataBox["artistTrekPlayNow"],
                  'large_image':msmp_streamIcon,
                  'small_image':"play",
                  'buttons':self.buttons,
                  'small_text':self.version,
                }  )
      except:printError(traceback.format_exc())
      
     def RPCupdate(self,details=None,state=None,large_text=None,large_image=None,small_image=None,small_text=None,buttons=None,end=None,ThreadQueue=True):
##       if (ThreadQueue):
##            if not(RPCupdateThread_stop==None):self.RPCupdateThread_stop.set()
##            self.RPCupdateThread = ProcessRunnable(target=self.scrobbleLastFM, args=(PlayNowMusicDataBox,))
##            self.RPCupdateThread_stop = self.RPCupdateThread.Event()
##            self.RPCupdateThread.start()
##       else:
        #if not(self.RpcDiscordQueue==None):    
          try:
               self.RPC.update(
                   **{
                      'details': details,
                      'state': state,
                      'large_text':large_text,
                      'large_image':large_image,
                      'small_image':small_image,
                      'small_text':small_text,
                      'buttons':buttons,
                      'end': end#((AudioTime-Audiolength)/1000)-((AudioTime-Audiolength)/1000)-((AudioTime-Audiolength)/1000)
                    }
                   )
          except pypresence.exceptions.InvalidID:
               printError(traceback.format_exc())
               try:
                    self.RPC=pypresence.Presence("811577404279619634")
                    self.RPC.connect()
                    self.RPC.update(
                         **{
                      'details': details,
                      'state': state,
                      'large_text':large_text,
                      'large_image':large_image,
                      'small_image':small_image,
                      'small_text':small_text,
                      'buttons':buttons,
                      'end': end#((AudioTime-Audiolength)/1000)-((AudioTime-Audiolength)/1000)-((AudioTime-Audiolength)/1000)
                    }
                   )
               except pypresence.exceptions.DiscordNotFound:
                    self.RPC=None
               
               
     def updatePlayerNow(self,PlayNowMusicDataBox,durationTreak=None,PlLen=None,Num=None,NowPlayIconRPC=None,ImgUrl="",buttons=None,timebox=None,firstPlay=False):

          if not(durationTreak==None):
               self.durationTreak=durationTreak
          self.buttons=buttons
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
               self.RPCupdate(
                   **{
                      'details': PlayNowMusicDataBox["titleTrekPlayNow"],
                      'state': PlayNowMusicDataBox["artistTrekPlayNow"]+self.lenPlayListStatus,
                      'large_text':PlayNowMusicDataBox["albumTrekPlayNow"],
                      'large_image':msmp_streamIcon,
                      'small_image':"play",
                      #'large_text':self.PlayNowMusicDataBox["albumTrekPlayNow"],
                      'small_text':self.version,
                      'buttons':self.buttons,
                      'end': time.time()+(self.durationTreak-self.timebox)#((AudioTime-Audiolength)/1000)-((AudioTime-Audiolength)/1000)-((AudioTime-Audiolength)/1000)
                    }
                   )
            else:
                self.RPCupdate(
                   **{
                      'details': PlayNowMusicDataBox["titleTrekPlayNow"],
                      'state': PlayNowMusicDataBox["artistTrekPlayNow"]+self.lenPlayListStatus,
                      'large_image':msmp_streamIcon,
                      'small_image':"play",
                      #'large_text':self.PlayNowMusicDataBox["albumTrekPlayNow"],
                      'small_text':self.version,
                      'buttons':self.buttons,
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
                 if not(self.RPC==None):self.RPCupdate(
                     **{
                         'large_image':"missing_texture",
                    })
          else:
                 if not(self.RPC==None):self.RPCupdate(
                     **{
                         'large_image':self.msmp_streamIcon,
                    })
     def UploadNewImg(self,PillowImg,ImgNameTreak):
        if not(self.ImgApiHost==None):
          MainImg=self.AlbumCaseImg.copy()

          MainImg.paste(PillowImg.resize((287,287)), (157, 109))

          MainImg.paste(self.AlbumCaseImgLi, (0, 0),self.AlbumCaseImgLi)
          
          byte_io = io.BytesIO()
          MainImg.save(byte_io, 'png')
          byte_io.seek(0)
          cookies = {"TOKEN":self.ImgApiHostTOKEN}

          r = requests.post(self.ImgApiHost+ImgNameTreak, cookies=cookies, files={'upload_file': ('1.png',byte_io)})

          return self.ImgApiHost+ImgNameTreak
        return None
