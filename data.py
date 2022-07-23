import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from singleton import Singleton
import os

class Data(metaclass=Singleton):
    def __init__(self):
        config = 'config.json'
        self.cred = credentials.Certificate(config)
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.users_col = self.db.collection(u'users')

    def get_users(self):
        users = list(self.users_col.stream())
        result = {}
        for doc in users:
            result = doc.to_dict(),doc.id
        return result