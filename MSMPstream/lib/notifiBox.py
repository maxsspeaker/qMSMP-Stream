import sys

if(sys.platform=="linux"):
     try:
          from notifypy import Notify
     except:
          pass
 
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
