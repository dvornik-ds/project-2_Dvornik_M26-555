[![asciicast](https://asciinema.org/a/87OUByHPkOeCp0tI.svg)](https://asciinema.org/a/87OUByHPkOeCp0tI)
## CRUD-операции
* `insert into <имя> values (<знач1>, <знач2>)` — добавить запись.
* `select from <имя> [where <столбец> = <значение>]` — вывести записи.
* `update <имя> set <столбец> = <значение> where <столбец> = <значение>` — обновить.
* `delete from <имя> where <столбец> = <значение>` — удалить.
* `info <имя>` — информация о таблице.

Пример работы:
```text
>>>Введите команду: create_table users name:str age:int
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int
>>>Введите команду: list_tables
- users
>>>Введите команду: drop_table users
Таблица "users" успешно удалена.