from django import forms
from django.conf import settings
from tinymce.widgets import TinyMCE
from .models import Etiquetas, Inmuebles

class CurrencyWidget(forms.TextInput):
    """Widget personalizado para campos de moneda con formato automático"""
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'currency-input',
            'style': 'text-align: right; font-family: monospace;',
            'placeholder': '$0',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
    
    class Media:
        js = ('admin/js/currency-formatter.js',)
        css = {
            'all': ('admin/css/currency-widget.css',)
        }

class EtiquetasForm(forms.ModelForm):
    class Meta:
        model = Etiquetas
        fields = '__all__'
        widgets = {
            'color': forms.TextInput(attrs={
                'type': 'color',
            }),
        }

class InmueblesForm(forms.ModelForm):
    """Formulario personalizado para inmuebles con widgets de moneda y rich text"""
    
    class Meta:
        model = Inmuebles
        fields = '__all__'
        widgets = {
            # Campos de moneda
            'precio_venta': CurrencyWidget(attrs={
                'placeholder': '$0 - Precio de venta'
            }),
            'precio_canon': CurrencyWidget(attrs={
                'placeholder': '$0 - Precio del canon'
            }),
            'precio_administracion': CurrencyWidget(attrs={
                'placeholder': '$0 - Precio administración'
            }),
            'precio_total': CurrencyWidget(attrs={
                'placeholder': '$0 - Precio total'
            }),
            # Campos de rich text
            'descripcion': TinyMCE(attrs={
                'cols': 80, 
                'rows': 10,
                'placeholder': 'Descripción completa del inmueble...'
            }, mce_attrs=settings.TINYMCE_DEFAULT_CONFIG),
            'descripcion_corta': TinyMCE(attrs={
                'cols': 80, 
                'rows': 5,
                'placeholder': 'Descripción breve del inmueble...'
            }, mce_attrs=settings.TINYMCE_SIMPLE_CONFIG),
        }