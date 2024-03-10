import requests
import environ
import os
from pathlib import Path
versionServer='https://luisvf3.pythonanywhere.com/api/v1' 
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)

class helper:
    def crear_cabecera():
        return {'Authorization': 'Bearer ' + env("CLAVE_ADMINISTRADOR"),"Content-Type": "application/json"}
    
    def obtener_usuarios_select():
        headers={'Authorization': 'Bearer '+env("CLAVE_ADMINISTRADOR")}
        response = requests.get(versionServer+'/usuario', headers=headers)
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
        response = requests.get(versionServer+'/huerto/'+str(id))#esta apiview no es la de huertos, es otra
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
        token_url=versionServer+ '/oauth2/token/'
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
        response = requests.get(versionServer+'/planta/'+str(id),headers=headers)#esta apiview no es la de huertos, es otra
        planta=response.json()
        return planta
    def obtener_plantas_select():
        headers={'Authorization': 'Bearer '+env("CLAVE_ADMINISTRADOR")}
        response = requests.get(versionServer+'/plantas', headers=headers)
        try:
            plantas = response.json()
            if not isinstance(plantas, list):
                print("La respuesta no es una lista: ", plantas)
                return []
            lista_plantas = [("", "Ninguno")]
            for planta in plantas:
                lista_plantas.append((int(planta["id"]),planta["id"]))
            return lista_plantas
        except ValueError as e:
            print("Error decodificando JSON: ", e)
            return []

    def obtener_riegos_select():
        headers={'Authorization': 'Bearer '+env("CLAVE_ADMINISTRADOR")}
        response = requests.get(versionServer+'/riegos', headers=headers)
        try:
            riegos = response.json()
            if not isinstance(riegos, list):
                print("La respuesta no es una lista: ", riegos)
                return []
            lista_riegos = [("", "Ninguno")]
            for riego in riegos:
                lista_riegos.append((int(riego["id"]), riego["id"]))
            return lista_riegos
        except ValueError as e:
            print("Error decodificando JSON: ", e)
            return []
    
    def obtener_Riego(id):
        headers={'Authorization': 'Bearer'+ env('CLAVE_ADMINISTRADOR')}
        response = requests.get(versionServer+'/riego/'+str(id))
        riego=response.json()
        return riego
    
    def obtener_PlantaRiego(id):
        headers={'Authorization': 'Bearer' + env('CLAVE_ADMINISTRADOR')}
        response = requests.get(versionServer +'/plantariego'+str(id))
        riego=response.json()
        return riego