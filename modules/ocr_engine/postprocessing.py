import re
from modules.db_manager.crud import validate_format

def verify_format(text: str) -> bool:
    # Проверка по таблице vehicles через CRUD
    return validate_format(text)