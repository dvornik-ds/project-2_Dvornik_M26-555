from .constants import VALID_TYPES
from .decorators import confirm_action, handle_db_errors, log_time


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает новую таблицу с указанными столбцами."""
    if table_name in metadata:
        return metadata, f'Ошибка: Таблица "{table_name}" уже существует.'

    parsed_columns = [{"name": "ID", "type": "int"}]
    
    for col in columns:
        if ":" not in col:
            return metadata, f"Некорректное значение: {col}. Попробуйте снова."
        
        parts = col.split(":", 1)
        col_name = parts[0].strip()
        col_type = parts[1].strip()
        
        if col_type not in VALID_TYPES:
            return metadata, f"Некорректное значение: {col}. Попробуйте снова."
            
        parsed_columns.append({"name": col_name, "type": col_type})
        
    new_metadata = metadata.copy()
    new_metadata[table_name] = parsed_columns
    
    cols_str = ", ".join([f"{c['name']}:{c['type']}" for c in parsed_columns])
    message = f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}'
    return new_metadata, message


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет таблицу и все её данные."""
    if table_name not in metadata:
        return metadata, f'Ошибка: Таблица "{table_name}" не существует.'
        
    new_metadata = metadata.copy()
    del new_metadata[table_name]
    return new_metadata, f'Таблица "{table_name}" успешно удалена.'


@handle_db_errors
@log_time
def insert(metadata, table_name, values, current_data):
    """Добавляет новую запись в таблицу."""
    if table_name not in metadata:
        return current_data, f'Ошибка: Таблица "{table_name}" не существует.'
        
    columns = metadata[table_name][1:]
    
    if len(values) != len(columns):
        message = f"Некорректное количество значений. Ожидалось {len(columns)}."
        return current_data, message
        
    new_record = {}
    if not current_data:
        new_record["ID"] = 1
    else:
        new_record["ID"] = max(row["ID"] for row in current_data) + 1
        
    for i, col in enumerate(columns):
        col_name = col["name"]
        col_type = col["type"]
        val = values[i]
        
        if col_type == "int":
            val = int(val)
        elif col_type == "bool":
            val = val.lower() == "true"
            
        new_record[col_name] = val
        
    new_data = list(current_data)
    new_data.append(new_record)
    new_id = new_record["ID"]
    message = f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".'
    return new_data, message


@handle_db_errors
@log_time
def select(table_data, where_clause):
    """Возвращает записи из таблицы, соответствующие условию."""
    if not where_clause:
        return table_data
        
    result = []
    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if str(row.get(key)).lower() != str(value).lower():
                match = False
                break
        if match:
            result.append(row)
    return result


@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Обновляет записи, соответствующие условию."""
    if not where_clause:
        return table_data, "Не задано условие where."
        
    new_data = []
    count = 0
    
    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if str(row.get(key)).lower() != str(value).lower():
                match = False
                break
                
        if match:
            new_row = row.copy()
            for set_key, set_val in set_clause.items():
                if set_key in new_row:
                    if isinstance(new_row[set_key], bool):
                        new_row[set_key] = set_val.lower() == "true"
                    elif isinstance(new_row[set_key], int):
                        new_row[set_key] = int(set_val)
                    else:
                        new_row[set_key] = set_val
            new_data.append(new_row)
            count += 1
        else:
            new_data.append(row)
            
    if count == 0:
        return table_data, "Записи не найдены."
    return new_data, f"Успешно обновлено записей: {count}."


@handle_db_errors
@confirm_action("удаление записи")
def delete(table_data, where_clause):
    """Удаляет записи, соответствующие условию."""
    if not where_clause:
        return table_data, "Не задано условие where."
        
    new_data = []
    deleted_count = 0
    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if str(row.get(key)).lower() != str(value).lower():
                match = False
                break
                
        if match:
            deleted_count += 1
        else:
            new_data.append(row)
            
    if deleted_count == 0:
        return table_data, "Записи не найдены."
    return new_data, f"Успешно удалено записей: {deleted_count}."