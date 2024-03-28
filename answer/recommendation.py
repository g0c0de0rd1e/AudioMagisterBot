from surprise import Dataset, Reader, SVD

from functools import lru_cache

import pandas as pd
import random

class RecommendationSystem:
    def __init__(self, user):
        self.user = user
        self.data = self.load_data()
        self.algo = SVD()

    @lru_cache(maxsize=128)
    def load_data(self):
        import main
        data = [(user_id, genre, visits) for user_id, user in main.user_profiles.items() for genre, visits in user.genre_visits.items()]
        reader = Reader(rating_scale=(1, 5))
        return Dataset.load_from_df(pd.DataFrame(data, columns=['user_id', 'genre', 'rating']), reader)
        reader = Reader(rating_scale=(1, 5))
        return Dataset.load_from_df(data, reader)

    @lru_cache(maxsize=128)
    def train(self):
        # Обучить модель на данных
        trainset = self.data.build_full_trainset()
        self.algo.fit(trainset)

    @lru_cache(maxsize=128)
    def predict(self, genre):
        # Предсказать рейтинг для данного жанра
        prediction = self.algo.predict(self.user.user_id, genre)
        return prediction.est

    @lru_cache(maxsize=128)
    def recommend(self):
        # Рекомендовать жанры пользователю
        genres = list(self.user.genre_visits.keys())
        if sum(self.user.genre_visits.values()) == 0:  # Если у пользователя нет посещений жанров
            return random.sample(genres, 3)  # Возвращает 3 случайных жанра
        else:
            predictions = {genre: self.predict(genre) for genre in genres}
            recommended_genres = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
            return [genre[0] for genre in recommended_genres[:3]]  # Возвращает топ-3 рекомендованных жанров
