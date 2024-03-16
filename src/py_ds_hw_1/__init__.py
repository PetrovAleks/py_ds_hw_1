from collections import UserDict
import pickle
from dataclasses import dataclass  
from datetime import datetime as dt
import os  

@dataclass
class Contact:
    name:str = ""
    phone:str = ""
    birthday:str = ""


def log_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return print(str(e))
    return inner

class BaseField:
    def __init__(self, value):
        if not value:
            raise ValueError(f"{self.__class__.__name__} value is required")
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class Name(BaseField):
    def __init__(self, name):
        super().__init__(name)


class Phone(BaseField):
    def __init__(self, phone):
        if len(phone) < 10:
            raise ValueError("Phone number is too short")
        super().__init__(phone)

class Birthday(BaseField):
    def __call__(self,):
        return self.value
    def __init__(self, birthday:str):
        if not birthday:
            raise Exception("Birthday is required")
        try:
          dt_birthday = dt.strptime(birthday, '%d.%m.%Y')
          super().__init__(dt_birthday.strftime('%d.%m.%Y'))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
     
class Record(UserDict,Birthday):
    __current_directory = os.getcwd()
    __contacts_file = "contacts.txt"

    def get_upcoming_birthdays(self) -> list[Contact]:
        users = self.get_users()
        if not users: raise Exception("No users found")
        upcoming_birthdays = []
        for user in users:
            dt_birthday  = dt.strptime(user['birthday'], '%d.%m.%Y') 
            if dt_birthday.month == dt.now().month and dt_birthday.day > dt.now().day and dt_birthday.weekday()  <= 6:
                upcoming_birthdays.append(user)
        return upcoming_birthdays

    def add_name(self, name):
        self.name = Name(name).value

    def add_phone(self, phone):
        self.phone = Phone(phone).value
        
    def add_birthday(self, name):
        self.name:str = Name(name).value
        if not self.name :
         raise Exception("Name is required")
        contacts:list[Contact] = self.get_users()   
        try:
            with open(self.get_file_path(self.__contacts_file), "wb") as file:
                for i in range(len(contacts)):
                    if self.name.lower() in contacts[i]["name"].lower():
                        birthday = Birthday(input("Enter birthday: ")).value
                        contacts[i]["birthday"] = birthday
                        pickle.dump(contacts,file)
                        print( "User contact changed successfully" ) 
                        return
            raise Exception("User not found")
        except FileNotFoundError as e:
            raise Exception(e)   

    def show_hot_birthdays(self):
        users = self.get_users()
        for user in users:
            if user["birthday"]:
                print(user["name"], user["birthday"])

    def get_users(self)->list[Contact]:
        if not os.path.exists(self.get_file_path(self.__contacts_file)):
            return []
        try:
            with open(self.get_file_path(self.__contacts_file), "rb") as file:
                users = []
                if os.path.getsize(self.get_file_path(self.__contacts_file)) > 0:
                    users =  pickle.load(file)
                return  users
        except FileNotFoundError :
            raise Exception("File not found!")  

    def get_file_path(self,file_name: str)->str:
        return os.path.join(self.__current_directory, file_name)

    def add_user(self):
        users = self.get_users()
    
        if not self.name or not self.name:
            raise  Exception("Name and phone are required")
        try:
            with open(self.get_file_path(self.__contacts_file), "wb") as file:
                contacts_lsit:list[Contact] = [
                    {"name": self.name, "phone": self.phone},
                ]

                if(users):
                    contacts_lsit.extend(users)
                    print("contacts_lsit")
                pickle.dump(contacts_lsit,file)
                print("User added successfully")   
        except FileNotFoundError as e:
            raise Exception("Something went wrong!")

    def change_user_contact(self):
        if not self.name :
            raise Exception("Name is required")
        contacts:list[Contact] = self.get_users()   
        try:
            with open(self.get_file_path(self.__contacts_file), "wb") as file:
                for i in range(len(contacts)):
                    if self.name.lower() in contacts[i]["name"].lower():
                        phone = input("Enter new phone number: ")
                        contacts[i]["phone"] = phone
                        pickle.dump(contacts, file)
                        print( "User contact changed successfully" ) 
                        return
            raise Exception("User not found")
        except FileNotFoundError as e:
            raise Exception(e)    

    def get_user(self, name:str):
        contacts:list[Contact] = self.get_users()   
        try:
            for i in range(len(contacts)):
                if name.lower() in contacts[i]["name"].lower():
                    return contacts[i]
            raise Exception("User not found")
        except FileNotFoundError as e:
            raise Exception(e)
    
    def delete_user(self,name:str):
        contacts:list[Contact] = self.get_users()   
        try:
            with open(self.get_file_path(self.__contacts_file), "wb") as file:
                for i in range(len(contacts)):
                    if name.lower() in contacts[i]["name"].lower():
                        contacts.pop(i)
                        pickle.dump(contacts,file)
                        print( "User deleted successfully" ) 
                        return
            raise Exception("User not found")
        except FileNotFoundError as e:
            raise Exception(e)
        

        
class AddressBook(Record):
    @log_error
    def add_record(self, name, phone):
        self.add_name(name)
        self.add_phone(phone)
        self.add_user()
    @log_error
    def change_phone(self, name):
        self.add_name(name)
        self.change_user_contact()
    @log_error
    def get_phone(self, name):
        try:
           users = self.get_users()
           if not users:
                raise Exception("No users found")
           user:Contact = users.__getattribute__(name)
           print(user["name"], user["phone"])

        except FileNotFoundError as e:
            raise Exception(e)          
    @log_error       
    def print_all_users(self):
        try:
            users = self.get_users()
            if not users:
                raise Exception("No users found")
            for user in users:
                print(user["name"], user["phone"])
        except FileNotFoundError as e:
            raise Exception(e)
        
    @log_error       
    def delete(self, name):
        self.delete_user(name)    

    @log_error
    def add_birthday(self, name):
        return super().add_birthday(name)

    @log_error 
    def show_birthday(self, name):
       user = self.get_user(name)
       print(user["name"], user["birthday"])

    @log_error 
    def  birthdays(self):
        users = super().get_upcoming_birthdays()
        if not users:
            print("No upcoming birthdays")
        for user in users:
                print(user["name"], user["birthday"])
    
    @log_error
    def print_user(self, name):
        user = self.get_user(name)    
        print(user["name"], user["phone"], user["birthday"])
        
    
    class Bot:
        def __init__(self):
            self.book = AddressBook()
        @log_error
        def parse_input(self):
            comand = {
                "1": "Add",
                "2": "Change",
                "3": "All",
                "4": "Delete user",
                "5": "Print user",
                "6": "Hello",
                "7": "Add birthday",
                "8": "Show birthday",
                "9": "Birthdays",
                "10": "Exit"
            }
            for key, value in comand.items():
                print(f"{key}: {value}")
            
            choice = input("How can I help you? Choose a command: ")
            
            if not choice :
                print("Choose a command")
                return   

            choice = choice.lower()
            match choice:
                case "1" | "add":
                    user = input("Enter user name and phone number: ").strip().split(" ")
                    self.book.add_record(user[0], user[1])
                case "2" |"change":
                    user = input("Enter user name : ").strip()
                    self.book.change_phone(user)
                case "3" | "all":
                    self.book.print_all_users()

                case "4" | "delete user":
                    user = input("Enter user name : ").strip()
                    self.book.delete_user(user)

                case "5" | "print user":
                    user = input("Enter user name : ").strip()
                    self.book.print_user(user)

                case "6" | "hello":
                     print("Hello! I'm Halper Bot!")
                     self.parse_input()   
                
                case "7" | "add birthday":
                    user = input("Enter user name: ").strip().split(" ")
                    self.book.add_birthday(user[0])
                
                case "8" | "show birthday":
                    user = input("Enter user name : ").strip()
                    self.book.show_birthday(user)
                
                case "9" | "birthdays":
                    self.book.birthdays()

                case "10" | "exit" | "close" | "quit":
                    print("Goodbye!")
                    exit()
                case _:
                    print("Invalid choice")
                    self.parse_input()
            self.parse_input()   

        def main(self):
            print("Welcome to Halper Bot!")
            self.parse_input()    

def start():
    bot = AddressBook.Bot()
    bot.main()
    
