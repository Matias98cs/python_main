from sub_main.database import obtener_session
from sub_main.models import Promocion, Ofertas, ArticulosWeb
from datetime import datetime
import requests
import json

arch = open('ConfigDB.ini', 'r')
DB = eval(arch.read())
user = DB['username']
password = DB['password']
ip_address = DB['server']
db_name = DB['database']

session_db = obtener_session(user, password, ip_address, db_name)

url_promociones = 'http://soportedlr.com.ar:9001/api/v1/promocioneswebec'
response_promociones = requests.get(url_promociones)
promociones = json.loads(response_promociones.content)

url_ofertas = 'http://soportedlr.com.ar:9001/api/v1/ofertaswebec?sucursal=1'
response_ofertas = requests.get(url_ofertas)
ofertas = json.loads(response_ofertas.content)

url_articulosweb = 'http://soportedlr.com.ar:9001/api/v1/articulosweb?sucursal=8'
response_articulosweb = requests.get(url_articulosweb)
articulosweb = json.loads(response_articulosweb.content)

lista_errores_promociones = []
for item in promociones['registros']:
    try:
        promocion = Promocion.crear_y_obtener(session_db, **item)
        session_db.commit()
    except Exception as e:
        print(f"Error al cargar los datos {e}")
        session_db.rollback()
        lista_errores_promociones.append(item)

session_db.commit()
print('Datos de promociones cargados en DB')


lista_errores_ofertas = []
for item in ofertas['registros']:
    try:
        oferta = Ofertas.crear_y_obtener(session_db, **item)
        session_db.commit()
    except Exception as e:
        print(f"Error al cargar dos ofertas : {e}")
        session_db.rollback()
        lista_errores_ofertas.append(item)

session_db.commit()
print('Datos de ofertas cargados en DB')

lista_errores_articulosweb = []
for item in articulosweb['registros']:
    try:
        art_web = ArticulosWeb.crear_y_obtener(session_db, **item)
        session_db.commit()
    except Exception as e:
        print(f"Error al cargar los articulos web : {e}")
        session_db.rollback()
        lista_errores_articulosweb.append(item)

session_db.commit()
print('Datos de articulos web cargados en DB')
