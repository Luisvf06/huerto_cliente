from django.urls import path 
from .import views

urlpatterns =[
    path('',views.index,name='index'),
    path('huerto/lista',views.huertos_lista_api,name='huertos_lista_api')
]