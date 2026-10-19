import shlex
from . import core
from . import utils


def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    db_file = "db_meta.json"

    while True:
        user_input = input(">>>Введите команду: ").strip()
        if not user_input:
            continue
            
        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Некорректное значение: ошибка в кавычках. Попробуйте снова.")
            continue
            
        command = args[0].strip().lower()
        
        if command == "exit":
            break
        elif command == "help":
            print_help()
        elif command == "list_tables":
            metadata = utils.load_metadata(db_file)
            if not metadata:
                print("Список таблиц пуст.")
            else:
                for table in metadata:
                    print(f"- {table}")
        elif command == "create_table":
            if len(args) < 3:
                print("Некорректное значение. Попробуйте снова.")
                continue
            table_name = args[1]
            columns = args[2:]
            metadata = utils.load_metadata(db_file)
            new_metadata, message = core.create_table(metadata, table_name, columns)
            print(message)
            if new_metadata != metadata:
                utils.save_metadata(db_file, new_metadata)
        elif command == "drop_table":
            if len(args) != 2:
                print("Некорректное значение. Попробуйте снова.")
                continue
            table_name = args[1]
            metadata = utils.load_metadata(db_file)
            new_metadata, message = core.drop_table(metadata, table_name)
            print(message)
            if new_metadata != metadata:
                utils.save_metadata(db_file, new_metadata)
        else:
            print(f"Функции {command} нет. Попробуйте снова.")