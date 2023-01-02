# to nie jest zadanie na jeden plik

from datetime import date, datetime, timedelta
import json
import jsonpickle
import os

class Reader(object):

    def __init__(self, username, id):
        self.username = username
        self.id = id
        self.list_of_borrowed_books = []  # samo borrowed_books by nie wystarczyło?
        self.list_of_reserved_books = []

    def borrow_book(self):
        Library.list_of_books = Library.deserialize(Menu.books_file)
        Library.list_of_readers = Library.deserialize(Menu.readers_file)
        print("Books that you can borrow")  # proszę iść do WBP przy Rajskiej i wyobrazić sobie wypisanie na ekran wszystkich książek z jednej sali
        [print(book) if not book["is_borrowed"] else book for book in Library.list_of_books]  # czy zwykła pętla nie byłaby czytelniejsza w tym przypadku?
        book_id = int(input("Enter id of a book that you want to borrow: "))
        for book in Library.list_of_books:
            if book["id"] == book_id:
                if book["is_borrowed"]:
                    print("Book is already borrowed, you can reserve it")
                    return
                else:
                    book["is_borrowed"] = True
                    book["borrowing_date"] = str(datetime.now())
                    book["due_date"] = str(datetime.now() + timedelta(weeks=4))
                    self.list_of_borrowed_books.append(book)
                    Library.list_of_readers = [self.__dict__ if reader["id"] == self.id else reader for reader in
                                               Library.list_of_readers]
                    print("You successfully borrowed a book: \ntitle: " + book["title"] + ", author: " + book["author"])
                    Library.serialize(Library.list_of_books, Menu.books_file)
                    Library.serialize(Library.list_of_readers, Menu.readers_file)
                    return

    def reserve_book(self):
        Library.list_of_books = Library.deserialize(Menu.books_file)
        Library.list_of_readers = Library.deserialize(Menu.readers_file)
        print("Books that you can reserve")
        [print(book) if book["is_borrowed"] else book for book in Library.list_of_books]
        book_id = int(input("Enter id of a book that you want to reserve"))
        for book in Library.list_of_books:
            if book["id"] == book_id:
                if not book["is_borrowed"]:
                    print("Book is not borrowed, you don't need to reserve it")
                    return
                else:
                    book["readers_that_reserved_book"].append(self.username)
                    self.list_of_reserved_books.append(book)
                    Library.list_of_readers = [self.__dict__ if reader["id"] == self.id else reader for reader in
                                               Library.list_of_readers]
                    print("You successfully reserved a book: \n" + book["title"] + ", author: " + book["author"])
                    Library.serialize(Library.list_of_books, Menu.books_file)
                    Library.serialize(Library.list_of_readers, Menu.readers_file)
                    return
        else:
            print("Book is not in catalog, you can't reserve it")

    def prolong_rental(self):  # komunikacja z użytkownikiem i logika biznesowa w jednej metodzie
        Library.list_of_books = Library.deserialize(Menu.books_file)
        Library.list_of_readers = Library.deserialize(Menu.readers_file)
        print("Books you have borrowed and can extend their return date")
        for book in self.list_of_borrowed_books:
            print(book)
        book_id = int(input("Write id of a book that you want to extend it return date: "))
        for book in self.list_of_borrowed_books:
            if book["id"] == book_id:
                num_of_weeks = int(input("Enter how many weeks you want to extend your rental by: "))
                if num_of_weeks > 4:
                    print("You can't prolong rental of a book longer than 4 weeks.")
                    return
                elif num_of_weeks < 1:
                    print("You entered number equal or less than 0")
                    return
                else:
                    new_date = datetime.strptime(str(book["due_date"]), "%Y-%m-%d %H:%M:%S.%f")
                    book["due_date"] = str(new_date + timedelta(weeks=num_of_weeks))
                    Library.list_of_books = [book if book2["id"] == book_id else book2 for book2 in
                                               Library.list_of_books]
                    Library.list_of_readers = [self.__dict__ if reader["id"] == self.id else reader for reader in
                                               Library.list_of_readers]
                    print("You succesfully proloned a book for " + str(num_of_weeks) + " weeks more")
                    Library.serialize(Library.list_of_books, Menu.books_file)
                    Library.serialize(Library.list_of_readers, Menu.readers_file)
                    return
        print("You didn't borrow this book so you can't prolong it")

    def dict_to_class_reader(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    @staticmethod
    def check_if_id_unique(id):
        Library.list_of_readers = Library.deserialize(Menu.readers_file)
        for reader in Library.list_of_readers:
            if reader["id"] ==  id:
                return False
        return True


class Book(object):

    def __init__(self, title, author, id):
        self.id = id
        self.title = title
        self.author = author
        self.is_borrowed = False
        self.borrowing_date = None
        self.due_date = None
        self.readers_that_reserved_book = []

    def __str__(self):
        return "title: " + self.title + ", author: " + self.author

    @staticmethod
    def check_if_id_unique(id):
        Library.list_of_books = Library.deserialize(Menu.books_file)
        for book in Library.list_of_books:
            if book["id"] == id:
                return False
        return True


class Librarian(object):

    def __init__(self, name):
        self.name = name

    def accept_return(self):
        Library.list_of_books = Library.deserialize(Menu.books_file)
        Library.list_of_readers = Library.deserialize(Menu.readers_file)
        print("Books that are currently on loan and you can accept their return")
        [print(book) if book["is_borrowed"] else book for book in Library.list_of_books]
        book_id = int(input("Enter id of the book you want to accept a return: "))
        for book in Library.list_of_books:
            if book["id"] == book_id:
                book["borrowing_date"] = None
                book["due_date"] = None
                book["is_borrowed"] = False
                Library.list_of_books = [book if book2["id"] == book_id else book2 for book2 in
                                         Library.list_of_books]
                for reader in Library.list_of_readers:
                    reader["list_of_borrowed_books"] = [readerbook for readerbook in reader["list_of_borrowed_books"] if readerbook["id"] != book_id]
        Library.serialize(Library.list_of_books, Menu.books_file)
        Library.serialize(Library.list_of_readers, Menu.readers_file)

    def add_book_to_catalog(self):
        Library.list_of_books = Library.deserialize(Menu.books_file)
        title = input("Enter title of a book: ")
        author = input("Enter author of a book: ")
        while True:
            id = int(input("Enter book id: "))
            if Book.check_if_id_unique(id):
                break
            else:
                print("Book with this id exist, try again")
        book = Book(title, author, id)
        Library.list_of_books.append(book.__dict__)
        Library.serialize(Library.list_of_books, Menu.books_file)

    def remove_book_from_catalog(self):
        Library.list_of_books = Library.deserialize(Menu.books_file)
        Library.list_of_readers = Library.deserialize(Menu.readers_file)
        id = int(input("Enter id of a book that you want to remove"))
        Library.list_of_books = [book for book in Library.list_of_books if not book["id"] == id]
        for reader in Library.list_of_readers:
            reader["list_of_borrowed_books"] = [readerbook for readerbook in reader["list_of_borrowed_books"] if
                                            readerbook["id"] != id]
        Library.serialize(Library.list_of_books, Menu.books_file)
        Library.serialize(Library.list_of_readers, Menu.readers_file)

    def add_reader(self):
        while True:
            id = int(input("Enter id of a reader that you want to create"))
            if Reader.check_if_id_unique(id):
                break
            else:
                print("User with this id exist, try again")
        username = input("Enter username of a reader that you want to create")
        reader = Reader(username, id)
        Library.list_of_readers = Library.deserialize(Menu.readers_file)
        Library.list_of_readers.append(reader.__dict__)
        Library.serialize(Library.list_of_readers, Menu.readers_file)


class Library(object): # ta klasa ma tylko atrybuty klasowe i metody statyczne
    list_of_books = []
    list_of_readers = []
    list_of_librarians = []
    base_books = [ {
        "id": 1,
        "title": "Potop",
        "author": "Henryk Sienkiewicz",
        "is_borrowed": False,
        "borrowing_date": None,
        "due_date": None,
        "readers_that_reserved_book": []
    },
        {
            "id": 2,
            "title": "Kod Leaonarda da Vinci",
            "author": "Dan Brown",
            "is_borrowed": False,
            "borrowing_date": None,
            "due_date": None,
            "readers_that_reserved_book": []
        }
    ]
    base_readers = [ {
        "username": "adratwa",
        "id": 3,
        "list_of_borrowed_books": [],
        "list_of_reserved_books": []
    }
    ]
    base_librarians = [ {
        "name": "Stefan"
    }
    ]
    @staticmethod
    def add_librarian(librarian):
        Library.list_of_librarians = Library.deserialize(Menu.librarians_file)
        Library.list_of_librarians.append(librarian)
        Library.serialize(Library.list_of_librarians, Menu.librarians_file)

    @staticmethod
    def search_catalog_by_title():
        books = []
        Library.list_of_books = Library.deserialize(Menu.books_file)
        title = input("Enter title of a book, that you want to find: ")
        for book in Library.list_of_books:
            if title.lower() == book["title"].lower():
                books.append(book)
        if books:
            print("Found books:")
            for book in books:
                print(book)
        else:
            print("No book that meets the above requirements was found")

    @staticmethod
    def search_catalog_by_author():
        books = []
        Library.list_of_books = Library.deserialize(Menu.books_file)
        author = input("Enter author of a book, that you want to find: ")
        for book in Library.list_of_books:
            if author.lower() == book["author"].lower():
                books.append(book)
        if books:
            print("Founded books:")
            for book in books:
                print(book)
        else:
            print("No book that meets the above requirements was found")

    @staticmethod
    def search_catalog_by_key_words():
        books = []
        Library.list_of_books = Library.deserialize(Menu.books_file)
        key_word = input("Enter key word of a book, that you want to find: ")
        for book in Library.list_of_books:
            if key_word.lower() in book["title"] or key_word.lower() in book["author"]:
                books.append(book)
        if books:
            print("Founded books:")
            for book in books:
                print(book)
        else:
            print("No book that meets the above requirements was found")

    @staticmethod
    def serialize(objects, filename):
        with open(filename, "w") as file_object:
            json_string_objects = jsonpickle.dumps(objects, unpicklable=False, indent=4)
            file_object.write(json_string_objects)

    @staticmethod
    def deserialize(filename):
        with open(filename, "r") as file_object_readers:
            return json.load(file_object_readers)

    @staticmethod
    def find_reader(username):
        Library.list_of_books = Library.deserialize(Menu.readers_file)
        for reader in Library.list_of_books:
            if username == reader["username"]:
                return reader
        return None

    @staticmethod
    def find_librarian(username):
        Library.list_of_librarians = Library.deserialize(Menu.librarians_file)
        for librarian in Library.list_of_librarians:
            if username == librarian["name"]:
                return librarian
        return None

    def __str__(self):
        books = ""
        for book in Library.list_of_books:
            books = books + str(book) + "\n"
        return books


class Menu:
    readers_file = "readers.json"  # jak się to ma do menu?
    books_file = "books.json"
    librarians_file = "librarians.json"

    @staticmethod
    def universal_menu(options):
        options = list(options.items())
        while True:
            for ind, option in enumerate(options, start=1):
                print("{}. {}".format(ind, option[0]))
            try:
                choice = int(input("Enter a number: "))
                if 0 < choice <= len(options):
                    func, args, kwargs = options[choice - 1][1]
                    return func(*args, **kwargs)
            except ValueError:
                print("You entered wrong number")

    @staticmethod
    def reader_menu():
        username = input("Enter username: ")
        reader_as_dict = Library.find_reader(username)
        if reader_as_dict is None:
            print("There is no user with that username")
            return
        else:
            reader = Reader(reader_as_dict["username"], reader_as_dict["id"])
            reader.dict_to_class_reader(reader_as_dict)
            while True:
                print("Choose what you want to do:")
                Menu.universal_menu({"Borrow a book": (reader.borrow_book, (), {}),
                                     "Reserve a book": (reader.reserve_book, (), {}),
                                     "Extend your rental": (reader.prolong_rental, (), {}),
                                     "Search book by title": (Library.search_catalog_by_title, (), {}),
                                     "Search book by author": (Library.search_catalog_by_author, (), {}),
                                     "Search book by key word": (Library.search_catalog_by_key_words, (), {}),
                                     "Return to main menu": (Menu.main_menu, (), {}),
                                     "Exit": (exit, (1,), {})
                                     })

    @staticmethod
    def librarian_menu():
        username = input("Enter username: ")
        librarian_as_dict = Library.find_librarian(username)
        if librarian_as_dict is None:
            print("There is no librarian with that username")
            return
        else:
            librarian = Librarian(librarian_as_dict["name"])
            while True:
                print("Choose what you want to do: ")
                Menu.universal_menu({"Accept a return": (librarian.accept_return, (), {}),
                                     "Add a new book": (librarian.add_book_to_catalog, (), {}),
                                     "Delete a book": (librarian.remove_book_from_catalog, (), {}),
                                     "Add a new reader": (librarian.add_reader, (), {}),
                                     "Search book by title": (Library.search_catalog_by_title, (), {}),
                                     "Search book by author": (Library.search_catalog_by_author, (), {}),
                                     "Search book by key word": (Library.search_catalog_by_key_words, (), {}),
                                     "Return to main menu": (Menu.main_menu, (), {}),
                                     "Exit": (exit, (1,), {})
                                     })

    @staticmethod
    def main_menu():
        if os.stat(Menu.librarians_file).st_size == 0:
            Library.serialize(Library.base_librarians, Menu.librarians_file)
        if os.stat(Menu.readers_file).st_size == 0:
            Library.serialize(Library.base_readers, Menu.readers_file)
        if os.stat(Menu.books_file).st_size == 0:
            Library.serialize(Library.base_books, Menu.books_file)
        while True:
            print("Welcome in library system, choose as who you want to login")
            Menu.universal_menu({"Librarian": (Menu.librarian_menu, (), {}), "Reader": (Menu.reader_menu, (), {}),
                                 "Exit": (exit, (1,), {})})


if __name__ == "__main__":
    Menu.main_menu()
