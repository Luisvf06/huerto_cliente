import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

class helper:
    def obtener_usuarios_select():
        response=requests.get('http://127.0.0.1:4999/api/v1/usuario')#tengo que crearlo en servidor para que funcione
        usuarios=response.json()
        lista_usuarios=[("","Ninguno")]
        for usuario in usuarios:
            lista_usuarios.append(usuario["id"],usuario["username"])
        return lista_usuarios
    
    def obtener_huerto(id):
        response = requests.get('http://127.0.0.1:4999/api/v1/huerto'+str(id))#esta apiview no es la de huertos, es otra
        huerto=response.json()
        return huerto