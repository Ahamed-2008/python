class Library:
    def __init__(self, books):
        self.books = books
        self.issuedBooks = []

    def displayAvailableBooks(self):
        print("Books present in this library are: ")
        for book in self.books:
            print(book)

    def borrowBook(self, name):
        borrow = input(f"Do you want to borrow {name}? (y/n): ")
        if borrow == "y":
            if name not in self.books:
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
        for book in self.issuedBooks:
            print(book)


l1 = Library(["book1", "book2", "book3"])
l1.displayAvailableBooks()
while True:
    book = input("Enter the name of the book: ")
    l1.borrowBook(book)
    l1.borrowedbooks()

   



    