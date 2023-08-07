from sqlalchemy import select, update
from helpers.format_data import format_json, search_articles
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
                    }
                    # match parametros:
                    #     case parametros if parametros['search'] != '' and parametros['search'] != None and parametros['search'] is not None:
                    #         print(
                    #             f"---------- search: {parametros['search']} ----------")
                    #         json_searched = search_articles(
                    #             parametros, data_big, time_stamp)
                    #         searched_articles = [
                    #             item for item in data_big if f"{parametros['search'].lower()}" in item['descripcion'].lower()]
                    #         cut_list = searched_articles
                    #         a['ctimestamp'] = time_stamp
                    #         a['registros'] = cut_list
                    #         json_searched = json.dumps(json_searched)
                    #         print(json_searched)
                    #         with session_mysql:
                    #             query = update(Peticioneservidor).values(estado=2, fecha=datetime.now(), parametro2=json_searched).where(
                    #                 (Peticioneservidor.instancia == 'Py1') & (Peticioneservidor.estado == 1))
                    #             session_mysql.execute(query)
                    #             session_mysql.commit()

                    #     case parametros if parametros['categoria'] != '' and parametros['categoria'] != None and parametros['categoria'] is not None:
                    #         print(
                    #             f"---------- categoria: {parametros['categoria']} ----------")
                    #         search_categoria = [item for item in data_big if int(
                    #             parametros['categoria']) == int(item['categoria']['categoria'])]
                    #         cut_list = search_categoria
                    #         a['ctimestamp'] = time_stamp
                    #         a['registros'] = cut_list
                    #         json_searched = json.dumps(a)
                    #         print(json_searched)
                    #         with session_mysql:
                    #             query = update(Peticioneservidor).values(estado=2, fecha=datetime.now(), parametro2=json_searched).where(
                    #                 (Peticioneservidor.instancia == 'Py1') & (Peticioneservidor.estado == 1))
                    #             session_mysql.execute(query)
                    #             session_mysql.commit()

                    #     case parametros if parametros['search'] == '' and parametros['search'] is not None and parametros['categoria'] != '' and parametros['categoria'] is not None:
                    #         a['ctimestamp'] = time_stamp
                    #         a['registros'] = []
                    #         json_searched = json.dumps(a)
                    #         print(json_searched)
                    #         with session_mysql:
                    #             query = update(Peticioneservidor).values(estado=2, fecha=datetime.now(), parametro2=json_searched).where(
                    #                 (Peticioneservidor.instancia == 'Py1') & (Peticioneservidor.estado == 1))
                    #             session_mysql.execute(query)
                    #             session_mysql.commit()

                    #     case _:
                    #         a['ctimestamp'] = time_stamp
                    #         a['registros'] = []
                    #         json_searched = json.dumps(a)
                    #         print(json_searched)
                    #         with session_mysql:
                    #             query = update(Peticioneservidor).values(estado=2, fecha=datetime.now(), parametro2=json_searched).where(
                    #                 (Peticioneservidor.instancia == 'Py1') & (Peticioneservidor.estado == 1))
                    #             session_mysql.execute(query)
                    #             session_mysql.commit()


if __name__ == "__main__":
    search()
