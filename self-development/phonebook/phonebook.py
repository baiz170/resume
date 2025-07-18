import csv
import psycopg2


def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="phonebook",
            user="madikbaizakov",  
            password="Madik1722"  
        )
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None


def upload_data_from_csv():
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()

            with open('/Users/madikbaizakov/Documents/vscode/PP2/lab10/phonebook/data.csv', 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  
                
                for row in csv_reader:
                    if len(row) == 3:
                        cursor.execute("INSERT INTO contacts (first_name, last_name, phone) VALUES (%s, %s, %s)",
                                       (row[0], row[1], row[2]))
                    else:
                        print(f"Skipping invalid row: {row}")

            conn.commit()
            cursor.close()
            conn.close()
            print("Data uploaded successfully!")
    except Exception as e:
        print(f"Error: {e}")


def insert_contact(first_name, last_name, phone):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO contacts (first_name, last_name, phone) VALUES (%s, %s, %s)",
                           (first_name, last_name, phone))
            conn.commit()
            print(f"Inserted contact: {first_name} {last_name}, {phone}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()


def update_contact(phone, new_first_name=None, new_last_name=None):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            if new_first_name:
                cursor.execute("UPDATE contacts SET first_name = %s WHERE phone = %s", (new_first_name, phone))
            if new_last_name:
                cursor.execute("UPDATE contacts SET last_name = %s WHERE phone = %s", (new_last_name, phone))
            conn.commit()
            print(f"Updated contact with phone: {phone}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()


def delete_contact(phone):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM contacts WHERE phone = %s", (phone,))
            conn.commit()
            print(f"Deleted contact with phone: {phone}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()


def query_contacts():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM contacts")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()


upload_data_from_csv()  

insert_contact("Alice", "Johnson", "5551234567")
insert_contact("Bob", "Miller", "5559876543")

print("All contacts:")
query_contacts()

update_contact("5551234567", new_first_name="Alicia")

print("\nUpdated contacts:")
query_contacts()

delete_contact("5559876543")

print("\nAfter deletion:")
query_contacts()
