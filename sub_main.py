from sqlalchemy import select, update
from sqlalchemy.sql import text
from database import crear_conexion, obtener_session
from models import Base, Peticioneservidor
from types import SimpleNamespace
import data
import time
import json
import calendar
from datetime import datetime

arch = open('ConfigDB.ini', 'r')
DB = eval(arch.read())
base_general = "pruebaspython"
engine_mysql = crear_conexion(
    f"{DB['username']}", f"{DB['password']}", f"{DB['server']}", base_general)


Base.metadata.create_all(engine_mysql)
session_mysql = obtener_session(engine_mysql)

a = {'statussalida': '',
     'registros': '',
     'camposseguros': '',
     'ctimestamp': '',
     }


def format_json():
    json_articulos = data.articulosWeb
    json_categoriasArticulosWeb = data.categoriasArticulosWeb

    articles = json_articulos['registros']

    categorias_dict = {f"{categoria['marca']}-{categoria['codigo']}":
                       categoria for categoria in json_categoriasArticulosWeb['registros']}

    for i in articles:
        key = f"{i['marca']}-{i['codigo']}"
        if key in categorias_dict:
            i['categoria'] = categorias_dict[key]

    articles = [item for item in articles if 'categoria' in item]
    return articles


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
        # consulta_1 = update(Peticioneservidor).values(instancia='Py1', estado=1,
        #                                               fechainsercion=datetime.now()).where(Peticioneservidor.estado == 0)

        with session_mysql:
            consulta_1 = update(Peticioneservidor).values(instancia='Py1', estado=1,
                                                          fechainsercion=datetime.now()).where(Peticioneservidor.estado == 0)
            session_mysql.execute(consulta_1)
            session_mysql.commit()

        # session_mysql.commit()
        # session_mysql.execute(consulta_1)
        # session_mysql.commit()
        # session_mysql.close()

        consulta_2 = select(Peticioneservidor.parametro1).where(
            (Peticioneservidor.instancia == 'Py1') & (Peticioneservidor.estado == 1))

        select_consult = session_mysql.execute(consulta_2).fetchall()
        # print(select_consult)
        # if select_consult == []:
        #     # print('VACIO')
        #     time.sleep(0.01)
        # session_mysql.close()

        for item in select_consult:
            print(item)
            current_time = time.gmtime()
            time_stamp = calendar.timegm(current_time)
            n += 1
            if item.parametro1 != '{}':
                obj_string = json.loads(
                    item.parametro1, object_hook=lambda d: SimpleNamespace(**d))

                parametros = {
                    "search": obj_string.s,
                    "categoria": obj_string.categoria,
                }
                match parametros:
                    case parametros if parametros['search'] != '' and parametros['search'] != None and parametros['search'] is not None:
                        print(
                            f"---------- search: {parametros['search']} ----------")
                        searched_articles = [
                            item for item in data_big if f"{parametros['search'].lower()}" in item['descripcion'].lower()]
                        cut_list = searched_articles
                        a['ctimestamp'] = time_stamp
                        a['registros'] = cut_list
                        json_searched = json.dumps(a)
                        print(json_searched)
                        with session_mysql:
                            query = update(Peticioneservidor).values(estado=2, fecha=datetime.now(), parametro2=json_searched).where(
                                (Peticioneservidor.instancia == 'Py1') & (Peticioneservidor.estado == 1))
                            session_mysql.execute(query)
                            session_mysql.commit()
                        # session_mysql.close()
                        # session_mysql.connection()
                        # query = update(Peticioneservidor).values(estado=2, fecha=datetime.now(), parametro2=json_searched).where(
                        #     (Peticioneservidor.instancia == 'Py1') & (Peticioneservidor.estado == 1))
                        # session_mysql.execute(query)
                        # session_mysql.commit()
                        # session_mysql.close()
                    case parametros if parametros['categoria'] != '' and parametros['categoria'] != None and parametros['categoria'] is not None:
                        print(
                            f"---------- categoria: {parametros['categoria']} ----------")
                        search_categoria = [item for item in data_big if int(
                            parametros['categoria']) == int(item['categoria']['categoria'])]
                        cut_list = search_categoria
                        a['ctimestamp'] = time_stamp
                        a['registros'] = cut_list
                        json_searched = json.dumps(a)
                        print(json_searched)
                        with session_mysql:
                            query = update(Peticioneservidor).values(estado=2, fecha=datetime.now(), parametro2=json_searched).where(
                                (Peticioneservidor.instancia == 'Py1') & (Peticioneservidor.estado == 1))
                            session_mysql.execute(query)
                            session_mysql.commit()
                        # session_mysql.close()
                        # session_mysql.connection()
                        # query = update(Peticioneservidor).values(estado=2, fecha=datetime.now(), parametro2=json_searched).where(
                        #     (Peticioneservidor.instancia == 'Py1') & (Peticioneservidor.estado == 1))
                        # session_mysql.execute(query)
                        # session_mysql.commit()
                        # session_mysql.close()
                    case parametros if parametros['search'] == '' and parametros['search'] is not None and parametros['categoria'] != '' and parametros['categoria'] is not None:
                        a['ctimestamp'] = time_stamp
                        a['registros'] = []
                        json_searched = json.dumps(a)
                        print(json_searched)
                        with session_mysql:
                            query = update(Peticioneservidor).values(estado=2, fecha=datetime.now(), parametro2=json_searched).where(
                                (Peticioneservidor.instancia == 'Py1') & (Peticioneservidor.estado == 1))
                            session_mysql.execute(query)
                            session_mysql.commit()
                        # session_mysql.close()
                    case _:
                        a['ctimestamp'] = time_stamp
                        a['registros'] = []
                        json_searched = json.dumps(a)
                        print(json_searched)
                        with session_mysql:
                            query = update(Peticioneservidor).values(estado=2, fecha=datetime.now(), parametro2=json_searched).where(
                                (Peticioneservidor.instancia == 'Py1') & (Peticioneservidor.estado == 1))
                            session_mysql.execute(query)
                            session_mysql.commit()
                        # session_mysql.close()
                        # session_mysql.connection()
                        # query = update(Peticioneservidor).values(estado=2, fecha=datetime.now(), parametro2=json_searched).where(
                        #     (Peticioneservidor.instancia == 'Py1') & (Peticioneservidor.estado == 1))
                        # session_mysql.execute(query)
                        # session_mysql.commit()
                        # session_mysql.close()


if __name__ == "__main__":
    search()
