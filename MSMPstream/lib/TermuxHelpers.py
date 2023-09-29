 

def setWindowFullScreen(self,app):
    screen = app.primaryScreen()
    size = screen.size()
    self.resize(size.width(), size.height())
    
