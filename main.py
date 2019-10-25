import mysql.connector as mysql
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = mysql.connect (
            host = "138.197.128.55",
            user = "username",
            passwd = "password",
            database = "every_book"
        )
        self.cursor = self.connection.cursor()
        print ("Connected to database...")

database = Database()

def input_data():

    book_name = input("Book Name: ").upper()
    held_by = input("Held By: ").upper()

    database.cursor.execute(f"SELECT * FROM books WHERE book_name='{book_name}' and held_by='{held_by}'") 
    results = database.cursor.fetchall()

    if len(results) != 0:
        print ("That book data already exists.")
        choice()

    quantity = input("Quantity: ")

    if not quantity.isdigit():
        print ("That must be a proper digit.")
        choice()

    now = datetime.now()

    statement = "INSERT INTO books (book_name, held_by, quantity, date_added) VALUES (%s, %s, %s, %s)"
    values = (book_name, held_by, quantity, now)

    database.cursor.execute(statement, values)
    database.connection.commit()

    print (f"Record inserted of {book_name}, {held_by}, {quantity}, {now}.")

    choice()

def read_data():

    book_name = input("Book Name: ").upper()

    database.cursor.execute(f"SELECT * FROM books WHERE book_name='{book_name}'")
    results = database.cursor.fetchall()

    if len(results) == 0:
        print ("No data for that book exists.")
        choice()

    print ("------------------------------------------")

    for data in results:
        print (f"{data[0]}, {data[1]}, {data[2]}, {data[3]}")

    print ("------------------------------------------")

    choice()

def choice():
    choice = input ("Input Data (1), Read Data (2): ")
    if choice == "1":
        input_data()
    elif choice == "2":
        read_data()
    else:
        print("That is not a proper choice.")
        choice()

choice()
