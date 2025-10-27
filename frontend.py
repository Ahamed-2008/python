import { useState } from "react";
import { BookOpen, BookMarked, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";

interface Book {
  id: string;
  title: string;
  author: string;
  year: number;
}

const INITIAL_BOOKS: Book[] = [
  { id: "1", title: "The Great Gatsby", author: "F. Scott Fitzgerald", year: 1925 },
  { id: "2", title: "To Kill a Mockingbird", author: "Harper Lee", year: 1960 },
  { id: "3", title: "1984", author: "George Orwell", year: 1949 },
  { id: "4", title: "Pride and Prejudice", author: "Jane Austen", year: 1813 },
  { id: "5", title: "The Catcher in the Rye", author: "J.D. Salinger", year: 1951 },
  { id: "6", title: "Moby-Dick", author: "Herman Melville", year: 1851 },
];

const Index = () => {
  const [availableBooks, setAvailableBooks] = useState<Book[]>(INITIAL_BOOKS);
  const [borrowedBooks, setBorrowedBooks] = useState<Book[]>([]);
  const [borrowInput, setBorrowInput] = useState("");
  const { toast } = useToast();

  const handleBorrow = () => {
    const bookToBorrow = availableBooks.find(
      (book) => book.title.toLowerCase().includes(borrowInput.toLowerCase())
    );

    if (!bookToBorrow) {
      toast({
        title: "Book not found",
        description: "Please check the book title and try again.",
        variant: "destructive",
      });
      return;
    }

    setAvailableBooks(availableBooks.filter((b) => b.id !== bookToBorrow.id));
    setBorrowedBooks([...borrowedBooks, bookToBorrow]);
    setBorrowInput("");
    
    toast({
      title: "Book borrowed successfully",
      description: `You borrowed "${bookToBorrow.title}"`,
    });
  };

  const handleReturn = (bookId: string) => {
    const bookToReturn = borrowedBooks.find((b) => b.id === bookId);
    
    if (!bookToReturn) return;

    setBorrowedBooks(borrowedBooks.filter((b) => b.id !== bookId));
    setAvailableBooks([...availableBooks, bookToReturn]);
    
    toast({
      title: "Book returned successfully",
      description: `You returned "${bookToReturn.title}"`,
    });
  };

  return (
    <div className="min-h-screen w-full py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="text-center mb-16">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Sparkles className="w-8 h-8 text-primary" />
            <h1 className="text-5xl font-light tracking-wide">VIT LIBRARY</h1>
            <Sparkles className="w-8 h-8 text-primary" />
          </div>
          <p className="text-muted-foreground text-lg font-light">Your Private Collection</p>
        </header>

        {/* Borrow Section */}
        <section className="mb-16 max-w-2xl mx-auto">
          <h2 className="heading-accent text-2xl font-medium mb-6 flex items-center gap-2">
            <BookMarked className="w-6 h-6 text-primary" />
            Borrow a Book
          </h2>
          <div className="book-card">
            <div className="flex flex-col sm:flex-row gap-4">
              <Input
                type="text"
                placeholder="Enter book title..."
                value={borrowInput}
                onChange={(e) => setBorrowInput(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleBorrow()}
                className="flex-1 bg-background border-border focus:border-primary transition-colors"
              />
              <Button 
                variant="luxury" 
                size="lg" 
                onClick={handleBorrow}
                className="sm:w-auto w-full"
              >
                Borrow Book
              </Button>
            </div>
          </div>
        </section>

        {/* Available Books Section */}
        <section className="mb-16">
          <h2 className="heading-accent text-2xl font-medium mb-6 flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-primary" />
            Available Books
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {availableBooks.map((book) => (
              <div key={book.id} className="book-card">
                <h3 className="text-xl font-medium mb-2">{book.title}</h3>
                <p className="text-muted-foreground mb-1">{book.author}</p>
                <p className="text-sm text-muted-foreground">Published: {book.year}</p>
              </div>
            ))}
          </div>
          {availableBooks.length === 0 && (
            <div className="text-center py-12 text-muted-foreground">
              <BookOpen className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p className="text-lg">All books have been borrowed</p>
            </div>
          )}
        </section>

        {/* Borrowed Books Section */}
        <section>
          <h2 className="heading-accent text-2xl font-medium mb-6 flex items-center gap-2">
            <BookMarked className="w-6 h-6 text-primary" />
            Your Borrowed Books
          </h2>
          <div className="space-y-4">
            {borrowedBooks.map((book) => (
              <div key={book.id} className="book-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h3 className="text-xl font-medium mb-1">{book.title}</h3>
                  <p className="text-muted-foreground">{book.author} • {book.year}</p>
                </div>
                <Button 
                  variant="outline" 
                  onClick={() => handleReturn(book.id)}
                  className="border-primary text-primary hover:bg-primary hover:text-primary-foreground transition-all duration-300 sm:w-auto w-full"
                >
                  Return Book
                </Button>
              </div>
            ))}
          </div>
          {borrowedBooks.length === 0 && (
            <div className="text-center py-12 text-muted-foreground book-card">
              <BookMarked className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p className="text-lg">You haven't borrowed any books yet</p>
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default Index;
