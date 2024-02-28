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
    path('huerto/mostrar/<int:id_huerto>',views.huerto_obtener,name='huerto_obtener'),
    path('gastos/buscas_avanzada',views.gastos_buscar_avanzada,name='gastos_buscar_avanzada'),
    path('blog/buscar_avanzada',views.blog_buscar_avanzada,name='blog_buscar_avanzada'),
    path('gastos/crear',views.gastos_crear,name='gastos_crear'),
    path('blog/crear',views.blog_crear,name='blog_crear'),
    path('gastos/eliminar/<int:gasto_id>',views.gastos_eliminar,name='gastos_eliminar'),
    path('blog/eliminar/<int:blog_id>',views.blog_eliminar,name='blog_eliminar'),
    path('huerto/editar/<int:huerto_id>',views.huerto_put,name='huerto_put'),
    path('gasto/actualizar/<int:id_gasto>',views.gasto_put,name='gasto_put'),
    path('blog/actualizar/<int:id_blog>',views.blog_put,name='blog_put'),



    path('huerto/actualizar/ubicacion/<int:id_huerto>',views.huerto_patch_ubi,name='huerto_patch_ubi'),
    path('huerto/actualizar/sitio/<int:id_huerto>',views.huerto_patch_sit,name='huerto_patch_sit'),
    path('huerto/actualizar/abonado/<int:id_huerto>',views.huerto_patch_abo,name='huerto_patch_abo'),
    path('huerto/actualizar/sustrato/<int:id_huerto>',views.huerto_patch_sus,name='huerto_patch_sus'),
    path('huerto/actualizar/area/<int:id_huerto>',views.huerto_patch_are,name='huerto_patch_are'),
    path('huerto/actualizar/acidez/<int:id_huerto>',views.huerto_patch_aci,name='huerto_patch_aci'),


    path('gasto/actualizar/factura/<int:id_gasto>',views.gasto_patch_factura,name='gasto_patch_factura'),
    path('gasto/actualizar/imprevisto/<int:id_gasto>',views.gasto_patch_imprevisto,name='gasto_patch_imprevisto'),
    path('gasto/actualizar/herramienta/<int:id_gasto>',views.gasto_patch_herramienta,name='gasto_patch_herramienta'),
    path('gasto/actualizar/descripcion/<int:id_gasto>',views.gasto_patch_descripcion,name='gasto_patch_descripcion'),
    path('gasto/actualizar/fecha/<int:id_gasto>',views.gasto_patch_fecha,name='gasto_patch_fecha'),

    path('blog/actualizar/etiqueta/<int:id_blog>',views.blog_patch_etiqueta,name='blog_patch_etiqueta'),
    path('blog/actualizar/publicacion/<int:id_blog>',views.blog_patch_publicacion,name='blog_patch_publicacion'),
    path('blog/actualizar/fecha/<int:id_blog>',views.blog_patch_fecha,name='blog_patch_fecha'),

    path('registrar',views.registrar,name='registrar'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    
#tarea final
    #Gabriela
    path('planta/recomendacion/<str:estacion>',views.plantas_estacion,name='recomendacion'),
    
    #Manuel
    path('huerto/disponibles',views.huerto_disponible,name='huerto_disponible'),
    
    #Irene
    path('huerto/recolectable/<int:id_huerto>',views.huerto_recolectable,name='huerto_recoletable'),

    #Álvaro

    #Alberto
    path('huerto/regar/<int:id_usuario>',views.aviso_riego,name='aviso_riego'),
    path('planta/regada',views.riego_planta_crear,name='riego_planta_crear'),#con esto quiero que al crear un neuvo evento de riego se resetee la fecha

    #Ivan
    path('huerto/peligrosidad/<int:id_huerto>',views.huerto_peligrosidad,name='huerto_peligrosidad'),
]