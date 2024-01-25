from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime


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

