from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import engine, get_db

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMAT - Sistema de Monitoreo de Alerta Temprana",
    version="1.0.0"
)

@app.post("/estaciones/", status_code=status.HTTP_201_CREATED, tags=["Gestión de Infraestructura"])
def crear_estacion(estacion: schemas.EstacionCreate, db: Session = Depends(get_db)):
    return {"msj": "Estacion guardada", "data": crud.create_estacion(db, estacion)}

@app.get("/estaciones/")
def listar_estaciones(db: Session = Depends(get_db)):
    return crud.get_estaciones(db)

@app.post("/lecturas/", status_code=status.HTTP_201_CREATED, tags=["Telemetría de Sensores"])
def registrar_lectura(lectura: schemas.LecturaCreate, db: Session = Depends(get_db)):
    if not crud.get_estacion(db, lectura.estacion_id):
        raise HTTPException(status_code=404, detail="Estacion no existe")
    return {"status": "Lectura guardada", "data": crud.create_lectura(db, lectura)}

@app.get("/estaciones/{id}/historial", tags=["Reportes Historicos"])
def obtener_historial(id: int, db: Session = Depends(get_db)):
    lecturas = crud.get_lecturas_by_estacion(db, id)
    if not lecturas:
        raise HTTPException(status_code=404, detail="Estacion sin lecturas o no encontrada")
    
    valores = [l.valor for l in lecturas]
    return {
        "estacion_id": id,
        "lecturas": lecturas,
        "conteo": len(lecturas),
        "promedio": sum(valores) / len(valores)
    }

@app.get("/estaciones/stats", tags=["Resumen Ejecutivo"])
def obtener_stats(db: Session = Depends(get_db)):
    estaciones = crud.get_estaciones(db)
    lecturas = crud.get_all_lecturas(db)

    if not estaciones or not lecturas:
        raise HTTPException(status_code=404, detail="No hay datos suficientes")

    valores = [l.valor for l in lecturas]
    return {
        "total_estaciones": len(estaciones),
        "total_lecturas": len(lecturas),
        "promedio_global": sum(valores) / len(valores)
    }