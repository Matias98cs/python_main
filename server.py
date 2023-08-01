import sqlalchemy
import requests
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, update, func
import time
from sqlalchemy.exc import SQLAlchemyError
import json
from datetime import datetime
from types import SimpleNamespace


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

    def __init__(self, parametro2):
        self.parametro2 = parametro2


@app.route('/', methods=['GET'])
def home():
    categoria = request.args.get('categoria')
    search = request.args.get('s')
    rangoregistros = request.args.get('rangoregistros')
    sucursal = request.args.get('sucursal')
    print(
        f"search: {search} | categoria: {categoria} | rangoregistros: {rangoregistros} | sucursal: {sucursal}")
    parametro2 = {
        "s": search,
        "categoria": categoria,
        "rangoregistros": rangoregistros,
        "sucursal": sucursal,
    }
    parametro2 = json.dumps(parametro2)
    params = Peticioneservidor(parametro2=parametro2)
    db.session.add(params)
    db.session.commit()
    print(params)
    return []


if __name__ == '__main__':
    app.run(debug=True)
