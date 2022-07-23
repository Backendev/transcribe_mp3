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


    def validate_params(self,request_data,dict_params):
        dict_types = {
            "text":self.validate_text,
            "number":self.validate_number,
            "week":self.validate_week,
            "date":self.validate_date}
        errors_types = {
            "text":"No debe estar vacio;  Debe comenzar con una letra y solo puede contener los siguientes caracteres numeros o -_*+@.",
            "number":"Debe ser un valor numerico",
            "week":"debe tener el siguiente formato [YYYY-W(numerico 1 o 2)] ejemplo 2020-W7",
            "date":"puede tener los siguientes formatos [YYYY-MM|M-DD|D] 2020-2-3 o 2020-02-03 [YYYY MM|M DD|D] 2020 02 03 o 2020 2 3 [YYYY/MM|M/DD|D] 2020/02/03 o 2020/2/3 [MM|M-DD|D-YYYY] 3-2-2020 o 03-02-2020 [MM|M DD|D YYYY] 03 02 2020 o 3 2 2020 [MM|M/DD|D/YYYY] 03/02/2020 o 3/2/2020"}
        list_results = {}
        errors = []
        for k,v in dict_params.items():
            result = dict_types[v](request_data[k])
            list_results[k] = result
            if result == None:
                errors.append("El parametro "+str(k)+" "+str(errors_types[v]))
        return list_results,errors







