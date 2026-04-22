from pydantic import BaseModel, ConfigDict

# Esquemas para Estaciones
class EstacionBase(BaseModel):
    id: int
    nombre: str
    ubicacion: str

class EstacionCreate(EstacionBase):
    pass

class Estacion(EstacionBase):
    model_config = ConfigDict(from_attributes=True)

# Esquemas para Lecturas
class LecturaBase(BaseModel):
    estacion_id: int
    valor: float

class LecturaCreate(LecturaBase):
    pass

class Lectura(LecturaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)