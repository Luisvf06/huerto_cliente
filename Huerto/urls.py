from django.urls import path 
from .import views


urlpatterns =[
    path('',views.index,name='index'),
    path('huerto/lista',views.huertos_lista_api,name='huertos_lista_api'),
    path('gasto/listaMejorada',views.Gastos_lista_mejorada,name='gasto_lista_api'),
    path('blog/listaMejorada',views.Blog_lista_mejorada,name='blog_lista_api'),
    path('huerto/listaMejorada',views.huertos_lista_mejorada,name='huertos_lista_mejorada_api'),
    
    
    path('huerto/buscar/',views.huerto_buscar_cl,name='huerto_buscar'),
    path('huerto/buscar_avanzada',views.huerto_buscar_avanzada,name='huerto_buscar_avanzada'),
    #hacer las busquedas de gastos y blog
    path('gastos/buscas_avanzada',views.gastos_buscar_avanzada,name='gastos_buscar_avanzada'),
    #path('blog/buscar_avanzada',views.blog_buscar_avanzada,name='blog_buscar_avanzada'),
    path('huerto/crear',views.huerto_crear,name='huertos_crear')

]