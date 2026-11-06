import mysql.connector
from datetime import date


def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PWD",
        database="lib_mgmt_sys"
    )


def display_books():
    try:
        a = connect_database()
        b = a.cursor()

        b.execute("SELECT * FROM books")
        c = b.fetchall()

        print("\n=== AVAILABLE BOOKS ===")

        if c:
            for d in c:
                print(d)
        else:
            print("NO BOOKS AVAILABLE!")

        b.close()
        a.close()

    except mysql.connector.Error as e:
        print("DATABASE ERROR:", e)


def add_book():
    a = None
    b = None
    print("\n== ADD BOOK DETAILS ==")

    try:
        a = connect_database()
        b = a.cursor()
        c = int(input("Enter Book ID: "))
        d = input("Enter Book Title: ")
        e = input("Enter Author Name: ")
        f = input("Enter Category: ")
        g = float(input("Enter Price: "))
        h = int(input("Enter Quantity: "))

        if g < 0 or h < 0:
            print("PRICE AND QUANTITY CANNOT BE NEGATIVE.")
            return

        i = "INSERT INTO books VALUES (%s, %s, %s, %s, %s, %s)"
        j = (c, d, e, f, g, h)

        b.execute(i, j)
        a.commit()

        print("BOOK ADDED SUCCESSFULLY!")

    except ValueError:
        print("INVALID INPUT. ENTER VALID NUMBERS")

    except mysql.connector.Error as e:
        print("DATABASE ERROR:", e)

    finally:
        if b:
            b.close()
        if a:
            a.close()


def search_book():
    try:
        a = connect_database()
        b = a.cursor()
        c = input("Enter Book Title To Search: ")

        b.execute(
            "SELECT * FROM books WHERE title LIKE %s",
            ("%" + c + "%",)
        )

        d = b.fetchall()

        if d:
            print("\n=== SEARCH RESULTS ===")

            for e in d:
                print(e)
        else:
            print("NO BOOKS FOUND WITH YOUR KEYWORDS!.")

        b.close()
        a.close()

    except mysql.connector.Error as e:
        print("DATABASE ERROR!:", e)


def add_student():
    a = None
    b = None
    print("\n=== ADD STUDENT DETAILS ===")

    try:
        a = connect_database()
        b = a.cursor()
        c = int(input("Enter Student ID: "))
        d = input("Enter Student Name: ")
        e = input("Enter Class: ")
        f = input("Enter Section: ")
        g = input("Enter Phone Number: ")

        h = "INSERT INTO students VALUES (%s, %s, %s, %s, %s)"
        i = (c, d, e, f, g)

        b.execute(h, i)
        a.commit()

        print("STUDENT ADDED SUCCESSFULLY!")

    except ValueError:
        print("Student ID Must Be A Number.")

    except mysql.connector.Error as e:
        print("DATABASE ERROR:", e)

    finally:
        if b:
            b.close()
        if a:
            a.close()


def display_students():
    try:
        a = connect_database()
        b = a.cursor()

        b.execute("SELECT * FROM students")
        c = b.fetchall()

        print("\n=== ALL STUDENTS ===")

        if c:
            for d in c:
                print(d)
        else:
            print("NO STUDENTS ////////")

        b.close()
        a.close()

    except mysql.connector.Error as e:
        print("Database Error:", e)


# DELETE STUDENT

def delete_student():
    a = None
    b = None

    try:
        a = connect_database()
        b = a.cursor()

        c = int(input("Enter Student ID to delete: "))

        b.execute(
            "SELECT * FROM students WHERE student_id = %s",
            (c,)
        )

        d = b.fetchone()

        if d is None:
            print("Student not found.")
            return

        print("\nStudent Details:", d)

        e = input("Confirm deletion? (Y/N): ")

        if e.upper() != "Y":
            print("Deletion cancelled.")
            return

        b.execute(
            "SELECT issue_id FROM issued_books "
            "WHERE student_id = %s AND status = 'Issued'",
            (c,)
        )

        if b.fetchone():
            print("Cannot delete student with an unreturned book.")
            return

        b.execute(
            "DELETE FROM students WHERE student_id = %s",
            (c,)
        )

        a.commit()

        print("Student deleted successfully!")

    except ValueError:
        print("Invalid Student ID.")

    except mysql.connector.Error as e:
        print("Database Error:", e)

    finally:
        if b:
            b.close()
        if a:
            a.close()


# ISSUE BOOK

def issue_book():
    a = None
    b = None

    try:
        a = connect_database()
        b = a.cursor()

        c = int(input("Enter Book ID: "))
        d = int(input("Enter Student ID: "))

        b.execute(
            "SELECT quantity FROM books WHERE book_id = %s",
            (c,)
        )

        e = b.fetchone()

        if e is None:
            print("Book not found.")
            return

        b.execute(
            "SELECT student_id FROM students WHERE student_id = %s",
            (d,)
        )

        f = b.fetchone()

        if f is None:
            print("Student not found.")
            return

        if e[0] <= 0:
            print("Book is currently unavailable.")
            return

        b.execute(
            "INSERT INTO issued_books "
            "(book_id, student_id, issue_date, status) "
            "VALUES (%s, %s, %s, %s)",
            (c, d, date.today(), "Issued")
        )

        b.execute(
            "UPDATE books SET quantity = quantity - 1 "
            "WHERE book_id = %s",
            (c,)
        )

        a.commit()

        print("Book issued successfully!")
        print("Issue Date:", date.today())

    except ValueError:
        print("Book ID and Student ID must be numbers.")

    except mysql.connector.Error as e:
        if a:
            a.rollback()
        print("Database Error:", e)

    finally:
        if b:
            b.close()
        if a:
            a.close()


# RETURN BOOK

def return_book():
    a = None
    b = None

    try:
        a = connect_database()
        b = a.cursor()

        c = int(input("Enter Book ID: "))
        d = int(input("Enter Student ID: "))

        b.execute(
            "SELECT issue_id FROM issued_books "
            "WHERE book_id = %s AND student_id = %s "
            "AND status = 'Issued' ORDER BY issue_id",
            (c, d)
        )

        e = b.fetchone()

        if e is None:
            print("No active issue record found.")
            return

        b.execute(
            "UPDATE issued_books "
            "SET return_date = %s, status = 'Returned' "
            "WHERE issue_id = %s",
            (date.today(), e[0])
        )

        b.execute(
            "UPDATE books SET quantity = quantity + 1 "
            "WHERE book_id = %s",
            (c,)
        )

        a.commit()

        print("Book returned successfully!")
        print("Return Date:", date.today())

    except ValueError:
        print("Book ID and Student ID must be numbers.")

    except mysql.connector.Error as e:
        if a:
            a.rollback()
        print("Database Error:", e)

    finally:
        if b:
            b.close()
        if a:
            a.close()


# UPDATE BOOK

def update_book():
    a = None
    b = None

    try:
        a = connect_database()
        b = a.cursor()

        c = int(input("Enter Book ID to update: "))

        b.execute(
            "SELECT * FROM books WHERE book_id = %s",
            (c,)
        )

        d = b.fetchone()

        if d is None:
            print("Book not found.")
            return

        e = input("Enter New Title: ")
        f = input("Enter New Author: ")
        g = input("Enter New Category: ")
        h = float(input("Enter New Price: "))
        i = int(input("Enter New Quantity: "))

        if h < 0 or i < 0:
            print("Price and quantity cannot be negative.")
            return

        b.execute(
            "UPDATE books SET title = %s, author = %s, "
            "category = %s, price = %s, quantity = %s "
            "WHERE book_id = %s",
            (e, f, g, h, i, c)
        )

        a.commit()

        print("Book updated successfully!")

    except ValueError:
        print("Invalid input.")

    except mysql.connector.Error as e:
        print("Database Error:", e)

    finally:
        if b:
            b.close()
        if a:
            a.close()


# DELETE BOOK

def delete_book():
    a = None
    b = None

    try:
        a = connect_database()
        b = a.cursor()

        c = int(input("Enter Book ID to delete: "))

        b.execute(
            "SELECT * FROM books WHERE book_id = %s",
            (c,)
        )

        d = b.fetchone()

        if d is None:
            print("Book not found.")
            return

        print("\nBook Details:", d)

        e = input("Confirm deletion? (Y/N): ")

        if e.upper() != "Y":
            print("Deletion cancelled.")
            return

        b.execute(
            "SELECT issue_id FROM issued_books "
            "WHERE book_id = %s AND status = 'Issued'",
            (c,)
        )

        if b.fetchone():
            print("Cannot delete a book that has not been returned.")
            return

        b.execute(
            "DELETE FROM books WHERE book_id = %s",
            (c,)
        )

        a.commit()

        print("Book deleted successfully!")

    except ValueError:
        print("Invalid Book ID.")

    except mysql.connector.Error as e:
        print("Database Error:", e)

    finally:
        if b:
            b.close()
        if a:
            a.close()


# VIEW ISSUED BOOKS

def view_issued_books():
    try:
        a = connect_database()
        b = a.cursor()

        c = """
        SELECT
            issued_books.issue_id,
            books.title,
            students.name,
            issued_books.issue_date,
            issued_books.return_date,
            issued_books.status
        FROM issued_books
        INNER JOIN books
            ON issued_books.book_id = books.book_id
        INNER JOIN students
            ON issued_books.student_id = students.student_id
        """

        b.execute(c)
        d = b.fetchall()

        print("\n========== ISSUED BOOKS ==========")

        if d:
            for e in d:
                print(e)
        else:
            print("No issue records found.")

        b.close()
        a.close()

    except mysql.connector.Error as e:
        print("Database Error:", e)


# MAIN MENU

while True:

    print("\n=========================")
    print("LIBRARY MANAGEMENT SYSTEM")
    print("=========================")

    print("1. Display Books")
    print("2. Add Book")
    print("3. Search Book")
    print("4. Add Student")
    print("5. Display Students")
    print("6. Delete Student")
    print("7. Issue Book")
    print("8. Return Book")
    print("9. Update Book")
    print("10. Delete Book")
    print("11. View Issued Books")
    print("12. Exit")

    a = input("\nEnter your choice: ")

    if a == "1":
        display_books()

    elif a == "2":
        add_book()

    elif a == "3":
        search_book()

    elif a == "4":
        add_student()

    elif a == "5":
        display_students()

    elif a == "6":
        delete_student()

    elif a == "7":
        issue_book()

    elif a == "8":
        return_book()

    elif a == "9":
        update_book()

    elif a == "10":
        delete_book()

    elif a == "11":
        view_issued_books()

    elif a == "12":
        print("Thank you for using the Library Management System.")
        break

    else:
        print("Invalid choice. Please enter a number from 1 to 12.")
