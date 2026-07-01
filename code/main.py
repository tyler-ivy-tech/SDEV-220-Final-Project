from dataclasses import dataclass
import sqlite3

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
        print("Table initialized successfully.")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

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
                       ) VALUES (?, ?)
                       """, (
                           user.first_name,
                           user.last_name,
                           user.street_address,
                           user.city_address,
                           user.state_address,
                           user.zip_address,
                           user.phone_number
                       ))
        
        conn.commit()
        print("User added successfully.")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def clear_table(conn: sqlite3.Connection, cursor: sqlite3.Cursor, table: str) -> None:
    try:
        cursor.execute(f"DELETE FROM {table};")
        conn.commit()
        cursor.execute("VACUUM;")
        print("Table cleared successfully.")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
    pass




def main() -> None:

    # NOTE: Since using a local db, keeping the connection open for the life of the app *should* be fine. 
    # Opening and closing the connection may be necessary to reduce risk of corruption or inadvertant events
    # on a server-based db

    connection : sqlite3.Connection = sqlite3.connect("local_database.db")
    cursor : sqlite3.Cursor = connection.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   age INTEGER
                   )"""
                   )
    
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
    connection.commit()

    cursor.execute("SELECT * FROM users")
    all_rows = cursor.fetchall()

    for row in all_rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")
    
    connection.close()


if __name__ == "__main__":
    main()
