from flask import Flask, request
from generate_token import TokenGen
from data import Data
from data_aux import DataAux

tg = TokenGen()
d = Data()
da = DataAux()

app = Flask(__name__)

_port = 5000



@app.route('/',methods=['GET'])
def inicio():
    return "Iniciando"



@app.route('/login',methods=['GET'])
def login():
    users = d.get_users()
    print(users)
    return "Ok"


@app.route('/crypto',methods=['POST'])
def crypto():
    request_data = request.args.to_dict()
    txt = request_data['texto']
    print(f"333 --- {txt}")
    cryp = da.cipher_pass(txt)
    print(cryp)
    decryp = da.decipher_pass(cryp)
    print(decryp)
    return "Ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=_port)