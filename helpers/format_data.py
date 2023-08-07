import data.data as data
import json

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


def search_articles(parametros, data_big, time_stamp):
    match parametros:
        case parametros if parametros['search'] != '' and parametros['search'] != None and parametros['search'] is not None:
            print(
                f"---------- search: {parametros['search']} ----------")
            json_searched = search_articles(
                parametros, data_big, time_stamp)
            searched_articles = [
                item for item in data_big if f"{parametros['search'].lower()}" in item['descripcion'].lower()]
            cut_list = searched_articles
            a['ctimestamp'] = time_stamp
            a['registros'] = cut_list
            json_searched = json.dumps(json_searched)
            print(json_searched)
            with session_mysql:
                query = update(Peticioneservidor).values(estado=2, fecha=datetime.now(), parametro2=json_searched).where(
                    (Peticioneservidor.instancia == 'Py1') & (Peticioneservidor.estado == 1))
                session_mysql.execute(query)
                session_mysql.commit()

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
