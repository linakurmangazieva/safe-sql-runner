# Безопасный SQL Runner

Простой Python-скрипт для безопасного выполнения SELECT-запросов к PostgreSQL с автоматическим добавлением LIMIT 5.

## Описание

Скрипт подключается к PostgreSQL, принимает SQL-запрос, проверяет, что это только SELECT, автоматически добавляет LIMIT 5 (если его нет), выполняет запрос и выводит результат в виде таблицы.

## Требования

- Python 3.10 или выше
- PostgreSQL (установленный и запущенный)
- Библиотеки из requirements.txt

## Установка

1. Клонируйте репозиторий

git clone https://github.com/ваш_username/safe-sql-runner.git
cd safe-sql-runner

2. Создайте файл .env на основе .env.example

cp .env.example .env

Или создайте вручную файл .env и укажите свои данные:

DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

3. Установите зависимости

pip install -r requirements.txt

## Запуск

python main.py

## Использование

После запуска программа попросит ввести SQL-запрос:

Введите SQL-запрос:

Введите SQL-запрос (только SELECT).

Примеры работы

SELECT с автоматическим добавлением LIMIT 5:

Введите SQL-запрос:
SELECT * FROM students

Выполнится запрос:

SELECT * FROM students LIMIT 5

SELECT с уже существующим LIMIT:

Введите SQL-запрос:
SELECT * FROM students LIMIT 10

Выполнится запрос без изменений (LIMIT 10 останется).

Блокировка DELETE:

Введите SQL-запрос:
DELETE FROM students

Вывод:

Ошибка: разрешены только SELECT-запросы

Блокировка других опасных команд:

- UPDATE
- INSERT
- DROP
- ALTER
- CREATE
- TRUNCATE
- REPLACE
- MERGE
- GRANT
- REVOKE

## Пример вывода

Безопасный SQL Runner (только SELECT)
Введите SQL-запрос:
SELECT * FROM students

Результат:
+----+---------+-----+
| id | name    | age |
+----+---------+-----+
|  1 | Alice   |  20 |
|  2 | Bob     |  22 |
|  3 | Charlie |  21 |
|  4 | Diana   |  23 |
|  5 | Eve     |  20 |
+----+---------+-----+

Всего строк: 5

## Безопасность

- Разрешены только SELECT-запросы
- Автоматически добавляется LIMIT 5 для предотвращения перегрузки БД
- Проверка на опасные ключевые слова
- Обработка ошибок подключения и выполнения

## Тестовые данные для проверки

Создайте тестовую таблицу в PostgreSQL:

CREATE DATABASE test_db;
\c test_db;

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER,
    grade VARCHAR(10)
);

INSERT INTO students (name, age, grade) VALUES
('Alice', 20, 'A'),
('Bob', 22, 'B'),
('Charlie', 21, 'A'),
('Diana', 23, 'C'),
('Eve', 20, 'B'),
('Frank', 24, 'A');

## Технологии

- Python 3.10+
- psycopg2-binary для подключения к PostgreSQL
- python-dotenv для загрузки переменных окружения
- tabulate для красивого вывода таблиц

## Структура проекта

safe-sql-runner/
├── main.py               Основной скрипт
├── requirements.txt      Зависимости
├── .env.example          Пример .env файла
├── .env                  Реальный .env (не в репозитории)
└── README.md             Документация

## Возможные ошибки и их решение

Ошибка: ModuleNotFoundError: No module named 'psycopg2'
Решение: Установите: pip install psycopg2-binary

Ошибка: Ошибка подключения к БД
Решение: Проверьте данные в .env и что PostgreSQL запущен

Ошибка: Ошибка: разрешены только SELECT-запросы
Решение: Используйте только SELECT запросы

Ошибка: Скрипт не видит .env
Решение: Убедитесь, что .env в той же папке, что и main.py

## Лицензия

MIT

