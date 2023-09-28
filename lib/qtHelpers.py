from PyQt6.QtWidgets import QSlider, QStyle
from PyQt6 import QtWidgets, QtCore, QtGui

import stagger
import io
from PIL import Image

def hhmmss(second):
    # s = 1000
    # m = 60000
    # h = 360000
    s = second

    
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return ("%d:%02d:%02d" % (h, m, s)) if h else ("%d:%02d" % (m, s))

def GetImgFile(PachFile):
    try:
         mp3 = stagger.read_tag(PachFile)
         by_data = mp3[stagger.id3.APIC][0].data
         im = io.BytesIO(by_data)
         return im
    except:
          print(traceback.format_exc())
          return None

class Slider(QSlider):
     def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            new_value = self.minimum() + ((self.maximum() - self.minimum()) * (event.pos().x()-6)) / self.width()
            self.setValue(int(new_value))
        super().mousePressEvent(event)


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    #Функция для обрезки изображения по центру.
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))



