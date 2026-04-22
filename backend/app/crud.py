from sqlalchemy.orm import Session
import models
import schemas

def get_estacion(db: Session, estacion_id: int):
    return db.query(models.EstacionDB).filter(models.EstacionDB.id == estacion_id).first()

def get_estaciones(db: Session):
    return db.query(models.EstacionDB).all()

def create_estacion(db: Session, estacion: schemas.EstacionCreate):
    db_estacion = models.EstacionDB(**estacion.model_dump())
    db.add(db_estacion)
    db.commit()
    db.refresh(db_estacion)
    return db_estacion

def create_lectura(db: Session, lectura: schemas.LecturaCreate):
    db_lectura = models.LecturaDB(**lectura.model_dump())
    db.add(db_lectura)
    db.commit()
    db.refresh(db_lectura)
    return db_lectura

def get_lecturas_by_estacion(db: Session, estacion_id: int):
    return db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == estacion_id).all()

def get_all_lecturas(db: Session):
    return db.query(models.LecturaDB).all()