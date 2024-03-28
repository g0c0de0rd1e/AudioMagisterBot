import pickle
import matplotlib.pyplot as plt
import time

from threading import Thread
from functools import lru_cache


@lru_cache(maxsize=128)
def user_data(filename):
    with open(filename, 'wb') as f:
        import main
        data = [(user_id, genre, visits) for user_id, user in main.user_profiles.items() for genre, visits in
                user.genre_visits.items()]
        pickle.dump(data, f)


@lru_cache(maxsize=128)
def load_data(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


@lru_cache(maxsize=128)
def plot_user_data(user):
    @lru_cache(maxsize=128)
    def plot():
        plt.ion()
        plt.figure(figsize=(10, 6))
        while True:
            plt.clf()
            genres = list(user.genre_visits.keys())
            visits = list(user.genre_visits.values())
            plt.barh(genres, visits, color=user.color)
            plt.xlabel('Посещения')
            plt.title('Посещения по жанрам')
            plt.pause(0.1)  # Пауза в 0.1 секунду
            time.sleep(1)  # Пауза в 1 секунду перед следующим обновлением графика

    Thread(target=plot).start()
