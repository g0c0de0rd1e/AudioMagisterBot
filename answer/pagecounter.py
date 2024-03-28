from text import books


def get_books_for_page(current_page, genre):
    books_per_page = 1
    genre_books = [book for book in books if book['genre'] == genre]  # Получаем книги выбранного жанра

    start_index = (current_page - 1) * books_per_page
    end_index = start_index + books_per_page

    page_books = genre_books[start_index:end_index]  # Используем книги выбранного жанра
    if page_books:  # Проверяем, есть ли книги на этой странице
        return f"Название: {page_books[0]['title']}\nЖанр: {page_books[0]['genre']}"  # Возвращаем только первую книгу
    else:
        return "Книги этого жанра не найдены на этой странице"


def create_pages(text, page_size=2048):
    for i in range(0, len(text), page_size):
        yield text[i:i+page_size]

def get_books_for_page(page, genre):
    from fileToText import convert_file_to_text
    # Фильтруем книги по жанру
    genre_books = [book for book in books if book['genre'] == genre]
    # Выбираем книгу на основе текущей страницы
    book = genre_books[page - 1]
    # Преобразование файла книги в текст
    book_text = convert_file_to_text(book['path'])
    # Создание страниц
    pages = create_pages(book_text)
    # Возвращаем текст первой страницы
    return next(pages)


def get_total_pages(genre):
    books_per_page = 1
    genre_books = [book for book in books if book['genre'] == genre]  # Получаем книги выбранного жанра
    total_pages = len(genre_books)  # Используем количество книг выбранного жанра

    if len(genre_books) % books_per_page != 0:
        total_pages += 1
    return total_pages

