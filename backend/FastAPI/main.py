from fastapi import FastAPI 
import routers.Producs as Producs
import routers.users as Users
from fastapi.staticfiles import StaticFiles # para los archivos estaticos

app = FastAPI()


#routers 

app.include_router(Producs.router)
app.include_router(Users.router)
app.mount("/statico",StaticFiles(directory='static'), name='statico')

#fin routes

@app.get('/')
async def root():
    return "Hola fastapi"

@app.get('/url')
async def url():
    return { "url": "http://localhost"}

# Inicia el server: py -m uvicorn main:app --reload
# Detener el server: CTRL+C
# http://127.0.0.1:8000/redoc