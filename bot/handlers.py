from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    Message,
    InputMediaDocument,
    FSInputFile,
)

import bot.texts as texts
import bot.keyboards as keyboards

import bot.db.crud.playlists as crud_playlist
from bot.db.models.playlists import Playlists

import bot.db.crud.tracks as crud_tracks
from bot.db.models.tracks import Tracks

import bot.yt_downloader as yt_downloader
import bot.utils as utils

from bot.bot import bot

import os

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text=texts.start_message,
        reply_markup=keyboards.start_keyboard
    )


@router.callback_query(F.data == "start")
async def start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    await state.clear()

    await callback.message.answer(
        text=texts.start_message,
        reply_markup=keyboards.start_keyboard
    )


@router.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup()

    await callback.message.answer(
        text=texts.about_message,
        reply_markup=keyboards.back_keyboard
    )


class CreatePlaylist(StatesGroup):
    name = State()


@router.callback_query(F.data == "create")
async def create(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    await callback.message.answer(
        text=texts.create_message,
        reply_markup=keyboards.back_keyboard
    )
    await state.set_state(CreatePlaylist.name)


@router.message(CreatePlaylist.name)
async def create_playlist(message: Message, state: FSMContext):
    playlist_name = str(message.text)
    user_id = int(message.from_user.id)
    if not crud_playlist.get_playlist(playlist_name, user_id):
        return await message.answer(
            text=texts.already_created,
            reply_markup=keyboards.back_keyboard
        )
    await state.clear()
    playlist = Playlists(
        user_id=int(message.from_user.id),
        name=playlist_name,
        tracks=""
    )

    crud_playlist.create_playlist(playlist)
    playlist_id = crud_playlist.get_playlist_id(playlist_name, user_id)
    await message.answer(
        text=texts.created.format(name=playlist_name),
        reply_markup=keyboards.playlist_created(playlist_id)
    )


@router.callback_query(F.data == "add")
async def add(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup()

    user_id = int(callback.from_user.id)

    playlists = crud_playlist.get_user_playlists(user_id)
    if not playlists:
        return await callback.message.answer(
            text=texts.not_added,
            reply_markup=keyboards.not_added_keyboard
        )

    await callback.message.answer(
        text=texts.added,
        reply_markup=keyboards.user_playlists(playlists)
    )


class AddTrack(StatesGroup):
    playlist_id = State()
    file_id = State()


@router.callback_query(F.data.startswith("add_"))
async def add_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    playlist_id = str(callback.data.split("_")[-1])

    await callback.message.answer(
        text=texts.give_youtube_track,
        reply_markup=keyboards.back_keyboard
    )

    await state.set_state(AddTrack.playlist_id)
    await state.update_data({"playlist_id": playlist_id})


@router.message(AddTrack.playlist_id)
async def add_track(message: Message, state: FSMContext):
    youtube_url = str(message.text)
    data = await state.get_data()

    download = yt_downloader.get_audio(youtube_url)
    if not download:
        return await message.answer(
            text=texts.incorrect_link,
            reply_markup=keyboards.back_keyboard
        )
    filename = utils.get_filename()
    file = FSInputFile(filename)
    file_ = await bot.send_document(
        chat_id=str(message.chat.id),
        document=file,
    )
    # os.remove(filename)
    file_id = str(file_.document.file_id)
    await message.answer(
        text=texts.add_track,
        reply_markup=keyboards.add_track_keyboard()
    )
    await state.set_state(AddTrack.file_id)
    await state.update_data({"file_id": file_id})


@router.callback_query(F.data == "yes")
async def yes(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    user_id = int(callback.from_user.id)
    data = await state.get_data()
    await state.clear()
    file_id, playlist_id = str(data["file_id"]), int(data["playlist_id"])
    print(playlist_id, file_id)
    track = Tracks(
        file_id=file_id,
    )

    crud_tracks.create_track(track)
    track_id = crud_tracks.get_track_by_file_id(file_id)

    crud_playlist.add_track_by_id(user_id, playlist_id, track_id)

    await callback.message.answer(
        text=texts.track_added,
        reply_markup=keyboards.full_add_keyboard,
    )


@router.callback_query(F.data == "listen")
async def listen(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup()
    user_id = int(callback.from_user.id)
    playlists = crud_playlist.get_user_playlists(user_id)
    if not playlists:
        return await callback.message.answer(
            text=texts.not_select_playlist,
            reply_markup=keyboards.not_added_keyboard
        )

    await callback.message.answer(
        text=texts.select_playlist,
        reply_markup=keyboards.listen_user_playlists(playlists)
    )


@router.callback_query(F.data.startswith("listen_"))
async def listen_user_playlists(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup()

    playlist_id = int(callback.data.split("_")[-1])
    get_tracks = crud_playlist.get_playlist_tracks(playlist_id)
    media_group = []
    for track_id in get_tracks.split(" "):
        file_id = crud_tracks.get_track_by_track_id(track_id)
        input_media = InputMediaDocument(media=file_id)
        media_group.append(input_media)
    await callback.message.answer_media_group(
        media_group,
    )
    await callback.message.answer(
        text=texts.media_text,
        reply_markup=keyboards.back_keyboard
    )


@router.callback_query(F.data == "my_playlists")
async def my_playlists(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup()

    user_id = int(callback.from_user.id)
    playlists = crud_playlist.get_user_playlists(user_id)
    await callback.message.answer(
        text=texts.added,
        reply_markup=keyboards.my_user_playlists(playlists)
    )
