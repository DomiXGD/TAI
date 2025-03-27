from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from fastapi.encoders import jsonable_encoder
from modelsPydantic import modelUsuario, modelAuth
from tokenGen import createToken
from Middlewares import BearerJWT
from DB.conexion import Session, engine, Base
from models.modelsDB import User

app = FastAPI(
    title="Mi primer API 196",
    description="Domingo Araujo Alvarez",
    version="0.1"
)
#levanta las tablas definidas en modelos
Base.metadata.create_all(bind=engine)

usuarios = [
    {"id": 1, "nombre": "Jesús Cruz", "edad": 21, "correo": "jesuscruz@gmail.com"},
    {"id": 2, "nombre": "Estrella Cuellar", "edad": 20, "correo": "estrellacuellar@gmail.com"},
    {"id": 3, "nombre": "Lucero Cuellar", "edad": 20, "correo": "lucerocuellar@gmail.com"},
    {"id": 4, "nombre": "Domingo Ar aujo", "edad": 20, "correo": "domingoaraujo@gmail.com"},
]


@app.get("/", tags=["Inicio"])
def main():
    return {"Hola FastAPI": "Domingo Araujo Alvarez"}

#dependencies=[Depends(BearerJWT())], response_model=list[modelUsuario],
# consultar todos los usuarios
@app.get("/usuarios", tags=["Operaciones CRUD"])
def ConsultarTodos():
    db= Session()
    try:
        consulta= db.query(User).all
        return JSONResponse(Content=jsonable_encoder(consulta))

    except Exception as x:
        return JSONResponse(status_code=500, content={"mensaje": "No fue posible consultar", "Exception": str(x)})

    finally:
        db.close()

# endpoitn consultar por id
@app.get('/usuarios/{id}', tags=["Operaciones CRUD"])
def ConsultarUno(id:int):
    db= Session()
    try:
        consulta= db.query(User).filter(User.id == id).first()
        if not consulta:
            return JSONResponse(status_code= 404,content={"Mensaje": "Usuario no encontrado"})
        return JSONResponse(Content=jsonable_encoder(consulta))

    except Exception as x:
        return JSONResponse(status_code=500, content={"mensaje": "No fue posible consultar", "Exception": str(x)})

    finally:
        db.close()


# endpoint para agregar un usuario
@app.post("/usuarios/", response_model=modelUsuario, tags=["Operaciones CRUD"])
def AgregarUsuario(usuarionuevo: modelUsuario):  # Usa el modelo Usuario en lugar de dict
   db= Session()
   try: 
       db.add(User(**usuarionuevo.model_dump()))
       db.commit()
       return JSONResponse(status_code=201, content={"mensaje":"Usuario Guardado","usuario":usuarionuevo.model_dump()})

   except Exception as e:
       db.rollback()
       return JSONResponse(status_code=400, content={"mensaje":"No se Guardo", "Excepcion":str(e)})
       
   finally:
       db.close()

# Actualizar un usuario PUT
@app.put("/usuarios/{id}", response_model=modelUsuario, tags=["Operaciones CRUD"])
def ActualizarUsuario(id: int, usuarioActualizado: modelUsuario):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuarioActualizado.model_dump()
            return usuarios[index]

    raise HTTPException(status_code=400, detail="Usuario no encontrado")

#Endpoint para elminar 
@app.delete("/usuarios/{id}", tags=["Operaciones CRUD"])
def Eliminar(id: int):
    for usr in (usuarios):
        if usr["id"] == id:
            usuarios.remove(usr)
            return {"Usuario Eliminado": usr}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# endpoint para generar un token 
@app.post('/auth', tags=['Autentificacion'])
def login(autorizado: modelAuth):
    if autorizado.correo == 'domi@example.com' and autorizado.passw == '123456789':
        token: str = createToken(autorizado.model_dump())
        print(token)
        return JSONResponse(content=token)
    else:
        return {"Aviso": "Usuario no autorizado"}


