from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel # esquema/modelo para el usuario
from typing import Union # para especificar mas de un tipo de datos para los atributo class user(BaseModel)
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer("/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # para descodificar la password hashed_password para este tipo de encryption


# no deberian de estar aqui, deberian de estar en una variable externa en archivo externo
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf" 
ALGORITHM = "HS256"

class User(BaseModel): # atributos que necesita el usuario y esta clase es para los usuarios generales
    username: str 
    full_name: Union[str, None] = None 
    email: Union[str, None] = None 
    disabled: Union[bool, None] = None 

class userInDB(User): # para los usuarios que ya estan dentro de la base de datos
    hashed_password: str
    


def get_user(db, username): # funcion que nos va a traer el usuario
    if username in db: # quiere decir que tenemos al usuario dentro de la base de datos
        user_data = db[username] #devuelve los datos del usuario
        return userInDB(**user_data) #**sera completado todos sus datos con lo que este en user_data
    return [] #sino consigue al usuario retorna un array basio 

def verify_password(plane_password, hashed_password):
    return pwd_context.verify(plane_password, hashed_password) # verificamos el que password sea igual al hashed password de la base de datos
                                                                # retorna true o false
def authenticate_user(db, username, password):
    user = get_user(db, username)
    if not user: # entra en el if si retorna basio []
        raise HTTPException(status_code=401 , detail="Could not validate credentials", headers=
                            {"WWW-Authenticate": "Bearer"})
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401 , detail="Could not validate credentials", headers=
                            {"WWW-Authenticate": "Bearer"})
    #si pasa el usuario y contraseña pasa a el usuario
    return user

def create_token(data: dict, time_expires: Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expires is None:
        expires =datetime.utcnow() + timedelta(minutes=15) #utcnow la hora actual
    else: 
        expires = datetime.utcnow() + time_expires
    #actualizamos los valores de data_copy para colocar el tiempo a expirar el token
    data_copy.update({"exp":expires})
    token_jwt = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def get_user_current(token: str = Depends(oauth2_scheme)): # donde trabajaremos la autenticacion nuevamente del usuario con el token
    try:
        #decodificacion de json web token
        token_decode = jwt.decode(token, key=SECRET_KEY,algorithms=[ALGORITHM])
        username = token_decode.get("sub")
        if username == None:
            raise HTTPException(status_code=401 , detail="Could not validate credentials", headers=
                            {"WWW-Authenticate": "Bearer"}) 
    except JWTError:
        raise HTTPException(status_code=401 , detail="Could not validate credentials", headers=
                            {"WWW-Authenticate": "Bearer"})
    user = get_user(fake_users_db, username)
    if not user:
        raise HTTPException(status_code=401 , detail="Could not validate credentials", headers=
                            {"WWW-Authenticate": "Bearer"})
    return user 

#verificar que no a expirado el token
def get_user_disable_current(user: User = Depends(get_user_current)):
    if user.disabled:
        raise HTTPException(status_code=400 , detail="Inactive user", headers=
                            {"WWW-Authenticate": "Bearer"})
    return user


@app.get('/')
async def root():
    return "hola soy fastapi"

# un depends es una inyeccion de depencias que va a ser una funcion que se jecutara al entrar en esta ruta
@app.get('/users/me')
async def user(user: User = Depends(get_user_disable_current)): 
    return user
    

#autenticar al usuario
@app.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = create_token({"sub": user.username}, access_token_expires)
    return {
        "access_token": access_token_jwt, #es donde ira el token para autenticar y lo que se pasara a las rutas
        "token_type": "bearer"
    }