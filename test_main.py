import pytest


class TestBooksCollector:

    @pytest.mark.parametrize(
        "book",
        {
            "Т",
            "Тепло наших тел",
            "Тепло наших телТепло наших телТепло наши",
        },
    )
    def test_add_new_book_valid_names(self, book, collector):
        collector.add_new_book(book)
        assert book in collector.books_genre
        assert len(collector.books_genre) == 1

    @pytest.mark.parametrize(
        "book",
        {
            "",
            "Тепло наших телТепло наших телТепло наших",
            "Тепло наших телТепло наших телТепло наших ",
            "Тепло наших телТепло наших телТепло наших телТепло наших тел",
        },
    )
    def test_add_new_book_invalid_names(self, book, collector):
        collector.add_new_book(book)
        assert book not in collector.books_genre
        assert len(collector.books_genre) == 0

    def test_add_new_book_add_similar_books_fifteen_characters(self, collector):
        collector.add_new_book("Тепло наших тел")
        collector.add_new_book("Тепло наших тел")
        assert len(collector.books_genre) == 1
        assert "Тепло наших тел" in collector.books_genre

    @pytest.mark.parametrize(
        "book, genre, expected",
        {
            ("Тепло наших тел", "Фантастика", "Фантастика"),
            ("Тепло наших тел", "Романтика", ""),
        },
    )
    def test_set_book_genre(self, book, genre, expected, collector):
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)
        assert collector.books_genre[book] == expected

    def test_set_book_genre_for_book_not_in_the_list(self, collector):
        collector.set_book_genre("Книги нет в словаре", "Фантастика")
        assert "Фантастика" not in collector.books_genre.values()
        assert len(collector.books_genre) == 0

    def test_get_book_genre_name_in_the_list(self, collector):
        collector.add_new_book("Тепло наших тел")
        collector.set_book_genre("Тепло наших тел", "Фантастика")
        assert collector.get_book_genre("Тепло наших тел") == "Фантастика"

    def test_get_book_genre_name_not_in_the_list(self, collector):
        collector.get_book_genre("Книги нет в словаре")
        assert "Книги нет в словаре" not in collector.books_genre
        assert len(collector.books_genre) == 0

    @pytest.mark.parametrize(
        "books_genre, genre, expected",
        [
            (
                {"Тепло наших тел": "Фантастика", "Сумерки": "Ужасы"},
                "Фантастика",
                ["Тепло наших тел"],
            ),
            ({"Сумерки": "Ужасы"}, "Ужасы", ["Сумерки"]),
            (
                {"Как приручить дракона": "Мультфильмы", "Всегда говори Да": "Комедии"},
                "Фантастика",
                [],
            ),
            ({"Хоббиты": "Фэнтези"}, "Фэнтези", []),
            ({}, "Детективы", []),
        ],
    )
    def test_get_books_with_specific_genre(
        self, books_genre, genre, expected, collector
    ):
        collector.books_genre = books_genre
        result = collector.get_books_with_specific_genre(genre)
        assert result == expected

    def test_get_books_for_children(self, collector):
        collector.add_new_book("Тепло наших тел")
        collector.add_new_book("Как приручить дракона")
        collector.set_book_genre("Тепло наших тел", "Ужасы")
        collector.set_book_genre("Как приручить дракона", "Мультфильмы")
        kids_books = collector.get_books_for_children()
        assert "Тепло наших тел" not in kids_books
        assert "Как приручить дракона" in kids_books

    def test_add_book_in_favorites_with_valid_name(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.add_book_in_favorites("Гарри Поттер")
        assert "Гарри Поттер" in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_with_valid_name(self, collector):
        collector.add_new_book("Тепло наших тел")
        collector.add_book_in_favorites("Тепло наших тел")
        collector.delete_book_from_favorites("Тепло наших тел")
        assert "Тепло наших тел" not in collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book("Тепло наших тел")
        collector.add_book_in_favorites("Тепло наших тел")
        assert len(collector.get_list_of_favorites_books()) == 1
