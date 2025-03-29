from fastapi import FastAPI
from DB.conexion import engine, Base
from routers.usuarios import routerUsuario
from routers.auth import routerAuth

app = FastAPI(
    title="Mi primer API 196",
    description="Domingo Araujo Alvarez",
    version="0.1"
)

# levanta las tablas definidas en modelos
Base.metadata.create_all(bind=engine)

app.include_router(routerUsuario)
app.include_router(routerAuth)

@app.get("/", tags=["Inicio"])
def main():
    return {"Hola FastAPI": "Domingo Araujo Alvarez"}