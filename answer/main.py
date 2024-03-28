import asyncio
import logging

from functools import lru_cache

from userProfile import User

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.types import Message, ContentType

import buttons
import text

from pagecounter import get_books_for_page, get_total_pages
from recommendation import RecommendationSystem

from fileToText import convert_file_to_text
from audio import text_to_speech

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
YOOTOKEN = os.getenv('YOOTOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

user_profiles = {}


# Я НЕ ГОВНОКОДЕР ЭТО ПРОСТО НЕДОСТАТОК СНА

############ ЛОГГИРОВАНИЕ В КОНСОЛИ ##############
@lru_cache(maxsize=128)
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


##################################################

############# ПРИВЕТСТВОВАНИЕ #####################
@lru_cache(maxsize=128)
@dp.message()
async def start_message(message: types.Message):
    await message.answer(text.greet.format(name=message.from_user.full_name),
                         reply_markup=buttons.menu)


#############################################################################


#############################################################################

########################### МЕНЮ ############################################
@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'echo_message')
async def echo_message(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)



    await bot.send_message(callback_query.from_user.id,
                           text.greet.format(name=callback_query.from_user.full_name),
                           reply_markup=buttons.menu)


#############################################################################

################################## ОЗВУЧКА #################################

@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'tts')
async def tts(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)

    await bot.send_message(callback_query.from_user.id,
                           text='Загрузите файл в формате .txt или .docx',
                           reply_markup=buttons.menu)

    file_id = callback_query.document.file_id
    file_info = await bot.get_file(file_id)
    file_path = await bot.download_file(file_info.file_path, destination='./books')

    textts = convert_file_to_text(file_path)
    if textts is not None:
        output_file = os.path.splitext(file_path)[0] + '.wav'
        text_to_speech(textts, output_file)
        with open(output_file, 'rb') as audio:
            await bot.send_voice(callback_query.chat.id, audio)

#############################################################################



################################## ПРОФИЛЬ #################################
@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'profile')
async def profile_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    await bot.answer_callback_query(callback_query.id)
    top_genres = user_profile.get_top_genres()
    if top_genres == 'Любимых жанров нет':
        favorite_genres = top_genres
    else:
        favorite_genres = ', '.join(genre for genre, _ in top_genres)
    await bot.send_message(callback_query.from_user.id,
                           text.profile.format(
                               id=callback_query.from_user.id,
                               name=callback_query.from_user.full_name,
                               read_books=user_profile.read_books,
                               listened_books=user_profile.listened_books,
                               favorite_genres=favorite_genres,
                               subscribtion=user_profile.check_subscription()),
                           reply_markup=buttons.menu
                           )


#############################################################################

###################### РЕКОМЕНДАЦИИ #########################################
@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'recommendation')
async def recommendation(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    rec_sys = RecommendationSystem(user_profile)
    rec_sys.train()
    recommended_genres = rec_sys.recommend()
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, f"Ваши рекомендованные жанры: {recommended_genres}",
                           reply_markup=buttons.recommendation)


#################################################################################################################################################

####################################### ЖАНРЫ ################################
@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'genres')
async def genres(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text.genres.format(),
                           reply_markup=buttons.genres_button)


############################## ОБРАБОТКА ЖАНРОВ ##############################

'''---------------РОМАН------------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'novel')
async def novel(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Роман',
                           reply_markup=buttons.novel_buttons)


'''-----------------ДЕТЕКТИВ------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'detective')
async def detective(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Детектив',
                           reply_markup=buttons.detective_buttons)


'''---------------ФЭНТЕЗИ----------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'fantasy')
async def fantasy(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Фэнтези\n\n',
                           reply_markup=buttons.fantasy_buttons)


'''--------------------ПРИКЛЮЧЕНИЯ----------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'adventure')
async def travel_story(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Приключения\n\n',
                           reply_markup=buttons.adventure_buttons)


'''--------------------УЖАСЫ----------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'horror')
async def horror(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Хоррор\n\n',
                           reply_markup=buttons.horror_buttons)


'''--------------------КЛАССИЧЕСКАЯ ЛИТЕРАТУРА----------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'classic_literature')
async def classic_literature(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Классическая литература\n\n',
                           reply_markup=buttons.classical_buttons)


'''--------------------ПРОЗА----------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'prose')
async def prose(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Проза\n\n',
                           reply_markup=buttons.prose_buttons)


'''--------------------ТЕХНИЧЕСКАЯ ЛИТЕРАТУРА----------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'technic_literature')
async def technic_literature(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Техническая литература\n\n',
                           reply_markup=buttons.technic_buttons)


'''--------------------ФАНТАСТИКА----------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'fantastical')
async def fantastical(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Фантастика\n\n',
                           reply_markup=buttons.fantastic_buttons)


'''--------------------ДРУГОЕ----------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'other')
async def fantastical(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Другое\n\n',
                           reply_markup=buttons.other_buttons)


'''--------------------ЭРОТИКА----------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == '_erotic')
async def _erotic(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Эротика\n\n',
                           reply_markup=buttons.erotic_buttons)


'''--------------------ФИЛОСОФИЯ----------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == '_philosophy')
async def _philosophy(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Философия\n\n',
                           reply_markup=buttons.philosophy_buttons)


'''--------------------ДРУГОЕ ПОДЖАНРЫ----------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == '_other')
async def _other(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Другое\n\n',
                           reply_markup=buttons._other_buttons)


'''--------------------ПОДРОСТКОВАЯ ЛИТЕРАТУРА----------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'teen_literature')
async def teen_literature(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Подростковая литература\n\n',
                           reply_markup=buttons.teen_buttons)


##################################################################################################


################################### ОБРАБОТКА ПОДЖАНРОВ ##########################################


'''-------------------------РОМАНЫ----------------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'love_novel')
async def love_novel(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Любовный роман')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Любовные романы\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'modern_love_novel')
async def modern_love_novel(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Современный любовный роман')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Современные любовные романы\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'short_love_novel')
async def short_love_novel(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Короткий любовный роман')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Короткие любовные романы\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'historical_love_novel')
async def historical_love_novel(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Исторический любовный роман')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Любовные романы\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'political_novel')
async def political_novel(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Политический роман')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Политические романы\n\n',
                           reply_markup=buttons.book_buttons)


'''-------------------------ДЕТЕКТИВЫ----------------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'fantastic_detective')
async def fantastic_detective(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Фантастический детектив')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Фантастический детектив\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'historical_detective')
async def historical_detective(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Исторический детектив')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Исторический детектив\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'spy_detective')
async def spy_detective(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Шпионский детектив')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Шпионский детектив\n\n',
                           reply_markup=buttons.book_buttons)


'''-----------------------------Фэнтези-------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'romantic_fantasy')
async def romantic_fantasy(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Романтическое фэнтези')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Романтическое фэнтези\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'fight_fantasy')
async def fight_fantasy(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Боевое фэнтези')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Боевое фэнтези\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'city_fantasy')
async def city_fantasy(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Городское фэнтези')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Городское фэнтези\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'dark_fantasy')
async def dark_fantasy(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Темное фэнтези')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Темное фэнтези\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'hero_fantasy')
async def hero_fantasy(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Героическое фэнтези')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Героическое фэнтези\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'epic_fantasy')
async def epic_fantasy(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Эпическое фэнтези')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Эпическое фэнтези\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'historical_fantasy')
async def historical_fantasy(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Историческое фэнтези')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Историческое фэнтези\n\n',
                           reply_markup=buttons.book_buttons)


'''-------------------------Фантастика---------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'fight_fantastic')
async def fight_fantastic(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Боевая фантастика')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Боевая фантастика\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'alt_history')
async def alt_history(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Альтернативная история')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Альтернативная история\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'space_fantastic')
async def space_fantastic(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Космическая фантастика')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Космическая фантастика\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == '_postapocalipsis')
async def _postapocalipsis(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Постапокалипсис')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Постапокалипсис\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'science_fantastic')
async def science_fantastic(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Научная фантастика')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Научная фантастика\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == '_antiutopia')
async def _antiutopia(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Антиутопия')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Антиутопия\n\n',
                           reply_markup=buttons.book_buttons)


'''-----------------------------Проза---------------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'historical_prose')
async def historical_prose(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Историческая проза')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Историческая проза\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'teen_prose')
async def teen_prose(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Подростковая проза')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Подростковая проза\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'classical_prose')
async def spy_detective(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Классическая проза')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Классическая проза\n\n',
                           reply_markup=buttons.book_buttons)


'''---------------------------Хоррор--------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == '_horror')
async def _horror(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Хоррор')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Хоррор\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == '_mistic')
async def _mistic(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Мистика')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Мистика\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == '_thriller')
async def _thriller(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Триллер')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Триллер\n\n',
                           reply_markup=buttons.book_buttons)


'''--------------------------------Приключения-----------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'historical_adventure')
async def historical_adventure(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Исторические приключения')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Исторические приключения\n\n',
                           reply_markup=buttons.book_buttons)


'''----------------------Классическая литература----------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'russian_classic')
async def russian_classic(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Русская классика')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Русская классика\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'foreign_classic')
async def foreign_classic(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Зарубежная классика')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Зарубежная классика\n\n',
                           reply_markup=buttons.book_buttons)


'''-----------------Техническая литература------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == '_business')
async def _business(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Экономика и бизнес')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Экономика и бизнес\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == '_physic')
async def _physic(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Физика')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Физика\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == '_science')
async def _science(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Наука')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Наука\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == '_programming')
async def _programming(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Программирование')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Программирование\n\n',
                           reply_markup=buttons.book_buttons)


'''------------------------Эротика-----------------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'romantic_erotic')
async def romantic_erotic(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Романтическая эротика')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Романтическая эротика\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'erotic_fantasy')
async def erotic_fantasy(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Эротическое фэнтези')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Эротическое фэнтези\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'erotic_fantastic')
async def erotic_fantastic(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Эротическая фантастика')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Эротическая фантастика\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'erotic_fanfic')
async def erotic_fanfic(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Эротический фанфик')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Эротический фанфик\n\n',
                           reply_markup=buttons.book_buttons)


'''------------------------Философия-----------------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'greece_philosophy')
async def greece_philosophy(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Древнегреческая философия')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Древнегреческая философия\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'russian_philosophy')
async def russian_philosophy(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Русская философия')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Русская философия\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=256)
@dp.callback_query(F.data == 'chinese_philosophy')
async def chinese_philosophy(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Китайская философия')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Китайская философия\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'roman_philosophy')
async def roman_philosophy(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Римская философия')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Римская философия\n\n',
                           reply_markup=buttons.book_buttons)


'''---------------------------Другое 2--------------------------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'fairy_tale')
async def fairy_tale(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Сказка')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Сказка\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'personality_developing')
async def personality_developing(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Развитие личности')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Развитие личности\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == '_publicist')
async def _publicist(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Публицистика')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Публицистика\n\n',
                           reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'kid_literature')
async def kid_literature(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].visit_genre('Детская литература')
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Жанр: Детская литература\n\n',
                           reply_markup=buttons.book_buttons)


# '''--------------Подростковая литература-----------------'''
#
#
# @dp.callback_query(F.data == 'spy_detective')
# async def spy_detective(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     if user_id not in user_profiles:
#         user_profiles[user_id] = User(user_id)
#     user_profiles[user_id].visit_genre('Шпионский детектив')
#     await bot.delete_message(callback_query.from_user.id,
#                              callback_query.message.message_id)
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id,
#                            text=f'Жанр: Шпионский детектив\n\n',
#                            reply_markup=buttons.book_buttons)


#############################################################################


############################ ЧИТАЛКА #################################################
current_page = 0

'''ОНО РАБОТАЕТ БЛЯТЬ'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'next_page')
async def next_page(callback_query: types.CallbackQuery):
    global user_profiles
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    selected_genre = user_profiles[user_id].get_selected_genre()  # Получаем выбранный жанр
    global current_page
    total_pages = get_total_pages(selected_genre)  # Получаем общее количество страниц
    if current_page >= total_pages:  # Проверяем, не превышает ли текущая страница общее количество страниц
        await bot.answer_callback_query(callback_query.id, "Вы достигли последней страницы.")
    else:
        current_page += 1
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=get_books_for_page(current_page, selected_genre),
                                    # Учитываем выбранный жанр при получении книг для страницы
                                    reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'prev_page')
async def prev_page(callback_query: types.CallbackQuery):
    global user_profiles
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    selected_genre = user_profiles[user_id].get_selected_genre()  # Получаем выбранный жанр
    global current_page
    if current_page <= 1:  # Проверяем, не меньше ли текущая страница первой
        await bot.answer_callback_query(callback_query.id, "Вы на первой странице.")
    else:
        current_page -= 1
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=get_books_for_page(current_page, selected_genre),
                                    # Учитываем выбранный жанр при получении книг для страницы
                                    reply_markup=buttons.book_buttons)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'open_book')
async def open_book(callback_query: types.CallbackQuery):
    global user_profiles
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].increment_read_books()
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.message.chat.id,
                               message_id=callback_query.message.message_id,
                               text=convert_file_to_text('books/'),
                               reply_markup=buttons.recommendation)


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'open_audio_book')
async def open_audio_book(callback_query: types.CallbackQuery):
    """Добавить логику к подписке"""
    global user_profiles
    user_id = callback_query.from_user.id
    user_profile = user_profiles.get(user_id, User(user_id))
    if user_id not in user_profiles:
        user_profiles[user_id] = user_profile
    user_profiles[user_id].increment_listened_books()
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.from_user.id)
    with open('output.wav', 'rb') as audio:
        await bot.send_voice(callback_query.from_user.id, audio)


#############################################################################


############################################# ТРАНЗАКЦИИ ##############################################################

'''--------------Создание подписки-------------'''


@lru_cache(maxsize=128)
@dp.callback_query(F.data == 'subscription')
async def sub_month(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,
                             callback_query.message.message_id)
    await bot.send_invoice(chat_id=callback_query.from_user.id,
                           title='Подписка на месяц',
                           description='Тест',
                           payload='month_sub',
                           provider_token=YOOTOKEN,
                           currency='RUB',
                           start_parameter='',
                           prices=[{'label': 'Руб', 'amount': 15000}])
    await bot.send_message(callback_query.from_user.id, 'Выйти в меню', reply_markup=buttons.back_to_menu)


'''-----------Проверка оплаты-----------'''


# Исправить
@lru_cache(maxsize=128)
@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    print("вход")
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


'''--------------Успешная подписка--------------'''


@lru_cache(maxsize=128)
@dp.message(F.data == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    print("вход")
    if message.succesful_payment.invoice_payload == 'month_sub':
        user_id = message.from_user.id
        if user_id not in user_profiles:
            user_profiles[user_id] = User(user_id)
        user_profiles[user_id].activate_subscribtion()
        user_profiles[user_id] = user_profiles[user_id]

    await bot.send_message(message.from_user.id, text='Вам выдана подписка на месяц')


################################################################################################


'''Обработать рекомендации'''

##### Запуска бота ########
if __name__ == '__main__':
    asyncio.run(main())
############################
