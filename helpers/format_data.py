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


def promo_json():
    json_promos = data.ofertas
    articles = json_promos
    return articles
