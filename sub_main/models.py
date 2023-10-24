from sqlalchemy import Column, Integer, String, TEXT, text, Date, case, func, Float, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import date
from .database import Base
from helpers.gestores import comun


class Peticioneservidor(Base, comun):
    __tablename__ = 'peticioneservidor'
    id = Column(Integer, primary_key=True)
    instancia = Column(String(255))
    estado = Column(Integer)
    parametro1 = Column(String(255))
    parametro2 = Column(TEXT)
    fechainsercion = Column(Date)
    fecha = Column(Date)


class Ofertas(Base, comun):
    __tablename__ = 'ofertas'
    id = Column(Integer, primary_key=True)
    marca = Column(Integer)
    codigo = Column(Integer)
    fechadesde = Column(DateTime)
    fechahasta = Column(DateTime)
    sucursal = Column(Integer)
    precio = Column(Float)
    preciomay = Column(Float)
    cantidadmayorista = Column(Integer)


class Promocion(Base, comun):
    __tablename__ = 'promociones'
    idpromocion = Column(Integer, primary_key=True)
    regla1 = Column(String(255))
    regla2 = Column(String(255))
    porcentaje = Column(Integer)
    monto = Column(Float)
    cantidad1 = Column(Integer)
    cantidad2 = Column(Integer)
    nombre = Column(String(255))
    abv = Column(String(255), default="")
    orden = Column(Integer)
    sucursal = Column(Integer)
    desde = Column(DateTime)
    hasta = Column(DateTime)
    martes = Column(String(1))
    miercoles = Column(String(1))
    jueves = Column(String(1))
    viernes = Column(String(1))
    sabado = Column(String(1))
    domingo = Column(String(1))
    tipo = Column(String(1))
    marca = Column(Integer)
    codigo = Column(Integer)
