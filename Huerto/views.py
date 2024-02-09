from django.shortcuts import render,redirect
from .forms import *
# Create your views here.
#Vistas API
from .helper import helper
import json
import requests
import environ
import os
from pathlib import Path
from datetime import datetime
from django.http import JsonResponse
import xml.etree.ElementTree as ET
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()
versionServer='http://127.0.0.1:4999/api/v1' 
#Diapositiva 45 Respuesta 1: se puede mejorar incluyendo el v1 en una variable, de forma que todos accediesen a la misma y si se actualizara, sólo hubiera que cambiar el valor donde se declara.
#Respuesta 2 se crea una nueva funcion que tenga en cuenta los dinstitos tipos de tipo de datos y se sustituye en la parte del response
# Create your views here.
#Vistas API



import os
from pathlib import Path
from requests.exceptions import HTTPError

def obtener_respuesta(response):
    # Función para obtener el contenido de la respuesta, independientemente del formato
    content_type = response.headers.get('Content-Type', '').lower()

    if 'application/json' in content_type:
        return response.json()
    elif 'application/xml' in content_type:
        # Aquí puedes implementar la lógica para manejar XML
        xml_content = ET.fromstring(response.text)
        # Devuelve el contenido procesado
        return xml_content
    else:
        # Si el formato no es ni JSON ni XML, puedes manejarlo de acuerdo a tus necesidades
        return response.text

def index(request):
    return render(request,'index.html')
def crear_cabecera():
    return {'Authorization': 'Bearer ' + env("CLAVE_ADMINISTRADOR"),"Content-Type": "application/json"
}
def huertos_lista_api(request):
    headers=crear_cabecera()
    #headers={'Authorization': 'Bearer PqKT5fQeiXpL5TPFZcsDBaCAkSgdVQ'}
    response = requests.get(versionServer+'/huertos',headers=headers)
    
    huertos=obtener_respuesta(response)
    #huertos=response.json() version que solo espera una respuesta en formato json
    return render(request,'huerto/lista_api.html',{'huertos_mostrar':huertos})

def huertos_lista_mejorada(request):
    headers=crear_cabecera()
    response = requests.get(versionServer+'/huertos_mejorada',headers=headers)
    huertos=obtener_respuesta(response)
    return render(request,'huerto/lista_mejorada.html',{'huertos_mostrar':huertos})

def gastos_lista_mejorada(request):
    headers=crear_cabecera()
    response= requests.get(versionServer+'/gastos',headers=headers)
    gastos=obtener_respuesta(response)
    return render(request,'gastos/lista_mejorada.html',{'gastos_mostrar':gastos})

            
def Blog_lista_mejorada(request):
    headers=crear_cabecera()
    response=requests.get(versionServer+'/blogs', headers=headers)
    blogs=obtener_respuesta(response)
    return render(request,'blog/lista_mejorada.html',{'blogs_mostrar':blogs})

def huerto_buscar_cl(request):
    formulario=BusquedaHuerto(request.GET)
    
    if formulario.is_valid():
        headers= crear_cabecera()
        response = requests.get(versionServer+'/huerto_busqueda_simple',headers=headers,params=formulario.cleaned_data)#en api/v1 antes estaba huertos pero devolvia toda la lista en lugar de las coincidencias, ahora no devuelve nada
        huertos = obtener_respuesta(response)
        
        return render(request, 'huerto/lista_api.html',{"huertos_mostrar":huertos})
    if ("HTTP_REFERER"in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index.html")
    

def huerto_buscar_avanzada(request):
    if(len(request.GET)>0):
        formulario=BusquedaAvanzadaHuerto(request.GET)
        try:
            headers=crear_cabecera()
            response=requests.get(versionServer+'/huerto_busqueda_avanzada',headers=headers,params=formulario.data)#huerto_busqueda_avanzada es el nombre que va en el archivo api_urls.py de servidor
            if response.status_code == 200:

                huertos=obtener_respuesta(response)
                return render(request,'huerto/lista_mejorada.html',{"huertos_mostrar":huertos})#tengo que crear la plantilla lista mejorada
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la peticion:{http_err}')
            if(response.status_code==400):
                errores=obtener_respuesta(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'huerto/busqueda_avanzada.html',{"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario=BusquedaAvanzadaHuerto(None)
        return render(request, 'huerto/busqueda_avanzada.html',{"formulario":formulario})

def gastos_buscar_avanzada(request):
    if len(request.GET)>0:
        formulario=BusquedaAvanzadaGastos(request.GET)
        try:
            headers=crear_cabecera()
            response=requests.get(versionServer+'/gastos_busqueda_avanzada',headers=headers,params=formulario.data)
            if response.status_code==200:
                gastos=obtener_respuesta(response)
                return render(request,'gastos/lista_mejorada.html',{"gastos_mostrar":gastos})#tengo que crear esta plantilla
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la peticion:{http_err}')
            if(response.status_code==400):
                errores=obtener_respuesta(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'gastos/busqueda_avanzada.html',{"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario=BusquedaAvanzadaGastos(None)
        return render(request,'gastos/busqueda_avanzada.html',{"formulario":formulario})

def blog_buscar_avanzada(request):
    if len(request.GET)>0:
        formulario=BusquedaAvanzadaBlog(request.GET)
        
        try:
            headers=crear_cabecera()
            response=requests.get(versionServer+'/blog_busqueda_avanzada',headers=headers,params=formulario.data)
            if response.status_code==200:
                blogs=obtener_respuesta(response)
                return render(request,'blog/lista_mejorada.html',{"blogs_mostrar":blogs})#tengo que crear esta plantilla
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la peticion:{http_err}')
            if(response.status_code==400):
                errores=obtener_respuesta(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'blog/busqueda_avanzada.html',{"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario=BusquedaAvanzadaBlog(None)
        return render(request,'blog/busqueda_avanzada.html',{"formulario":formulario})

def huerto_crear(request):
    if(request.method=="POST"):
        try:
            formulario=HuertoForm(request.POST)
            headers= crear_cabecera()
            datos=formulario.data.copy()
            datos["usuarios"]= request.POST.get("usuarios")
            if(not 'abonado' in datos):
                datos['abonado'] = "off"
            response=requests.post(
                versionServer+'/huertos/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("huertos_lista_api")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la peticion: {http_err}')
            if(response.status_code==400):
                errores=obtener_respuesta(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,
                            'huerto/crear_huerto.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)  
    else:
        formulario = HuertoForm(None)
    return render(request,'huerto/crear_huerto.html',{"formulario":formulario})

def gastos_crear(request):
    if request.method == "POST":
        print(request.POST)
        try:
            formulario = GastoForm(request.POST)
            headers = crear_cabecera()
            
            fecha_str = request.POST.get('fecha')
            
            # Convertir la cadena de fecha a un objeto datetime
            fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y')
            
            # Asignar la fecha al formato dd/mm/yyyy
            fecha_formatted = fecha_obj.strftime('%Y-%m-%d')
            
            # Definir los datos a enviar en el POST request
            datos = {
                "fecha": fecha_formatted,
                "herramientas": request.POST.get('herramientas'),
                "facturas": request.POST.get('facturas'),
                "imprevistos": request.POST.get('imprevistos'),
                "Descripcion": request.POST.get('Descripcion'),
                "usuario": request.POST.get('usuario'),
            }
            
            response = requests.post(versionServer+'/gastos/crear', headers=headers, data=json.dumps(datos))
            if response.status_code == requests.codes.ok:
                return redirect("gasto_lista_api")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'gastos/crear_gasto.html', {"formulario": formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = GastoForm(None)
    return render(request, 'gastos/crear_gasto.html', {"formulario": formulario})
def blog_crear(request):
    if (request.method=="POST"):
        try:
            formulario=BlogForm(request.POST)
            headers= crear_cabecera()
            fecha_str = request.POST.get('fecha')
            
            # Convertir la cadena de fecha a un objeto datetime
            fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y')
            
            # Asignar la fecha al formato dd/mm/yyyy
            fecha_formatted = fecha_obj.strftime('%Y-%m-%d')
            
            # Definir los datos a enviar en el POST request
            datos = {
                "fecha": fecha_formatted,
                "publicacion": request.POST.get('publicacion'),
                "etiqueta": request.POST.get('etiqueta'),
                "usuario": request.POST.get('usuario'),
            }
            response=requests.post(versionServer+'/blog/crear', headers=headers, data=json.dumps(datos))
            if(response.status_code==requests.codes.ok):
                return redirect("blog_lista_api")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            #continuar el except

def huerto_obtener(request,huerto_id):
    huerto=helper.obtener_huerto(huerto_id)
    return render(request,'huerto/huerto_mostrar.html',{"huerto":huerto})



def huerto_eliminar(request,huerto_id):
    try:
        headers = crear_cabecera()
        response= request.delete(versionServer+'/huertos/eliminar/'+str(huerto_id),headers=headers)
        if (response.status_code == request.codes.ok):
            return redirect("huertos_lista_mejorada_api")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error:{err}')
        return mi_error_500(request)
    return redirect('huertos_lista_mejorada_api')
'''
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 'blog/crear_blog.html',{"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500
    else:
        formulario=BlogForm(None)
        return render(request,'blog/crear_blog.html',{"formulario":formulario})
'''            
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)