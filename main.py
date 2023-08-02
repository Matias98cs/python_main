import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
import json
from datetime import datetime
import requests
from types import SimpleNamespace
from sqlalchemy import func
import calendar
import time
import json
import data

a = {'statussalida': '',
     'registros': '',
     'camposseguros': '',
     'ctimestamp': '',
     }


def searchDB(DB):
    driver = DB['driver'][1:11]
    if driver == 'SQL Server':
        URI = f'mysql+pymysql://{DB["username"]}:{DB["password"]}@{DB["server"]}:{DB["port"]}/{DB["database"]}'
    elif driver == 'PostgreSQL':
        URI = f'postgresql+psycopg2://{DB["username"]}:{DB["password"]}@{DB["server"]}:{DB["port"]}/{DB["database"]}'
    return URI


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


def search(SQLALCHEMY_DATABASE_URI, articles):
    engine = sqlalchemy.create_engine(
        SQLALCHEMY_DATABASE_URI, pool_recycle=1800, pool_size=100, max_overflow=100, echo=False)

    fecha = datetime.today().strftime('%Y-%m-%d')
    fecha_aux = 1
    n = 1
    print('Andando...')
    while True:
        if fecha_aux == 1 or fecha_aux > fecha:
            json_read = articles
            json_text = json_read
            fecha = datetime.today().strftime('%Y-%m-%d')

        fecha_aux = datetime.today().strftime('%Y-%m-%d')
        connection = engine.connect()
        connection.execute(sqlalchemy.text(
            f"UPDATE peticioneservidor SET instancia='Py1', estado=1, fechainsercion=CURRENT_TIMESTAMP WHERE estado=0"))

        connection.commit()
        connection.close()

        connection_2 = engine.connect()
        time.sleep(0.01)
        result = connection_2.execute(sqlalchemy.text(
            "SELECT * FROM peticioneservidor WHERE instancia='Py1' and estado=1"))
        res2 = result.fetchall()

        if res2 == []:
            # print('vacio')
            time.sleep(0.1)

        connection_2.close()

        for item in res2:
            data_big = json_text
            current_time = time.gmtime()
            time_stamp = current_time
            n += 1
            if item.parametro1 != '{}':
                obj_string = json.loads(
                    item.parametro1, object_hook=lambda d: SimpleNamespace(**d))

                parametros = {
                    "search": obj_string.s,
                    "categoria": obj_string.categoria,
                }
                print(f'------------ encontrado: {n} ------------')
                match parametros:
                    case parametros if parametros['search'] != '' and parametros['search'] != None:
                        print(
                            f"---------- search: {parametros['search']} ----------")
                        searched_articles = [
                            item for item in data_big if f"{parametros['search'].lower()} " in item['descripcion'].lower()]
                        cut_list = searched_articles
                        a['ctimestamp'] = time_stamp
                        a['registros'] = cut_list
                        json_searched = json.dumps(a)
                        print(json_searched)
                        connection3 = engine.connect()
                        query = text("Update Peticioneservidor SET estado=2,"
                                     " fecha=CURRENT_TIMESTAMP, parametro2='"+json_searched+"' WHERE instancia='Py1' AND estado=1")
                        connection3.execute(query)
                        connection3.commit()
                        connection3.close()

                    case parametros if parametros['categoria'] != '' and parametros['categoria'] != None:
                        print(
                            f"---------- categoria: {parametros['categoria']} ----------")
                        search_categoria = [item for item in data_big if int(
                            parametros['categoria']) == int(item['categoria']['categoria'])]
                        cut_list = search_categoria
                        a['ctimestamp'] = time_stamp
                        a['registros'] = cut_list
                        json_searched = json.dumps(a)
                        print(json_searched)
                        connection4 = engine.connect()
                        query = text("Update Peticioneservidor SET estado=2,"
                                     " fecha=CURRENT_TIMESTAMP, parametro2='"+json_searched+"' WHERE instancia='Py1' AND estado=1")
                        connection4.execute(query)
                        connection4.commit()
                        connection4.close()

                    case parametros if parametros['search'] == '' and parametros['categoria'] == '':
                        a['ctimestamp'] = time_stamp
                        a['registros'] = []
                        json_searched = json.dumps(a)
                        connection5 = engine.connect()
                        query = text("Update Peticioneservidor SET estado=2,"
                                     " fecha=CURRENT_TIMESTAMP, parametro2='"+json_searched+"' WHERE instancia='Py1' AND estado=1")
                        connection5.execute(query)
                        connection5.commit()
                        connection5.close()


if __name__ == '__main__':
    arch = open('ConfigDB.ini', 'r')
    DB = eval(arch.read())
    SQLALCHEMY_DATABASE_URI = searchDB(DB)
    articles = format_json()
    search(SQLALCHEMY_DATABASE_URI, articles)
