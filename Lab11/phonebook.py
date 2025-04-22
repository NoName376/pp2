import psycopg2
import csv
from tabulate import tabulate

conn = psycopg2.connect(
    host="82.97.250.165", dbname="postgres", user="kbtu", password="kbtu", port=5435
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        phone VARCHAR(255) NOT NULL
    )
""")

conn.commit()

def insert_data():
    choice = input('Введите "csv" для файла или "w" для ручного ввода: ').strip().lower()
    if choice == "w":
        name = input("Имя: ")
        surname = input("Фамилия: ")
        phone = input("Телефон: ")
        cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))
        conn.commit()
    elif choice == "csv":
        filepath = input("Введите путь к CSV файлу: ")
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", row)
        conn.commit()

def update_data():
    column = input("Введите колонку для обновления (name, surname, phone): ").strip().lower()
    old_value = input(f"Введите текущее {column}: ")
    new_value = input(f"Введите новое {column}: ")
    cur.execute(f"UPDATE phonebook SET {column} = %s WHERE {column} = %s", (new_value, old_value))
    conn.commit()

def delete_data():
    phone = input("Введите номер телефона для удаления: ")
    cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()

def query_data():
    column = input("Введите колонку для поиска (id, name, surname, phone): ").strip().lower()
    value = input(f"Введите {column} для поиска: ")
    cur.execute(f"SELECT * FROM phonebook WHERE {column} = %s", (value,))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))

def display_data():
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))

def main():
    commands = {
        "i": insert_data,
        "u": update_data,
        "d": delete_data,
        "q": query_data,
        "s": display_data
    }

    while True:
        print("""
        КОМАНДЫ:
        i - Вставить данные
        u - Обновить данные
        d - Удалить данные
        q - Запрос данных
        s - Показать все записи
        f - Завершить
        """)
        command = input("Выберите команду: ").strip().lower()
        if command == "f":
            break
        elif command in commands:
            commands[command]()
        else:
            print("Неверная команда.")

main()

cur.close()
conn.close()
