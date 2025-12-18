# Student Information Database
# Matthew Tyler, David Stalmakov, 12/18/2025

import sqlite3

def main():
    conn = sqlite3.connect("student.db")
    cur = conn.cursor()

    # Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            school_id TEXT,
            name TEXT,
            address TEXT,
            major TEXT,
            gpa REAL,
            email TEXT,
            phone TEXT,
            favorite_food TEXT
        )
    """)
    conn.commit()

    quit_program = "n"
    while quit_program != "y":
        display_menu()
        choice = input("Select a choice: ")

        if choice == "1":
            display_record(conn)
        elif choice == "2":
            add_record(conn)
        elif choice == "3":
            edit_record(conn)
        elif choice == "4":
            delete_record(conn)
        elif choice == "5":
            quit_program = "y"
        else:
            print("Invalid choice")

    conn.close()
    print("Program closed.")


def display_record(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Students")
    records = cur.fetchall()

    print("\n--- Student Records ---")
    if not records:
        print("No records found.")
    else:
        for record in records:
            print(record)


def add_record(conn):
    cur = conn.cursor()
    print("\nEnter new student information:")
    school_id = input("School ID: ")
    name = input("Name: ")
    address = input("Address: ")
    major = input("Major: ")

    while True:
        try:
            gpa = float(input("GPA: "))
            break
        except ValueError:
            print("Invalid GPA. Please enter a number.")

    email = input("Email: ")
    phone = input("Phone: ")
    favorite_food = input("Favorite Food: ")

    cur.execute("""
        INSERT INTO Students 
        (school_id, name, address, major, gpa, email, phone, favorite_food)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (school_id, name, address, major, gpa, email, phone, favorite_food))

    conn.commit()
    print("Record added successfully.")


def edit_record(conn):
    cur = conn.cursor()
    display_record(conn)

    try:
        edit_id = int(input("\nEnter the student_id to edit: "))
    except ValueError:
        print("Invalid ID")
        return

    print("\nSelect field to edit:")
    print("1. School ID")
    print("2. Name")
    print("3. Address")
    print("4. Major")
    print("5. GPA")
    print("6. Email")
    print("7. Phone")
    print("8. Favorite Food")

    try:
        choice = int(input("Select field: "))
    except ValueError:
        print("Invalid choice")
        return

    fields = {
        1: "school_id",
        2: "name",
        3: "address",
        4: "major",
        5: "gpa",
        6: "email",
        7: "phone",
        8: "favorite_food"
    }

    if choice not in fields:
        print("Invalid choice")
        return

    if fields[choice] == "gpa":
        try:
            new_value = float(input("Enter new GPA: "))
        except ValueError:
            print("Invalid GPA")
            return
    else:
        new_value = input("Enter new value: ")

    cur.execute(
        f"UPDATE Students SET {fields[choice]} = ? WHERE student_id = ?",
        (new_value, edit_id)
    )

    conn.commit()
    print("Record updated successfully.")


def delete_record(conn):
    cur = conn.cursor()
    display_record(conn)

    try:
        delete_id = int(input("\nEnter the student_id to delete: "))
    except ValueError:
        print("Invalid ID")
        return

    confirm = input("Are you sure you want to delete this record? (y/n): ")
    if confirm.lower() != "y":
        print("Deletion cancelled.")
        return

    cur.execute("DELETE FROM Students WHERE student_id = ?", (delete_id,))
    conn.commit()
    print("Record deleted successfully.")


def display_menu():
    print("\n--- Student Database Menu ---")
    print("1. Display All Student Records")
    print("2. Add a New Student Record")
    print("3. Edit a Student Record")
    print("4. Delete a Student Record")
    print("5. Quit")


if __name__ == "__main__":
    main()