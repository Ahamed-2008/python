# app.py
import streamlit as st
from dataclasses import dataclass, field

from typing import List, Tuple


@dataclass
class Book:
    title: str
    author: str
    year: int

# -------------------------
# Backend: Library (your logic, polished)
# -------------------------
@dataclass
class Library:
    books: List[Book] = field(default_factory=list)
    issuedBooks: List[str] = field(default_factory=list)  # store titles

    def display_available(self) -> List[Book]:
        return [b for b in self.books if b.title not in self.issuedBooks]

    def borrow(self, name: str) -> Tuple[bool, str]:
        if name == "":
            return False, "No book name provided."
        found = next((b for b in self.books if b.title == name), None)
        if not found:
            return False, f"'{name}' does not exist in the library."
        if name in self.issuedBooks:
            return False, f"'{name}' is already issued."
        self.issuedBooks.append(name)
        return True, f"'{name}' has been borrowed successfully."

    def return_book(self, name: str) -> Tuple[bool, str]:
        if name == "":
            return False, "No book name provided."
        if name in self.issuedBooks:
            self.issuedBooks.remove(name)
            return True, f"'{name}' has been returned successfully."
        return False, f"'{name}' is not currently issued."

    def all_books(self) -> List[Book]:
        return list(self.books)

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Lux Library", page_icon="📚", layout="centered")

# --- CSS for aesthetic luxury look ---
st.markdown(
    """
<style>
/* page background */
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(180deg, #0b0b0b 0%, #121212 100%);
    color: #e9e6e1;
    min-height: 100vh;
}

/* card style */
.card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(192,160,96,0.12);
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.6);
    margin-bottom: 12px;
}

/* headings */
h1, h2, h3 {
    font-family: 'Inter', sans-serif;
    color: #f6f4f0;
}

/* gold accent */
.gold {
    color: #C0A060;
}

/* buttons */
.stButton>button {
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
    background: linear-gradient(90deg, rgba(192,160,96,0.95), rgba(192,160,96,0.85));
    color: #101010;
    border: none;
}

/* inputs */
.stTextInput>div>input, .stTextArea>div>textarea {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    color: #e9e6e1;
    border-radius: 8px;
    padding: 10px;
}

/* list items */
.list-item {
    padding: 8px 10px;
    border-radius: 8px;
    margin-bottom: 6px;
    background: rgba(255,255,255,0.01);
    border: 1px solid rgba(255,255,255,0.02);
}

/* small subdued text */
.small {
    color: rgba(255,255,255,0.55);
    font-size: 13px;
}

/* hover effect for headings */
.hover-underline:hover {
    text-decoration: underline;
    text-decoration-color: #C0A060;
}
</style>
""",
    unsafe_allow_html=True,
)

# top header (title + tagline)
st.markdown("<h1 style='margin-bottom:6px'>📚 Lux Library</h1>", unsafe_allow_html=True)
st.markdown("<div class='small'>Minimal. Quietly premium. Borrow with style.</div>", unsafe_allow_html=True)
st.markdown("---")

# Initialize library in session_state for persistence
if "library" not in st.session_state:
    initial_books = [
        Book("The Great Gatsby", "F. Scott Fitzgerald", 1925),
        Book("To Kill a Mockingbird", "Harper Lee", 1960),
        Book("1984", "George Orwell", 1949),
        Book("Pride and Prejudice", "Jane Austen", 1813),
        Book("The Catcher in the Rye", "J.D. Salinger", 1951),
        Book("Moby-Dick", "Herman Melville", 1851),
        Book("Design Patterns", "Erich Gamma et al.", 1994),
        Book("Clean Code", "Robert C. Martin", 2008),
        Book("Deep Work", "Cal Newport", 2016),
    ]
    st.session_state.library = Library(initial_books)

lib: Library = st.session_state.library

# Layout: two columns (left: available + search; right: borrowed + actions)
col1, col2 = st.columns([2, 1.3], gap="large")

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='gold'>📚 Available Books</h2>", unsafe_allow_html=True)

    search = st.text_input("Search available books", value="", placeholder="Type to filter…")
    available = lib.display_available()
    filtered = [b for b in available if search.lower() in b.title.lower() or search.lower() in b.author.lower()]

    if not filtered:
        st.markdown("<div class='small'>No matching books found.</div>", unsafe_allow_html=True)
    else:
        for b in filtered:
            st.markdown(f"<div class='list-item'><strong>{b.title}</strong> — {b.author} ({b.year})</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("", unsafe_allow_html=True)

    # Optional: show all books (for admin view)
    with st.expander("Show all library books (including issued)", expanded=False):
        for b in lib.all_books():
            tag = " — issued" if b.title in lib.issuedBooks else ""
            color = "#C0A060" if b.title in lib.issuedBooks else "#e9e6e1"
            st.markdown(f"<div class='list-item' style='color:{color}'><strong>{b.title}</strong> — {b.author} ({b.year}){tag}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='gold'>💼 Borrow / Return</h2>", unsafe_allow_html=True)

    action = st.radio("Action", options=["Borrow", "Return"], index=0, horizontal=False)

    book_name = st.text_input("Book name", placeholder="Type the exact book title (case-sensitive)")
    if action == "Borrow":
        if st.button("Borrow Book"):
            success, msg = lib.borrow(book_name.strip())
            if success:
                st.success(msg)
                # little celebration
                st.balloons()
            else:
                st.error(msg)
    else:  # Return
        if st.button("Return Book"):
            success, msg = lib.return_book(book_name.strip())
            if success:
                st.success(msg)
            else:
                st.error(msg)

    st.markdown("<div class='small' style='margin-top:10px'>Tip: You can click 'Borrow' then type the exact name shown on the left (or copy-paste).</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Borrowed books card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='gold'>🧾 Your Borrowed Books</h3>", unsafe_allow_html=True)
    if not lib.issuedBooks:
        st.markdown("<div class='small'>You haven't borrowed any books yet.</div>", unsafe_allow_html=True)
    else:
        for title in lib.issuedBooks:
            book = next((b for b in lib.books if b.title == title), None)
            if book:
                st.markdown(f"<div class='list-item'><strong>{book.title}</strong> — {book.author} ({book.year})</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='list-item'>{title}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div class='small'>Made with minimalist luxury vibes • Try borrowing <span class='gold'>Design Patterns</span> or <span class='gold'>Clean Code</span></div>", unsafe_allow_html=True)
