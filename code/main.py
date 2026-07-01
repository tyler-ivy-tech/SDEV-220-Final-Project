from dataclasses import dataclass
import sqlite3
import os

@dataclass
class Book:
    isbn : int
    title : str
    author : str
    genre : list[str]

@dataclass
class User:
    first_name : str
    last_name : str
    street_address : str
    city_address : str
    state_address : str
    zip_address : int
    phone_number : int

@dataclass
class BookInstance:
    book : Book
    is_checked_out : bool = False
    user : User = None

    def check_out(self, u : User) -> bool:
        if not u:
            return False
        
        if self.is_checked_out:
            return False
        
        self.user = u
        self.is_checked_out = True
        return True

    def check_in(self) -> bool:
        if self.is_checked_out:
            self.is_checked_out = False
            self.person = None
            return True
        else:
            return False


DB_NAME : str = "local_database.db"

def initialize_tables(conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    try:
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        street_address TEXT NOT NULL,
                        city_address TEXT NOT NULL,
                        state_address TEXT NOT NULL,
                        zip_address INTEGER NOT NULL,
                        phone_number INTEGER
                        )
                    """)
        
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS genres (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL
                        )
                    """)

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL
                        )
                    """)
        
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS book_genres (
                        book_id INTEGER,
                        genre_id INTEGER,
                        PRIMARY KEY (book_id, genre_id),
                        FOREIGN KEY (book_id) REFERENCES books(id),
                        FOREIGN KEY (genre_id) REFERENCES genres(id)
                        )
                    """)
        
        conn.commit()
        print("Tables initialized successfully.")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        # cursor.close()
        # conn.close()
        pass

def add_user(conn: sqlite3.Connection, cursor: sqlite3.Cursor, user: User) -> None:
    try:
        cursor.execute("""
                       INSERT INTO users (
                       first_name, 
                       last_name, 
                       street_address, 
                       city_address, 
                       state_address, 
                       zip_address, 
                       phone_number
                       ) VALUES (?, ?, ?, ?, ?, ?, ?)
                       """, (
                           user.first_name,
                           user.last_name,
                           user.street_address,
                           user.city_address,
                           user.state_address,
                           user.zip_address,
                           user.phone_number,
                       ))
        
        conn.commit()
        print("User added successfully.")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        # cursor.close()
        # conn.close()
        pass


def add_book_with_genres(conn: sqlite3.Connection, cursor: sqlite3.Cursor, book: Book) -> None:
    try:
        cursor.execute(f"INSERT INTO books (title, author) VALUES (?, ?);", (book.title, book.author,))
        book_id : int = cursor.lastrowid

        for genre in book.genre:
            # Insert genre if it doesn't already exist
            cursor.execute("INSERT OR IGNORE INTO genres (name) VALUES (?)", (genre,))
            
            # Get the genre_id
            cursor.execute("SELECT id FROM genres WHERE name = ?", (genre,))
            genre_id = cursor.fetchone()[0]

            # Link book and genre
            cursor.execute("INSERT INTO book_genres (book_id, genre_id) VALUES (?, ?)", (book_id, genre_id))

        conn.commit()
        print(f"Book {book.title} added successfully.")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        # cursor.close()
        # conn.close()
        pass


def clear_table(conn: sqlite3.Connection, cursor: sqlite3.Cursor, table_name: str) -> None:
    if not table_name.isidentifier():
        raise ValueError(f"Invalid or unsafe table name: {table_name}")
    
    try:
        cursor.execute(f"DELETE FROM {table_name};")
        conn.commit()
        cursor.execute("VACUUM;")
        print(f"Table {table_name} cleared successfully.")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        # cursor.close()
        # conn.close()
        pass





def main() -> None:

    # HACK: For prototype testing only. Remove.
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Database {DB_NAME} successfully deleted.")
    else:
        print("The database file does not exist.")


    # NOTE: Since using a local db, keeping the connection open for the life of the app *should* be fine. 
    # Opening and closing the connection may be necessary to reduce risk of corruption or inadvertant events
    # on a server-based db

    connection : sqlite3.Connection = sqlite3.connect(DB_NAME)
    cursor : sqlite3.Cursor = connection.cursor()

    initialize_tables(connection, cursor)

    user1 = User("John", "Doe", "123 New Rd", "Pleasantville", "IN", 12345, 5553332121)
    user2 = User("Amy", "Allen", "444 Temple Rd", "Fort Wayne", "IN", 44444, 213465798)

    add_user(connection, cursor, user1)
    add_user(connection, cursor, user2)

    # cursor.execute("""
    #                CREATE TABLE IF NOT EXISTS users (
    #                id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                name TEXT NOT NULL,
    #                age INTEGER
    #                )"""
    #                )
    
    # cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
    # connection.commit()

    cursor.execute("SELECT * FROM users")
    all_rows = cursor.fetchall()

    for row in all_rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")
    
    connection.close()


if __name__ == "__main__":
    main()
