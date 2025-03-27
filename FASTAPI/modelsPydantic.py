from pydantic import BaseModel, Field, EmailStr


# modelo para validación de datos
class modelUsuario(BaseModel):
    name: str = Field(..., min_length=3, max_length=215,description="Nombre solo debe de contener letras y espacios ")
    age: int 
    email: str 


class modelAuth(BaseModel):
    correo: EmailStr
    passw: str = Field(..., min_length=8, strip_whitespace=True, description="Contraseña minimo 8 caracteres")