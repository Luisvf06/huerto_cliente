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

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()
# Create your views here.
#Vistas API


import requests

import os
from pathlib import Path
from requests.exceptions import HTTPError

def index(request):
    return render(request,'index.html')
def crear_cabecera():
    return {'Authorization': 'Bearer ' + env("CLAVE_ADMINISTRADOR"),
}
def huertos_lista_api(request):
    headers={'Authorization': 'Bearer PqKT5fQeiXpL5TPFZcsDBaCAkSgdVQ'}
    response = requests.get('http://127.0.0.1:4999/api/v1/huertos',headers=headers)
    
    huertos=response.json()
    return render(request,'huerto/lista_api.html',{'huertos_mostrar':huertos})

def huertos_lista_mejorada(request):
    headers=crear_cabecera()
    response = requests.get('http://127.0.0.1:4999/api/v1/huertos_mejorada',headers=headers)
    huertos=response.json()
    return render(request,'huerto/lista_mejorada.html',{'huertos_mostrar':huertos})

def Gastos_lista_mejorada(request):
    headers={'Authorization': 'Bearer vwT0f2nGyaNXl6kFDLynuicsBZQTB1'}
    response= requests.get('http://127.0.0.1:4999/api/v1/gastos')
    gastos=response.json()
    return render(request,'gasto/lista_mejorada.html',{'gastos_mostrar':gastos})

            
def Blog_lista_mejorada(request):
    headers={'Authorization': 'Bearer rym15d5na7hpGWtUXgNOncq1OfGTkh'}
    response=requests.get('http://127.0.0.1:4999/api/v1/blogs')
    blogs=response.json()
    return render(request,'blog/lista_mejorada.html',{'blogs_mostrar':blogs})

def huerto_buscar_cl(request):
    formulario=BusquedaHuerto(request.GET)
    
    if formulario.is_valid():
        headers= crear_cabecera()
        response = requests.get('http://127.0.0.1:4999/api/v1/huerto_busqueda_simple',headers=headers,params=formulario.cleaned_data)#en api/v1 antes estaba huertos pero devolvia toda la lista en lugar de las coincidencias, ahora no devuelve nada
        huertos = response.json()
        
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
            response=requests.get('http://127.0.0.1:4999/api/v1/huerto_busqueda_avanzada',headers=headers,params=formulario.data)#huerto_busqueda_avanzada es el nombre que va en el archivo api_urls.py de servidor
            if response.status_code == 200:

                huertos=response.json()
                return render(request,'huerto/lista_mejorada.html',{"huertos_mostrar":huertos})#tengo que crear la plantilla lista mejorada
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la peticion:{http_err}')
            if(response.status_code==400):
                errores=response.json()
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
            response=request.get('')
            response=requests.get('http://127.0.0.1:4999/api/v1/gastos_busqueda_avanzada',headers=headers,params=formulario.data)
            if response.status_code==200:
                gastos=response.json()
                return render(request,'gastos/lista_mejorada.html',{"gastos_mostrar":gastos})#tengo que crear esta plantilla
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la peticion:{http_err}')
            if(response.status_code==400):
                errores=response.json()
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

def huerto_crear(request):
    if(request.method=="POST"):
        try:
            formulario=HuertoForm(request.POST)
            headers= {
                "Content-Type": "application/json"
            }
            datos=formulario.data.copy()
            datos["usuarios"]= request.POST.getlist("usuarios");
            response=requests.post(
                'http://127.0.0.1:4999/api/v1/huertos/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("huerto_lista")
            else:
                print(response.status.code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
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
        
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)