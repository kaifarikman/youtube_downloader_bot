from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_buttons = [
    [
        InlineKeyboardButton(text="создать плейлист", callback_data="create"),
    ],
    [
        InlineKeyboardButton(text="добавить трек в плейлист", callback_data="add")
    ],
    [
        InlineKeyboardButton(text="прослушать плейлист", callback_data="listen")
    ],
    [
        InlineKeyboardButton(text="мои плейлисты", callback_data="my_playlists")
    ],
]

start_keyboard = InlineKeyboardMarkup(inline_keyboard=start_buttons)

back_buttons = [
    [
        InlineKeyboardButton(text="Перейти в главное меню", callback_data="start")
    ]
]

back_keyboard = InlineKeyboardMarkup(inline_keyboard=back_buttons)


def playlist_created(playlist_name: str):
    playlist_created_buttons = [
        [
            InlineKeyboardButton(text="Добавить трек", callback_data=f"add_{playlist_name}")
        ],
        [
            InlineKeyboardButton(text="Перейти в главное меню", callback_data="start")
        ]
    ]

    playlist_created_keyboard = InlineKeyboardMarkup(inline_keyboard=playlist_created_buttons)
    return playlist_created_keyboard


not_added_buttons = [
    [
        InlineKeyboardButton(text="Создать плейлист", callback_data="create")
    ],
    [
        InlineKeyboardButton(text="Перейти в главное меню", callback_data="start")
    ]
]
not_added_keyboard = InlineKeyboardMarkup(inline_keyboard=not_added_buttons)

full_add_buttons = [
    [
        InlineKeyboardButton(text="Послушать плейлисты", callback_data="listen")
    ],
    [
        InlineKeyboardButton(text="Перейти в главное меню", callback_data="start")
    ]
]

full_add_keyboard = InlineKeyboardMarkup(inline_keyboard=full_add_buttons)


def user_playlists(playlists: list):
    playlist_buttons = []
    for playlist in playlists:
        playlist_buttons.append(
            [InlineKeyboardButton(text=f"{playlist.name}", callback_data=f"add_{playlist.id}")]
        )
    playlist_buttons.append(
        [
            InlineKeyboardButton(text="Перейти в главное меню", callback_data="start")
        ]
    )
    playlist_keyboard = InlineKeyboardMarkup(inline_keyboard=playlist_buttons)
    return playlist_keyboard


def listen_user_playlists(playlists: list):
    playlist_buttons = []
    for playlist in playlists:
        playlist_buttons.append(
            [InlineKeyboardButton(text=f"{playlist.name}", callback_data=f"listen_{playlist.id}")]
        )
    playlist_buttons.append(
        [
            InlineKeyboardButton(text="Перейти в главное меню", callback_data="start")
        ]
    )
    playlist_keyboard = InlineKeyboardMarkup(inline_keyboard=playlist_buttons)
    return playlist_keyboard


def my_user_playlists(playlists: list):
    playlist_buttons = []
    for playlist in playlists:
        playlist_buttons.append(
            [InlineKeyboardButton(text=f"{playlist.name}", callback_data=f"listen_{playlist.id}")]
        )
    playlist_buttons.append(
        [
            InlineKeyboardButton(text="Перейти в главное меню", callback_data="start")
        ]
    )
    playlist_keyboard = InlineKeyboardMarkup(inline_keyboard=playlist_buttons)
    return playlist_keyboard


def add_track_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Да", callback_data=f"yes")
        ],
        [
            InlineKeyboardButton(text="Нет", callback_data=f"no")
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
