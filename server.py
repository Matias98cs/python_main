from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from sub_main.models import Ofertas, Promocion
import json
import time
import asyncio


def searchDB(DB):
    driver = DB['driver'][1:11]
    if driver == 'SQL Server':
        # URI = f'mssql+pymssql://{DB["username"]}:{DB["password"]}@{DB["server"]}:{DB["port"]}/{DB["database"]}'
        URI = f'mysql+pymysql://{DB["username"]}:{DB["password"]}@{DB["server"]}:{DB["port"]}/{DB["database"]}'
    elif driver == 'PostgreSQL':
        URI = f'postgresql+psycopg2://{DB["username"]}:{DB["password"]}@{DB["server"]}:{DB["port"]}/{DB["database"]}'
    return URI


arch = open('configDB.ini', 'r')
DB = eval(arch.read())
SQLALCHEMY_DATABASE_URI = searchDB(DB)
app = Flask(__name__)
# CORS(app, origins=["http://localhost:5173"])
CORS(app, origins=["*"])
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


with app.app_context():
    db.create_all()


class Peticioneservidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instancia = db.Column(db.String)
    estado = db.Column(db.Integer)
    parametro1 = db.Column(db.String)
    parametro2 = db.Column(db.String)
    fechainsercion = db.Column(db.DateTime)
    fecha = db.Column(db.DateTime)
    peticion = db.Column(db.Integer)

    def __init__(self, parametro1, estado, peticion):
        self.parametro1 = parametro1
        self.estado = estado
        self.peticion = peticion


class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    precio = db.Column(db.Integer)
    descripcion = db.Column(db.String)
    categoria_id = db.Column(db.Integer)


class Categorias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)


def insertar_y_obtener_datos(parametro1):
    try:
        with db.session.begin():
            obj_saved = Peticioneservidor(
                parametro1=parametro1, estado=0, peticion=724)
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
    consult_id = insertar_y_obtener_datos(parametro1)
    await asyncio.sleep(0.01)
    find = db.session.query(Peticioneservidor).filter_by(id=consult_id).first()
    if find.parametro2 is not None:
        response = make_response(find.parametro2, 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response([], 200)
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
