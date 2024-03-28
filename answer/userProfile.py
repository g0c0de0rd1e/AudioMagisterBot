from datetime import datetime, timedelta

from functools import lru_cache

import random

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.color = (random.random(), random.random(), random.random())
        self.read_books = 0
        self.listened_books = 0
        self.favorite_genres = []
        self.subscription = False
        self.subscription_end_date = None
        self.selected_genre = None
        self.genre_visits = {
            'Любовный роман': 0,
            'Современный любовный роман': 0,
            'Короткий любовный роман': 0,
            'Исторический любовный роман': 0,
            'Политический роман': 0,
            'Фантастический детектив': 0,
            'Исторический детектив': 0,
            'Шпионский детектив': 0,
            'Романтическое фэнтези': 0,
            'Боевое фэнтези': 0,
            'Городское фэнтези': 0,
            'Героическое фэнтези': 0,
            'Эпическое фэнтези': 0,
            'Историческое фэнтези': 0,
            'Боевая фантастика': 0,
            'Альтернативная история': 0,
            'Космическая фантастика': 0,
            'Постапокалипсис': 0,
            'Научная фантастика': 0,
            'Антиутопия': 0,
            'Историческая проза': 0,
            'Подростковая проза': 0,
            'Классическая проза': 0,
            'Хоррор': 0,
            'Мистика': 0,
            'Триллер': 0,
            'Исторические приключения': 0,
            'Русская классика': 0,
            'Зарубежная классика': 0,
            'Экономика и бизнес': 0,
            'Физика': 0,
            'Наука': 0,
            'Программирование': 0,
            'Романтическая эротика': 0,
            'Эротическое фэнтези': 0,
            'Эротическая фантастика': 0,
            'Эротический фанфик': 0,
            'Древнегреческая философия': 0,
            'Русская философия': 0,
            'Китайская философия': 0,
            'Римская философия': 0,
            'Сказка': 0,
            'Развитие личности': 0,
            'Публицистика': 0,
            'Детская литература': 0
        }

    @lru_cache(maxsize=128)
    def increment_read_books(self):
        self.read_books += 1

    @lru_cache(maxsize=128)
    def increment_listened_books(self):
        self.listened_books += 1

    @lru_cache(maxsize=128)
    def add_favorite_genre(self, genre):
        if genre not in self.favorite_genres:
            self.favorite_genres.append(genre)

    @lru_cache(maxsize=128)
    def activate_subscription(self, duration=30):
        self.subscription = True
        self.subscription_end_date = datetime.now() + timedelta(days=duration)
        return self.subscription, self.subscription_end_date

    @lru_cache(maxsize=128)
    def check_subscription(self):
        if self.subscription:
            if datetime.now() > self.subscription_end_date:
                self.subscription = False
                self.subscription_end_date = None
                return "Подписка неактивна"
            else:
                return f"Подписка активна до {self.subscription_end_date.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            return "Подписка неактивна"

    @lru_cache(maxsize=128)
    def visit_genre(self, genre):
        if genre not in self.genre_visits:
            self.genre_visits[genre] = 0
        self.genre_visits[genre] += 1
        self.add_favorite_genre(genre)
        self.selected_genre = genre

    @lru_cache(maxsize=128)
    def get_top_genres(self, n=2):
        if not self.favorite_genres:
            return 'Любимых жанров нет'
        else:
            return sorted(self.genre_visits.items(), key=lambda item: item[1], reverse=True)[:n]

    @lru_cache(maxsize=128)
    def get_selected_genre(self):
        return self.selected_genre
