from sqlalchemy import Column, Integer, String, TEXT, text, Date, case, func
from sqlalchemy.orm import relationship, declarative_base
from datetime import date
from .database import Base


class Peticioneservidor(Base):
    __tablename__ = 'peticioneservidor'
    id = Column(Integer, primary_key=True)
    instancia = Column(String(255))
    estado = Column(Integer)
    parametro1 = Column(String(255))
    parametro2 = Column(TEXT)
    fechainsercion = Column(Date)
    fecha = Column(Date)
