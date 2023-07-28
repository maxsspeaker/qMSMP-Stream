import os
import json

def subfoldersLoader(MusicFolderPach,subfolders=True):
        MusicFolderdir=os.listdir(MusicFolderPach)
        allFiles=[]
        i=0
        while not len(MusicFolderdir)==i:
            if(os.path.exists(MusicFolderPach+"/"+MusicFolderdir[i])):
                if(os.path.isfile(MusicFolderPach+"/"+MusicFolderdir[i])):
                    print(MusicFolderPach+"/"+MusicFolderdir[i])
                    allFiles.append(MusicFolderPach+"/"+MusicFolderdir[i])
                else:
                    if(subfolders):
                        allFiles=allFiles+subfoldersLoader(MusicFolderPach+"/"+MusicFolderdir[i])
            i=i+1
        
        return allFiles
     


AllMusic=subfoldersLoader(r"A:\Music",subfolders=True)
PlayList=[]

for AudioPatch in AllMusic:
     foxName=os.path.basename(AudioPatch).split(".")
     if(foxName[len(foxName)-1]=="mp3"):
          PlayList.append({"ID": "MyFiles", "url": AudioPatch, "name": os.path.basename(AudioPatch.replace(".mp3","")), "duration": 0, "Publis": False})

plToSave={"playlist":PlayList,"iconPlayList": None, "ContinuePlayData": None,"VerisonCore":2}

with open("MyFiles.plmsmpsbox","w") as file:
     json.dump(plToSave,file)
