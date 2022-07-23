import os,random,jwt
from singleton import Singleton

class TokenGen(metaclass=Singleton):
    
    
    
    def __init__(self):
        self.secret = ["eftdrnkbi","eyhfgijfui"]
        self.token = None
    

    def gen_token(self,message):
        self.token = jwt.encode(message, random.choice(self.secret), algorithm='HS256')


    def get_token(self):
        return self.token