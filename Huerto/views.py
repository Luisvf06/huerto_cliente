from django.shortcuts import render,redirect
from .forms import *
# Create your views here.
#Vistas API


import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# Create your views here.
#Vistas API


import requests

import os
from pathlib import Path


def index(request):
    return render(request,'index.html')
def crear_cabecera():
    return {'Authorization': 'Bearer OjSzCkAWynmruDYbzT7MV4QAmavcV9'}
def huertos_lista_api(request):
    headers={'Authorization': 'Bearer OjSzCkAWynmruDYbzT7MV4QAmavcV9'}
    response = requests.get('http://127.0.0.1:4999/api/v1/huertos',headers=headers)
    
    huertos=response.json()
    return render(request,'huerto/lista_api.html',{'huertos_mostrar':huertos})

def huerto_buscar_cl(request):
    formulario=BusquedaHuerto(request.GET)
    
    if formulario.is_valid():
        headers= crear_cabecera()
        response = requests.get('http://127.0.0.1:4999/api/v1/huertos',headers=headers,params=formulario.data)
        huertos = response.json()
        
        return render(request, 'huerto/lista_api.html',{"huertos_mostrar":huertos})
    if ("HTTP_REFERER"in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index.html")