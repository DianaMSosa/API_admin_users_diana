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

def validate_role(role: str) -> bool:
    if role in ['admin', 'read', 'update_domicilio']:
        return True
    else:
        return False

def validate_username(username: str) -> bool:
    # Sin espacios, sin acentos, sí permite caracteres especiales, no puede estar vacío
    pattern = r'^[A-Za-zÑñ0-9!"#$%&\'()*+,-./:<=>?@[\]^_`{|}~]+$'
    return bool(re.match(pattern, username))

def validate_password(password: str) -> bool:
    # Solo alfanumérico
    # Con espacios, con acentos, sí permite caracteres especiales, no puede estar vacío
    pattern = r'^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9 !"#$%&\'()*+,-./:<=>?@[\]^_`{|}~]+$'
    return bool(re.match(pattern, password)) 

def validate_address(address: str) -> bool:
    # Solo alfanumérico
    # Con espacios, con acentos, sí permite caracteres especiales, no puede estar vacío
    pattern = r'^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9 !"#$%&\'()*+,-./:<=>?@[\]^_`{|}~]+$'
    return bool(re.match(pattern, address)) 