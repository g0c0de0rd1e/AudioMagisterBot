from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = [
    [InlineKeyboardButton(text='Жанры 📚', callback_data='genres'),
     InlineKeyboardButton(text='Рекомендации 🌟', callback_data='recommendation'),
     InlineKeyboardButton(text='Книги 📖', callback_data='books')],
    [InlineKeyboardButton(text='Озвучка книг 🎧', callback_data='tts'),
     InlineKeyboardButton(text='Профиль 👤', callback_data='profile')],
    [InlineKeyboardButton(text='Подписка 💳', callback_data='subscription')]
]

genres_button = [
    [
         InlineKeyboardButton(text='📚 Роман', callback_data='novel'),
         InlineKeyboardButton(text='🔎 Детектив', callback_data='detective'),
         InlineKeyboardButton(text='🐲 Фэнтези', callback_data='fantasy'),
     ],
    [
        InlineKeyboardButton(text='🗺 Приключения', callback_data='adventure'),
        InlineKeyboardButton(text='👻 Хоррор и мистика', callback_data='horror'),
        InlineKeyboardButton(text='🎭 Классическая литература', callback_data='classic_literature'),
    ],
    [
        InlineKeyboardButton(text='Проза', callback_data='prose'),
        InlineKeyboardButton(text='Техническая литература', callback_data='technic_literature'),
        InlineKeyboardButton(text='Фантастика', callback_data='fantastical'),
    ],
    [
        InlineKeyboardButton(text='Другая литература', callback_data='other'),
    ],
    [InlineKeyboardButton(text='Меню 🏠', callback_data='echo_message')]
]

novel_buttons = [
    [
        InlineKeyboardButton(text='Любовные романы', callback_data='love_novel'),
        InlineKeyboardButton(text='Современный любовный роман', callback_data='modern_love_novel'),
        InlineKeyboardButton(text='Короткий любовный романы', callback_data='short_love_novel'),
    ],
    [
        InlineKeyboardButton(text='Исторический любовный романы', callback_data='historical_love_novel'),
        InlineKeyboardButton(text='Политический роман', callback_data='political_novel'),
    ],
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

detective_buttons = [
    [
        InlineKeyboardButton(text='Фантастический детектив', callback_data='fantastic_detective'),
        InlineKeyboardButton(text='Исторический детектив', callback_data='historical_detective'),
    ],
    [
        InlineKeyboardButton(text='Шпионский детектив', callback_data='spy_detective'),
    ],
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

fantasy_buttons = [
    [
        InlineKeyboardButton(text='Романтическое фэнтези', callback_data='romantic_fantasy'),
        InlineKeyboardButton(text='Боевое фэнтези', callback_data='fight_fantasy'),
        InlineKeyboardButton(text='Городское фэнтези', callback_data='city_fantasy'),
    ],
    [
        InlineKeyboardButton(text='Темное фэнтези', callback_data='dark_fantasy'),
        InlineKeyboardButton(text='Героическое фэнтези', callback_data='hero_fantasy'),
    ],
    [
         InlineKeyboardButton(text='Эпическое фэнтези', callback_data='epic_fantasy'),
         InlineKeyboardButton(text='Историческое фэнтези', callback_data='historical_fantasy'),
    ],
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

prose_buttons = [
    [
        InlineKeyboardButton(text='Историческая проза', callback_data='historical_prose'),
        InlineKeyboardButton(text='Подростковая проза', callback_data='teen_prose'),
    ],
    [
        InlineKeyboardButton(text='Классическая проза', callback_data='classical_prose'),
    ],
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

horror_buttons = [
    [
        InlineKeyboardButton(text='Хоррор', callback_data='_horror'),
        InlineKeyboardButton(text='Мистика', callback_data='_mistic'),
    ],
    [
        InlineKeyboardButton(text='Триллер', callback_data='_thriller'),
    ],
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

fantastic_buttons = [
    [
        InlineKeyboardButton(text='Боевая фантастика', callback_data='fight_fantastic'),
        InlineKeyboardButton(text='Альтернативная история', callback_data='alt_history'),
        InlineKeyboardButton(text='Космическая фантастика', callback_data='space_fantastic'),
    ],
    [
        InlineKeyboardButton(text='Постапокалипсис', callback_data='_postapocalipsis'),
        InlineKeyboardButton(text='Научная фантастика', callback_data='science_fantastic'),
        InlineKeyboardButton(text='Антиутопия', callback_data='_antiutopia'),
    ],
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

adventure_buttons = [
    [InlineKeyboardButton(text='Исторические приключения', callback_data='historical_adventure')],
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

classical_buttons = [
    [
        InlineKeyboardButton(text='Русская классика', callback_data='russian_classic'),
        InlineKeyboardButton(text='Зарубежная классика', callback_data='foreign_classic'),
    ],
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

technic_buttons = [
    [
        InlineKeyboardButton(text='Экономика и бизнес', callback_data='_business'),
        InlineKeyboardButton(text='Физика', callback_data='_physic'),
    ],
    [
        InlineKeyboardButton(text='Наука', callback_data='_science'),
        InlineKeyboardButton(text='Программирование', callback_data='_programming'),
    ],
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

other_buttons = [
    [
        InlineKeyboardButton(text='Эротика', callback_data='_erotic'),
        InlineKeyboardButton(text='Философия', callback_data='_philosophy'),
    ],
    [
        InlineKeyboardButton(text='Другое', callback_data='_other'),
        InlineKeyboardButton(text='Подростковая литература', callback_data='teen_literature'),
    ],
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

erotic_buttons = [
    [
        InlineKeyboardButton(text='Романтическая эротика', callback_data='romantic_erotic'),
        InlineKeyboardButton(text='Эротическое фэнтези', callback_data='erotic_fantasy'),
    ],
    [
        InlineKeyboardButton(text='Эротическая фантастика', callback_data='erotic_fantastic'),
        InlineKeyboardButton(text='Эротический фанфик', callback_data='erotic_fanfic'),
    ],
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

philosophy_buttons = [
    [
        InlineKeyboardButton(text='Древнегреческая философия', callback_data='greece_philosophy'),
        InlineKeyboardButton(text='Русская философия', callback_data='russian_philosophy'),
    ],
    [
        InlineKeyboardButton(text='Китайская философия', callback_data='chinese_philosophy'),
        InlineKeyboardButton(text='Римская философия', callback_data='roman_philosophy'),
    ],
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

_other_buttons = [
    [
        InlineKeyboardButton(text='Сказка', callback_data='fairy_tale'),
        InlineKeyboardButton(text='Развитие личности', callback_data='personality_developing'),
    ],
    [
        InlineKeyboardButton(text='Публицистика', callback_data='_publicist'),
        InlineKeyboardButton(text='Детская литература', callback_data='kid_literature'),
    ],
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

teen_buttons = [
    [InlineKeyboardButton(text='Назад', callback_data='genres')]
]

recommendation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='prev_page'),
     InlineKeyboardButton(text='Вперед', callback_data='next_page')],
    [InlineKeyboardButton(text='Меню 🏠', callback_data='echo_message')]
])

book_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='prev_page'),
     InlineKeyboardButton(text='Вперед', callback_data='next_page')],
    [InlineKeyboardButton(text='Открыть книгу 📖', callback_data='open_book'),
     InlineKeyboardButton(text='Открыть аудиокнигу📖', callback_data='open_audio_book')],
    [InlineKeyboardButton(text='Меню 🏠', callback_data='echo_message')]
])

back_to_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Меню 🏠', callback_data='echo_message')]])

menu = InlineKeyboardMarkup(inline_keyboard=menu)
genres_button = InlineKeyboardMarkup(inline_keyboard=genres_button)
novel_buttons = InlineKeyboardMarkup(inline_keyboard=novel_buttons)
detective_buttons = InlineKeyboardMarkup(inline_keyboard=detective_buttons)
fantasy_buttons = InlineKeyboardMarkup(inline_keyboard=fantasy_buttons)
prose_buttons = InlineKeyboardMarkup(inline_keyboard=prose_buttons)
horror_buttons = InlineKeyboardMarkup(inline_keyboard=horror_buttons)
fantastic_buttons = InlineKeyboardMarkup(inline_keyboard=fantastic_buttons)
adventure_buttons = InlineKeyboardMarkup(inline_keyboard=adventure_buttons)
classical_buttons = InlineKeyboardMarkup(inline_keyboard=classical_buttons)
technic_buttons = InlineKeyboardMarkup(inline_keyboard=technic_buttons)
other_buttons = InlineKeyboardMarkup(inline_keyboard=other_buttons)
erotic_buttons = InlineKeyboardMarkup(inline_keyboard=erotic_buttons)
philosophy_buttons = InlineKeyboardMarkup(inline_keyboard=philosophy_buttons)
_other_buttons = InlineKeyboardMarkup(inline_keyboard=_other_buttons)
teen_buttons = InlineKeyboardMarkup(inline_keyboard=teen_buttons)
