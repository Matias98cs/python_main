from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text, and_, func
from sqlalchemy import select, update
from flask import Flask, request, make_response, jsonify


class comun():
    @classmethod
    def crear_y_obtener(cls, session, **kwargs):
        kwargs.pop('imagen', None)
        entidad = session.query(cls).filter_by(**kwargs).first()
        if not entidad:
            entidad = cls(**kwargs)
            session.add(entidad)
        return entidad


# class comun():
#     @classmethod
#     def update_estado(cls, session, **kwargs):
#         try:
#             with session.begin():
#                 stmt = text(
#                     'SET TRANSACTION ISOLATION LEVEL READ COMMITTED')
#                 session.execute(stmt)
#                 consulta = (
#                     update(cls)
#                     .where(cls.estado == 0)
#                     .values(**kwargs)
#                 )
#                 session.execute(consulta)
#             session.commit()
#         except IntegrityError as e:
#             print(f"Error de integridad: {e}")
#             session.rollback()
#         except Exception as e:
#             print(f"Error desconocido: {e}")
#             session.rollback()
#         finally:
#             session.close()

#     @classmethod
#     def select_requests(cls, session, **kwargs):
#         try:
#             with session.begin():
#                 consulta_2 = select(cls.parametro1).where(
#                     (cls.instancia == 'Py1') & (cls.estado == 1))

#                 select_consult = session.execute(consulta_2).fetchall()
#                 if select_consult is not None and len(select_consult) > 0:
#                     return select_consult
#         except IntegrityError as e:
#             print(f"Error de integridad: {e}")
#             session.rollback()
#         except Exception as e:
#             print(f"Error desconocido: {e}")
#             session.rollback()
#         finally:
#             session.close()

#     @classmethod
#     def update_request(cls, session, **kwargs):
#         parametro = kwargs.get('parametro')
#         c = kwargs.get('c')
#         estado = kwargs.get('estado')
#         fecha = kwargs.get('fecha')
#         parametro2 = kwargs.get('parametro2')
#         try:
#             with session.begin():
#                 # JSON_VALUE
#                 # JSON_EXTRACT
#                 query = (
#                     update(cls)
#                     .values(estado=estado, fecha=fecha, parametro2=parametro2)
#                     .where(
#                         and_(
#                             cls.instancia == 'Py1',
#                             cls.estado == 1,
#                             func.JSON_VALUE(
#                                 cls.parametro1, f"$.{c}") == parametro
#                         )
#                     )
#                 )
#                 session.execute(query)
#             session.commit()
#         except IntegrityError as e:
#             print(f"Error de integridad: {e}")
#             session.rollback()
#         except Exception as e:
#             print(f"Error desconocido: {e}")
#             session.rollback()
#         finally:
#             session.close()
