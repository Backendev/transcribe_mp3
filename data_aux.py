from datetime import datetime
import re,os,calendar
import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

class DataAux():

    def __init__(self):
        self.iv =  'BBBBBBBBBBBBBBBB'.encode('utf-8')
        self.secret = "3zYzcqzv4h2zn2b4bNcqYD8YzVOZGdON"


    def cipher_pass(self,text):
        text = str(text)
        key = self.secret
        data= pad(text.encode(),16)
        cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,self.iv)
        cipher= base64.b64encode(cipher.encrypt(data))
        result = cipher.decode("utf-8", "ignore")
        return result


    def decipher_pass(self,text):
        text = str(text)
        key = self.secret
        enc = base64.b64decode(text)
        decipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, self.iv)
        decipher= unpad(decipher.decrypt(enc),16)
        result = decipher.decode("utf-8", "ignore")
        return result



        

    @staticmethod
    def validate_result(result,text):
        if len(result) > 0 and result[0] == text:
            result = text
        else:
            result = None
        return result
    

    def validate_text(self,text):
        patron = r"[A-Za-z\s]*[A-Za-z-_*+@.0-9\s]*"
        result = re.findall(patron,text)
        if len(text) == 0:
            result = []
        return self.validate_result(result,text)
        
    
    def validate_number(self,text):
        patron = r"[0-9]*"
        result = re.findall(patron,text)
        return self.validate_result(result,text)
        
    
    def validate_week(self,text):
        patron = r"[0-9]{4}-W[0-9]{1,2}"
        result = re.findall(patron,text)
        return self.validate_result(result,text)







