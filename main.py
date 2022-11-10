import config
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
import youtube_downloader


class PlaylistCreator:

    def __init__(self):
        self.token = config.token_school_bot
        self.bot = Bot(self.token)
        self.dp = Dispatcher(bot=self.bot)
        self.create_new_playlist = r"/create\s.+"
        self.listen_playlist = r"/listen\s" + r"\S+"
        self.yt_download = r"https://.+outu.+/.+,\s.+"
        self.yt_link = r"https://.+outu.+/.+"
        self.tracklist = r"/tracklist\s" + r"\S+"

    def do_it(self):
        @self.dp.message_handler(filters.Regexp(self.create_new_playlist))
        async def create_playlist(message: types.Message):
            user_id = message.from_user.id
            pl_name = f"{message.text[8:]} - {user_id}"
            with open("musicc\\names_of_playlists.txt", "r+", encoding="utf-8") as file:
                lst = file.readlines()
                flag = True
                if lst:
                    for i in lst:
                        line = i.strip().split(" - ")[0]
                        if line == pl_name.split(" - ")[0]:
                            await message.answer("Такой плейлист уже существует")
                            flag = False
                            break
                    if flag:
                        file.write(pl_name + "\n")
                        await message.answer("Плейлист создан")
                else:
                    file.write(pl_name + "\n")
                    await message.answer("Плейлист создан")

        @self.dp.message_handler(filters.Regexp(self.yt_download))
        async def yt_download(message: types.Message):
            link_of_yt_song, name_of_playlist = message.text.split(",")
            name_of_playlist = name_of_playlist[1:]
            if youtube_downloader.yt_downloader_mp3_format(link_of_yt_song, name_of_playlist) == "added":
                await message.answer("Успешно добавлено в плейлист")
            elif youtube_downloader.yt_downloader_mp3_format(link_of_yt_song, name_of_playlist) == "this is here":
                await message.answer("Такой трек уже есть в твоём плейлисте так-то")
            elif youtube_downloader.yt_downloader_mp3_format(link_of_yt_song, name_of_playlist) == "botva":
                await message.answer("Сначала создайте такой плейлист")

        @self.dp.message_handler(filters.RegexpCommandsFilter([self.listen_playlist]))
        async def listen_playlist(message: types.Message):
            name_of_playlist = message.text[8:]
            with open("musicc\\names_of_playlists.txt", "r", encoding="utf-8") as file:
                lst = [line.strip().split(" - ")[0] for line in file.readlines()]
                if name_of_playlist in lst:
                    with open(f"musicc\\{name_of_playlist}\\{name_of_playlist}.txt", "r",
                              encoding="utf-8") as listen_file:
                        try:
                            for i in listen_file.readlines()[::-1]:
                                listen_music = i.strip()
                                try:
                                    await message.answer_audio(
                                        open(f"musicc\\{name_of_playlist}\\{listen_music}", "rb"))
                                except:
                                    await message.answer(f"С {listen_music} что-то не то")
                            await message.answer(f"Музыка из плейлиста - <code>{name_of_playlist}</code> была скинута", parse_mode="HTML")
                        except:
                            await message.answer(f"Он пустой")
                else:
                    await message.answer(f"Такого плейлиста не существует, попробуй ввести заново или он пустой")

        @self.dp.message_handler(filters.RegexpCommandsFilter([self.tracklist]))
        async def watch_tracklist(message: types.Message):
            user_id = str(message.from_user.id)
            playlist = message.text[11:]
            with open(f"musicc\\names_of_playlists.txt", "r", encoding="utf-8") as file:
                s = ""
                ids = list()
                for line in file.readlines():
                    name_of_playlist, idd = map(str, line.strip().split(" - "))
                    if user_id == idd:
                        ids.append(name_of_playlist)
                if ids:
                    for i in ids:
                        if i == playlist:
                            try:
                                with open(f"musicc\\{playlist}\\{playlist}.txt", "r", encoding="utf-8") as file2:
                                    for j in file2.readlines():
                                        if j != "\n":
                                            s += f"■<b><u>{j}</u></b>"
                                        else:
                                            break
                            except FileNotFoundError:
                                await message.answer(f"Скорее всего твой плейлист пустой")
                    if s:
                        await message.answer(f"<code>Твой трекслист данного плейлиста:</code>\n"
                                             f"{s}", parse_mode="HTML")
                else:
                    await message.answer(f"Скорее всего твой плейлист пустой😒")

        @self.dp.message_handler(filters.Regexp(self.yt_link))
        async def yt_link(message: types.Message):
            await message.answer(f"Ты забыл написать название плейлиста:((")

        @self.dp.message_handler(commands=["my_playlists"])
        async def my_playlists(message: types.Message):
            user_id = str(message.from_user.id)
            with open(f"musicc\\names_of_playlists.txt", "r", encoding="utf-8") as file:
                s = ""
                count = 0
                for line in file.readlines():
                    name_of_playlist, idd = map(str, line.strip().split(" - "))
                    if user_id == idd:
                        try:
                            with open(f"musicc\\{name_of_playlist}\\{name_of_playlist}.txt", "r",
                                      encoding="utf-8") as file2:
                                lenq = 0
                                for i in file2.readlines():
                                    if i != "\n":
                                        lenq += 1
                            if lenq % 10 == 1:
                                llenq = ""
                            elif lenq % 10 in (2, 3, 4):
                                llenq = "а"
                            else:
                                llenq = "ов"
                            s += f"●<b>{name_of_playlist}</b> - {lenq} трек{llenq}\n"
                            count += 1
                        except FileNotFoundError:
                            s += f"●<b>{name_of_playlist}</b> - 0 треков\n"
                            count += 1
                if s:
                    await message.answer(f"Вы создали <b>{count}</b> плейлиста:\n"
                                         f"{s}", parse_mode="HTML")
                else:
                    await message.answer(f"Пока что вы не создали ни одного плейлиста")

        @self.dp.message_handler(commands=["start"])
        async def start(message: types.Message):
            await message.answer(f"Вас приветствует бот @king_offkaif\n"
                                 f"Бот умеет создавать плейлисты, скачивая треки с ютуба\n"
                                 f"<i>Есть такие фунции , как:</i>\n"
                                 f"<b>/create</b> - создать плейлист\n"
                                 f"<b>/download</b> - скачать трек\n"
                                 f"<b>/listen</b> - прослушать плейлист\n"
                                 f"<b>/my_playlists</b> - узнать свои плейлисты\n"
                                 f"<b>/tracklist</b> - треклист плейлиста", parse_mode="HTML")

        @self.dp.message_handler(commands=["create"])
        async def create(message: types.Message):
            await message.answer(f"Для создания плейлиста напишите функцию\n<b>/create + название плейлиста</b>\n"
                                 f"<b><code>НАПРИМЕР:</code></b>\n"
                                 f"<b>/create new playlist\n</b>"
                                 f"<b>/create новый плейлист\n</b>", parse_mode="HTML")

        @self.dp.message_handler(commands=["download"])
        async def download(message: types.Message):
            await message.answer(f"Чтобы скачать музыку скиньте ссылку на трек\nи через запятую название плейлиста\n"
                                 f"<code>НАПРИМЕР:</code>\n"
                                 f"<b>link</b>,<u>(здесь пробел)</u><i>name_of_playlist</i>", parse_mode="HTML")

        @self.dp.message_handler(commands=["listen"])
        async def listen(message: types.Message):
            await message.answer(f"Чтобы послушать плейлист, напишите\n"
                                 f"/listen <code>название плейлиста</code>\n"
                                 f"<code>НАПРИМЕР:</code>\n"
                                 f"<i>/listen</i>,<u>(здесь пробел)</u><i>новый плейлист</i>", parse_mode="HTML")

        @self.dp.message_handler(commands=["tracklist"])
        async def tracklist(message: types.Message):
            await message.answer(f"Для прсомотра трейлиста плейлиста напишите:\n"
                                 f"/tracklist <b>название плейлиста</b>\n"
                                 f"<code>НАПРИМЕР:</code>\n"
                                 f"<b>/tracklist</b>,<u>(здесь пробел)</u><i>новый плейлист</i>", parse_mode="HTML")

        @self.dp.message_handler()
        async def nothing(message: types.Message):
            await message.answer("Бот такого не знает, проверь своё сообщение")

        executor.start_polling(self.dp, skip_updates=True)


if __name__ == "__main__":
    PlaylistCreator().do_it()
