import re
from datetime import datetime

def validate_curp(curp: str) -> bool:
    pattern = r'^([A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[HM](?:AS|B[CS]|C[CLMSH]|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]|T[CSL]|VZ|YN|ZS)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$'
    return bool(re.match(pattern, curp))

def validate_cp(cp: str) -> bool:
    return cp.isdigit() and len(cp) == 5

def validate_rfc(rfc: str) -> bool:
    pattern = r'^([A-ZÑ&]{3,4})\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])([A-Z\d]{3})$'
    return bool(re.match(pattern, rfc))

def validate_phone(phone: str) -> bool:
    return phone.isdigit() and len(phone) == 10

def validate_date(date: str) -> bool:
    try:
        datetime.strptime(date, '%d-%m-%Y')
        return True
    except ValueError:
        return False
    