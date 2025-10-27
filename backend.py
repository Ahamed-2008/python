class Library:
    def __init__(self, books):
        self.books = books
        self.issuedBooks = []

    def displayAvailableBooks(self):
        print("Books present in this library are: ")
        for book in self.books:
            from dataclasses import dataclass
            from typing import List


            @dataclass
            class Book:
                title: str
                author: str
                year: int


            class Library:
                def __init__(self, books: List[Book]):
                    self.books = books
                    self.issuedBooks = []  # store titles

                def displayAvailableBooks(self):
                    print("Books present in this library are: ")
                    for book in self.books:
                        tag = " — issued" if book.title in self.issuedBooks else ""
                        print(f"{book.title} — {book.author} ({book.year}){tag}")

                def borrowBook(self, name):
                    borrow = input(f"Do you want to borrow {name}? (y/n): ")
                    if borrow == "y":
                        found = next((b for b in self.books if b.title == name), None)
                        if not found:
                            print(f"{name} is not available")
                        elif name not in self.issuedBooks:
                            print(f"The book {name} has been successfully borrowed by you")
                            self.issuedBooks.append(name)
                        else:
                            print(f"The book {name} has already been issued to you")
                    else:
                        rtrn = input("Do you want to return this book? (y/n): ")
                        if rtrn == "y":
                            if name in self.issuedBooks:
                                print("You have successfully returned the book")
                                self.issuedBooks.remove(name)
                            else:
                                print(f"The book {name} is not issued to you")

                def borrowedbooks(self):
                    print("Books issued to you are: ")
                    for title in self.issuedBooks:
                        book = next((b for b in self.books if b.title == title), None)
                        if book:
                            print(f"{book.title} — {book.author} ({book.year})")
                        else:
                            print(title)


            l1 = Library([
                Book("The Great Gatsby", "F. Scott Fitzgerald", 1925),
                Book("1984", "George Orwell", 1949),
                Book("Clean Code", "Robert C. Martin", 2008),
            ])

            l1.displayAvailableBooks()
            while True:
                book = input("Enter the name of the book: ")
                l1.borrowBook(book)
                l1.borrowedbooks()

    



