import streamlit as st
import requests

st.set_page_config(page_title="Smart Library", layout="centered")

st.title("📚 Smart Library Assistant")

# Ensure message state exists before reading it
if "last_message" not in st.session_state:
    st.session_state.last_message = None

# --- Show any pending message from previous action ---
if st.session_state.last_message:
    kind = st.session_state.last_message.get("type")
    msg = st.session_state.last_message.get("msg", "")
    if kind == "success":
        st.success(msg)
    elif kind == "warning":
        st.warning(msg)
    elif kind == "error":
        st.error(msg)
    st.session_state.last_message = None

# --- Initialize session state ---
if "borrowed_books" not in st.session_state:
    st.session_state.borrowed_books = []
if "search_text" not in st.session_state:
    st.session_state.search_text = ""
if "selected_book" not in st.session_state:
    st.session_state.selected_book = None

if "last_message" not in st.session_state:
    st.session_state.last_message = None


# --- Function to get Google Books suggestions ---
def get_suggestions(query):
    if not query:
        return []
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5"
        res = requests.get(url)
        data = res.json()
        if "items" in data:
            return [item["volumeInfo"]["title"] for item in data["items"]]
    except Exception:
        return []
    return []


# --- Search box ---
search = st.text_input("Search for a book", value=st.session_state.search_text)

# --- Show suggestions ---
suggestions = get_suggestions(search)
if suggestions:
    st.write("### Suggestions:")
    for idx, title in enumerate(suggestions):
        if st.button(title, key=f"sugg_{idx}"):
            st.session_state.search_text = title
            st.session_state.selected_book = title
            st.rerun()

# --- Selected book display ---
if st.session_state.selected_book:
    st.success(f"Selected Book: {st.session_state.selected_book}")

    # Borrow / Return section
    option = st.radio("Choose an action:", ["Borrow", "Return"], horizontal=True)

    if st.button("Confirm"):
        book = st.session_state.selected_book
        if option == "Borrow":
            if book not in st.session_state.borrowed_books:
                st.session_state.borrowed_books.append(book)
                st.session_state.last_message = {"type": "success", "msg": f"✅ '{book}' borrowed successfully!"}
            else:
                st.session_state.last_message = {"type": "warning", "msg": f"'{book}' is already borrowed."}
        elif option == "Return":
            if book in st.session_state.borrowed_books:
                st.session_state.borrowed_books.remove(book)
                st.session_state.last_message = {"type": "success", "msg": f"📘 '{book}' returned successfully!"}
            else:
                st.session_state.last_message = {"type": "error", "msg": f"'{book}' has not been borrowed."}

        # Clear selection
        st.session_state.selected_book = None
        st.session_state.search_text = ""
        st.rerun()

# --- Borrowed books list ---
if st.session_state.borrowed_books:
    st.write("## Borrowed Books:")
    for i, book in enumerate(st.session_state.borrowed_books):
        col1, col2 = st.columns([4, 1])
        col1.write(f"📖 {book}")
        if col2.button("Return", key=f"return_{i}"):
            st.session_state.borrowed_books.remove(book)
            st.session_state.last_message = {"type": "success", "msg": f"📘 '{book}' returned successfully!"}
            st.rerun()
