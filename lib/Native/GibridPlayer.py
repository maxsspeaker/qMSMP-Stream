import vlc

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
