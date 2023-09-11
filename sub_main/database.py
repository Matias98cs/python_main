from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()


def _crear_conexion(db_user, db_password, db_ip_address, db_name):
    url = f"mysql+pymysql://{db_user}:{db_password}@{db_ip_address}/{db_name}"
    try:
        engine = create_engine(
            url, echo=False, isolation_level='READ COMMITTED')
        return engine
    except:
        print(f"Error al crear conexion servidor: {db_ip_address}")
        return None


def obtener_session(db_user, db_password, db_ip_address, db_name):
    engine = _crear_conexion(db_user, db_password, db_ip_address, db_name)
    Base.metadata.create_all(engine)
    if engine:
        Session = sessionmaker(bind=engine)
        return Session()
    return None
