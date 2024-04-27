from pathlib import Path


def get_filename():
    pathlist = Path("../bot/audio/").glob('*.mp4')
    for path in pathlist:
        return str(path)
