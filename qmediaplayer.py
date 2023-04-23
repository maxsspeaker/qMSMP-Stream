from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import time
import sys

class VideoPlayer:

    def __init__(self):
        self.video = QVideoWidget()
        self.video.resize(300, 300)
        self.video.move(0, 0)
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video)
        self.player.setMedia(QMediaContent(QUrl("https://pybms.tk/Server/YouTubefast-music?dl=1&cast=140&url=https://www.youtube.com/watch?v=3yzKpWj3Lu0")))
        

        
    def callback(self):
        #self.player.setPosition(0) # to start at the beginning of the video every time
        self.player.setPosition(72855)
        self.video.show()
        self.player.play()
        print(self.player.duration())

    def callback2(self):
        print("2")


        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = VideoPlayer()
    b = QPushButton('start')
    s = QPushButton('pos')
    b.clicked.connect(v.callback)
    s.clicked.connect(v.callback2)
    b.show()
    s.show()
    sys.exit(app.exec_()) 



#        file_path = 'https://pybms.tk/Server/YouTubefast-music?dl=1&cast=140&url=https://www.youtube.com/watch?v=3yzKpWj3Lu0'

##from PyQt5.QtWidgets import *
##from PyQt5.QtMultimedia import *
##from PyQt5.QtCore import *
##from PyQt5.QtGui import *
##
##import numpy as np
##import sys
##
##
##from pydub.audio_segment import AudioSegment
##def set_sample_width(self, sample_width):
##    # Get the number of bytes per sample for the new sample width
##    new_bytes_per_sample = int(sample_width / 8)
##
##    # Get the number of bytes per sample for the existing sample width
##    old_bytes_per_sample = int(self.sample_width / 8)
##
##    # Don't do anything if the sample width is already correct
##    if new_bytes_per_sample == old_bytes_per_sample:
##        return self
##
##    # Calculate the new data length
##    if new_bytes_per_sample == 0:
##        new_length = 0
##    else:
##        new_length = int(len(self._data) * old_bytes_per_sample / new_bytes_per_sample)
##
##    # Convert the data to the new sample width
##    new_data = bytearray(new_length)
##    for i in range(new_length):
##        start = i * new_bytes_per_sample
##        end = (i + 1) * new_bytes_per_sample
##        new_data[i] = int.from_bytes(self._data[start:end], byteorder='little', signed=True)
##    self._data = bytes(new_data)
##    self.sample_width = sample_width
##    return self
##
##AudioSegment.set_sample_width=set_sample_width
##
##class Visualizer(QWidget):
##    def __init__(self):
##        QWidget.__init__(self)
##
##        # Set up the visualizer widget
##        self.setMinimumSize(200, 200)
##        self.setAutoFillBackground(True)
##        self.palette = self.palette()
##        self.palette.setColor(QPalette.Window, QColor(50, 50, 50))
##        self.setPalette(self.palette)
##
##        # Create a QMediaPlayer object
##        self.media_player = QMediaPlayer()
##
##        # Create a QAudioProbe object to get audio visualization data
##        self.audio_probe = QAudioProbe()
##        self.audio_probe.setSource(self.media_player)
##
##        # Connect the audio probe to a callback function
##        self.audio_probe.audioBufferProbed.connect(self.on_audio_buffer_probed)
##
##        # Load the audio stream from a URL
##        url = QUrl("https://pybms.tk/Server/YouTubefast-music?dl=1&cast=140&url=https://www.youtube.com/watch?v=3yzKpWj3Lu0")
##        content = QMediaContent(url)
##        self.media_player.setMedia(content)
##
##        # Begin playback
##        self.media_player.play()
##
##    def paintEvent(self, event):
##        # Draw the visualizer
##        painter = QPainter(self)
##        pen = QPen(QColor(255, 255, 255))
##        painter.setPen(pen)
##        brush = QBrush(QColor(255, 255, 255))
##        painter.setBrush(brush)
##        peak = np.amax(self.levels)
##        height = self.height()
##        width = self.width()
##        bar_width = width / len(self.levels)
##        for i, level in enumerate(self.levels):
##            value = level / peak if peak > 0 else 0
##            x = int(i * bar_width)
##            y = int((1 - float(value)) * height)
##            painter.drawRect(x, y, int(bar_width), int(height - y))
##
##    def on_audio_buffer_probed(self, audio_buffer):
##        # Update the visualizer with the new audio data
##        num_samples = audio_buffer.frameCount()
##        num_channels = audio_buffer.format().channelCount()
##
##        # Create a numpy array with the correct length for each channel
##        audio = np.zeros((num_channels, num_samples), dtype=np.int16)
##
##        # Convert the byte array to an AudioSegment object
##        data = audio_buffer.constData().asstring(audio_buffer.byteCount())
##        segment = AudioSegment(data, sample_width=audio_buffer.format().sampleSize(), channels=num_channels, frame_rate=audio_buffer.format().sampleRate())
##
##        # Convert the audio to 16-bit
##        segment = segment.set_sample_width(sample_width=2)
##
##        # Calculate the peak and normalize the levels
##        levels = np.array(segment.get_array_of_samples()).astype(np.float16)
##        levels /= np.iinfo(np.int16).max
##        peak = 0
##        if levels.size > 0:
##            peak = np.abs(levels).max()
##            levels = np.interp(np.linspace(0, 50, 100), np.arange(len(levels)), levels)
##
##        # Update the levels and redraw the visualizer if we have data
##        if levels.size > 0:
##            self.levels = levels
##            self.update()
##
##
##if __name__ == '__main__':
##    app = QApplication([])
##    visualizer = Visualizer()
##    visualizer.show()
##    sys.exit(app.exec_())
