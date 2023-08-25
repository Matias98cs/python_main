import data.data as data
import json
import requests


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


# def products_api():
#     json_products = requests.get(
#         'https://api.escuelajs.co/api/v1/products', verify=False)
#     data_products = json.loads(json_products.content)
#     return data_products


def promo_json():
    json_promos = data.ofertas
    articles = json_promos
    return articles
