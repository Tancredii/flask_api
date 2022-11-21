from flask import Flask, request, Response
from flask_sqlachemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/db'


db = SQLAlchemy(app)

class Client(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True)
    birthday = db.Column(db.Datetime)
    cpf = db.Column(db.String(11))

    def to_json(self):
        return {"id": self.id, "name": self.name, "email": self.email, "birthday": self.birthday, "cpf": self.cpf}


    #criar cliente
    @app.route("/client", methods=["POST"])
    def register_client():
        body = request.get_json()

        try:
            client = Client(name=body["name"], email=body["email"], birthday=body["birthday"], cpf=body["birthday"])
            db.session.add(client)
            db.session.commit()
            return gera_response(201, "client", client.to_json(), "criado com sucesso")
        except Exception as e:
            print(e)
            return gera_response(400, "client", {}, "erro ao cadastrar")


    #Editar cliente
    @app.route("client/<id>", methods=["PUT"])
    def update_client(id):
        client_obj = Client.query.filter_by(id=id).first()
        body = request.get_json()

        try:
            if('name' in body):
                client_obj.name = body['name']
            if ('email' in body):
                client_obj.email = body['email']
            if ('birthday' in body):
                client_obj.birthday = body['birthday']
            if ('cpf' in body):
                client_obj.cpf = body['cpf']

            db.session.add(client_obj)
            db.session.commit
            return gera_response(200, "client", client_obj.to_json(), "Atualizado com sucesso")
        except Exception as e:
            print('Erro', e)
            return gera_response(400, "client", {}, "Erro ao atualizar")

    # lista um cliente especifico
    @app.route("client/<id>", methods=["GET"])
    def client_id(id):
        client_obj = Client.query.filter_by(id=id).first()
        client_json = client_obj.to_json()

        return gera_response(200, "client", client_json)


    #listar clientes
    @app.route("/clients, methods=["GET"])
    def select_clients():
        client_obj = Client.query.all()
        client_json = [client.to_json() for client in client_obj]

        return gera_response(200, "clients", client_json)


    def gera_response(status, nome_conteudo, conteudo, mensagem=False):
        body = {}
        body[nome_conteudo] = conteudo

        if(mensagem):
            body["mensagem"] = mensagem

        return Response(json.dumps(body), status=status, mimetype="application/json")

    app.run()



