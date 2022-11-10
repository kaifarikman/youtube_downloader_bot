from pytube import YouTube
import os


def yt_downloader_mp3_format(url, name_of_playlist):
    with open("musicc\\names_of_playlists.txt", "r+", encoding="utf-8") as file:
        lst = [line.strip().split(" - ")[0] for line in file.readlines()]
        if name_of_playlist in lst:
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path=".")
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            if not os.path.isdir(f"musicc\\{name_of_playlist}"):
                os.mkdir(f"musicc\\{name_of_playlist}")

            s = ""
            for i in new_file.split("\\"):
                if i != ".":
                    s += f"{i}\\"
                else:
                    s += f'musicc\\{name_of_playlist}\\'
            last_file = s[:len(s) - 1]
            name_of_song = last_file.split("\\")[-1]
            with open(f"musicc\\{name_of_playlist}\\{name_of_playlist}.txt", "a", encoding="utf-8") as file:
                try:
                    os.rename(out_file, last_file)
                    try:
                        lines = []
                        for i in file.readlines():
                            lines.append(i.strip())
                        if name_of_song not in lines:
                            file.write(f"{name_of_song}\n")
                            return "added"
                    except:
                        file.write(f"{name_of_song}\n")
                        return "added"
                except FileExistsError:
                    os.remove(out_file)
                    return "this is here"

        else:
            return "botva"