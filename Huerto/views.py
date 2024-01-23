from django.shortcuts import render,redirect
from django.views.defaults import bad_request
from django.core import serializers
import requests
from django.db.models import Q, Prefetch, Avg
def index(request):
    return render(request,'index.html')

def huertos_lista_api(request):
    headers={'Authorization': 'Bearer OjSzCkAWynmruDYbzT7MV4QAmavcV9'}
    response = requests.get('http://127.0.0.1:4999/api/v1/huertos',headers=headers)
    
    huertos=response.json()
    return render(request,'huerto/lista_api.html',{'huertos_mostrar':huertos})

