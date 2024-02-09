from django.urls import path 
from .import views


urlpatterns =[
    path('',views.index,name='index'),
    path('huerto/lista',views.huertos_lista_api,name='huertos_lista_api'),
    path('gasto/listaMejorada',views.gastos_lista_mejorada,name='gasto_lista_api'),
    path('blog/listaMejorada',views.Blog_lista_mejorada,name='blog_lista_api'),
    path('huerto/listaMejorada',views.huertos_lista_mejorada,name='huertos_lista_mejorada_api'),
    
    
    path('huerto/buscar/',views.huerto_buscar_cl,name='huerto_buscar'),
    path('huerto/buscar_avanzada',views.huerto_buscar_avanzada,name='huerto_buscar_avanzada'),
    path('huerto/crear',views.huerto_crear,name='huertos_crear'),
    path('huerto/eliminar/<int:huerto_id>', views.huerto_eliminar,name='huerto_eliminar'),

    path('gastos/buscas_avanzada',views.gastos_buscar_avanzada,name='gastos_buscar_avanzada'),
    path('blog/buscar_avanzada',views.blog_buscar_avanzada,name='blog_buscar_avanzada'),
    path('gastos/crear',views.gastos_crear,name='gastos_crear'),
    path('blog/crear',views.blog_crear,name='blog_crear'),
    path('gastos/eliminar/<int:gasto_id>',views.gastos_eliminar,name='gastos_eliminar'),
    path('blog/eliminar/<int:blog_id>',views.blog_eliminar,name='blog_eliminar'),
    path('huerto/actualizar/<int:id_huerto>',views.huerto_put,name='huerto_put'),
    path('gasto/actualizar/<int:id_gasto>',views.gasto_put,name='gasto_put'),
    path('blog/actualizar/<int:id_blog>',views.blog_put,name='blog_put')
]