## Запуск тестового задания

В директории проекта переименовать `.env.example` в `.env`.


Для запуска проекта из корневой директории выполнить команду:
```
docker-compose up --build
```

---

## Запуск тестов

Для запуска тестов необходимо в директории `/tests/functional` переименовать `.env.example` в `.env`

Запустить тесты можно одним из вариантов:

1. Запуск тестов в docker контейнере \
 \
   Для запуска тестов из директории `tests/functional` выполнить команду: 
   ```
    docker-compose up --build
   ```
2. Запуск тестов локально \
\
 Для запуска необходимо в .env указать настройки приложения и redis,  запущенных локально (или в docker с пробросом портов). \
 Выполнить команду для запуска тестов
    ```
    pytest
    ```
---

## SQL задание 

Решение для PostgreSQL

Первый вариант:

```sql
    UPDATE full_name
    SET status = (
    SELECT short_name.status
    FROM short_name
    WHERE split_part(full_name.name, '.', 1) = short_name."name"

```
Также можно использовать **string_to_array**: `WHERE (string_to_array(full_name."name", '.'))[1] = short_name."name");`

Второй вариант: 

```sql
    UPDATE full_name
    SET status  = short_name.status 
    FROM short_name 
    WHERE split_part(full_name.name, '.', 1) = short_name.name;

```

Решения основываются на идеи взять часть названия до расширения и сопоставить со значениями из таблицы short_name.
Для других субд можно использовать подобные функции.