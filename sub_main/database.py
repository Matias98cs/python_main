from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()

arch = open('ConfigDB.ini', 'r')
DB = eval(arch.read())
user = DB['username']
password = DB['password']
ip_address = DB['server']
db_name = DB['database']


def _crear_conexion(db_user, db_password, db_ip_address, db_name):
    url = f"mysql+pymysql://{db_user}:{db_password}@{db_ip_address}/{db_name}"
    try:
        engine = create_engine(url, echo=False)
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


def searchDB(DB):
    driver = DB['driver'][1:11]
    if driver == 'SQL Server':
        # URI = f'mssql+pymssql://{DB["username"]}:{DB["password"]}@{DB["server"]}:{DB["port"]}/{DB["database"]}'
        URI = f'mysql+pymysql://{DB["username"]}:{DB["password"]}@{DB["server"]}:{DB["port"]}/{DB["database"]}'
    elif driver == 'PostgreSQL':
        URI = f'postgresql+psycopg2://{DB["username"]}:{DB["password"]}@{DB["server"]}:{DB["port"]}/{DB["database"]}'
    return URI


conexion_uri = searchDB(DB)
db_session = obtener_session(user, password, ip_address, db_name)
