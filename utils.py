import re

def validate_date(date_str:str) -> bool:
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date_str))

def validate_amount(amount:str) -> bool:
    return bool(re.match(r"^\d+(\.\d{1,2})?$", amount))