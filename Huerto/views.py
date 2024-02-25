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
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
#from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import datetime



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
    '''
    usuario = request.user.username
    password = usuario.password  # Necesitas obtener la contraseña de alguna manera segura

    # Obtener el token de sesión del usuario logueado
    token = helper.obtener_token_session(usuario, password)

    # Usar el token en la solicitud a la API
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }'''
    headers=crear_cabecera()
    response = requests.get(versionServer + '/gastos', headers=headers)
    gastos = obtener_respuesta(response)
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
            if(not 'disponible' in datos):
                datos['disponible'] ="off"
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
@login_required()
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
@login_required()
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

def gastos_eliminar(request,gastos_id):
    try:
        headers = crear_cabecera()
        response= request.delete(versionServer+'/gastos/eliminar/'+str(gastos_id),headers=headers)
        if (response.status_code == request.codes.ok):
            return redirect("gasto_lista_api")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error:{err}')
        return mi_error_500(request)
    return redirect('gasto_lista_api')

def blog_eliminar(request,blog_id):
    try:
        headers = crear_cabecera()
        response= request.delete(versionServer+'/blog/eliminar/'+str(blog_id),headers=headers)
        if (response.status_code == request.codes.ok):
            return redirect("blog_lista_api")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error:{err}')
        return mi_error_500(request)
    return redirect('blog_lista_api')

def huerto_put(request,huerto_id):
    datosFormulario=None

    if request.method=="POST":
        datosFormulario=request.POST
        huerto=helper.obtener_huerto(huerto_id)
        formulario=HuertoForm(datosFormulario,
                            initial={
                                'ubicacion':huerto['ubicacion'],
                                'sitio':huerto['sitio'],
                                'sustrato':huerto['sustrato'],
                                'acidez':huerto['acidez'],
                                'abonado':huerto['abonado'],
                                'area':huerto['area'],
                                'usuario':huerto['usuario']['id']
                            })
        if(request.method=="POST"):
            try:
                formulario=HuertoForm(request.POST)
                headers=crear_cabecera()
                datos=request.POST.copy()
                datos["usuarios"]= request.POST.get("usuarios")
                if(not 'abonado' in datos):
                    datos['abonado'] = "off"
                response=requests.put(versionServer+'/huerto/editar'+str(huerto_id),headers=headers,data=json.dumps(datos))
                if(response.status_code==requests.codes.ok):
                    return redirect("huertos_lista_mejorada_api",huerto_id=huerto_id)
                else:
                    print(response.status_code)
                    response.raise_for_status()
            except HTTPError as http_err:
                print(f'Hubo un error en la peticion: {http_err}')
                if(response.status_code==400):
                    errores=response.json()
                    for error in errores:
                        formulario.add_error(error,errores[error])
                    return render(request,'huerto/actualizar.html',{"formulario":formulario,"huerto":huerto})
                else:
                    return mi_error_500(request)
            except Exception as err:
                print(f'Ocurrió un rror:{err}')
                return mi_error_500(request)
        return render(request,'huerto/actualizar.html',{"formulario":formulario,"huerto":huerto})
    
def gasto_put(request,gasto_id):
    datosFormulario=None

    if request.method=="POST":
        datosFormulario=request.POST
        gasto=helper.obtener_gasto(gasto_id)
        formulario=GastoForm(datosFormulario,
                            initial={
                                'herramientas':gasto['herramientas'],
                                'facturas':gasto['facturas'],
                                'Descripcion':gasto['Descripcion'],
                                'imprevistos':gasto['imprevistos'],
                                'fecha':datetime.datetime.strptime(gasto['fecha'], '%d-%m%Y').date()

                            })
        if(request.method=="POST"):
            try:
                formulario=GastoForm(request.POST)
                headers=crear_cabecera()
                datos=request.POST.copy()
                fecha_str = request.POST.get('fecha')
            
            # Convertir la cadena de fecha a un objeto datetime
                fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y')
                
                # Asignar la fecha al formato dd/mm/yyyy
                fecha_formatted = fecha_obj.strftime('%Y-%m-%d')

                response=requests.put(versionServer+'/gasto/editar'+str(gasto_id),headers=headers,data=json.dumps(datos))
                if(response.status_code==requests.codes.ok):
                    return redirect("gasto_lista_api",gasto_id=gasto_id)
                else:
                    print(response.status_code)
                    response.raise_for_status()
            except HTTPError as http_err:
                print(f'Hubo un error en la peticion: {http_err}')
                if(response.status_code==400):
                    errores=response.json()
                    for error in errores:
                        formulario.add_error(error,errores[error])
                    return render(request,'gastos/actualizar.html',{"formulario":formulario,"gasto":gasto})
                else:
                    return mi_error_500(request)
            except Exception as err:
                print(f'Ocurrió un rror:{err}')
                return mi_error_500(request)
        return render(request,'gastos/actualizar.html',{"formulario":formulario,"gasto":gasto})
def blog_put(request,blog_id):
    datosFormulario=None

    if request.method=="POST":
        datosFormulario=request.POST
        blog=helper.obtener_gasto(blog_id)
        formulario=GastoForm(datosFormulario,
                            initial={
                                'publicacion':blog['publicacion'],
                                'etiqueta':blog['etiqueta'],
                                'fecha':datetime.datetime.strptime(blog['fecha'], '%d-%m%Y').date()
                            })
        if(request.method=="POST"):
            try:
                formulario=BlogForm(request.POST)
                headers=crear_cabecera()
                datos=request.POST.copy()
                fecha_str = request.POST.get('fecha')
            
            # Convertir la cadena de fecha a un objeto datetime
                fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y')
                
                # Asignar la fecha al formato dd/mm/yyyy
                fecha_formatted = fecha_obj.strftime('%Y-%m-%d')
                response=requests.put(versionServer+'/blog/editar'+str(blog_id),headers=headers,data=json.dumps(datos))
                if(response.status_code==requests.codes.ok):
                    return redirect("blog_lista_api",blog_id=blog_id)
                else:
                    print(response.status_code)
                    response.raise_for_status()
            except HTTPError as http_err:
                print(f'Hubo un error en la peticion: {http_err}')
                if(response.status_code==400):
                    errores=response.json()
                    for error in errores:
                        formulario.add_error(error,errores[error])
                    return render(request,'blog/actualizar.html',{"formulario":formulario,"blog":blog})
                else:
                    return mi_error_500(request)
            except Exception as err:
                print(f'Ocurrió un rror:{err}')
                return mi_error_500(request)
        return render(request,'blog/actualizar.html',{"formulario":formulario,"blog":blog})
    

def huerto_patch_ubi(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_huerto(huerto_id)
    formulario=HuertoActualizarUbiForm(datosFormulario,initial={
        'ubicacion':huerto['ubicacion'],
    })
    if (request.method=="POST"):
        try:
            formulario=HuertoForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/huerto/actualizar/ubicacion'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("huerto_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'huerto/actualizar_ubicacion.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'huerto/actualizar_ubicacion.html',{"formulario":formulario,"huerto":huerto})



def huerto_patch_sit(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_huerto(huerto_id)
    formulario=HuertoActualizarSitForm(datosFormulario,initial={
        'sitio':huerto['sitio'],
    })
    if (request.method=="POST"):
        try:
            formulario=HuertoForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/huerto/actualizar/sitio'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("huerto_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'huerto/actualizar_sitio.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'huerto/actualizar_sitio.html',{"formulario":formulario,"huerto":huerto})


def huerto_patch_sus(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_huerto(huerto_id)
    formulario=HuertoActualizarSusForm(datosFormulario,initial={
        'sustrato':huerto['sustrato'],
    })
    if (request.method=="POST"):
        try:
            formulario=HuertoForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/huerto/actualizar/sustrato'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("huerto_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'huerto/actualizar_sustrato.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'huerto/actualizar_sustrato.html',{"formulario":formulario,"huerto":huerto})


def huerto_patch_abo(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_huerto(huerto_id)
    formulario=HuertoActualizarAboForm(datosFormulario,initial={
        'abonado':huerto['abonado'],
    })
    if (request.method=="POST"):
        try:
            formulario=HuertoForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/huerto/actualizar/abonado'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("huerto_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'huerto/actualizar_abonado.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'huerto/actualizar_abonado.html',{"formulario":formulario,"huerto":huerto})


def huerto_patch_are(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_huerto(huerto_id)
    formulario=HuertoActualizarAreaForm(datosFormulario,initial={
        'area':huerto['area'],
    })
    if (request.method=="POST"):
        try:
            formulario=HuertoForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/huerto/actualizar/area'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("huerto_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'huerto/actualizar_area.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'huerto/actualizar_area.html',{"formulario":formulario,"huerto":huerto})


def huerto_patch_aci(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_huerto(huerto_id)
    formulario=HuertoActualizarAciForm(datosFormulario,initial={
        'acidez':huerto['acidez'],
    })
    if (request.method=="POST"):
        try:
            formulario=HuertoForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/huerto/actualizar/acidez'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("huerto_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'huerto/actualizar_acidez.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'huerto/actualizar_acidez.html',{"formulario":formulario,"huerto":huerto})

def gasto_patch_factura(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_gasto(huerto_id)
    formulario=GastoActualizarFacForm(datosFormulario,initial={
        'factura':huerto['factura'],
    })
    if (request.method=="POST"):
        try:
            formulario=GastoForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/Gasto/actualizar/factura'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("gasto_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'gasto/actualizar_factura.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'gasto/actualizar_factura.html',{"formulario":formulario,"huerto":huerto})

def gasto_patch_descripcion(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_gasto(huerto_id)
    formulario=GastoActualizarDesForm(datosFormulario,initial={
        'descripcion':huerto['descripcion'],
    })
    if (request.method=="POST"):
        try:
            formulario=GastoForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/Gasto/actualizar/descripcion'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("gasto_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'gasto/actualizar_descripcion.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'gasto/actualizar_descripcion.html',{"formulario":formulario,"huerto":huerto})

def gasto_patch_herramienta(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_gasto(huerto_id)
    formulario=GastoActualizarHerForm(datosFormulario,initial={
        'herramientas':huerto['herramientas'],
    })
    if (request.method=="POST"):
        try:
            formulario=GastoForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/Gasto/actualizar/herramientas'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("gasto_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'gasto/actualizar_herramientas.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'gasto/actualizar_herramientas.html',{"formulario":formulario,"huerto":huerto})

def gasto_patch_imprevisto(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_gasto(huerto_id)
    formulario=GastoActualizarImpForm(datosFormulario,initial={
        'imprevisto':huerto['imprevisto'],
    })
    if (request.method=="POST"):
        try:
            formulario=GastoForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/Gasto/actualizar/imprevisto'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("gasto_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'gasto/actualizar_imprevisto.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'gasto/actualizar_imprevisto.html',{"formulario":formulario,"huerto":huerto})

def gasto_patch_fecha(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_gasto(huerto_id)
    formulario=GastoActualizarFecForm(datosFormulario,initial={
        'fecha':huerto['fecha'],
    })
    if (request.method=="POST"):
        try:
            formulario=GastoForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/Gasto/actualizar/fecha'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("gasto_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'gasto/actualizar_fecha.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'gasto/actualizar_fecha.html',{"formulario":formulario,"huerto":huerto})

def blog_patch_etiqueta(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_blog(huerto_id)
    formulario=BlogActualizarEtiForm(datosFormulario,initial={
        'fecetiqueta':huerto['etiqueta'],
    })
    if (request.method=="POST"):
        try:
            formulario=BlogForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/Blog/actualizar/etiqueta'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("blog_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'blog/actualizar_etiqueta.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'blog/actualizar_etiqueta.html',{"formulario":formulario,"huerto":huerto})

def blog_patch_publicacion(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_blog(huerto_id)
    formulario=BlogActualizarPubForm(datosFormulario,initial={
        'fecetiqueta':huerto['etiqueta'],
    })
    if (request.method=="POST"):
        try:
            formulario=BlogForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/Blog/actualizar/publicacion'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("blog_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'blog/actualizar_publicacion.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'blog/actualizar_publicacion.html',{"formulario":formulario,"huerto":huerto})

def blog_patch_fecha(request,huerto_id):
    datosFormulario=None
    if request.method=="POST":
        datosFormulario=request.POST
    huerto=helper.obtener_blog(huerto_id)
    formulario=BlogActualizarFecForm(datosFormulario,initial={
        'fecetiqueta':huerto['etiqueta'],
    })
    if (request.method=="POST"):
        try:
            formulario=BlogForm(request.POST)
            headers=crear_cabecera()
            datos=request.POST.copy()
            response=requests.patch(
                versionServer+'/Blog/actualizar/Fecha'+str(huerto_id),headers=headers,data=json.dumps(datos)
            )
            if (response.status_code==requests.codes.ok):
                return redirect("blog_obtener")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un rror en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'blog/actualizar_fecha.html',{"formulario":formulario,"huerto":huerto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request,'blog/actualizar_fecha.html',{"formulario":formulario,"huerto":huerto})

def registrar(request):
    if(request.method=="POST"):
        try:
            formulario=RegistroForm(request.POST)
            if(formulario.is_valid()):
                headers={
                    "Content-Type":"application/json"
                }
                response =requests.post(versionServer+'/registrar/usuario', headers=headers,
                    data=json.dumps(formulario.cleaned_data)
                )

                if (response.status_code==requests.codes.ok):
                    usuario=response.json()
                    token_acceso=helper.obtener_token_session(formulario.cleaned_data.get("username"),formulario.cleaned_data.get("password1"))
                    request.session["usuario"]=usuario
                    request.session["token"]=token_acceso
                    redirect("index")
                else:
                    print(response.status_code)
                    response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la peticion: {http_err}')
            if(response.status_code==400):
                errores=response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,'registro/registro.html',{'formulario':formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error:{err}')
            return mi_error_500(request)
    else:
        formulario=RegistroForm()
    return render(request,'registro/registro.html',{'formulario':formulario})



def login(request):
    if(request.method=="POST"):
        formulario=LoginForm(request.POST)
        try:
            token_acceso=helper.obtener_token_session(formulario.data.get("usuario"),formulario.data.get("password"))
            request.session["token"]=token_acceso
            headers={"Authorization":"Bearer"+token_acceso}
            response=requests.get(versionServer+'/usuario/token/'+token_acceso,headers=headers)
            usuario=response.json()
            request.session["usuario"]=usuario
            
            return redirect("index")
        except Exception as excepcion:
            print(f'Hubo un error en la peticion {excepcion}')
            formulario.add_error('usuario',excepcion)
            formulario.add_error("password",excepcion)
            return render(request,'registro/login.html',{"form":formulario})
    else:
        formulario=LoginForm()
    return render(request,"registro/login.html",{"form":formulario})

def logout(request):
    del request.session['token']
    return redirect('index')

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)

#Tarea final

#Gabriela
def plantas_estacion(request, estacion):
    headers = crear_cabecera()
    params = {'estacion': estacion}
    response = requests.get(f'{versionServer}/plantas_estacion/{estacion}/', headers=headers, params=params)
    plantas = obtener_respuesta(response)
    return render(request, 'planta/lista_estacion.html', {'plantas_mostrar': plantas})

#Manuel

def huerto_disponible(request):
    headers=crear_cabecera()
    response=requests.get(f'{versionServer}/huerto_disponible', headers=headers)
    huerto=obtener_respuesta(response)
    return render(request, 'huerto/disponibilidad.html',{'huertos':huerto})