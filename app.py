import streamlit as st
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any
import requests
from requests.exceptions import RequestException
from difflib import get_close_matches

# -------------------------
# Data model
# -------------------------
@dataclass
class Book:
    title: str
    author: str
    year: int = 0

# -------------------------
# Library backend
# -------------------------
@dataclass
class Library:
    books: List[Book] = field(default_factory=list)
    issuedBooks: List[str] = field(default_factory=list)

    def display_available(self) -> List[Book]:
        return [b for b in self.books if b.title not in self.issuedBooks]

    def borrow(self, name: str) -> Tuple[bool, str]:
        name = name.strip()
        if not name:
            return False, "No book name provided."
        found = next((b for b in self.books if b.title.lower() == name.lower()), None)
        if not found:
            return False, f"'{name}' does not exist in the library."
        if found.title in self.issuedBooks:
            return False, f"'{found.title}' is already issued."
        self.issuedBooks.append(found.title)
        return True, f"'{found.title}' has been borrowed successfully."

    def return_book(self, name: str) -> Tuple[bool, str]:
        name = name.strip()
        if not name:
            return False, "No book name provided."
        found = next((t for t in self.issuedBooks if t.lower() == name.lower()), None)
        if found:
            self.issuedBooks.remove(found)
            return True, f"'{found}' has been returned successfully."
        return False, f"'{name}' is not currently issued."

    def all_books(self) -> List[Book]:
        return list(self.books)

# -------------------------
# Google Books API (cached)
# -------------------------
@st.cache_data(show_spinner=False)
def fetch_google_books_suggestions(query: str, max_results: int = 6) -> List[Dict[str, Any]]:
    if not query or not query.strip():
        return []
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": query, "maxResults": max_results}
    try:
        r = requests.get(url, params=params, timeout=6)
        r.raise_for_status()
        data = r.json()
        out = []
        for item in data.get("items", []):
            vi = item.get("volumeInfo", {})
            title = vi.get("title", "Unknown Title")
            authors = vi.get("authors", ["Unknown Author"])
            published = vi.get("publishedDate", "")
            year = 0
            if isinstance(published, str) and len(published) >= 4 and published[:4].isdigit():
                year = int(published[:4])
            out.append({"title": title, "author": authors[0], "year": year})
        return out
    except RequestException as e:
        raise e
    except Exception as e:
        raise e

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Lux Library", page_icon="📚", layout="centered")

# CSS
st.markdown(
    """
<style>
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(180deg, #0b0b0b 0%, #121212 100%);
    color: #e9e6e1;
    min-height: 100vh;
}
.card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(192,160,96,0.12);
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.6);
    margin-bottom: 12px;
}
h1, h2, h3 { font-family: 'Inter', sans-serif; color: #f6f4f0; }
.gold { color: #C0A060; }
.stButton>button { border-radius: 10px; padding: 8px 14px; font-weight: 600;
    background: linear-gradient(90deg, rgba(192,160,96,0.95), rgba(192,160,96,0.85));
    color: #101010; border: none;
}
.stTextInput>div>input { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06);
    color: #e9e6e1; border-radius: 8px; padding: 10px; }
.list-item { padding: 8px 10px; border-radius: 8px; margin-bottom: 6px; background: rgba(255,255,255,0.01);
    border: 1px solid rgba(255,255,255,0.02); }
.small { color: rgba(255,255,255,0.55); font-size: 13px; }
.suggestion { padding:6px 8px; border-radius:8px; margin:4px 2px; display:inline-block; cursor:pointer; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("<h1 style='margin-bottom:6px'>📚 Lux Library</h1>", unsafe_allow_html=True)
st.markdown("<div class='small'>Minimal. Quietly premium. Borrow with style.</div>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session
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
if "last_fetch_error" not in st.session_state:
    st.session_state.last_fetch_error = ""

col1, col2 = st.columns([2, 1.3], gap="large")

# -------------------------
# Column 1: Available Books
# -------------------------
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='gold'>📚 Available Books</h2>", unsafe_allow_html=True)

    if "search_available" not in st.session_state:
        st.session_state.search_available = ""

    search_available = st.text_input("Search available books", key="search_available", placeholder="Type a title or author…")
    available = lib.display_available()
    filtered = available

    q = (search_available or "").strip()
    if q:
        ql = q.lower()
        filtered = [b for b in available if ql in b.title.lower() or ql in b.author.lower()]
        if not filtered:
            titles = [b.title for b in available]
            close = get_close_matches(q, titles, n=6, cutoff=0.4)
            filtered = [b for b in available if b.title in close]

    if not filtered:
        st.markdown("<div class='small'>No matching books found.</div>", unsafe_allow_html=True)
    else:
        for b in filtered:
            st.markdown(f"<div class='list-item'><strong>{b.title}</strong> — {b.author} ({b.year if b.year else '—'})</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Show all library books (including issued)", expanded=False):
        for b in lib.all_books():
            tag = " — issued" if b.title in lib.issuedBooks else ""
            color = "#C0A060" if b.title in lib.issuedBooks else "#e9e6e1"
            st.markdown(f"<div class='list-item' style='color:{color}'><strong>{b.title}</strong> — {b.author} ({b.year if b.year else '—'}){tag}</div>", unsafe_allow_html=True)

# -------------------------
# Column 2: Borrow / Return
# -------------------------
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='gold'>💼 Borrow / Return</h2>", unsafe_allow_html=True)

    action = st.radio("Action", options=["Borrow", "Return"], index=0, horizontal=False)

    if "book_name" not in st.session_state:
        st.session_state.book_name = ""

    prefill_value = st.session_state.get("temp_book_name", "")
    book_name = st.text_input(
        "Book name",
        key="book_name",
        value=prefill_value,
        placeholder="Start typing — local + web suggestions will appear…"
    )
    if "temp_book_name" in st.session_state:
        st.session_state.pop("temp_book_name")

    # Local suggestions
    local_suggestions = []
    q = (book_name or "").strip()
    if q:
        ql = q.lower()
        local_suggestions = [b.title for b in lib.display_available() if ql in b.title.lower() or ql in b.author.lower()][:6]
        if not local_suggestions:
            local_titles = [b.title for b in lib.display_available()]
            local_suggestions = get_close_matches(q, local_titles, n=6, cutoff=0.4)

    if local_suggestions:
        st.caption("Local matches:")
        cols = st.columns(len(local_suggestions))
        for i, s in enumerate(local_suggestions):
            if cols[i].button(s, key=f"local_sugg_{i}"):
                st.session_state.temp_book_name = s
                st.rerun()

    # Google suggestions
    google_suggestions = []
    try:
        if q:
            google_suggestions = fetch_google_books_suggestions(q, max_results=6)
            if google_suggestions:
                st.caption("Web suggestions (Google Books):")
                for i, gs in enumerate(google_suggestions):
                    label = f"{gs['title']} — {gs['author']} ({gs['year'] if gs['year'] else '—'})"
                    if st.button(label, key=f"g_sugg_{i}"):
                        st.session_state.temp_book_name = gs["title"]

                        exists = any(b.title.lower() == gs["title"].lower() for b in lib.books)
                        if not exists:
                            yr = gs.get("year", 0) or 0
                            try:
                                lib.books.append(Book(gs["title"], gs["author"], int(yr) if isinstance(yr, int) or (isinstance(yr, str) and yr.isdigit()) else 0))
                            except Exception:
                                lib.books.append(Book(gs["title"], gs["author"], 0))
                        st.rerun()
    except Exception as e:
        st.session_state.last_fetch_error = str(e)

    # Borrow / Return
    if action == "Borrow":
        if st.button("Borrow Book"):
            success, msg = lib.borrow(book_name.strip())
            if success:
                st.success(msg)
                st.balloons()
            else:
                st.error(msg)
    else:
        if st.button("Return Book"):
            success, msg = lib.return_book(book_name.strip())
            if success:
                st.success(msg)
            else:
                st.error(msg)

    st.markdown("<div class='small' style='margin-top:10px'>Tip: Click a suggestion to autofill the input. Web suggestions come from Google Books.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Borrowed Books
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='gold'>🧾 Your Borrowed Books</h3>", unsafe_allow_html=True)
    if not lib.issuedBooks:
        st.markdown("<div class='small'>You haven't borrowed any books yet.</div>", unsafe_allow_html=True)
    else:
        for title in lib.issuedBooks:
            book = next((b for b in lib.books if b.title == title), None)
            if book:
                st.markdown(f"<div class='list-item'><strong>{book.title}</strong> — {book.author} ({book.year if book.year else '—'})</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='list-item'>{title}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer + Debug
st.markdown("---")
st.markdown("<div class='small'>Made with minimalist luxury vibes • Powered by Google Books API ✨</div>", unsafe_allow_html=True)

with st.expander("Debug & last fetch error (expand if something fails)", expanded=False):
    st.write("Last fetch error (if any):")
    st.text(st.session_state.get("last_fetch_error", "") or "No recorded fetch error.")
    st.write("Session state snapshot:")
    dbg = {k: v for k, v in st.session_state.items() if k in ["search_available", "book_name", "library", "last_fetch_error"]}
    if "library" in dbg and isinstance(dbg["library"], Library):
        dbg["library"] = {"books_count": len(dbg["library"].books), "issued_count": len(dbg["library"].issuedBooks)}
    st.json(dbg)
