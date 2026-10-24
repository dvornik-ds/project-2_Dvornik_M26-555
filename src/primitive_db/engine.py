import shlex
from . import core
from . import utils
from . import parser
from prettytable import PrettyTable

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
            args = shlex.split(user_input, posix=False)
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
                try:
                    import os
                    os.remove(f"data/{table_name}.json")
                except FileNotFoundError:
                    pass
                
        elif command == "insert" and len(args) >= 4 and args[1] == "into":
            table_name = args[2]
            start_idx = user_input.find("(")
            end_idx = user_input.find(")")
            
            if start_idx == -1 or end_idx == -1:
                print("Некорректное значение. Попробуйте снова.")
                continue
                
            values_str = user_input[start_idx+1:end_idx]
            values = [v.strip().strip("\"'") for v in values_str.split(",")]
            
            metadata = utils.load_metadata(db_file)
            current_data = utils.load_table_data(table_name)
            
            new_data, message = core.insert(metadata, table_name, values, current_data)
            print(message)
            if new_data != current_data:
                utils.save_table_data(table_name, new_data)
                
        elif command == "select" and len(args) >= 3 and args[1] == "from":
            table_name = args[2]
            current_data = utils.load_table_data(table_name)
            where_clause = parser.parse_where(args)
            
            result = core.select(current_data, where_clause)
            
            if not result:
                print("Записи не найдены.")
                continue
                
            pt = PrettyTable()
            pt.field_names = list(result[0].keys())
            for row in result:
                pt.add_row([row[k] for k in pt.field_names])
            print(pt)
            
        elif command == "update" and len(args) >= 6:
            table_name = args[1]
            set_clause = parser.parse_set(args)
            where_clause = parser.parse_where(args)
            
            current_data = utils.load_table_data(table_name)
            new_data, message = core.update(current_data, set_clause, where_clause)
            print(message)
            if new_data != current_data:
                utils.save_table_data(table_name, new_data)
                
        elif command == "delete" and len(args) >= 3 and args[1] == "from":
            table_name = args[2]
            where_clause = parser.parse_where(args)
            
            current_data = utils.load_table_data(table_name)
            new_data, message = core.delete(current_data, where_clause)
            print(message)
            if new_data != current_data:
                utils.save_table_data(table_name, new_data)
                
        elif command == "info" and len(args) == 2:
            table_name = args[1]
            metadata = utils.load_metadata(db_file)
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
                
            current_data = utils.load_table_data(table_name)
            cols = metadata[table_name]
            cols_str = ", ".join([f"{c['name']}:{c['type']}" for c in cols])
            
            print(f"Таблица: {table_name}")
            print(f"Столбцы: {cols_str}")
            print(f"Количество записей: {len(current_data)}")
            
        else:
            print(f"Функции {command} нет. Попробуйте снова.")