from django import forms
from .models import *
from datetime import date
import datetime
from .helper import helper
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BusquedaHuerto(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaHuerto(forms.Form):
    textoBusqueda=forms.CharField(required=False)
    SITIO=[
        ("M","maceta"),
        ("J","jardin"),
        ("T","terraza"),
        ("P","parcela"),
    ]
    sitio= forms.MultipleChoiceField(choices=SITIO, required=False,widget=forms.CheckboxSelectMultiple())
    SUSTRATO=[
        ("ARE","arenoso"),
        ("ARC","arcilloso"),
        ("LIM","limoso"),
        ("FRA","franco"),
        ("TUR","turbado"),
    ]
    sustrato=forms.MultipleChoiceField(choices=SUSTRATO,required=False,widget=forms.CheckboxSelectMultiple())

    area_minima=forms.FloatField(label="Área mínima",required=False)
    #tenia esto en los widgets de las areas pero me daba error ,widgets=[forms.NumberInput(attrs={'type': 'number', 'step': '0.01'}),forms.NumberInput(attrs={'type': 'number', 'step': '0.1'})]
    area_maxima=forms.FloatField(label="Área máxima",required=False)
    
    abonado=forms.BooleanField(required=False)

    ubicacion = forms.CharField(label="Ubicación",required=False,  widget=forms.TextInput(attrs={'placeholder': 'Ingrese la ubicación'}))#de momento no consigo hacer funcionar los widgets que encuentro para plainlocationfield

class BusquedaAvanzadaGastos(forms.Form):
    gasto_busqueda=forms.FloatField(label="Importe",required=False)
    texto_busqueda=forms.CharField(label="Texto",required=False)

class BusquedaAvanzadaBlog(forms.Form):
    PUBLICACION=[('C','comentario'),('N','noticia'),('E','enlace'),('T','tutorial'),('R','reseña')]
    publicacion=forms.MultipleChoiceField(choices=PUBLICACION,required=False,widget=forms.CheckboxSelectMultiple)
    etiqueta=forms.CharField(label='Etiqueta',required=False)
    
    fecha_desde = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2026))
                                )
    
    fecha_hasta = forms.DateField(label="Fecha Hasta",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2026))
                                )



class HuertoForm(forms.Form):#formulario de crear
    SITIO=[
        ("M","maceta"),
        ("J","jardin"),
        ("T","terraza"),
        ("P","parcela"),
    ]
    sitio= forms.ChoiceField(choices=SITIO,widget=forms.Select())
    SUSTRATO=[
        ("ARE","arenoso"),
        ("ARC","arcilloso"),
        ("LIM","limoso"),
        ("FRA","franco"),
        ("TUR","turbado"),
    ]
    sustrato=forms.ChoiceField(choices=SUSTRATO,required=True,widget=forms.Select())

    area=forms.FloatField(label="Área",required=True)
    
    acidez=forms.FloatField(label='Acidez',required=True)
    
    abonado=forms.BooleanField(required=False)
    disponible=forms.BooleanField(required=False)#tarea de manuel
    
    ubicacion = forms.CharField(label="Ubicación",required=True,  widget=forms.TextInput(attrs={'placeholder': 'Ingrese la ubicación'}))#de momento no consigo hacer funcionar los widgets que encuentro para plainlocationfield

    
    def __init__(self, *args, **kwargs):
        super(HuertoForm,self).__init__(*args,**kwargs)
        
        usuariosDisponibles = helper.obtener_usuarios_select()
        self.fields["usuario"]=forms.ChoiceField(
            choices=usuariosDisponibles,
            widget=forms.Select,
            required=True
        )
        
class GastoForm(forms.Form): #formulario crear
    herramientas=forms.FloatField(label='Herramientas',required=True)
    
    facturas=forms.FloatField(label='Facturas',required=True)
    
    imprevistos=forms.FloatField(label='Imprevistos',required=True)
    Descripcion=forms.CharField(label='Descripción',required=True)
    fecha=forms.DateField(label='Fecha',required=False,initial=datetime.date.today,widget=forms.SelectDateWidget(years=range(1990,2024)))

    def __init__(self,*args,**kwargs):
        super(GastoForm,self).__init__(*args,**kwargs)
        usuario=helper.obtener_usuarios_select()
        self.fields["usuario"] = forms.ChoiceField(
            choices=usuario, 
            widget=forms.Select, 
            required=True)

    
class BlogForm(forms.Form):
    PUBLICACION=[
        ("C","comentario"),
        ("N","noticia"),
        ("E","enlace"),
        ("T","tutorial"),
        ("R","reseña"),
        ]
    publicacion=forms.ChoiceField(choices=PUBLICACION,required=True,widget=forms.Select())
    fecha=forms.DateField(label='Fecha',initial=datetime.date.today,widget=forms.SelectDateWidget, required=False)
    etiqueta=forms.CharField(label='Etiqueta',required=False)
    
    def __init__(self, *args, **kwargs):
        super(BlogForm,self).__init__(*args,**kwargs)
        
        usuariosDisponibles = helper.obtener_usuarios_select()
        self.fields["usuario"]=forms.ChoiceField(
            choices=usuariosDisponibles,
            widget=forms.Select,
            required=True
        )

class HuertoActualizarUbiForm(forms.Form):
    ubicacion=forms.CharField(label="ubic",required=True)
class HuertoActualizarAciForm(forms.Form):
    acidez=forms.FloatField(label="acidez",required=True)
class HuertoActualizarSitForm(forms.Form):
    sitio=forms.ChoiceField(widget=forms.Select(),required=True)
class HuertoActualizarSusForm(forms.Form):
    sustrato=forms.ChoiceField(widget=forms.Select(),required=True)
class HuertoActualizarAboForm(forms.Form):
    abonado=forms.BooleanField(required=False)
'''
class HuertoActualizarAreaForm(forms.Form):
    area=forms.FloatField(forms.Form)'''



class GastoActualizarHerForm(forms.Form):
    h=forms.FloatField(label="herr",required=True)

class GastoActualizarFacForm(forms.Form):
    f=forms.FloatField(label="Fac",required=True)

class GastoActualizarImpForm(forms.Form):
    i=forms.FloatField(label="impr",required=True)
class GastoActualizarDesForm(forms.Form):
    d=forms.CharField(label="desc",required=True)
class GastoActualizarFecForm(forms.Form):
    fe=forms.FloatField(label="fecha",required=True,widget=forms.SelectDateWidget())



class BlogActualizarPubForm(forms.Form):
    p=forms.ChoiceField(widget=forms.Select(),required=True)

class BlogActualizarEtiForm(forms.Form):
    e=forms.ChoiceField(label="etiqueta",required=True)
class BlogActualizarFecForm(forms.Form):
    f=forms.ChoiceField(label="fecha",required=True,widget=forms.SelectDateWidget())

class RegistroForm(UserCreationForm):
    roles =(
            (1, 'usu'),
            (2,'usu_premium'),
    )
    rol = forms.ChoiceField(choices=roles)
    class Meta:
        model=User
        fields= ('username','email','password1','password2','rol')
    
class LoginForm(forms.Form):
    usuario=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())