from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from typing import List, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import json
import os
from datetime import datetime, timedelta, timezone
from validators import validate_curp, validate_cp, validate_rfc, validate_phone, validate_date, validate_role, validate_username, validate_password, validate_address

# Configuración de la aplicación
app = FastAPI()

# Configuración de seguridad
SECRET_KEY = "b108f85e34a5c3dd3dd8fd59d891ff83b10996f1f8354f4c0c737be280543d71"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*3

# Contexto de cifrado para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelo de usuario en la base de datos
class UserInDB(BaseModel):
    username: str
    hashed_password: str
    role: str  # Roles: admin, read, update_domicilio
    curp: str
    cp: str
    rfc: str
    phone: str
    birthdate: str
    address: str

# Modelo de usuario para la creación
class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    curp: str
    cp: str
    rfc: str
    phone: str
    birthdate: str
    address: str


    @field_validator('curp')
    def validate_curp(cls, v):
        if not validate_curp(v):
            raise ValueError('Formato de CURP inválido, no coincide con el formato oficial')  
        return v

    @field_validator('cp')
    def validate_cp(cls, v):
        if not validate_cp(v):
            raise ValueError('Formato de Código Postal inválido: El campo debe contener solo caracteres numéricos y ser de 5 digitos')
        return v

    @field_validator('rfc')
    def validate_rfc(cls, v):
        if not validate_rfc(v):
            raise ValueError('Formato de RFC inválido, no coincide con el formato oficial')
        return v

    @field_validator('phone')
    def validate_phone(cls, v):
        if not validate_phone(v):
            raise ValueError('Formato de Teléfono inválido: El campo debe contener solo caracteres numéricos y ser de 10 digitos')
        return v

    @field_validator('birthdate')
    def validate_birthdate(cls, v):
        if not validate_date(v):
            raise ValueError('Formato de Fecha inválido: Debe ser dd-mm-yyyy')
        return v

    @field_validator('role')
    def validate_role(cls, v):
        if not validate_role(v):
            raise ValueError('El rol del usuario solo puede ser una de las siguientes opciones: admin, read, update_domicilio')
        return v

    @field_validator('username')
    def validate_username(cls, v):
        if not validate_username(v):
            raise ValueError('El campo username solo permite caracteres alfanuméricos, además, no puede contener espacios ni acentos, ni estar vacío')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if not validate_password(v):
            raise ValueError('El campo password solo permite caracteres alfanuméricos y no puede estar vacío')
        return v

    @field_validator('address')
    def validate_address(cls, v):
        if not validate_address(v):
            raise ValueError('El campo address solo permite caracteres alfanuméricos y no puede estar vacío')
        return v
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    curp: Optional[str] = None
    cp: Optional[str] = None
    rfc: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[str] = None
    address: Optional[str] = None

    @field_validator('curp')
    def validate_curp(cls, v):
        if v is not None and not validate_curp(v):
            raise ValueError('Formato de CURP inválido...')
        return v

    @field_validator('cp')
    def validate_cp(cls, v):
        if v is not None and not validate_cp(v):
            raise ValueError('Formato de Código Postal inválido...')
        return v

    @field_validator('rfc')
    def validate_rfc(cls, v):
        if v is not None and not validate_rfc(v):
            raise ValueError('Formato de RFC inválido...')
        return v

    @field_validator('phone')
    def validate_phone(cls, v):
        if v is not None and not validate_phone(v):
            raise ValueError('Formato de Teléfono inválido...')
        return v

    @field_validator('birthdate')
    def validate_birthdate(cls, v):
        if v is not None and not validate_date(v):
            raise ValueError('Formato de Fecha inválido...')
        return v

    @field_validator('role')
    def validate_role(cls, v):
        if not validate_role(v):
            raise ValueError('El rol del usuario solo puede ser una de las siguientes opciones: admin, read, update_domicilio')
        return v

# Modelo de usuario para respuesta sin la contraseña
class UserResponse(BaseModel):
    username: str
    role: str
    curp: str
    cp: str
    rfc: str
    phone: str
    birthdate: str
    address: str

# Modelo de usuario para respuesta donde solo se debe ver el domicilio
class UserResponseDomicilio(BaseModel):
    username: str
    address: str

# Modelo de token
class Token(BaseModel):
    access_token: str
    token_type: str

# Modelo de datos de token
class TokenData(BaseModel):
    username: Optional[str] = None

# Configuración de OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # Capturar errores 422 (Unprocessable Entity) y personalizar el mensaje
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=422,
#         content={"detail": "Entidad no procesable. La solicitud es semánticamente incorrecta, contiene datos no válidos o hay parámetros faltantes."},
#     )

# Función para cargar usuarios desde el archivo JSON
def load_users():
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            json.dump([], f)
    with open('users.json', 'r') as f:
        return json.load(f)

# Función para guardar usuarios en el archivo JSON
def save_users(users: List[dict]):
    with open('users.json', 'w') as f:
        json.dump(users, f)

# Función para verificar la contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para obtener el hash de la contraseña
def get_password_hash(password):
    return pwd_context.hash(password)

# Función para obtener un usuario por su nombre de usuario
def get_user(username: str):
    users = load_users()
    user_dict = next((user for user in users if user['username'] == username), None)
    if user_dict:
        return UserInDB.model_validate(user_dict)

# Función para autenticar un usuario
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Función para crear un token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def encontrar_indice_username(lista, username_buscado):
    for indice, usuario in enumerate(lista):
        if usuario['username'] == username_buscado:
            return indice
    return -1  # Retorna -1 si no se encuentra el username

# Función para obtener el usuario actual a partir del token JWT
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Ruta para obtener el token JWT
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta para crear un usuario (solo admin)
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para realizar esta acción")
    users = load_users()
    if any(u['username'] == user.username for u in users):
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    hashed_password = get_password_hash(user.password)
    user_dict = user.model_dump()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    users.append(user_dict)
    save_users(users)
    return UserResponse(**user_dict)

# Ruta para obtener todos los usuarios (admin, read, update_domicilio)
@app.get("/users/", response_model=List[UserResponse])
async def read_users(current_user: UserInDB = Depends(get_current_user)):
    print(current_user.role)
    if current_user.role not in ["admin", "read"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para realizar esta acción")

    users = load_users()

    return [UserResponse(**user) for user in users]

# Ruta para obtener todos los usuarios (admin, read, update_domicilio)
@app.get("/users/domicilio", response_model=List[UserResponseDomicilio])
async def read_users(current_user: UserInDB = Depends(get_current_user)):
    print(current_user.role)
    if current_user.role not in ["admin", "read", "update_address"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para realizar esta acción")

    users = load_users()

    return [UserResponseDomicilio(username=user['username'], address=user['address']) for user in users]

# Ruta para actualizar un usuario (admin)
@app.put("/users/{username}", response_model=UserResponse)
async def update_user(username: str, user: UserCreate, current_user: UserInDB = Depends(get_current_user)):
    if current_user.role not in ["admin"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para realizar esta acción")
    users = load_users()
    user_to_update = next((u for u in users if u['username'] == username), None)
    if not user_to_update:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    hashed_password = get_password_hash(user.password)
    user_to_update.update(user.model_dump())
    user_to_update["hashed_password"] = hashed_password
    del user_to_update["password"]

    save_users(users)
    return UserResponse(**user_to_update)

# Ruta para eliminar un usuario (solo admin)
@app.delete("/users/{username}")
async def delete_user(username: str, current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para realizar esta acción")
    users = load_users()
    user_to_delete = next((u for u in users if u['username'] == username), None)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    users.remove(user_to_delete)
    save_users(users)
    return {"message": f"Usuario {username} eliminado correctamente"}


@app.patch("/users/{username}", response_model=UserResponse)
async def patch_user(username: str, user: UserUpdate, current_user: UserInDB = Depends(get_current_user)):
    # Validar permisos
    if current_user.role not in ["admin"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para realizar esta acción")

    # Buscar el usuario en la base de datos
    users = load_users()
    user_to_update = next((u for u in users if u["username"] == username), None)
    if not user_to_update:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Aplicar solo los campos enviados
    updated_data = user.model_dump(exclude_unset=True)

    if user.password:
        hashed_password = get_password_hash(user.password)
        updated_data["hashed_password"] = hashed_password
        del updated_data["password"]

    user_to_update.update(updated_data)

    indice = encontrar_indice_username(users, username)
    users[indice] = user_to_update
    save_users(users)

    return UserResponse(**user_to_update)

@app.patch("/users/domicilio/{username}", response_model=UserResponseDomicilio)
async def patch_user(username: str, updates: UserUpdate, current_user: UserInDB = Depends(get_current_user)):
    # Validar permisos
    if current_user.role not in ["admin", "update_address"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para realizar esta acción")

    # Buscar el usuario en la base de datos
    users = load_users()
    user_to_update = next((u for u in users if u["username"] == username), None)
    if not user_to_update:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    updates_dict = updates.model_dump()

    # Actualizar solo el campo 'address'
    for key in updates_dict: # cada item es un (name_item, valor)
        if key != 'address' and updates_dict[key] != None:  # Evita agregar campos no válidos
            raise HTTPException(status_code=403, detail="Solo se puede modificar el campo de domicilio")

    user_to_update["address"] = updates.address

    indice = encontrar_indice_username(users, username)
    users[indice] = user_to_update
    save_users(users)

    return UserResponseDomicilio(username=user_to_update['username'], address=user_to_update['address'])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)