import sys
import requests
import yt_dlp
import os


class MyYTLogger:
    def __init__(self):
         self.firk=True
         pass

        
    def debug(self, msg):
         pass

    def info(self, msg):  
        pass

    def warning(self, msg):
         pass

    def error(self, msg):
         pass
first=True

def my_hook(d):
        global first
        if d['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(d['filename']))
            print("Done downloading {}".format(file_tuple[1]))
        if d['status'] == 'downloading':
            p = d['_percent_str'] #_total_bytes_str #_speed_str #_total_bytes_str
            p = p.replace('%','')
            #self.progress.setValue(float(p))
            if(first):
                 first=False
                 for key in d:
                      print(str(key)+": "+str(d[key]))
            print("firk"+p)
            print("firk"+p)
            #print("firk"+p)
            #print(d['filename'], d['_percent_str'], d['_eta_str'])

ydl_opts = {
     'forceurl':True,
     'ignoreerrors': True,
#                         'logger':MyYTLogger(FullInfo,logger=self.logger),
     'progress_hooks': [my_hook],
     'logger':MyYTLogger(),
     'ignore-config':True,
     'extract_flat':True,
     #'extractaudio': True,
     'format':"bestaudio[ext=m4a]/best[ext=m4a]"
#     'outtmpl':
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl: #
     #r = ydl.extract_info("https://www.youtube.com/watch?v=OoDQX7_qbcQ", download=False)
     ydl.download(["https://www.youtube.com/watch?v=CNy0rZyr7GE"])
     #if r != None:
 #         link = r['formats'][-1]['url']
                            
##file_name = "download.data"
##with open(file_name, "wb") as f:
##    print("Downloading %s" % file_name)
##    response = requests.get(link, stream=True)
##    total_length = response.headers.get('content-length')
##    print(total_length)
##
##    if total_length is None: # no content length header
##        f.write(response.content)
##    else:
##        dl = 0
##        total_length = int(total_length)
##        for data in response.iter_content(chunk_size=4096):
##            dl += len(data)
##            f.write(data)
##            done = int(50 * dl / total_length)
##            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
##            sys.stdout.flush()
