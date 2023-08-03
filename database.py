from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker


def crear_conexion(db_user, db_password, db_ip_address, db_name):
    url = f"mysql+pymysql://{db_user}:{db_password}@{db_ip_address}/{db_name}"
    try:
        engine = create_engine(url, echo=False)
        return engine
    except:
        print(f"Error al crear conexion")
        return None


def obtener_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
