import os
import re
import sys
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from tabulate import tabulate

# Загружаем переменные из .env
load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}

def get_connection():
    """Создаёт и возвращает подключение к PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        sys.exit(1)

def is_select_only(query: str) -> bool:
    """Проверяет, что запрос начинается с SELECT и не содержит опасных ключевых слов."""
    # Удаляем комментарии и лишние пробелы
    clean_query = re.sub(r"--.*$", "", query, flags=re.MULTILINE)
    clean_query = re.sub(r"/\*.*?\*/", "", clean_query, flags=re.DOTALL)
    clean_query = clean_query.strip()

    # Проверяем, что первый значимый токен — SELECT
    if not re.match(r"^\s*SELECT\b", clean_query, re.IGNORECASE):
        return False

    # Запрещаем любые модифицирующие операции
    dangerous_keywords = [
        r"\bDELETE\b",
        r"\bUPDATE\b",
        r"\bINSERT\b",
        r"\bDROP\b",
        r"\bALTER\b",
        r"\bCREATE\b",
        r"\bTRUNCATE\b",
        r"\bREPLACE\b",
        r"\bMERGE\b",
        r"\bGRANT\b",
        r"\bREVOKE\b",
    ]
    for kw in dangerous_keywords:
        if re.search(kw, clean_query, re.IGNORECASE):
            return False
    return True

def add_limit_if_missing(query: str) -> str:
    """Добавляет LIMIT 5, если его нет и запрос — SELECT."""
    # Проверяем, есть ли уже LIMIT или FETCH FIRST
    if re.search(r"\bLIMIT\s+\d+", query, re.IGNORECASE):
        return query
    if re.search(r"\bFETCH\s+(FIRST|NEXT)\s+\d+\s+(ROW|ROWS)\s+ONLY", query, re.IGNORECASE):
        return query

    # Добавляем LIMIT в конец, если нет ORDER BY / GROUP BY / HAVING
    # Простая эвристика: добавляем в самый конец
    return query.strip() + " LIMIT 5"

def execute_and_print(query: str):
    """Выполняет запрос и выводит результат в виде таблицы."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query)
        if cur.description is None:
            print("Запрос выполнен, но не вернул данных (возможно, это не SELECT).")
            return

        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        print("\n Результат:")
        if rows:
            print(tabulate(rows, headers=columns, tablefmt="grid"))
            print(f"\n Всего строк: {len(rows)}")
        else:
            print(" Запрос вернул 0 строк.")
    except Exception as e:
        print(f" Ошибка выполнения запроса: {e}")
    finally:
        cur.close()
        conn.close()

def main():
    print(" Безопасный SQL Runner (только SELECT)")
    user_input = input("Введите SQL-запрос:\n").strip()

    if not user_input:
        print(" Запрос не может быть пустым.")
        return

    # 1. Проверка безопасности
    if not is_select_only(user_input):
        print(" Ошибка: разрешены только SELECT-запросы")
        return

    # 2. Добавляем LIMIT
    final_query = add_limit_if_missing(user_input)

    # 3. Выполняем
    execute_and_print(final_query)

if __name__ == "__main__":
    main()