from fastapi import APIRouter

router = APIRouter(prefix="/products",tags=["products"] ,responses={404: {"mensage": "No encontrado"}}) 
# el tags es para la documentacion

producs_list = ['producto1', 'producto2', 'producto3','producto4']

@router.get('/')
async def producs():
    return producs_list

@router.get('/{id}')
async def producs(id: int):
    return producs_list[id]