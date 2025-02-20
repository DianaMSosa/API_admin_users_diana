# Documentación API para administración de usuarios

**Descripción general:** Esta API está construida con FastAPI y proporciona un sistema de autenticación y gestión de usuarios. Los usuarios pueden registrarse, autenticarse, y realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre los datos de los usuarios, dependiendo de sus roles. A continuación se detalla la documentación completa de la API, incluyendo los endpoints, modelos de datos, y ejemplos de uso.

Creado por: **Diana Karina Martínez Sosa**

---

## **Tabla de Contenidos**
1. [Requisitos y manual de instalación](#requisitos)
2. [Información relevante para pruebas](#info-pruebas)
3. [Autenticación](#autenticación)
4. [Endpoints](#endpoints)
   - [Obtener Todos los Usuarios](#obtener-todos-los-usuarios)
   - [Crear Usuario](#crear-usuario)
   - [Actualizar Usuario](#actualizar-usuario)
   - [Actualización Parcial de Usuario](#actualización-parcial-de-usuario)
   - [Eliminar Usuario](#eliminar-usuario)
   - [Obtener Domicilios de Usuarios](#obtener-domicilios-de-usuarios)
   - [Actualización únicamente de Domicilio](#actualización-parcial-de-domicilio)
5. [Modelos de Datos](#modelos-de-datos)
6. [Consideraciones de Seguridad](#consideraciones-de-seguridad)

---

## **Requisitos y manual de instalación**

### **Requisitos**

- **Python:** `3.8 o superior`

### **Manual de instalación**

1. Crear una carpeta designada para el proyecto, nombre sugerido: `API_evaluacion_diana`
2. Abrir la terminal y ubicarse en la carpeta del proyecto `API_evaluacion_diana`
    -  **Clonar el repositorio:**
        - Ejecutar: 	**git clone https://github.com/DianaMSosa/API_admin_users_diana.git**
    - **Crear un entorno virtual:**
    Ejemplo con venv
	    - En Windows:
            1.	Ejecutar: 	**python -m venv api_diana_env**
            2.	Ejecutar:	**api_diana_env\Scripts\activate**
            3.	Ejecutar:	**python -m pip install --upgrade pip**
        - En Linux y Mac OS:
            1.	Ejecutar: 	**python -m venv api_diana_env**
                - Nota: En caso de que la versión por defecto sea python 2, se tendría que ejecutar como **python3 -m venv api_diana_env**
            2.	Ejecutar:	**source api_diana_env/bin/activate**
            3.	Ejecutar:	**python -m pip install --upgrade pip**

    Como resultado, la carpeta designada al proyecto tendrá la siguiente estructura:

    ```
    API_evaluacion_diana/
    │── API_admin_users_diana/   # Carpeta con el código de la API
    └── api_diana_env/           # Entorno virtual de Python
    ```

    En el IDE preferido, abrir el repositorio con el código de la API `API_admin_users_diana` y configurar como intérprete el entorno virtual que se creó previamente.
    El repositorio tendrá la siguiente estructura:
    
    ```
    API_admin_users_diana/
    │── Documentacion.md            # Documentación de la API
    │── main.py                     # Archivo principal de la API
    │── README.md                   # Información general del proyecto
    │── requirements.txt            # Dependencias del proyecto
    │── users.json                  # Archivo JSON con datos de usuarios
    └── validators.py               # Módulo para validaciones
    ```

    Y si la configuración del intérprete se hizo correctamente, se verá de una forma similar a:
        `Python 3.12.5('api_diana_env')`
        
    Una vez situados en la carpeta `API_admin_users_diana` y con el entorno virtual correctamente configurado
3. **Instalar las dependencias del proyecto**
    - Ejecutar: **pip install -r requirements.txt**
4. **Ejecutar el proyecto**
    - Ejecutar: **uvicorn main:app --reload**


---

## **Información relevante para pruebas**

FastAPI genera documentación automática basada en las rutas y modelos definidos en la aplicación. Esta documentación se puede acceder de forma interactiva y permite realizar pruebas directamente desde el navegador.  

FastAPI proporciona dos interfaces principales para la documentación:  
- **Swagger UI**: Disponible en `127.0.0.1:8000/docs`, ofrece una interfaz visual para probar los endpoints de la API.  
- **ReDoc**: Disponible en `127.0.0.1:8000/redoc`, presenta la documentación en un formato estructurado y detallado.  

Estas herramientas facilitan la exploración y prueba de la API sin necesidad de herramientas externas.

---
    
## **Autenticación**

La API utiliza OAuth2 con contraseña y tokens JWT para la autenticación. Para acceder a los endpoints protegidos, primero debes obtener un token de acceso.
Los tokens generados tienen una vigencia de 3 horas para fines de suficiencia en las pruebas.

### **Obtener Token de Acceso**

- **Endpoint:** `/token`
- **Método:** `POST`
- **Descripción:** Autentica al usuario y devuelve un token JWT.
- **Request body: Type `x-www-form-urlencoded`**
  - `username`: Username del usuario.
  - `password`: Contraseña del usuario.
- **Respuesta:**
  - `access_token`: Token JWT.
  - `token_type`: Tipo de token (siempre será "bearer").

La base de datos cuenta previamente con 3 usuarios, uno para cada rol existente con el fin de hacer pruebas. Estos son sus datos de acceso:
1. **Usuario con rol de administrador (admin):**
    - `username`:ejemplo_admin
    - `password`:123456
1. **Usuario con rol de lector (read):**
    - `username`:ejemplo_lector
    - `password`:654321
1. **Usuario con rol que permite ver y editar direcciones (update_address):**
    - `username`:ejemplo_editor_direcciones
    - `password`:abcdef

**Ejemplo de Solicitud:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=ejemplo_admin&password=123456'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlamVtcGxvX2FkbWluIiwiZXhwIjoxNzQwMDI5NzAxfQ.zzWybUTA6Yo8Zsoc1bJLHKKorg_ERzOsn0XtWzS5NJw",
  "token_type": "bearer"
}
```

---

## **Endpoints**

---

### **Obtener Todos los Usuarios**

- **Endpoint:** `/users/`
- **Método:** `GET`
- **Descripción:** Devuelve una lista de todos los usuarios con sus respectivas propiedades. 
- **Acceso:** Accesible por usuarios con roles `admin` o `read`.
- **Respuesta:** Lista de usuarios.

Este método no requiere de parámetros adicionales, sin embargo, dado que su acceso es limitado según el rol del usuario, requiere de un token de acceso, el cual debe proporcionarse en la sección de **Headers** con formato `"Authorization: Bearer <TOKEN_DE_ACCESO>"`, o bien, como Bearer Token en la sección de autorización de la herramienta que se esté utilizando. 

**Ejemplo de Solicitud:**
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlamVtcGxvX2FkbWluIiwiZXhwIjoxNzQwMDI5NzAxfQ.zzWybUTA6Yo8Zsoc1bJLHKKorg_ERzOsn0XtWzS5NJw'
```

**Respuesta:**
```json
[
  {
    "username": "ejemplo_admin",
    "role": "admin",
    "curp": "YUHW771101MDGEVS23",
    "cp": "12345",
    "rfc": "GMIR500514PL0",
    "phone": "1234567890",
    "birthdate": "01-01-1990",
    "address": "ejemplo_direccion"
  },
  {
    "username": "ejemplo_lector",
    "role": "read",
    "curp": "GITJ920502HBCCGQ48",
    "cp": "54321",
    "rfc": "VILX690609NE9",
    "phone": "0987654321",
    "birthdate": "15-05-1985",
    "address": "ejemplo_direccion"
  },
  {
    "username": "ejemplo_editor_direcciones",
    "role": "update_address",
    "curp": "EQCO730520HSRGCK21",
    "cp": "67890",
    "rfc": "TMHN210405DS5",
    "phone": "5555555555",
    "birthdate": "20-10-1975",
    "address": "ejemplo_direccion"
  }
]
```

---

### **Crear Usuario**

- **Endpoint:** `/users/`
- **Método:** `POST`
- **Descripción:** Crea un nuevo usuario. 
- **Acceso:** Solo accesible por usuarios con rol `admin`.
- **Request body: Type `application/json`**
  - `username (str)`: Username del usuario (solo caracteres alfanuméricos, además, no puede contener espacios ni acentos).
  - `password (str)`: Contraseña del usuario (solo caracteres alfanuméricos).
  - `role (str)`: Rol del usuario (`admin`, `read`, `update_address`).
  - `curp (str)`: CURP del usuario (formato oficial). 
  - `cp (str)`: Código Postal del usuario (solo caracteres numéricos, 5 dígitos).
  - `rfc (str)`: RFC del usuario (formato oficial).
  - `phone (str)`: Teléfono del usuario (solo caracteres numéricos, 10 dígitos).
  - `birthdate (str)`: Fecha de nacimiento del usuario (formato `dd-mm-yyyy`).
  - `address (str)`: Domicilio del usuario (solo caracteres alfanuméricos).
- **Respuesta:** Devuelve los datos del usuario creado, excluyendo la contraseña.

**Ejemplo de Solicitud:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlamVtcGxvX2FkbWluIiwiZXhwIjoxNzQwMDI5NzAxfQ.zzWybUTA6Yo8Zsoc1bJLHKKorg_ERzOsn0XtWzS5NJw' \
  -H 'Content-Type: application/json' \
  -d ' {
    "username": "ejemplo_post",
    "password": "password123",
    "role": "read",
    "curp": "MASD000611MMCRSNA3",
    "cp": "53710",
    "rfc": "MASD0006113Y0",
    "phone": "5562120122",
    "birthdate": "11-06-2000",
    "address": "ejemplo_direccion"
  }'
```

**Respuesta:**
```json
{
  "username": "ejemplo_post",
  "role": "read",
  "curp": "MASD000611MMCRSNA3",
  "cp": "53710",
  "rfc": "MASD0006113Y0",
  "phone": "5562120122",
  "birthdate": "11-06-2000",
  "address": "ejemplo_direccion"
}
```


---


### **Actualizar Usuario**

- **Endpoint:** `/users/{username}`
- **Método:** `PUT`
- **Descripción:** Actualiza todos los campos de un usuario. 
- **Acceso:** Solo accesible por usuarios con rol `admin`.
- **Parámetros:**
  - `username`: username del usuario a actualizar (se coloca en el URL).
- **Request body: Type `application/json`**
  - `username (str)`: Username del usuario (solo caracteres alfanuméricos, además, no puede contener espacios ni acentos).
  - `password (str)`: Contraseña del usuario (solo caracteres alfanuméricos).
  - `role (str)`: Rol del usuario (`admin`, `read`, `update_address`).
  - `curp (str)`: CURP del usuario (formato oficial). 
  - `cp (str)`: Código Postal del usuario (solo caracteres numéricos, 5 dígitos).
  - `rfc (str)`: RFC del usuario (formato oficial).
  - `phone (str)`: Teléfono del usuario (solo caracteres numéricos, 10 dígitos).
  - `birthdate (str)`: Fecha de nacimiento del usuario (formato `dd-mm-yyyy`).
  - `address (str)`: Domicilio del usuario (solo caracteres alfanuméricos).
- **Respuesta:** Devuelve los datos actualizados del usuario.

**Ejemplo de Solicitud:**
```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/users/ejemplo_post' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlamVtcGxvX2FkbWluIiwiZXhwIjoxNzQwMDI5NzAxfQ.zzWybUTA6Yo8Zsoc1bJLHKKorg_ERzOsn0XtWzS5NJw' \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "ejemplo_put",
    "password": "password123",
    "role": "admin",
    "curp": "MASD000611MMCRSNA3",
    "cp": "53710",
    "rfc": "MASD0006113Y0",
    "phone": "5562120122",
    "birthdate": "11-06-2000",
    "address": "ejemplo_direccion_put"
  }'
```

**Respuesta:**
```json
{
  "username": "ejemplo_put",
  "role": "admin",
  "curp": "MASD000611MMCRSNA3",
  "cp": "53710",
  "rfc": "MASD0006113Y0",
  "phone": "5562120122",
  "birthdate": "11-06-2000",
  "address": "ejemplo_direccion_put"
}
```

---


### **Actualización Parcial de Usuario**

- **Endpoint:** `/users/{username}`
- **Método:** `PATCH`
- **Descripción:** Actualiza campos específicos de un usuario. 
- **Acceso:** Solo accesible por usuarios con rol `admin`.
- **Parámetros:**
  - `username`: username del usuario a actualizar (se coloca en el URL).
- **Request body: Type `application/json`** 
`updates`: Campos a actualizar en formato JSON, todos los campos son **opcionales**.
  - `username (str)`: Username del usuario (solo caracteres alfanuméricos, además, no puede contener espacios ni acentos).
  - `password (str)`: Contraseña del usuario (solo caracteres alfanuméricos).
  - `role (str)`: Rol del usuario (`admin`, `read`, `update_address`).
  - `curp (str)`: CURP del usuario (formato oficial). 
  - `cp (str)`: Código Postal del usuario (solo caracteres numéricos, 5 dígitos).
  - `rfc (str)`: RFC del usuario (formato oficial).
  - `phone (str)`: Teléfono del usuario (solo caracteres numéricos, 10 dígitos).
  - `birthdate (str)`: Fecha de nacimiento del usuario (formato `dd-mm-yyyy`).
  - `address (str)`: Domicilio del usuario (solo caracteres alfanuméricos).
- **Respuesta:** Devuelve los datos actualizados del usuario.

**Ejemplo de Solicitud:**
```bash
curl -X 'PATCH' \
  'http://127.0.0.1:8000/users/ejemplo_put' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlamVtcGxvX2FkbWluIiwiZXhwIjoxNzQwMDI5NzAxfQ.zzWybUTA6Yo8Zsoc1bJLHKKorg_ERzOsn0XtWzS5NJw' \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "ejemplo_patch",
    "password": "password1234567890",
    "role": "read",
    "address": "ejemplo_direccion_patch"
  }'
```

**Respuesta:**
```json
{
  "username": "ejemplo_patch",
  "role": "read",
  "curp": "MASD000611MMCRSNA3",
  "cp": "53710",
  "rfc": "MASD0006113Y0",
  "phone": "5562120122",
  "birthdate": "11-06-2000",
  "address": "ejemplo_direccion_patch"
}
```

---

### **Eliminar Usuario**

- **Endpoint:** `/users/{username}`
- **Método:** `DELETE`
- **Descripción:** Elimina un usuario. 
- **Acceso:** Solo accesible por usuarios con rol `admin`.
- **Parámetros:**
  - `username`: username del usuario a eliminar (se coloca en el URL).
- **Respuesta:** Mensaje de confirmación.

**Ejemplo de Solicitud:**
```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/users/ejemplo_patch' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlamVtcGxvX2FkbWluIiwiZXhwIjoxNzQwMDI5NzAxfQ.zzWybUTA6Yo8Zsoc1bJLHKKorg_ERzOsn0XtWzS5NJw'
```

**Respuesta:**
```json
{
  "message": "Usuario ejemplo_patch eliminado correctamente"
}
```

---

### **Obtener Domicilios de Usuarios**

- **Endpoint:** `/users/domicilio`
- **Método:** `GET`
- **Descripción:** Devuelve una lista de usuarios con solo su username y domicilio. 
- **Acceso:** Accesible por usuarios con roles `admin`, `read`, o `update_address`.
- **Respuesta:** Lista de usuarios con username y domicilio.

**Ejemplo de Solicitud:**
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/users/domicilio' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlamVtcGxvX2FkbWluIiwiZXhwIjoxNzQwMDI5NzAxfQ.zzWybUTA6Yo8Zsoc1bJLHKKorg_ERzOsn0XtWzS5NJw'
```

**Respuesta:**
```json
[
  {
    "username": "ejemplo_admin",
    "address": "ejemplo_direccion"
  },
  {
    "username": "ejemplo_lector",
    "address": "ejemplo_direccion"
  },
  {
    "username": "ejemplo_editor_direcciones",
    "address": "ejemplo_direccion"
  }
]
```

---

### **Actualización únicamente de Domicilio**

- **Endpoint:** `/users/domicilio/{username}`
- **Método:** `PATCH`
- **Descripción:** Actualiza solo el campo de domicilio de un usuario. 
- **Acceso:** Accesible por usuarios con roles `admin` o `update_address`.
- **Parámetros:**
  - `username`: username del usuario a actualizar (se coloca en el URL).
- **Request body: Type `application/json`** 
  - `address (str)`: Domicilio del usuario (solo caracteres alfanuméricos).
- **Respuesta:** Devuelve los datos actualizados del usuario (únicamente username y domicilio).

**Ejemplo de Solicitud:**
```bash
curl -X 'PATCH' \
  'http://127.0.0.1:8000/users/domicilio/ejemplo_lector' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlamVtcGxvX2FkbWluIiwiZXhwIjoxNzQwMDI5NzAxfQ.zzWybUTA6Yo8Zsoc1bJLHKKorg_ERzOsn0XtWzS5NJw' \
  -H 'Content-Type: application/json' \
  -d '{
  "address": "ejemplo_direccion modificada"
}'
```

**Respuesta:**
```json
{
  "username": "ejemplo_lector",
  "address": "ejemplo_direccion modificada"
}
```

---

## **Modelos de Datos**

### **UserCreate**
- **Descripción:** Modelo para la creación de un usuario.
- **Validaciones:** Este modelo contiene validaciones de formato para username, contraseña, rol, curp, cp, rfc, teléfono, fecha y dirección.
- **Campos:**
  - `username`: Nombre de usuario.
  - `password`: Contraseña.
  - `role`: Rol del usuario.
  - `curp`: CURP del usuario.
  - `cp`: Código Postal.
  - `rfc`: RFC del usuario.
  - `phone`: Teléfono.
  - `birthdate`: Fecha de nacimiento.
  - `address`: Domicilio.

### **UserInDB**
- **Descripción:** Modelo para la representación de usuarios en base de datos.
- **Campos:**  Los mismos `UserCreate`, pero cambiando `password` por `hashed_password`, es decir, guarda la contraseña encriptada. 

### **UserUpdate**
- **Descripción:** Modelo para la actualización de un usuario. Todos los campos son opcionales.
- **Validaciones:** Este modelo contiene validaciones de formato para username, contraseña, rol, curp, cp, rfc, teléfono, fecha y dirección.
- **Campos:** Los mismos `UserCreate`, pero todos los campos son opcionales.

### **UserResponse**
- **Descripción:** Modelo para la respuesta de un usuario (sin contraseña).
- **Campos:** Igual que `UserCreate`, excluyendo `password`.

### **UserResponseDomicilio**
- **Descripción:** Modelo para la respuesta de un usuario con solo nombre y domicilio. Utilizado para respuestas con permisos restringidos. 
- **Campos:**
  - `username`: Nombre de usuario.
  - `address`: Domicilio.

### **Token**
- **Descripción:** Modelo para la respuesta del token JWT.
- **Campos:**
  - `access_token`: Token JWT.
  - `token_type`: Tipo de token.

---


## **Consideraciones de Seguridad**

- **Tokens JWT:** Los tokens tienen un tiempo de expiración de 3 horas para fines de pruebas.
- **Roles:** Los usuarios tienen roles específicos que determinan qué operaciones pueden realizar.
- **Validación de Datos:** Los datos de entrada son validados antes de ser procesados.
- **Cifrado de Contraseñas:** Las contraseñas se almacenan cifradas usando bcrypt.

---

Esta documentación proporciona una guía completa para utilizar la API. Para más detalles, consulta el código fuente o ejecuta la API localmente y accede a la documentación interactiva de FastAPI en `http://localhost:8000/docs`.
