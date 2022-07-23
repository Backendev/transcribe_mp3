import os,random,jwt
import traceback
from singleton import Singleton

class TokenGen(metaclass=Singleton):
    
    
    
    def __init__(self):
        self.secret = ["eftdrnkbi","eyhfgijfui"]
        self.token = None
    

    def gen_token(self,message):
        self.token = jwt.encode(message, random.choice(self.secret), algorithm='HS256')


    def get_token(self):
        return self.token

    def get_desc_token(self,token):
        token_decode = None
        for i in self.secret:
            try:
                token_decode = jwt.decode(token,i,algorithms=['HS256'])
            except:
                pass
            if token_decode != None:
                return token_decode      
        return False