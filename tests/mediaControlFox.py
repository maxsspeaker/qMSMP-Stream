from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QCoreApplication, pyqtSlot
from PyQt6.QtDBus import QDBusConnection, QDBusInterface

class MediaControlApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        QCoreApplication.setApplicationName("MediaControlApp")

        self.connection = QDBusConnection.sessionBus()
        self.player_name = "org.mpris.MediaPlayer2.vlc"  # Example: VLC media player
        self.player_interface = QDBusInterface(self.player_name, "/org/mpris/MediaPlayer2",
                                               "org.mpris.MediaPlayer2.Player", self.connection)

        self.connection.connect(self.player_name, "/org/mpris/MediaPlayer2",
                                "org.freedesktop.DBus.Properties", "PropertiesChanged",
                                self.media_status_changed_handler)

    @pyqtSlot(str, dict, list)
    def media_status_changed_handler(self, interface_name, changed_properties, invalidated_properties):
        print("Media status changed:", interface_name, changed_properties)

def main():
    app = MediaControlApp([])
    app.exec()

if __name__ == "__main__":
    main()
