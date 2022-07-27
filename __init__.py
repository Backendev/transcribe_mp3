from datetime import datetime
from flask import Flask, request
from generate_token import TokenGen
from data import Data
from data_aux import DataAux
import json,os
from functools import wraps
from utils import Utils

tg = TokenGen()
d = Data()
da = DataAux()
ut = Utils()
app = Flask(__name__)

_port = 5000

def generate_response(message,code=200,type="text"):
    response = None
    if type == "json":
        response = app.response_class(
            response=json.dumps(message),
            status=code,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=message,
            status=code,
            mimetype='text/plain'
        )
    return response


def verify_token(fun):
    @wraps(fun)
    def verifing(*args,**kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        token = auth_headers[1]
        result = False
        try:
            result = tg.get_desc_token(token)
            if result != False:
                user_id = str(list(result.keys())[0])
                token = True
                return fun(user_id)
            else:
                resp = "Token Incorrecto"
                return generate_response(resp,302)
        except Exception as e:
            resp = "Error en el servidor"
            return generate_response(resp,500)


    return verifing


@app.route('/',methods=['GET'])
def inicio():
    return "Iniciando"



@app.route('/login',methods=['POST'])
def login():
    request_data = request.args.to_dict()
    user = request_data['user']
    passd = request_data['pass']
    res = d.get_user(user,passd)
    if res != None:
        try:
            message = {res[1]:res[0]['user']}
            token = tg.gen_token(message)
            result = tg.get_token()
            return generate_response(result,200)
        except:
            return generate_response("error",500)
    else:
        return generate_response("Usuario o contraseña incorrectos",200)

@app.route('/new_user',methods=['POST'])
@verify_token
def new_user(user):
    request_data = request.args.to_dict()
    try:
        user = request_data['user']
        passd = request_data['pass']
        print(f"user {user}")
        print(f"pass {passd}")
        
        resp = d.new_user(user,passd)
        print(f"user res {resp}")
        return generate_response(resp,200)
    except:
        return generate_response("error",500)


@app.route('/crypto',methods=['POST'])
def crypto():
    request_data = request.args.to_dict()
    txt = request_data['texto']
    cryp = da.cipher_pass(txt)
    print(cryp)
    decryp = da.decipher_pass(cryp)
    print(decryp)
    return "Ok"


@app.route('/verify',methods=['POST'])
@verify_token
def verify(user):
    user = d.get_user_id(user)
    return generate_response("Yes",200)


@app.route('/transcode',methods=['POST'])
@verify_token
def transcode(user):
    request_data = request.args.to_dict()
    words = request_data['words']
    route = request_data['route']
    text_audio = ut.read_mp3(route,words)
    print(text_audio)
    data = {'mp3_file':route,'response':text_audio,"date":datetime.now()}
    d.add_history(data)
    return generate_response(text_audio,200)

@app.route('/history',methods=['GET'])
@verify_token
def get_history(user):
    history = d.get_history()
    return history


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=_port)