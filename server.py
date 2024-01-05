from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from sub_main.models import Ofertas, Promocion, Peticioneservidor, Documentos, Productos, Categorias
from sub_main.database import conexion_uri
import json
import time
import asyncio

app = Flask(__name__)
# CORS(app, origins=["http://localhost:5173"])
CORS(app, origins=["*"])
app.config["SQLALCHEMY_DATABASE_URI"] = conexion_uri
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


def insertar_y_obtener_datos(parametro1, nro_peticion):
    try:
        with db.session.begin():
            obj_saved = Peticioneservidor(
                parametro1=parametro1, estado=0, peticion=nro_peticion)
            db.session.add(obj_saved)
            db.session.flush()
        obj_id = db.session.query(Peticioneservidor).filter_by(
            id=obj_saved.id).first()
        return obj_id.id
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error de integridad: {e}")
    except Exception as e:
        db.session.rollback()
        print(f"Error desconocido: {e}")
    finally:
        db.session.close()


@app.route('/', methods=['GET'])
async def home():
    categoria = request.args.get('categoria')
    search = request.args.get('s')
    rangoregistros = request.args.get('rangoregistros')
    sucursal = request.args.get('sucursal')
    ofertas = request.args.get('ofertas')
    print(
        f"search: {search} | categoria: {categoria} | rangoregistros: {rangoregistros} | sucursal: {sucursal} | ofertas: {ofertas}")
    parametro1 = {
        "s": search,
        "categoria": categoria,
        "rangoregistros": rangoregistros,
        "sucursal": sucursal,
        "ofertas": ofertas,
    }
    parametro1 = json.dumps(parametro1)
    consult_id = insertar_y_obtener_datos(parametro1, 724)
    await asyncio.sleep(0.01)
    find = db.session.query(Peticioneservidor).filter_by(id=consult_id).first()
    if find.parametro2 is not None:
        response = make_response(find.parametro2, 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            {"msg": 'No se contesto la peticion, instancias caidas...'}, 200)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/promocionweb2', methods=['GET'])
async def promociones_ofertas():
    marca = request.args.get('marca')
    codigo = request.args.get('codigo')
    precio = request.args.get('precio')
    timestamp = request.args.get('timestamp')
    cantidad = request.args.get('cantidad')
    clienteol = request.args.get('clienteol')
    instancia = request.args.get('instancia')
    parametro1 = {
        "marca": marca,
        "codigo": codigo,
        "precio": precio,
        "timestamp": timestamp,
        "cantidad": cantidad,
        "clienteol": clienteol,
        "instancia": instancia
    }
    print(f'Promociones web 2 : {parametro1}')
    parametro1 = json.dumps(parametro1)
    consulta_id = insertar_y_obtener_datos(parametro1, 729)
    await asyncio.sleep(0.2)
    find = db.session.query(Peticioneservidor).filter_by(
        id=consulta_id).first()
    if find.parametro2 is not None:
        response = make_response(find.parametro2, 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            {"msg": "Aun no se contesta la peticion, instancias caidas..."}, 200)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/itempedidoweb', methods=['POST'])
def itempedidoweb():
    data_post = request.get_json()
    clienteol = data_post.get('clienteol')
    estado = data_post.get('estado')
    articulos = data_post.get('articulos')
    if clienteol:
        parametros1 = {
            "clienteol": clienteol,
            "estado": estado,
            "articulos": articulos
        }
        print(parametros1)
        articulos_json = json.dumps(articulos)
        existente = db.session.query(Documentos).filter_by(
            clienteol=clienteol).first()
        if existente:
            try:
                existente.articulos = articulos_json
                db.session.commit()
                db.session.close()
                response = make_response(
                    {"msg": 'Documento creado y guardado', "informacion": parametros1}, 200)
                response.headers['Content-Type'] = 'application/json'
                return response
            except Exception as e:
                print(
                    f"Error al actualizar articulos del Documento del cliente: {clienteol} - Error: {e}")
        else:
            try:
                objeto = Documentos(
                    estado='B', articulos=articulos_json, clienteol=clienteol)
                db.session.add(objeto)
                db.session.commit()
                print('Documento guardado')
                response = make_response(
                    {"msg": 'Documento creado y guardado', "informacion": parametros1}, 200)
                response.headers['Content-Type'] = 'application/json'
                db.session.close()
                return response
            except Exception as e:
                print(f"Error al insertar a la tabla Documentos: {e}")

    response = make_response({"msg": "No se envio en ClienteOl"}, 404)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/ofertasweb', methods=['GET'])
def get_ofertas():
    try:
        get_all_ofertas = db.session.query(Ofertas).all()
        ofertas_list = []
        for oferta in get_all_ofertas:
            oferta_dict = {
                "marca": oferta.marca,
                "codigo": oferta.codigo,
                "sucursal": oferta.sucursal,
                "precio": oferta.precio,
            }
            ofertas_list.append(oferta_dict)

        response = make_response({"registro": ofertas_list}, 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        print(f"Error al obtener Ofertas : {e}")
        return jsonify({"error": str(e)})


@app.route('/promocionesweb', methods=['GET'])
def get_promociones():
    try:
        get_all_promociones = db.session.query(Promocion).all()
        promociones_list = []
        for promo in get_all_promociones:
            promocion_dict = {
                "idpromocion": promo.idpromocion,
                "regla1": promo.regla1,
                "regla2": promo.regla2,
                "porcentaje": promo.porcentaje,
                "monto": promo.monto,
                "cantidad1": promo.cantidad1,
                "cantidad2": promo.cantidad2,
                "marca": promo.marca,
                "codigo": promo.codigo,
            }
            promociones_list.append(promocion_dict)
        response = make_response({"registro": promociones_list}, 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        print(f"Error al obtener Promociones : {e}")
        return jsonify({"error": str(e)})


@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        get_all_productos = db.session.query(Productos).all()
        productos_list = []
        for product in get_all_productos:
            product_dict = {
                'id': product.id,
                'nombre': product.nombre,
                'precio': product.precio,
                'descripcion': product.descripcion,
                'categoria_id': product.categoria_id,

            }
            productos_list.append(product_dict)
        response = make_response(productos_list, 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    except Exception as e:
        print(f"Hubo un error: {e}")
        return jsonify({"error": str(e)})


@app.route('/categorias', methods=['GET'])
def get_categorias():
    try:
        get_categorias = db.session.query(Categorias).all()
        categorias_list = []
        for categoria in get_categorias:
            categoria_dict = {
                "id": categoria.id,
                "nombre": categoria.nombre
            }
            categorias_list.append(categoria_dict)
        response = make_response(categorias_list, 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        print(f"Hubo un error: {e}")
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
