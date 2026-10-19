def create_table(metadata, table_name, columns):
    if table_name in metadata:
        return metadata, f'Ошибка: Таблица "{table_name}" уже существует.'
    
    parsed_columns = [{"name": "ID", "type": "int"}]

    for col in columns:
        if ":" not in col:
            return metadata, f'Некорректное значение: {col}. Попробуйте снова.'
        
        parts = col.split(":", 1)
        col_name = parts[0].strip()
        col_type = parts[1].strip()

        if col_type not in ["int", "str", "bool"]:
            return metadata, f'Некорректное значение: {col}. Попробуйте снова.'
            
        parsed_columns.append({"name": col_name, "type": col_type})

    new_metadata = metadata.copy()
    new_metadata[table_name] = parsed_columns
    cols_str = ", ".join([f"{c['name']}:{c['type']}" for c in parsed_columns])

    return new_metadata, f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}.'

def drop_table(metadata, table_name):
    if table_name not in metadata:
        return metadata, f'Ошибка: Таблица "{table_name}" не существует.'

    del metadata[table_name]
    return metadata, f'Таблица "{table_name}" успешно удалена.'