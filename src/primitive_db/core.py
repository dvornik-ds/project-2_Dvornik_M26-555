def create_table(metadata, table_name, columns):
    if table_name in metadata:
        return metadata, f'Ошибка: Таблица "{table_name}" уже существует.'

    parsed_columns = [{"name": "ID", "type": "int"}]
    
    for col in columns:
        if ":" not in col:
            return metadata, f"Некорректное значение: {col}. Попробуйте снова."
        
        parts = col.split(":", 1)
        col_name = parts[0].strip()
        col_type = parts[1].strip()
        
        if col_type not in ["int", "str", "bool"]:
            return metadata, f"Некорректное значение: {col}. Попробуйте снова."
            
        parsed_columns.append({"name": col_name, "type": col_type})
        
    new_metadata = metadata.copy()
    new_metadata[table_name] = parsed_columns
    
    cols_str = ", ".join([f"{c['name']}:{c['type']}" for c in parsed_columns])
    return new_metadata, f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}'


def drop_table(metadata, table_name):
    if table_name not in metadata:
        return metadata, f'Ошибка: Таблица "{table_name}" не существует.'
        
    new_metadata = metadata.copy()
    del new_metadata[table_name]
    return new_metadata, f'Таблица "{table_name}" успешно удалена.'


def insert(metadata, table_name, values, current_data):
    if table_name not in metadata:
        return current_data, f'Ошибка: Таблица "{table_name}" не существует.'
        
    columns = metadata[table_name][1:]
    
    if len(values) != len(columns):
        return current_data, f"Некорректное количество значений. Ожидалось {len(columns)}."
        
    new_record = {}
    if not current_data:
        new_record["ID"] = 1
    else:
        new_record["ID"] = max(row["ID"] for row in current_data) + 1
        
    for i, col in enumerate(columns):
        col_name = col["name"]
        col_type = col["type"]
        val = values[i]
        
        try:
            if col_type == "int":
                val = int(val)
            elif col_type == "bool":
                val = val.lower() == "true"
        except ValueError:
            return current_data, f"Некорректное значение: {val}."
            
        new_record[col_name] = val
        
    new_data = list(current_data)
    new_data.append(new_record)
    return new_data, f'Запись с ID={new_record["ID"]} успешно добавлена в таблицу "{table_name}".'


def select(table_data, where_clause):
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


def update(table_data, set_clause, where_clause):
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


def delete(table_data, where_clause):
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