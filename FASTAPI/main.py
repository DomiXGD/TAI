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

# levanta las tablas definidas en modelos
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

# consultar todos los usuarios
@app.get("/usuarios", tags=["Operaciones CRUD"])
def ConsultarTodos():
    db = Session()
    try:
        consulta = db.query(User).all()
        return JSONResponse(content=jsonable_encoder(consulta))
    except Exception as x:
        return JSONResponse(status_code=500, content={"mensaje": "No fue posible consultar", "Exception": str(x)})
    finally:
        db.close()

# endpoint consultar por id
@app.get('/usuarios/{id}', tags=["Operaciones CRUD"])
def ConsultarUno(id: int):
    db = Session()
    try:
        consulta = db.query(User).filter(User.id == id).first()
        if not consulta:
            return JSONResponse(status_code=404, content={"Mensaje": "Usuario no encontrado"})
        return JSONResponse(content=jsonable_encoder(consulta))
    except Exception as x:
        return JSONResponse(status_code=500, content={"mensaje": "No fue posible consultar", "Exception": str(x)})
    finally:
        db.close()

# endpoint para agregar un usuario
@app.post("/usuarios/", response_model=modelUsuario, tags=["Operaciones CRUD"])
def AgregarUsuario(usuarionuevo: modelUsuario):
    db = Session()
    try:
        usuario = User(**usuarionuevo.model_dump())
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return JSONResponse(status_code=201, content={"mensaje": "Usuario Guardado", "usuario": jsonable_encoder(usuario)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=400, content={"mensaje": "No se Guardó", "Excepcion": str(e)})
    finally:
        db.close()

# Actualizar un usuario PUT
@app.put("/usuarios/{id}", response_model=modelUsuario, tags=["Operaciones CRUD"])
def ActualizarUsuario(id: int, usuarioActualizado: modelUsuario):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        for key, value in usuarioActualizado.model_dump().items():
            setattr(usuario, key, value)
        db.commit()
        db.refresh(usuario)
        return JSONResponse(content=jsonable_encoder(usuario))
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"mensaje": "Error al actualizar", "Excepcion": str(e)})
    finally:
        db.close()

# Endpoint para eliminar 
@app.delete("/usuarios/{id}", tags=["Operaciones CRUD"])
def Eliminar(id: int):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        db.delete(usuario)
        db.commit()
        return {"mensaje": "Usuario eliminado", "usuario": jsonable_encoder(usuario)}
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"mensaje": "Error al eliminar", "Excepcion": str(e)})
    finally:
        db.close()

# endpoint para generar un token 
@app.post('/auth', tags=['Autentificacion'])
def login(autorizado: modelAuth):
    if autorizado.correo == 'domi@example.com' and autorizado.passw == '123456789':
        token: str = createToken(autorizado.model_dump())
        return JSONResponse(content=token)
    else:
        return {"Aviso": "Usuario no autorizado"}
