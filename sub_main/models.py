from sqlalchemy import Column, Integer, String, TEXT, text, Date, case, func, Float, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import date
from .database import Base
from helpers.gestores import comun


# class Peticioneservidor(Base, comun):
#     __tablename__ = 'peticioneservidor'
#     id = Column(Integer, primary_key=True)
#     instancia = Column(String(255))
#     estado = Column(Integer)
#     parametro1 = Column(String(255))
#     parametro2 = Column(TEXT)
#     fechainsercion = Column(Date)
#     fecha = Column(Date)

#     def __init__(self, parametro1, estado, peticion):
#         self.parametro1 = parametro1
#         self.estado = estado
#         self.peticion = peticion

# class Documentos(Base, comun):
#     __tablename__ = 'Documentos'
#     id = Column(Integer, primary_key=True)
#     estado = Column(String(255))
#     articulos = Column(String(255))
#     clienteol = Column(String(255))

#     def __init__(self, estado, articulos, clienteol):
#         self.estado = estado
#         self.articulos = articulos
#         self.clienteol = clienteol


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


class ArticulosWeb(Base, comun):
    __tablename__ = 'articulosweb'
    id = Column(Integer, primary_key=True, autoincrement=True)
    marca = Column(Integer)
    codigo = Column(Integer)
    precio = Column(Float)
    precionormal = Column(Float)
    descripcion = Column(String(255))
    presentacion = Column(String(255))
    pesable = Column(Boolean)
    pesableporunidad = Column(Boolean)
    cmax = Column(Float)
    nombremarca = Column(String(255))
    marcareal = Column(Integer)
    cantidad = Column(Integer)
    fraccion = Column(Integer)
    ppfraccion = Column(Float)
    coeficiente = Column(Float)
    preciopor = Column(Float)
    unidaddmedida = Column(String(255))
    cantidadmayorista = Column(Integer)
    preciomayorista = Column(Float)
    etiquetamedida = Column(String(255))
    da = Column(String(255))
    de = Column(String(255))
    foto = Column(String(255))
