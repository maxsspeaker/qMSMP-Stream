import vlc

def audio_level_callback(event, data):
    if event.type == vlc.EventType.MediaPlayerAudioVolume:
        volume = data.volume
        print(f"Volume level: {volume}")

# Создание экземпляра плеера VLC
player = vlc.MediaPlayer("Knife Party - Fire Hive.mp3")

# Регистрация обратного вызова для получения уровней звука
player.event_manager().event_attach(vlc.EventType.MediaPlayerAudioVolume, audio_level_callback)

# Воспроизведение медиафайла
player.play()

# Ожидание окончания воспроизведения
while True:
    pass

# Остановка плеера
player.stop()
