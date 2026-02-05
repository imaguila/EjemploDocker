from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import os

# --- 1. Configuración de Base de Datos ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:password@db:5432/biblioteca")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. Modelos (Tablas en Postgres) ---
class Libro(Base):
    __tablename__ = "libros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    total = Column(Integer)
    prestados = Column(Integer, default=0)

class Prestamo(Base):
    __tablename__ = "prestamos"
    id = Column(Integer, primary_key=True, index=True)
    libro_id = Column(Integer, ForeignKey("libros.id"))
    alumno = Column(String)
    libro = relationship("Libro")

# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)

# --- 3. Esquemas (Validación de datos que entran/salen) ---
class LibroCreate(BaseModel):
    titulo: str
    total: int

class PrestamoCreate(BaseModel):
    libro_id: int
    alumno: str

# --- 4. La Aplicación ---
app = FastAPI()

# Dependencia para obtener la base de datos en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/libros")
def listar_libros(db: Session = Depends(get_db)):
    return db.query(Libro).all()

@app.post("/api/libros")
def crear_libro(libro: LibroCreate, db: Session = Depends(get_db)):
    nuevo = Libro(titulo=libro.titulo, total=libro.total)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/api/prestamos")
def listar_prestamos(db: Session = Depends(get_db)):
    # Unimos la tabla prestamos con libros para saber el título
    return db.query(Prestamo).all()

@app.post("/api/prestar")
def realizar_prestamo(prestamo: PrestamoCreate, db: Session = Depends(get_db)):
    libro = db.query(Libro).filter(Libro.id == prestamo.libro_id).first()
    
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    if libro.prestados >= libro.total:
        raise HTTPException(status_code=400, detail="No quedan ejemplares disponibles")
    
    # Lógica de negocio
    libro.prestados += 1
    nuevo_prestamo = Prestamo(libro_id=libro.id, alumno=prestamo.alumno)
    db.add(nuevo_prestamo)
    db.commit()
    return {"mensaje": "Préstamo realizado"}

@app.delete("/api/devolver/{prestamo_id}")
def devolver_libro(prestamo_id: int, db: Session = Depends(get_db)):
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no existe")
        
    libro = db.query(Libro).filter(Libro.id == prestamo.libro_id).first()
    libro.prestados -= 1 # Devolvemos el stock
    
    db.delete(prestamo)
    db.commit()
    return {"mensaje": "Libro devuelto"}