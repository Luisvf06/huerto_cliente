from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime
from .helper import helper


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
    sitio= forms.ChoiceField(choices=SITIO,widget=forms.CheckboxSelectMultiple())
    SUSTRATO=[
        ("ARE","arenoso"),
        ("ARC","arcilloso"),
        ("LIM","limoso"),
        ("FRA","franco"),
        ("TUR","turbado"),
    ]
    sustrato=forms.ChoiceField(choices=SUSTRATO,required=True,widget=forms.CheckboxSelectMultiple())

    area_minima=forms.FloatField(label="Área mínima",required=True)
    
    area_maxima=forms.FloatField(label="Área máxima",required=True)
    
    abonado=forms.BooleanField(required=True)

    ubicacion = forms.CharField(label="Ubicación",required=True,  widget=forms.TextInput(attrs={'placeholder': 'Ingrese la ubicación'}))#de momento no consigo hacer funcionar los widgets que encuentro para plainlocationfield

    
    def __init__(self, *args, **kwargs):
        super(HuertoForm,self).__init__(*args,**kwargs)
        
        usuariosDisponibles = helper.obtener_usuarios_select()
        self.fields["usuario"]=forms.ChoiceField(
            choices=usuariosDisponibles,
            widget=forms.Select,
            required=True
        )