from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelsPydantic import modelUsuario
from Middlewares import BearerJWT
from DB.conexion import Session
from models.modelsDB import User
from fastapi import APIRouter

routerUsuario= APIRouter()

#dependencies= [Depends(BearerJWT())]

# consultar todos los usuarios
@routerUsuario.get("/usuarios", tags=["Operaciones CRUD"])
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
@routerUsuario.get('/usuarios/{id}', tags=["Operaciones CRUD"])
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
@routerUsuario.post("/usuarios/", response_model=modelUsuario, tags=["Operaciones CRUD"])
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
@routerUsuario.put("/usuarios/{id}", response_model=modelUsuario, tags=["Operaciones CRUD"])
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
@routerUsuario.delete("/usuarios/{id}", tags=["Operaciones CRUD"])
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