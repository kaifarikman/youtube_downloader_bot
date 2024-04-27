from pytube import YouTube


def get_audio(video_link):
    path = "../bot/audio/"
    try:
        video = YouTube(video_link)
        audio = video.streams.filter(only_audio=True, file_extension='mp4').first()
        audio.download(path)
        print('Downloaded audio')
        return True

    except Exception as e:
        print('No downloaded')
        return False

