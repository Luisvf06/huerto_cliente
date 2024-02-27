import requests
import environ
import os
from pathlib import Path
versionServer='http://127.0.0.1:4999/api/v1' 
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)

class helper:
    def crear_cabecera():
        return {'Authorization': 'Bearer ' + env("CLAVE_ADMINISTRADOR"),"Content-Type": "application/json"}
    def obtener_usuarios_select():
        headers={'Authorization': 'Bearer '+env("CLAVE_ADMINISTRADOR")}
        response = requests.get('http://127.0.0.1:4999/api/v1/usuario', headers=headers)
        try:
            usuarios = response.json()
            if not isinstance(usuarios, list):
                print("La respuesta no es una lista: ", usuarios)
                return []
            lista_usuarios = [("", "Ninguno")]
            for usuario in usuarios:
                lista_usuarios.append((int(usuario["id"]), usuario["username"]))
            return lista_usuarios
        except ValueError as e:
            print("Error decodificando JSON: ", e)
            return []

    
    def obtener_huerto(id):
        headers={'Authorization': 'Bearer '+env("CLAVE_ADMINISTRADOR")}
        response = requests.get('http://127.0.0.1:4999/api/v1/huerto/'+str(id))#esta apiview no es la de huertos, es otra
        huerto=response.json()
        return huerto
    
    def obtener_gasto(id):
        headers={'Authorization': 'Bearer '+env("CLAVE_ADMINISTRADOR")}
        response = requests.get(versionServer+'/gasto/'+str(id))#esta apiview no es la de huertos, es otra
        gasto=response.json()
        return gasto
    
    def obtener_blog(id):
        headers={'Authorization': 'Bearer '+env("CLAVE_ADMINISTRADOR")}
        response = requests.get(versionServer+'/blog/'+str(id))#esta apiview no es la de huertos, es otra
        blog=response.json()
        return blog
    
    def obtener_token_session(usuario,password):
        token_url='http://127.0.0.1:4999/oauth2/token/'
        data={'grant_type':'password',
            'username':usuario,
            'password':password,
            'client_id':'aplicacion',
            'client_secret':'aplicacion_secret',
            }
        response=requests.post(token_url,data=data)
        respuesta=response.json()
        if response.status_code==200:
            return respuesta.get('access_token')
        else:
            raise Exception (respuesta.get("error_description"))
        
#Alberto
    def obtener_Planta(id):
        headers={'Authorization': 'Bearer '+env("CLAVE_ADMINISTRADOR")}
        response = requests.get(versionServer+'/planta/'+str(id))#esta apiview no es la de huertos, es otra
        planta=response.json()
        return planta