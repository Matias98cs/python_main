from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
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

    def __init__(self, parametro1, estado):
        self.parametro1 = parametro1
        self.estado = estado


def insertar_y_obtener_datos(parametro1):
    try:
        with db.session.begin():
            obj_saved = Peticioneservidor(parametro1=parametro1, estado=0)
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
    find = db.session.query(Peticioneservidor).filter_by(
        id=consult_id).first()
    response = make_response(find.parametro2, 200)
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
