import psycopg2


conn = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="madikbaizakov",
    password="Madik1722"
)
cur = conn.cursor()


def add_contact(name, phone):
    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    print("✅ Контакт добавлен!")


def get_all_contacts():
    cur.execute("SELECT * FROM contacts")
    contacts = cur.fetchall()
    if not contacts:
        print("📭 Список контактов пуст.")
    else:
        for c in contacts:
            print(f"ID: {c[0]}, Name: {c[1]}, Phone: {c[2]}")


def update_contact(contact_id, new_name, new_phone):
    cur.execute("UPDATE contacts SET name=%s, phone=%s WHERE id=%s", (new_name, new_phone, contact_id))
    conn.commit()
    print("✏️ Контакт обновлён.")


def delete_contact(contact_id):
    cur.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
    conn.commit()
    print("🗑️ Контакт удалён.")


def find_contact_by_name(name):
    cur.execute("SELECT * FROM contacts WHERE name ILIKE %s", ('%' + name + '%',))
    results = cur.fetchall()
    if not results:
        print("🙈 Контакт не найден.")
    else:
        for c in results:
            print(f"ID: {c[0]}, Name: {c[1]}, Phone: {c[2]}")

def menu():
    while True:
        print("\n📱 PhoneBook Меню:")
        print("1. Добавить контакт")
        print("2. Показать все контакты")
        print("3. Обновить контакт")
        print("4. Удалить контакт")
        print("5. Найти контакт по имени")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Имя: ")
            phone = input("Телефон: ")
            add_contact(name, phone)
        elif choice == "2":
            get_all_contacts()
        elif choice == "3":
            contact_id = input("ID контакта для обновления: ")
            new_name = input("Новое имя: ")
            new_phone = input("Новый телефон: ")
            update_contact(contact_id, new_name, new_phone)
        elif choice == "4":
            contact_id = input("ID контакта для удаления: ")
            delete_contact(contact_id)
        elif choice == "5":
            name = input("Введите имя для поиска: ")
            find_contact_by_name(name)
        elif choice == "0":
            print("👋 Выход из программы.")
            break
        else:
            print("❗ Неверный ввод. Повторите.")

    cur.close()
    conn.close()


if __name__ == "__main__":
    menu()
