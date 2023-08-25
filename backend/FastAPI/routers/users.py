from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=['users'])

#entidad users
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name='Samuel', surname='Zabala', url='http://youtube.com', age=28),
             User(id=2, name='Rous', surname='Centeno', url='http://youtube.com', age=28),
             User(id=3, name='Rengar', surname='Pochosos', url='http://youtube.com', age=1)
        ]

@router.get('/usersjson')
async def usersjson():
    return [{
                'name': 'samuel',
                'surname': 'Zabala',
                'url': 'http://youtube.com',
                'age': 28
            },
            {
                'name': 'Rous',
                'surname': 'Centeno',
                'url': 'http://youtube.com',
                'age': 28
            },
            {
                'name': 'Rengar',
                'surname': 'Pochosos',
                'url': 'http://youtube.com',
                'age': 1
            }]

@router.get('/users')
async def users():
    return users_list

@router.get('/user/{id}') # se manda el id por Path
async def user(id: int):
   return search_users(id)
   

@router.get('/user/') # se manda el id por Query
async def user(id: int):
    return search_users(id)

@router.post('/user/', response_model=User ,status_code=201) # agregar un nuevo usuario
async def user(user: User): # lo colocamos de tipo usuario
    if type(search_users(user.id)) == User:     #verificamos si el usuario existe
        raise HTTPException(status_code=404, detail="El usuario ya existe") # raise para colocar el error
    else:
        users_list.append(user) # lo insertamos en la lista de usuario
        return user

@router.put('/user/', response_model=User, status_code=200) # actualizar usuario
async def user(user: User):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        raise HTTPException(status_code=404, detail="No se ha actualizado el usuario")
        

    return user

@router.delete("/user/{id}", status_code=200)
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        raise HTTPException(status_code=404, detail="No se ha eliminado el usuario")
        



def search_users(id: int):
    users = filter(lambda data: data.id == id, users_list)
    try: 
        return list(users)[0] #accedemos solo al primer elemento de la lista
    except:
        raise HTTPException(status_code=404, detail="no se a encontrado el usuario")
      
    


# Inicia el server:  py -m uvicorn users:app --reload
# Detener el server: CTRL+C