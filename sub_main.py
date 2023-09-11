from sqlalchemy import select, update
from helpers.format_data import format_json, a, promo_json
from sqlalchemy.sql import text
from sub_main.database import obtener_session
from sqlalchemy.exc import IntegrityError
from sub_main.models import Peticioneservidor
from types import SimpleNamespace
import time
import json
import calendar
from datetime import datetime

arch = open('ConfigDB.ini', 'r')
DB = eval(arch.read())
base_general = "pruebaspython"

session_mysql = obtener_session(
    f"{DB['username']}", f"{DB['password']}", f"{DB['server']}", base_general)


def search():
    fecha = datetime.today().strftime('%Y-%m-%d')
    fecha_aux = 1
    n = 0
    print('Entro')
    while True:
        if fecha_aux == 1 or fecha_aux > fecha:
            data_big = format_json()
            data_promos = promo_json()
            # data_products = products_api()
            fecha = datetime.today().strftime('%Y-%m-%d')
        fecha_aux = datetime.today().strftime('%Y-%m-%d')

        Peticioneservidor.update_estado(session_mysql, instancia='Py1', estado=1,
                                        fechainsercion=datetime.now())

        select_consult = Peticioneservidor.select_requests(session_mysql)

        if select_consult is not None and len(select_consult) > 0:
            for item in select_consult:
                current_time = time.gmtime()
                time_stamp = calendar.timegm(current_time)
                n += 1
                if item.parametro1 != '{}':
                    obj_string = json.loads(
                        item.parametro1, object_hook=lambda d: SimpleNamespace(**d))

                    parametros = {
                        "search": obj_string.s if hasattr(obj_string, 's') else '',
                        "categoria": obj_string.categoria if hasattr(obj_string, 'categoria') else '',
                        "sucursal": obj_string.sucursal if hasattr(obj_string, 'sucursal') else '',
                        "rangoregistros": obj_string.rangoregistros if hasattr(obj_string, 'rangoregistros') else '',
                        "ofertas": obj_string.ofertas if hasattr(obj_string, 'ofertas') else '',
                    }
                    match parametros:
                        case parametros if parametros['search'] != '' and parametros['categoria'] == '' and parametros['ofertas'] == '':
                            print(
                                f"---------- search: {parametros['search']} ----------")
                            searched_articles = [
                                item for item in data_big if f"{parametros['search'].lower()}" in item['descripcion'].lower()]
                            cut_list = searched_articles
                            a['ctimestamp'] = time_stamp
                            a['registros'] = cut_list
                            json_searched = json.dumps(a)
                            Peticioneservidor.update_request(session_mysql, estado=2, fecha=datetime.now(
                            ), parametro2=json_searched, parametro=parametros['search'], c='s')

                            # try:
                            #     with session_mysql.begin():
                            # query = text(
                            #     "UPDATE Peticioneservidor SET estado = 2, fecha = CURRENT_TIMESTAMP, parametro2 = '"+json_searched+"' WHERE instancia = 'Py1' AND estado = 1 AND JSON_EXTRACT(parametro1, '$.s') = '"+parametros[
                            #         'search']+"' "
                            # )
                            #         session_mysql.execute(query)
                            #     session_mysql.commit()
                            # except IntegrityError as e:
                            #     print(f"Error de integridad: {e}")
                            #     session_mysql.rollback()
                            # except Exception as e:
                            #     session_mysql.rollback()
                            # finally:
                            #     session_mysql.close()

                        case parametros if parametros['categoria'] != '' and parametros['search'] == '' and parametros['ofertas'] == '':
                            print(
                                f"---------- categoria: {parametros['categoria']} ----------")
                            search_categoria = [item for item in data_big if int(
                                parametros['categoria']) == int(item['categoria']['categoria'])]
                            cut_list = search_categoria
                            a['ctimestamp'] = time_stamp
                            a['registros'] = cut_list
                            json_searched = json.dumps(a)
                            Peticioneservidor.update_request(
                                session_mysql, estado=2, fecha=datetime.now(), parametro2=json_searched, parametro=parametros['categoria'], c='categoria')

                        case parametros if parametros['ofertas'] == 'S' and parametros['ofertas'] != '' and parametros['search'] == '' and parametros['categoria'] == '':
                            print(
                                f"---------- Promos: {parametros['ofertas']} ----------")
                            a['ctimestamp'] = time_stamp
                            a['registros'] = data_promos
                            json_searched = json.dumps(a)
                            Peticioneservidor.update_request(
                                session_mysql, estado=2, fecha=datetime.now(), parametro2=json_searched, parametro=parametros['ofertas'], c='ofertas')

                        case parametros if parametros['search'] == '' and parametros['categoria'] == '' and parametros['ofertas'] == '' and parametros['sucursal'] == '':
                            print(
                                f"---------- Vacio: {'parametros vacios'} ----------")
                            a['ctimestamp'] = time_stamp
                            a['registros'] = []
                            json_searched = json.dumps(a)
                            Peticioneservidor.update_request(
                                session_mysql, estado=2, fecha=datetime.now(), parametro2=json_searched)

                        case parametros if parametros['sucursal'] != '' and parametros['search'] == '' and parametros['categoria'] == '':
                            print(
                                f"---------- Todos los productos: {parametros['sucursal']} ----------")
                            a['ctimestamp'] = time_stamp
                            a['registros'] = data_big
                            json_searched = json.dumps(a)
                            Peticioneservidor.update_request(
                                session_mysql, estado=2, fecha=datetime.now(), parametro2=json_searched)
                        case _:
                            a['ctimestamp'] = time_stamp
                            a['registros'] = []
                            json_searched = json.dumps(a)
                            Peticioneservidor.update_request(
                                session_mysql, estado=2, fecha=datetime.now(), parametro2=json_searched, parametro=parametros['ofertas'], c='sucursal')


if __name__ == "__main__":
    search()
