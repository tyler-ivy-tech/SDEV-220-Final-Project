from dataclasses import dataclass

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
