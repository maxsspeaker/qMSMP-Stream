import sys,socket, time, os, traceback,random,json


class EventHandler():
     #FoxMSMPstreamProtocol
     def __init__(self,CustomPort=59715,RunCommands=[],downloaderNodeF=None):
          self.HOST = "127.0.0.1"
          if not(downloaderNodeF==None):
           try:
               if(RunCommands[1]=="--downloader") or (RunCommands[1]=="-d"):
                    downloaderNode=True
               else:
                    downloaderNode=False
           except IndexError:
               downloaderNode=False
          else:
               downloaderNode=downloaderNodeF
          #downloaderNode=True
          if(downloaderNode):
               print("downloaderNode")
               self.PORT = 59716
          else:
               self.PORT = 59715
          self.downloaderNode=downloaderNode
          self.FirstApp=self.RunCommandBox(RunCommands)
          self.ServerStarted=True
          #return downloaderNode

     def RunCommandBox(self,RunCommands=[]):
          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
               try:
                    s.connect((self.HOST, self.PORT))
                    s.sendall(json.dumps(RunCommands).encode()) 
                    data = s.recv(1024)
                    print(f"Received {data!r}")
                    return False
               except ConnectionRefusedError:
                    return True
               

     def RunEventServer(self):
          print("Fox Firk")
          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
               s.bind((self.HOST, self.PORT))
               s.listen()
               while self.ServerStarted:
                    print("Fox Firk2")
                    conn, addr = s.accept()
                    while True:
                         data = conn.recv(1024)
                         #
                         if not data:
                              break
                         try:
                            #if not(self.downloaderNode):
                            if(json.loads(data.decode())[1]=="--downloader") or (json.loads(data.decode())[1]=="-d"):
                                   downloaderNode=True
                            if not(downloaderNode==self.downloaderNode):
                                 conn.sendall(data)
                            else:
                              print(json.loads(data.decode()))
                              if(downloaderNode):
                                   Sirdata=json.loads(data.decode())[2]
                                   dataFix=urllib.parse.unquote(json.loads(data.decode())[2])
                              else:
                                   Sirdata=json.loads(data.decode())[1]
                                   dataFix=urllib.parse.unquote(json.loads(data.decode())[1])
                              
                              dataFix2=dataFix.replace("fox-msmp-stream:///?foxdata=","")
                              
                              print(dataFix2)
                              print("Fox1")
                              try:
                                   ProtocolData=json.loads(dataFix2.replace("'",'"'))
                                   print(ProtocolData)
                              except json.decoder.JSONDecodeError:
                                   ProtocolData=None
                              print("Fox2")
                              if(ProtocolData):
                                   print("firk")
                                   conn.sendall(data)
                                   print("firk22")
                                   if not(self.downloaderNode):
                                     if(ProtocolData.get("ytvideo")):
                                        print("firk222")
                                        self.MainWindow.TrekBoxUi.NoPlayListMode=True
                                        print("firk1")
                                        self.MainWindow.TrekBoxUi.UrlText.setText(ProtocolData.get("ytvideo"))
                                        print("firk2")
                                        self.MainWindow.TrekBoxUi.FindTrek(ProtocolData.get("ytvideo"))
                                        print("firk3")
                                        #self.MainWindow.TrekBoxUi.show()
                                        if(self.MainWindow.TrekBoxUi.TypeTreak):
                                             self.MainWindow.TrekBoxUi.AddTrek()
                                   else:
                                        try:
                                             #Params=json.loads(ProtocolData)
                                             print(ProtocolData)
                                             if(ProtocolData.get("YtUrl")):
                                                  print(ProtocolData["filePatch"])
                                                  ex.DownloadYtFox(ProtocolData["YtUrl"],ProtocolData["filePatch"])
                                        except:
                                             print(traceback.format_exc())
                                        #if(ProtocolData.get("dataFox")):
                                        #     print(ProtocolData.get("dataFox"))

                              else:
                                   if (str(os.path.splitext(Sirdata)[1]).endswith(".plmsmpsbox")):
                                        conn.sendall(data)
                                        self.MainWindow.OpenPLmsmp(Sirdata)
                                   else:
                                        conn.sendall(data)
                              print(f"Received {dataFix}")          
                            #else:
                            #     pass
                              
                              
##                              fixJson={}
##                              for key, value  in json.loads(data.decode()):
##                                   fixJson[urllib.parse.unquote(key)]=urllib.parse.unquote(value)
##                              print(fixJson)
                              
                         except:
                              print(traceback.format_exc())
                              conn.sendall(data)
                    conn.close() 

