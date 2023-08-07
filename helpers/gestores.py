from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from sqlalchemy import select, update


class comun():
    @classmethod
    def update_estado(cls, session, **kwargs):
        try:
            with session.begin():
                stmt = text(
                    'SET TRANSACTION ISOLATION LEVEL READ COMMITTED')
                session.execute(stmt)
                consulta = (
                    update(cls)
                    .where(cls.estado == 0)
                    .values(**kwargs)
                )
                session.execute(consulta)
            session.commit()
        except IntegrityError as e:
            print(f"Error de integridad: {e}")
            session.rollback()
        except Exception as e:
            print(f"Error desconocido: {e}")
            session.rollback()
        finally:
            session.close()

    @classmethod
    def select_requests(cls, session, **kwargs):
        try:
            with session.begin():
                consulta_2 = select(cls.parametro1).where(
                    (cls.instancia == 'Py1') & (cls.estado == 1))

                select_consult = session.execute(consulta_2).fetchall()
                if select_consult is not None and len(select_consult) > 0:
                    return select_consult
        except IntegrityError as e:
            print(f"Error de integridad: {e}")
            session.rollback()
        except Exception as e:
            print(f"Error desconocido: {e}")
            session.rollback()
        finally:
            session.close()
