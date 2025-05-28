from fastapi import FastAPI, Request, Depends
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

# Configuración de la base de datos con nombre DNS
DB_USER = "natalia"
DB_PASS = "123"
DB_HOST = "db.najoma.lans"  # Aquí va el nombre DNS
DB_NAME = "proyecto_db"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelo tabla accesos
class Acceso(Base):
    __tablename__ = "accesos"
    id = Column(Integer, primary_key=True, index=True)
    ip_cliente = Column(String(45), nullable=False)
    fecha = Column(TIMESTAMP, server_default=func.now())

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def raiz(request: Request, db=Depends(get_db)):
    ip = request.client.host
    nuevo_acceso = Acceso(ip_cliente=ip)
    db.add(nuevo_acceso)
    db.commit()

    total_accesos = db.query(Acceso).filter(Acceso.ip_cliente == ip).count()

    return {
        "mensaje": f"Bienvenido, te conectaste desde la IP {ip}",
        "veces_conectado": total_accesos
    }
