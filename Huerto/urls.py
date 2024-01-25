from django.urls import path 
from .import views

urlpatterns =[
    path('',views.index,name='index'),
    path('huerto/lista',views.huertos_lista_api,name='huertos_lista_api'),
    path('huerto/buscar/',views.huerto_buscar_cl,name='huerto_buscar'),
    path('huerto/buscar_avanzada',views.huerto_buscar_avanzada,name='huerto_buscar_avanzada')
]