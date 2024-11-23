import json
import os


class Library:
    def __init__(self, json_name: str = "library.json"):
        """Инициализация библиотеки и загрузка данных из JSON."""
        self.json_name: str = json_name
        self.library: list[dict] = self.load_json()
        self.book_template: dict = {
            "id": None,
            "title": None,
            "author": None,
            "year": None,
            "status": "в наличии"
        }

    def load_json(self) -> list[dict]:
        """Загружает библиотеку из файла JSON."""
        if not os.path.exists(self.json_name):
            return []
        with open(self.json_name, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_json(self) -> None:
        """Сохраняет библиотеку в файл JSON."""
        try:
            with open(self.json_name, "w", encoding="utf-8") as file:
                json.dump(self.library, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

    def check_library(self) -> bool:
        """Проверка, пуста ли библиотека."""
        if not self.library:
            print("Библиотека пуста")
            return True
        return False

    def add(self) -> None:
        """Добавляет новую книгу в библиотеку."""
        book: dict = self.book_template.copy()
        book["title"] = input("Введите название книги: ").strip()
        if not book["title"]:
            print("Название книги не может быть пустым")
            return
        book["author"] = input("Введите автора книги: ").strip()
        if not book["author"]:
            print("Автор книги не может быть пустым")
            return
        year: str = input("Введите год издания книги: ").strip()
        if not year.isdigit():
            print("Год должен быть числом")
            return
        book["year"] = int(year)
        book["id"] = len(self.library) + 1
        self.library.append(book)
        self.save_json()
        print("Книга добавлена")

    def delete(self) -> None:
        """Удаляет книгу из библиотеки по ID."""
        if self.check_library():
            return
        try:
            book_id: int = int(input("Введите ID книги для удаления: "))
        except ValueError:
            print("ID должен быть числом")
            return
        for book in self.library:
            if book["id"] == book_id:
                self.library.remove(book)
                self.save_json()
                print("Книга удалена")
                return
        print("Книга с таким ID не найдена")

    def search(self) -> None:
        """Ищет книгу в библиотеке по типу."""
        if self.check_library():
            return
        search_type: str = input("Искать по (title/author/year): ").strip().lower()
        if search_type not in ["title", "author", "year"]:
            print("Выберите 'title', 'author' или 'year'")
            return
        query: str = input("Введите значение для поиска: ").strip()
        if not query:
            print("Поиск пустой")
            return
        results: list[dict] = [
            book for book in self.library
            if str(book.get(search_type, "")).lower() == query.lower()
        ]
        if results:
            self.display(results)
        else:
            print("Книги не найдены")

    def display(self, books=None) -> None:
        """Отображает список книг в библиотеке."""
        books = books if books is not None else self.library
        if self.check_library():
            return
        print("Список книг:")
        for book in books:
            print(f"ID: {book['id']}, Название: {book['title']}, "
                  f"Автор: {book['author']}, Год: {book['year']}, "
                  f"Статус: {book['status']}")

    def change_status(self) -> None:
        """Изменяет статус книги."""
        if self.check_library():
            return
        try:
            book_id: int = int(input("Введите ID книги для изменения статуса: "))
        except ValueError:
            print("ID должен быть числом")
            return
        new_status: str = input(
            "Введите новый статус ('в наличии' или 'выдана'): "
        ).strip().lower()
        if new_status not in ["в наличии", "выдана"]:
            print("Введите 'в наличии' или 'выдана'")
            return
        for book in self.library:
            if book["id"] == book_id:
                book["status"] = new_status
                self.save_json()
                print("Статус книги изменён")
                return
        print("Книга с таким ID не найдена")

    def run(self) -> None:
        """Запускает меню взаимодействия с библиотекой."""
        while True:
            print("\nМеню:\n1. Добавить книгу\n2. Удалить книгу\n"
                  "3. Искать книгу\n4. Отобразить все книги\n"
                  "5. Изменить статус книги\n6. Выход")
            choice: str = input("Выберите действие: ").strip()
            if choice == "1":
                self.add()
            elif choice == "2":
                self.delete()
            elif choice == "3":
                self.search()
            elif choice == "4":
                self.display()
            elif choice == "5":
                self.change_status()
            elif choice == "6":
                print("Выход из программы")
                break
            else:
                print("Некорректный выбор")


if __name__ == "__main__":
    library = Library()
    library.run()
