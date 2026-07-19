import sqlite3
from data_classes import Book, User

class LibraryManagementSystem:
    def __init__(self, db_location: str):
        self.db_location = db_location
    
    def setup_tables(self):
        try:
            conn : sqlite3.Connection = sqlite3.connect(self.db_location)
            curs : sqlite3.Cursor = conn.cursor()

            # Users Table
            curs.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    street_address TEXT NOT NULL,
                    city_address TEXT NOT NULL,
                    state_address TEXT NOT NULL,
                    zip_address INTEGER NOT NULL,
                    phone_number INTEGER NOT NULL
                )
            """)

            # Genres Table
            curs.execute("""
                CREATE TABLE IF NOT EXISTS genres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            """)

            # Books Table
            curs.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn INTEGER NOT NULL,
                )
            """)

            # Book-Genres Interface Table
            curs.execute("""
                CREATE TABLE IF NOT EXISTS book_genres (
                    book_id INTEGER,
                    genre_id INTEGER,
                    PRIMARY KEY (book_id, genre_id),
                    FOREIGN KEY (book_id) REFERENCES books(id),
                    FOREIGN KEY (genre_id) REFERENCES genres(id)
                )
            """)

            conn.commit()
            print("tables initialized successfully.")
       
        except sqlite3.Error as e:
            conn.rollback()
            print(f"An error occurred: {e}")
        
        finally:
            curs.close()
            conn.close()

    def add_user(self, user: User):
        try:
            conn : sqlite3.Connection = sqlite3.connect(self.db_location)
            curs : sqlite3.Cursor = conn.cursor()

            curs.execute("""
                INSERT INTO users (
                    first_name,
                    last_name,
                    street_address,
                    city_address,
                    state_address,
                    zip_address,
                    phone_number
                ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    user.first_name,
                    user.last_name,
                    user.street_address,
                    user.city_address,
                    user.state_address,
                    user.zip_address,
                    user.phone_number,
                )
            )

            conn.commit()
            print("User added successfully.")
       
        except sqlite3.Error as e:
            conn.rollback()
            print(f"An error occurred: {e}")
        
        finally:
            curs.close()
            conn.close()

    def add_book(self, book: Book):
        try:
            conn : sqlite3.Connection = sqlite3.connect(self.db_location)
            curs : sqlite3.Cursor = conn.cursor()

            # Add book
            curs.execute(
                "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)",
                (book.title, book.author, book.isbn)
            )
            book_id : int = curs.lastrowid

            if len(book.genre) > 0:
                for genre in book.genre:
                    curs.execute(
                        "INSERT OR IGNORE INTO genres (name) VALUES (?)",
                        (genre,)
                    )

                    curs.execute(
                        "SELECT id FROM genres WHERE name = ?",
                        (genre,)
                    )
                    genre_id = curs.fetchone()[0]

                    curs.execute(
                        "INSERT INTO book_genres (book_id, genre_id) VALUES (?, ?)",
                        (book_id, genre_id)
                    )
        
            conn.commit()
            print("Book added successfully.")
       
        except sqlite3.Error as e:
            conn.rollback()
            print(f"An error occurred: {e}")
        
        finally:
            curs.close()
            conn.close()


    def clear_table(self, table_name: str):
        try:
            if not table_name.isidentifier():
                raise ValueError(f"Invalid or unsafe table name: {table_name}")
            
            conn : sqlite3.Connection = sqlite3.connect(self.db_location)
            curs : sqlite3.Cursor = conn.cursor()

            curs.execute(f"DELETE FROM {table_name};")
            conn.commit()
            curs.execute("VACUUM;")
            print(f"Table {table_name} cleared successfully.")
       
        except sqlite3.Error as e:
            conn.rollback()
            print(f"An error occurred: {e}")
        
        finally:
            curs.close()
            conn.close()
