import sys
import yt_dlp
import json

print(sys.argv)

ydl_opts = {
     'ignoreerrors': True,
     'ignore-config':True,
     'extract_flat':True
}

if(sys.argv[3]=="--cookies"):
     ydl_opts['cookiefile']=sys.argv[4]

#if(cookies):
##     #ydl_opts['cookiefile']=
##

#if(cookies):
     #ydl_opts['cookiefile']=
#if(cookies):
#            print('потключены кукии файл, теперь ты можешь экпортировать и плейлисты "Джем"')
playlist=[]
print("Loading...")

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
     playlist_dict = ydl.extract_info(sys.argv[1], download=False)
     for r in playlist_dict['entries']:
                    if not r:
                        print('ERROR: Unable to get info. Continuing...')
                        continue
                    if("[Deleted video]"==str(r['title'])) or ("[Private video]"==str(r['title'])):
                         print('ERROR: Unable to get info. Continuing...')
                         continue
                    print("добавлен: "+str(r['title']))
                    try:
                         playlist.append({"ID":"YouTube","url":r["id"],"name":r['title'],"uploader":r['uploader'],"duration":int(r['duration']),"Publis":False})
                    except KeyError:
                         try:
                              playlist.append({"ID":"YouTube","url":r["id"],"name":r['title'],"uploader":r["channel"],"duration":int(r['duration']),"Publis":False})
                         except KeyError:
                              playlist.append({"ID":"YouTube","url":r["id"],"name":r['title'],"uploader":'???',"duration":int(r['duration']),"Publis":False})

                    #for property in ['thumbnail', 'id', 'title', 'description', 'duration']:
                        #print(property, '--', video.get(property))
        
        
        #saveplaylist(fd.asksaveasfilename(filetypes=(("MSMP Stream PlayList files", "*.plmsmpsbox"),)),playlist)
print("Плейлист Успешно экспортирован!")

playlistSave={"playlist":playlist}
with open(sys.argv[2], 'w') as fw:
     json.dump(playlistSave,fw, indent=2)
     fw.close()
     
with open("DebugPlaylist.json", 'w') as fw:
     json.dump(playlist_dict,fw, indent=2)
     fw.close()

