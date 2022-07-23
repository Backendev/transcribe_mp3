import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from singleton import Singleton
import os
from data_aux import DataAux

class Data(metaclass=Singleton):
    def __init__(self):
        config = 'config.json'
        self.cred = credentials.Certificate(config)
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.users_col = self.db.collection(u'users')
        self.da = DataAux()


#___________________________________________________#
#######_________________USERS_________________#######
#___________________________________________________#
    def get_users(self):
        users = list(self.users_col.stream())
        result = {}
        for doc in users:
            result = doc.to_dict(),doc.id
        return result

    def get_user(self,user,passd=None,idu=None):
        docs = []
        if idu != None:
            users = list(self.users_col.where(u'user', u'==',user).stream())
            if users[0].id == idu:
                docs = users
        elif passd != None:
            passd = self.da.cipher_pass(passd)
            docs = list(self.users_col.where(u'user', u'==',user).where(u'pass',u'==',passd).stream())
        else:
            docs = list(self.users_col.where(u'user', u'==',user).stream())
        l = len(list(docs))
        result = None
        if l > 0:
            for doc in docs:
                result = doc.to_dict(),doc.id
        return result

    def get_user_id(self,idu):
        doc = self.users_col.document(u''+str(idu)).get()
        res = None
        res = doc.to_dict()
        return res

    def new_user(self,user,passd):
        print("2222")
        user_old = self.get_user(user=user)
        result = None
        print(user)
        if user_old != None:
            result = "Usuario "+str(user)+" ya existe"
        else:
            passd = self.da.cipher_pass(passd)
            docs = list(self.users_col.stream())
            ids = int(len(docs))
            new_id = ids +1
            new_user = self.users_col.document(u''+str(new_id))
            res = new_user.set({
                u'user': user,
                u'pass':passd
            })
            result = "Usuario "+str(user)+" creado"
        return result