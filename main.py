import mysql.connector as mysql
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = mysql.connect (
            host = "138.197.128.55",
            user = "user",
            passwd = "password",
            database = "every_book"
        )
        self.cursor = self.connection.cursor()
        print ("Connected to database...")

database = Database()

def print_results(results):

    print ("------------------------------------------")

    for data in results:
        print (f"{results.index(data) + 1}: {data[0]}, {data[1]}, {data[2]}, {data[3]}")

    print ("------------------------------------------")


def input_data():

    book_name = input("Book Name: ").upper()
    held_by = input("Held By: ").upper()

    database.cursor.execute("SELECT * FROM books WHERE book_name=%s and held_by=%s", (book_name, held_by)) 
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

    database.cursor.execute("SELECT * FROM books WHERE book_name=%s", (book_name,))
    results = database.cursor.fetchall()

    if len(results) == 0:
        print ("No data for that book exists.")
        choice()

    print_results(results)

    choice()


def change_data():
    
    book_name = input("Book Name: ").upper()

    database.cursor.execute("SELECT * FROM books WHERE book_name=%s", (book_name,))
    results = database.cursor.fetchall()

    if len(results) == 0:
        print ("No data for that book exists.")
        choice()

    print_results(results)

    change_choice = input("Type the related row number to select that specific row (eg. 1): ")

    if not change_choice.isdigit():
        print ("That is an invalid input.")
        choice()

    if len(results) < change_choice:
        print ("That is an invalid input.")
        choice()
        
    result = results[change_choice - 1]

    print (f"{result[0]} [1] {result[1]} [2] {result[3]} [3]")

    column = input("Select the column number that correlates to the data: ")

    


def delete_data():

    book_name = input("Book Name: ").upper()

    database.cursor.execute("SELECT * FROM books WHERE book_name=%s", (book_name,))
    results = database.cursor.fetchall()

    if len(results) == 0:
        print ("No data for that book exists.")
        choice()

    print_results(results)

    delete_choice = input("Type 'all' to delete all data for that book or type the related row number to delete that specific row (eg. 1): ")

    if delete_choice == "all":
        statement = "DELETE FROM books WHERE book_name=%s"
        database.cursor.execute(statement, (book_name,))
    elif delete_choice.isdigit():
        delete_choice = int(delete_choice)
        if len(results) >= delete_choice:
            statement = "DELETE FROM books WHERE book_name=%s AND held_by=%s"
            database.cursor.execute(statement, (book_name, results[delete_choice - 1][1]))
        else:
            print ("That is not one of the rows.")
            choice()
    else:
        print ("That is an invalid input.")
        choice()

    database.connection.commit()

    print ("Successfully deleted that/those row(s).")

    choice()

def choice():
    choice = input ("Input Data (1), Read Data (2), Change Data (3), Delete Data (4), Exit (e): ")
    if choice == "1":
        input_data()
    elif choice == "2":
        read_data()
    elif choice == "3":
        change_data()
    elif choice == "4":
        delete_data()
    elif choice == "e":
        exit()
    else:
        print("That is not a proper choice.")
        choice()


choice()
