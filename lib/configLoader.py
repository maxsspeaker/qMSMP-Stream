import json, yaml,os
from appdirs import user_config_dir
 
def loadLocal(NameLocal):
     with open(NameLocal,"r", encoding='utf-8') as f:
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
          with open(configFile,"r", encoding='utf-8') as f:
               config = yaml.safe_load(f)
          return config,configDir,MyPlaylistsPath
     else:
          cacheFolder = "cache"
          download_MusicFolder = "download_Music"
          cacheFolderPath = os.path.join(configDir,cacheFolder)
          download_MusicFolderPath = os.path.join(configDir,download_MusicFolder)
          config={
               'MSMP Stream': 
                    {'audioVisual': 'visual',
                     'cache': True,
                     'cacheimgpachfolder': cacheFolderPath+"/",
                     'downloadMusicFolder': download_MusicFolderPath+"/",
                     'localizationBox': 'lengboxs/ru.loclb',
                     'NowPlayningPlayBoxActive': False,
                     'VideoMode': False,
                     'latest_playlist':"",
                     'CDcaseImgRPC': False,
                     'force-ipv4':False
                     },
               'MSMP Stream Equalizer':
                    {'EqualizerOnOff': False,
                     'EqualizerSettings': [7.5, 7.5, 3.9, 0.1, 0, 0, 0, 0, 1.6, 1.6, 7.0]
                     },
               'MSMP Stream RPC':{
                    'Discord_rpc':True,
                    'Discord_Buttons':True,
                    "last-fmAllowed":False,
                    },
               }
          os.makedirs(os.path.dirname(configFile), exist_ok=True)
          os.makedirs(MyPlaylistsPath, exist_ok=True)
          os.makedirs(download_MusicFolderPath, exist_ok=True)
          os.makedirs(cacheFolderPath, exist_ok=True)
          
          print("firk")
          with open(configFile,"w", encoding='utf-8') as f:
               yaml.dump(config,f)
          return config,configDir,MyPlaylistsPath
