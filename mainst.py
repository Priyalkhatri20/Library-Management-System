import streamlit as st
import mysql.connector

# DB Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="priyal767",
        database="library",
        port=3306
    )

# Login Check
def check_login(username, password):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM login WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    con.close()
    return result is not None

# Add Book
def add_book(book_id, title, author, genre):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("INSERT INTO book (book_id, title, author, genre) VALUES (%s, %s, %s, %s)", (book_id, title, author, genre))
    con.commit()
    con.close()

# View Books
def get_all_books():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM book")
    rows = cursor.fetchall()
    con.close()
    return rows

# App UI
st.set_page_config(page_title="Library System", layout="wide")

# Optional Background Image
page_bg_img = '''
<style>
.stApp {
    background-image: url("https://www.voicesofruralindia.org/wp-content/uploads/2021/08/The-Walking-Library_Rahul-Mahale2.jpg");
    background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("📚 Library Management System")

# Login form
if "logged_in" not in st.session_state:
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(username, password):
            st.success("Login successful")
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")
else:
    # Dashboard
    menu = st.sidebar.selectbox("Menu", ["Add Book", "View Books"])

    if menu == "Add Book":
        st.subheader("➕ Add New Book")
        book_id = st.text_input("Book ID")
        title = st.text_input("Title")
        author = st.text_input("Author")
        genre = st.text_input("Genre")
        if st.button("Add Book"):
            add_book(book_id, title, author, genre)
            st.success("Book added successfully!")

    elif menu == "View Books":
        st.subheader("📖 All Books")
        books = get_all_books()
        for b in books:
            st.write(f"📗 ID: {b[0]} | Title: {b[1]} | Author: {b[2]} | Genre: {b[3]}")
