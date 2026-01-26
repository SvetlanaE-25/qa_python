from main import BooksCollector

import pytest


class TestBooksCollector:

    def test__init__(self):  # проверка инициализации объекта
        collector = BooksCollector()
        assert collector.books_genre == {}
        assert collector.favorites == []
        assert collector.genre == ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']
        assert collector.genre_age_rating == ['Ужасы', 'Детективы']

    @pytest.mark.parametrize('name', ['A' * 1, 'А' * 20, 'А' * 39, 'А' * 40])
    def test_add_new_book_valid_length_name_true(self,
                                                 name):  # проверка добавления книги с названием принимаемым количеством символов
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.books_genre

    @pytest.mark.parametrize('name', ['А' * 41, 'А' * 60])
    def test_add_new_book_too_long_name_true(self,
                                             name):  # проверка, что в словарь не добавляются книги с количеством символов более 40
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name not in collector.books_genre

    def test_add_new_book_empty_true(self):  # проверка не добавления книги с пустым названием
        collector = BooksCollector()
        name = ''
        collector.add_new_book(name)
        assert name not in collector.books_genre

    def test_add_new_book_duplicate_name_true(self):  # проверка добавления одной и той же книги один раз
        collector = BooksCollector()
        collector.add_new_book('Вино из одуванчиков')
        collector.add_new_book('Вино из одуванчиков')
        assert len(collector.books_genre) == 1

    @pytest.mark.parametrize('name, genre', [['1984', 'Фантастика'], ['Кладбище домашних животных', 'Ужасы'],
                                             ['Приключения Шерлока Холмса', 'Детективы'],
                                             ['Сказка о царе Салтане', 'Мультфильмы'], ['Комедия ошибок', 'Комедии']])
    def test_set_book_genre_for_name_existed_in_dictionary_true(self, name,
                                                                genre):  # проверка установки жанра книге, добавленной в словарь
        collector = BooksCollector()
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.books_genre[name] == genre

    def test_set_genre_for_name_not_existed_in_dictionary_true(
            self):  # проверка, что нельзя установить жанр несуществующей в словаре книги
        collector = BooksCollector()
        name = 'В словаре не значился'
        collector.set_book_genre(name, 'Детективы')
        assert name not in collector.books_genre

    def test_set_book_genre_not_existed_genre_true(self):  # проверка, что нельзя установить несуществующий жанр
        collector = BooksCollector()
        name = '1984'
        collector.add_new_book(name)
        collector.set_book_genre(name, 'Несуществующий жанр')
        assert collector.books_genre[name] == ''

    @pytest.mark.parametrize('name, genre', [['1984', 'Фантастика'], ['Кладбище домашних животных', 'Ужасы'],
                                             ['Приключения Шерлока Холмса', 'Детективы'],
                                             ['Сказка о царе Салтане', 'Мультфильмы'], ['Комедия ошибок', 'Комедии']])
    def test_get_book_genre_for_existed_name_true(self, name, genre):  # проверка получения жанра по названию книги
        collector = BooksCollector()
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == genre

    @pytest.mark.parametrize('name, genre', [['1984', 'Фантастика'], ['Кладбище домашних животных', 'Ужасы'],
                                             ['Приключения Шерлока Холмса', 'Детективы'],
                                             ['Сказка о царе Салтане', 'Мультфильмы'], ['Комедия ошибок', 'Комедии']])
    def test_get_books_with_specific_genre_existing_in_dictionary_true(self, name,
                                                                       genre):  # проверка вывода списка существующих в словаре книг с определенным жанром
        collector = BooksCollector()
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_books_with_specific_genre(genre) == [name]

    @pytest.mark.parametrize('name, genre',
                             [['Вокруг света за 80 дней', 'Фантастика'], ['Сказка о царе Салтане', 'Мультфильмы'],
                              ['Комедия ошибок', 'Комедии']])
    def test_get_books_for_children_genre_without_age_rating_true(self, name,
                                                                  genre):  # проверка получения книг, подходящих детям
        collector = BooksCollector()
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert name in collector.get_books_for_children()

    @pytest.mark.parametrize('name, genre',
                             [['Кладбище домашних животных', 'Ужасы'], ['Приключения Шерлока Холмса', 'Детективы']])
    def test_get_books_for_children_genre_with_age_rating_true(self, name,
                                                               genre):  # проверка, что для детей не выведутся книги с возрастным ограничением
        collector = BooksCollector()
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert name not in collector.get_books_for_children()

    def test_add_book_in_favorites_name_existed_in_dictionary_true(
            self):  # проверка добавления в избранное книги, существующей в словаре
        collector = BooksCollector()
        collector.add_new_book('Любимая книга')
        collector.add_book_in_favorites('Любимая книга')
        assert 'Любимая книга' in collector.favorites

    def test_delete_book_from_favorites_name_existed_in_favorites_true(self):  # проверка удаления книги из избранного
        collector = BooksCollector()
        collector.add_new_book('Любимая книга')
        collector.add_book_in_favorites('Любимая книга')
        collector.delete_book_from_favorites('Любимая книга')
        assert 'Любимая книга' not in collector.favorites

    def test_get_list_of_favorites_books_true(self):  # проверка получения списка избранных книг
        collector = BooksCollector()
        collector.add_new_book('Любимая книга 1')
        collector.add_new_book('Любимая книга 2')
        collector.add_book_in_favorites('Любимая книга 1')
        collector.add_book_in_favorites('Любимая книга 2')
        result = collector.get_list_of_favorites_books()
        assert 'Любимая книга 1' in result
        assert 'Любимая книга 2' in result

    @pytest.mark.parametrize('name, genre',
                             [['Вокруг света за 80 дней', 'Фантастика'], ['Сказка о царе Салтане', 'Мультфильмы'],
                              ['Комедия ошибок', 'Комедии']])
    def test_get_books_for_children_genre_without_age_rating_true(self, name,
                                                                  genre):  # проверка получения книг, подходящих детям
        collector = BooksCollector()
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert name in collector.get_books_for_children()

    @pytest.mark.parametrize('name, genre',
                             [['Кладбище домашних животных', 'Ужасы'], ['Приключения Шерлока Холмса', 'Детективы']])
    def test_get_books_for_children_genre_with_age_rating_true(self, name,
                                                                genre):  # проверка, что для детей не выведутся книги с возврастным ограничением
        collector = BooksCollector()
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert name not in collector.get_books_for_children()

    def test_add_book_in_favorites_name_excisted_in_dictionary_true(
            self):  # проверка добавления в избранное книги, существующей в словаре
        collector = BooksCollector()
        collector.add_new_book('Любимая книга')
        collector.add_book_in_favorites('Любимая книга')
        assert 'Любимая книга' in collector.favorites

    def test_delete_book_from_favorites_name_excisted_in_favorites_true(self):  # проверка удаления книги из избранного
        collector = BooksCollector()
        collector.add_new_book('Любимая книга')
        collector.add_book_in_favorites('Любимая книга')
        collector.delete_book_from_favorites('Любимая книга')
        assert 'Любимая книга' not in collector.favorites

    def test_get_list_of_favorites_books_true(self):  # проверка получения списка избранных книг
        collector = BooksCollector()
        collector.add_new_book('Любимая книга 1')
        collector.add_new_book('Любимая книга 2')
        collector.add_book_in_favorites('Любимая книга 1')
        collector.add_book_in_favorites('Любимая книга 2')
        result = collector.get_list_of_favorites_books()
        assert 'Любимая книга 1' in result
        assert 'Любимая книга 2' in result