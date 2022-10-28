# -*- coding: utf-8 -*-

def _to_sql_value(value) -> str:
    if isinstance(value, str):
        return f"'{value}'"
    elif isinstance(value, (int, float)):
        return str(value)
