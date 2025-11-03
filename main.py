import streamlit as st
import requests

st.set_page_config(page_title="Smart Library", layout="centered")

st.markdown(
    """
<style>
/* Page-level sizing to cover entire page */
html, body { height: 100%; margin: 0; }
body { background: #0a1628; }
[data-testid="stAppViewContainer"] { min-height: 100%; }
[data-testid="stAppViewContainer"] > .main {
  min-height: 100%;
  padding: 0;
  background: linear-gradient(135deg, #0a1628 0%, #0d1b2a 50%, #0a1628 100%);
  position: relative;
  overflow: visible;
}

/* Remove default Streamlit padding */
.block-container {
    padding-top: 3rem !important;
    padding-bottom: 3rem !important;
    max-width: 1000px !important;
}

/* Animated overlay */
.overlay-radial {
  position: fixed; inset: 0;
  background: radial-gradient(ellipse at top, rgba(34, 211, 238, 0.15), transparent 60%);
  opacity: 0.6; pointer-events: none;
  animation: pulse 8s ease-in-out infinite;
}

/* Glow animation */
@keyframes glow { 
  0%,100% { filter: drop-shadow(0 0 20px rgba(34, 211, 238, .4)); }
  50% { filter: drop-shadow(0 0 35px rgba(34, 211, 238, .6)); } 
}
@keyframes pulse { 
  0%,100% { opacity: .5 } 
  50% { opacity: .75 } 
}
@keyframes fadeIn { 
  from { opacity: 0; transform: translateY(10px);} 
  to { opacity: 1; transform: translateY(0);} 
}
@keyframes scaleIn { 
  from { opacity: 0; transform: scale(.97);} 
  to { opacity: 1; transform: scale(1);} 
}

/* Hero */
.hero { 
  position: relative; 
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  justify-content: center;
  min-height: 50vh; 
  text-align: center; 
  padding: 40px 16px; 
  animation: fadeIn .8s ease both; 
}

.hero-title { 
  font-size: clamp(56px, 10vw, 96px); 
  font-weight: 700; 
  letter-spacing: -0.03em;
  background: linear-gradient(90deg, #22d3ee 0%, #06b6d4 50%, #f59e0b 100%); 
  -webkit-background-clip: text; 
  background-clip: text; 
  color: transparent;
  margin: 0;
  line-height: 1.1;
}

.hero-sub { 
  margin-top: 16px; 
  font-size: clamp(18px, 3vw, 22px); 
  color: rgba(148, 163, 184, 0.9);
  font-weight: 400;
}

.icon-wrap { 
  position: relative; 
  display: inline-flex; 
  align-items: center; 
  justify-content: center; 
  margin-bottom: 24px; 
}

.icon-book { 
  width: 72px; 
  height: 72px; 
  color: #22d3ee; 
  animation: glow 4s ease-in-out infinite; 
}

.icon-blur { 
  position:absolute; 
  inset:0; 
  filter: blur(30px); 
  background: rgba(34, 211, 238, 0.5); 
  border-radius: 50%; 
  opacity:.7; 
  animation: pulse 6s ease-in-out infinite; 
}

/* Card-like search container */
.search-wrap { 
  width: 100%; 
  max-width: 760px; 
  margin: 0 auto; 
  padding: 0 20px; 
  animation: scaleIn .6s ease both; 
}

.search-card { 
  background: rgba(15, 23, 42, 0.6); 
  border: 1px solid rgba(34, 211, 238, 0.1); 
  border-radius: 20px; 
  padding: 20px; 
  box-shadow: 0 20px 40px rgba(0,0,0,.4), 0 0 0 1px rgba(34, 211, 238, 0.05) inset;
  backdrop-filter: blur(10px);
}

/* Make the text input look like the mock (large, rounded, icon) */
.search-card [data-baseweb="input"] input,
.search-card .stTextInput input {
  height: 60px !important;
  border-radius: 16px !important;
  padding-left: 56px !important;
  font-size: 16px !important;
  color: #cbd5e1 !important;
  border: 1px solid rgba(34, 211, 238, 0.2) !important;
  background: rgba(15, 23, 42, 0.8) !important;
  box-shadow: 0 4px 16px rgba(0,0,0,.3);
  transition: all 0.3s ease;
}

.search-card .stTextInput input::placeholder {
  color: rgba(148, 163, 184, 0.6) !important;
}

.search-card .stTextInput {
  position: relative;
}

.search-card .stTextInput:before {
  content: "";
  position: absolute;
  width: 22px; 
  height: 22px; 
  left: 22px; 
  top: 50%; 
  transform: translateY(-50%);
  z-index: 10;
  pointer-events: none;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="none" stroke="%2322d3ee" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>');
  background-size: 22px 22px;
  opacity: .9;
}

.search-card .stTextInput:focus-within input { 
  outline: none !important; 
  box-shadow: 0 0 0 2px rgba(34, 211, 238, .4), 0 8px 24px rgba(0,0,0,.4) !important; 
  border-color: rgba(34, 211, 238, .5) !important; 
}

.muted-hint { 
  margin-top: 20px; 
  text-align: center; 
  color: rgba(148, 163, 184, 0.7); 
  font-size: 15px; 
}

/* Suggestions styling */
.suggestions { 
  margin-top: 12px; 
  display: grid; 
  grid-template-columns: repeat(auto-fill, minmax(180px,1fr)); 
  gap: 10px; 
}

/* Streamlit button overrides for suggestions */
div[data-testid="column"] button {
  width: 100% !important;
  text-align: left !important;
  background: rgba(15, 23, 42, 0.6) !important;
  color: #cbd5e1 !important;
  border: 1px solid rgba(34, 211, 238, 0.15) !important;
  border-radius: 10px !important;
  padding: 10px 14px !important;
  font-size: 14px !important;
  transition: all 0.2s ease !important;
}

div[data-testid="column"] button:hover {
  background: rgba(34, 211, 238, 0.1) !important;
  border-color: rgba(34, 211, 238, 0.4) !important;
  transform: translateY(-1px);
}

/* Borrowed books list */
.borrowed-wrap { 
  margin-top: 32px; 
  background: rgba(15, 23, 42, 0.5); 
  border: 1px solid rgba(34, 211, 238, 0.1); 
  border-radius: 16px; 
  padding: 20px;
  backdrop-filter: blur(10px);
}

.borrowed-wrap h3 {
  color: #22d3ee !important;
  font-size: 20px !important;
  margin-bottom: 16px !important;
}

.borrow-row { 
  display:flex; 
  align-items:center; 
  justify-content: space-between; 
  padding: 12px 16px; 
  border-radius: 12px; 
  border: 1px solid rgba(34, 211, 238, 0.15); 
  background: rgba(15, 23, 42, 0.6); 
  margin-bottom: 10px;
  color: #cbd5e1;
  font-size: 15px;
}

/* Action buttons styling */
.stRadio > div {
  background: rgba(15, 23, 42, 0.5) !important;
  padding: 12px !important;
  border-radius: 12px !important;
  border: 1px solid rgba(34, 211, 238, 0.1) !important;
}

.stRadio label {
  color: #cbd5e1 !important;
}

/* Success/Warning/Error messages */
.stSuccess, .stWarning, .stError {
  background: rgba(15, 23, 42, 0.8) !important;
  border-radius: 12px !important;
  border-left: 4px solid #22d3ee !important;
  color: #cbd5e1 !important;
}

/* Bottom gradient fade */
.bottom-fade { 
  position: fixed; 
  left: 0; 
  right: 0; 
  bottom: 0; 
  height: 120px; 
  background: linear-gradient(to top, #0a1628, transparent); 
  pointer-events: none; 
}

/* Floating book icons */
.floating-books { 
  position: fixed; 
  left: 0; 
  right: 0; 
  bottom: -20px; 
  pointer-events: none; 
  height: 200px; 
  overflow: visible; 
}

.floating-books .book { 
  position: absolute; 
  bottom: 0; 
  opacity: .6; 
}

@keyframes floatUp { 
  from { transform: translateY(0) translateX(0); opacity:.0 } 
  to { transform: translateY(-200px) translateX(10px); opacity:.7 } 
}

.book svg { 
  width: 24px; 
  height: 24px; 
  color: #22d3ee; 
  opacity: .7; 
}

.book.a { left: 12%; animation: floatUp 10s linear infinite; animation-delay: .4s }
.book.b { left: 28%; animation: floatUp 12s linear infinite; animation-delay: 1.5s }
.book.c { left: 44%; animation: floatUp 11s linear infinite; animation-delay: .9s }
.book.d { left: 60%; animation: floatUp 13s linear infinite; animation-delay: 2s }
.book.e { left: 76%; animation: floatUp 10.5s linear infinite; animation-delay: .2s }
.book.f { left: 90%; animation: floatUp 14s linear infinite; animation-delay: 1.3s }
</style>
<div class="overlay-radial"></div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<section class="hero">
  <div class="icon-wrap">
    <svg class="icon-book" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
      <path d="M20 22H6.5A2.5 2.5 0 0 1 4 19.5V5.5A2.5 2.5 0 0 1 6.5 3H20v19Z" />
    </svg>
    <div class="icon-blur"></div>
  </div>
  <h1 class="hero-title">Library</h1>
  <p class="hero-sub">Discover your next great read</p>
</section>
""",
    unsafe_allow_html=True,
)

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


# --- Function to get Google Books suggestions ---
def get_suggestions(query):
    if not query:
        return []
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=5"
        res = requests.get(url, timeout=5)
        data = res.json()
        if "items" in data:
            return [item["volumeInfo"]["title"] for item in data["items"]]
    except Exception:
        return []
    return []


# --- Search box (styled container) ---
st.markdown('<div class="search-wrap"><div class="search-card">', unsafe_allow_html=True)
search = st.text_input("Search for a book", value=st.session_state.search_text, placeholder="Search for a book...", label_visibility="collapsed")

# --- Show suggestions ---
suggestions = get_suggestions(search)
if suggestions:
    st.caption("📚 Suggestions")
    cols = st.columns(min(4, max(1, len(suggestions))))
    for idx, title in enumerate(suggestions):
        c = cols[idx % len(cols)]
        with c:
            if st.button(title, key=f"sugg_{idx}"):
                st.session_state.search_text = title
                st.session_state.selected_book = title
                st.rerun()

st.markdown('<div class="muted-hint">Search through thousands of books</div></div></div>', unsafe_allow_html=True)

# --- Selected book display ---
if st.session_state.selected_book:
    st.success(f"Selected Book: {st.session_state.selected_book}")

    # Borrow / Return section
    option = st.radio("Choose an action:", ["Borrow", "Return"], horizontal=True)

    if st.button("Confirm", use_container_width=True):
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
    st.markdown('<div class="borrowed-wrap">', unsafe_allow_html=True)
    st.markdown("<h3>🧾 Your Borrowed Books</h3>", unsafe_allow_html=True)
    for i, book in enumerate(st.session_state.borrowed_books):
        c1, c2 = st.columns([5, 1])
        with c1:
            st.markdown(f"<div class='borrow-row'>📖 {book}</div>", unsafe_allow_html=True)
        with c2:
            if st.button("Return", key=f"return_{i}"):
                st.session_state.borrowed_books.remove(book)
                st.session_state.last_message = {"type": "success", "msg": f"📘 '{book}' returned successfully!"}
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Bottom gradient fade
st.markdown('<div class="bottom-fade"></div>', unsafe_allow_html=True)

# Floating book icons similar to BookIcons component
st.markdown(
    """
<div class="floating-books">
  <div class="book a">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
      <path d="M20 22H6.5A2.5 2.5 0 0 1 4 19.5V5.5A2.5 2.5 0 0 1 6.5 3H20v19Z" />
    </svg>
  </div>
  <div class="book b">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
      <path d="M20 22H6.5A2.5 2.5 0 0 1 4 19.5V5.5A2.5 2.5 0 0 1 6.5 3H20v19Z" />
    </svg>
  </div>
  <div class="book c">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
      <path d="M20 22H6.5A2.5 2.5 0 0 1 4 19.5V5.5A2.5 2.5 0 0 1 6.5 3H20v19Z" />
    </svg>
  </div>
  <div class="book d">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
      <path d="M20 22H6.5A2.5 2.5 0 0 1 4 19.5V5.5A2.5 2.5 0 0 1 6.5 3H20v19Z" />
    </svg>
  </div>
  <div class="book e">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
      <path d="M20 22H6.5A2.5 2.5 0 0 1 4 19.5V5.5A2.5 2.5 0 0 1 6.5 3H20v19Z" />
    </svg>
  </div>
  <div class="book f">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
      <path d="M20 22H6.5A2.5 2.5 0 0 1 4 19.5V5.5A2.5 2.5 0 0 1 6.5 3H20v19Z" />
    </svg>
  </div>
</div>
""",
    unsafe_allow_html=True,
)