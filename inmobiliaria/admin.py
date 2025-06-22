from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .forms import EtiquetasForm, InmueblesForm
from .models import (
    Assesor, 
    City, 
    Barrios, 
    Caracteristica, 
    EstadosInmueble,
    Etiquetas,
    TipoConsignacion,
    TiposInmueble,
    UsosInmueble,
    Inmuebles,
    InmuebleCaracteristicas,
    Imagenes
)

# Función reutilizable para mostrar precios
def formatear_moneda(campo, etiqueta):
    def _metodo(self, obj):
        valor = getattr(obj, campo)
        return f"${valor:,.2f}" if valor else "-"
    _metodo.short_description = etiqueta
    _metodo.__name__ = f'{campo}_formateado'
    return _metodo

class InmobiliariaAdminSite(AdminSite):
    site_header = _("Inmobiliaria Administration")
    site_title = _("Inmobiliaria Admin")
    index_title = _("Welcome to the Inmobiliaria Admin")
    
admin_site = InmobiliariaAdminSite(name='inmobiliaria_admin')

# Inline para InmuebleCaracteristicas
class InmuebleCaracteristicasInline(admin.TabularInline):
    model = InmuebleCaracteristicas
    extra = 1
    autocomplete_fields = ['caracteristica']
    
    # Solo campos básicos para evitar errores
    fields = ['caracteristica', 'valor_texto', 'valor_numerico', 'valor_booleano']
    
    # Evitar campos que puedan causar problemas
    exclude = ['created_at', 'updated_at']

# Inline para Galería de Imágenes
class ImagenesInline(admin.TabularInline):
    model = Imagenes
    extra = 1
    
    fields = ['imagen_preview', 'url', 'url_local', 'orden', 'estado_descarga']
    readonly_fields = ['imagen_preview', 'estado_descarga', 'created_at', 'updated_at']
    
    # Ordenar por campo orden
    ordering = ['orden']
    
    def imagen_preview(self, obj):
        """Mostrar preview de la imagen usando el campo url"""
        if obj.url:
            return format_html(
                '<a href="{}" target="_blank" title="Click para ver en tamaño completo">'
                '<img src="{}" width="100" height="80" '
                'style="border-radius: 8px; object-fit: cover; border: 2px solid #ddd; '
                'cursor: pointer; transition: transform 0.2s;" '
                'onmouseover="this.style.transform=\'scale(1.05)\'" '
                'onmouseout="this.style.transform=\'scale(1)\'" /></a>',
                obj.url, obj.url
            )
        return format_html(
            '<div style="width: 100px; height: 80px; background-color: #f0f0f0; '
            'border-radius: 8px; display: flex; align-items: center; justify-content: center; '
            'border: 2px dashed #ccc; color: #999; font-size: 12px;">Sin URL</div>'
        )
    
    imagen_preview.short_description = 'Vista Previa'
    
    def estado_descarga(self, obj):
        """Mostrar el estado de descarga de forma visual"""
        if obj.descargada:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✅ Descargada</span>'
            )
        return format_html(
            '<span style="color: #dc3545; font-weight: bold;">❌ Pendiente</span>'
        )
    
    estado_descarga.short_description = 'Estado'
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Personalizar campos del formulario"""
        if db_field.name == 'orden':
            kwargs['widget'] = admin.widgets.AdminIntegerFieldWidget(attrs={
                'style': 'width: 60px;',
                'min': '0',
                'max': '999'
            })
        elif db_field.name == 'descargada':
            from django import forms
            kwargs['widget'] = forms.Select(
                choices=[(0, 'No'), (1, 'Sí')],
                attrs={'style': 'width: 80px;'}
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    class Media:
        css = {
            'all': ('admin/css/widgets.css',)
        }
        js = ('admin/js/admin/RelatedObjectLookups.js',)

# Registrar solo en el admin principal
@admin.register(Assesor)
class AsesoresAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono_formateado', 'foto_preview', 'activo_display', 'created_at_display']
    search_fields = ('nombre', 'email', 'telefono')
    list_filter = ('created_at', 'activo')
    date_hierarchy = 'created_at'
    
    # Configuración de botones de acción
    save_on_top = True
    save_as = True
    
    # Campos de solo lectura - timestamps y vista previa de foto
    readonly_fields = ('created_at', 'updated_at', 'foto_display')
    
    # Organización de campos en el formulario
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'email', 'telefono')
        }),
        ('Foto', {
            'fields': ('foto', 'foto_display'),
            'description': 'Selecciona una imagen para subir. Se guardará automáticamente en la carpeta asesores/'
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Sección colapsable
            'description': 'Fechas de creación y última modificación (solo lectura)'
        }),
    )
    
    # Ordenamiento
    ordering = ['-created_at']
    
    # Paginación
    list_per_page = 25
    
    # Método para formatear el teléfono
    def telefono_formateado(self, obj):
        if obj.telefono:
            # Limpiar el número de espacios y caracteres especiales
            telefono = ''.join(filter(str.isdigit, obj.telefono))
            
            # Formatear según la longitud del número
            if len(telefono) == 10:  # Número colombiano: 3XX XXX XXXX
                return f"{telefono[:3]} {telefono[3:6]} {telefono[6:]}"
            elif len(telefono) == 7:  # Número local: XXX XXXX
                return f"{telefono[:3]} {telefono[3:]}"
            else:
                return obj.telefono  # Devolver original si no coincide con formato esperado
        return "-"
    
    telefono_formateado.short_description = 'Teléfono'
    telefono_formateado.admin_order_field = 'telefono'
    
    # Método para mostrar vista previa de la foto
    def foto_preview(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.foto.url
            )
        return "Sin foto"
    
    foto_preview.short_description = 'Foto'
    
    # Método para mostrar la foto completa en el detalle
    def foto_display(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" width="150" height="150" style="border-radius: 10px; object-fit: cover;" /><br/>'
                '<small>Archivo: {}</small>',
                obj.foto.url,
                obj.foto.name
            )
        return "Sin foto"
    
    foto_display.short_description = 'Vista Previa de Foto'
    
    # Método para mostrar el estado activo de forma más amigable
    def activo_display(self, obj):
        if obj.activo == 1:
            return "✅ Activo"
        else:
            return "❌ Inactivo"
    
    activo_display.short_description = 'Estado'
    activo_display.admin_order_field = 'activo'
    
    # Método para mostrar la fecha de creación formateada
    def created_at_display(self, obj):
        if obj.created_at:
            return obj.created_at.strftime('%d/%m/%Y %H:%M')
        return "-"
    
    created_at_display.short_description = 'Fecha de Creación'
    created_at_display.admin_order_field = 'created_at'
    
    # Método para mostrar la fecha de actualización formateada
    def updated_at_display(self, obj):
        if obj.updated_at:
            return obj.updated_at.strftime('%d/%m/%Y %H:%M')
        return "-"
    
    updated_at_display.short_description = 'Última Actualización'
    updated_at_display.admin_order_field = 'updated_at'
    
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'departamento']
    search_fields = ('nombre', 'departamento')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ['nombre']
    
    # Campos de solo lectura - timestamps y vista previa de foto
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información de la Ciudad', {
            'fields': ('nombre', 'departamento')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Sección colapsable
            'description': 'Fechas de creación y última modificación (solo lectura)'
        }),
    )
    
@admin.register(Barrios)
class BarriosAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad']
    search_fields = ('nombre', 'ciudad__nombre')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ['nombre']
    autocomplete_fields = ['ciudad']
    
    # Campos de solo lectura - timestamps
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información del Barrio', {
            'fields': ('nombre', 'ciudad')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Sección colapsable
            'description': 'Fechas de creación y última modificación (solo lectura)'
        }),
    )
    
@admin.register(Caracteristica)
class CaracteristicaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo','unidad','descripcion']
    search_fields = ('nombre', 'tipo', 'unidad')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_filter = ('nombre',)
    ordering = ['nombre']
    
    # Paginación
    list_per_page = 25
    
    # Campos de solo lectura - timestamps
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información de la Caracteristica', {
            'fields': ('nombre', 'tipo', 'unidad', 'descripcion')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Sección colapsable
            'description': 'Fechas de creación y última modificación (solo lectura)'
        }),
    )
    
@admin.register(EstadosInmueble)
class EstadoInmuebleAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ('nombre',)
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ['nombre']
    
    # Paginación
    list_per_page = 25
    
    # Campos de solo lectura - timestamps
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información del Estado del Inmueble', {
            'fields': ('nombre',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Sección colapsable
            'description': 'Fechas de creación y última modificación (solo lectura)'
        }),
    )
    
@admin.register(Etiquetas)
class EtiquetasAdmin(admin.ModelAdmin):    
    form = EtiquetasForm
    list_display = ['nombre', 'color', 'color_muestra', 'descripcion']
    list_filter = ('created_at', 'updated_at')
    search_fields = ('nombre', 'descripcion')
    date_hierarchy = 'created_at'
    
    ordering = ['nombre']
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at')
    
    def color_muestra(self, obj):
        return format_html(
            '<div style="width: 30px; height: 30px; background-color: {}; border: 1px solid #000; border-radius: 50%"></div>',
            obj.color
        )
    color_muestra.short_description = 'Vista color'
    
    fieldsets = (
        ('Información de la Etiqueta', {
            'fields': ('nombre', 'color', 'descripcion')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Sección colapsable
            'description': 'Fechas de creación y última modificación (solo lectura)'
        }),
    )

@admin.register(TipoConsignacion)
class TipoConsignacionAdmin(admin.ModelAdmin):
    list_display = ['nombre','resumen_texto']
    search_fields = ('nombre',)
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ['nombre']
    
    # funcion que corta la descripción si es muy larga
    def resumen_texto(self, obj):
        return (obj.descripcion[:47] + '...') if len(obj.descripcion) > 50 else obj.descripcion
    resumen_texto.short_description = "Descripción"
    
    # Paginación
    list_per_page = 25
    
    # Campos de solo lectura - timestamps
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información del Tipo de Consignación', {
            'fields': ('nombre','descripcion')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Sección colapsable
            'description': 'Fechas de creación y última modificación (solo lectura)'
        }),
    )
    
@admin.register(TiposInmueble)
class TiposInmuebleAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ['nombre']
    
    # Paginación
    list_per_page = 25
    
    # Campos de solo lectura - timestamps
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información del Tipo de Inmueble', {
            'fields': ('nombre',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Sección colapsable
            'description': 'Fechas de creación y última modificación (solo lectura)'
        }),
    )

@admin.register(UsosInmueble)
class UsosInmuebleAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ('nombre',)
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ['nombre']
    
    # Paginación
    list_per_page = 25
    
    # Campos de solo lectura - timestamps
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información del Uso del Inmueble', {
            'fields': ('nombre',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Sección colapsable
            'description': 'Fechas de creación y última modificación (solo lectura)'
        }),
    ) 
    
@admin.register(Inmuebles)
class InmueblesAdmin(admin.ModelAdmin):
    form = InmueblesForm
    list_display = ('cod_syn', 'imagen_principal', 'ref','slug', 'nombre_ciudad','tipoinmueble','precio_canon_formateado', 'precio_venta_formateado', 'mostrar_activo', 'mostrar_destacado')
    search_fields = ('titulo', 'codigo_sincronizacion', 'direccion', 'slug')
    list_filter = ('ciudad', 'barrio', 'estado_inmueble', 'tipo_consignacion', 'activo', 'destacado')

    autocomplete_fields = (
        'ciudad', 'barrio', 'tipo_inmueble', 'uso_inmueble',
        'estado_inmueble', 'tipo_consignacion', 'asesor',
    )
    
    inlines = [InmuebleCaracteristicasInline, ImagenesInline]
    
    # Configuración de botones de acción
    save_on_top = True
    save_as = True
    save_as_continue = True
    
    list_per_page = 25
    
    
    ordering = ('-ref',)
    
    def cod_syn(self, obj):
        return obj.codigo_sincronizacion if obj.codigo_sincronizacion else "-"
    cod_syn.short_description = "cod_sync"
    
    def nombre_ciudad(self, obj):
        return obj.ciudad.nombre if obj.ciudad else "-"
    nombre_ciudad.short_description = "Ciudad"
    
    def tipoinmueble(self, obj):
        return obj.tipo_inmueble.nombre if obj.tipo_inmueble else "-"
    tipoinmueble.short_description = "Tipo Inmueble"
    
    precio_venta_formateado = formatear_moneda('precio_venta', 'Precio Venta')
    precio_canon_formateado = formatear_moneda('precio_canon', 'Canon')
    
    readonly_fields = (
        'ref', 'codigo_sincronizacion', 'slug','hash_datos',
        'fecha_creacion', 'fecha_actualizacion', 'fecha_sincronizacion',)
    
    # def precio_venta_decimales(self, obj):
    #     return f"${obj.precio_venta:,.2f}" if obj.precio_venta else "-"
    # precio_venta_decimales.short_description = "Precio de Venta"
    
    def mostrar_activo(self, obj):
        return "✅ Sí" if obj.activo else "❌ No"
    mostrar_activo.short_description = "Activo"
    
    def mostrar_destacado(self, obj):
        return format_html('⭐') if obj.destacado else ''
    mostrar_destacado.short_description = "Destacado"
    
    def imagen_principal(self, obj):
        """Muestra la imagen principal del inmueble (orden 0)"""
        imagen = obj.get_imagen_principal()
        
        if imagen and imagen.url:
            return format_html(
                '<a href="{}" target="_blank" title="Ver imagen completa">'
                '<img src="{}" width="80" height="60" '
                'style="border-radius: 6px; object-fit: cover; border: 2px solid #ddd; '
                'cursor: pointer; transition: transform 0.2s;" '
                'onmouseover="this.style.transform=\'scale(1.1)\'" '
                'onmouseout="this.style.transform=\'scale(1)\'" /></a>',
                imagen.url, imagen.url
            )
        return format_html(
            '<div style="width: 80px; height: 60px; background-color: #f0f0f0; '
            'border-radius: 6px; display: flex; align-items: center; justify-content: center; '
            'border: 2px dashed #ccc; color: #999; font-size: 11px;">Sin imagen</div>'
        )
    
    imagen_principal.short_description = "Imagen"
    imagen_principal.allow_tags = True
    
    fieldsets = (
        ('Identificación', {
            'fields': ('ref', 'codigo_sincronizacion', 'slug')
        }),
        ('Información general', {
            'fields': (
                'titulo', 'descripcion_corta', 'descripcion',
                'ciudad', 'barrio',
                'tipo_inmueble', 
                'uso_inmueble', 
                'estado_inmueble', 
                'tipo_consignacion',
                'asesor'
            )
        }),
        ('Áreas', {
            'fields': (
                'area', 'area_construida', 'area_privada', 'area_terreno'
            )
        }),
        ('Características', {
            'fields': ('habitaciones', 'banos', 'garajes', 'estrato')
        }),
        ('Precios', {
            'fields': (
                'precio_venta', 'precio_canon', 'precio_administracion', 'precio_total'
            )
        }),
        ('Ubicación', {
            'fields': ('direccion', 'latitud', 'longitud')
        }),
        ('Estado', {
            'fields': ('activo', 'destacado', 'en_caliente')
        }),
        ('Tiempos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion', 'fecha_sincronizacion')
        }),
        ('Otros', {
            'fields': ('hash_datos',)
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/currency-widget.css',)
        }
        js = ('admin/js/currency-formatter.js',)

@admin.register(Imagenes)
class ImagenesAdmin(admin.ModelAdmin):
    list_display = ['imagen_miniatura', 'inmueble_info', 'orden', 'estado_descarga', 'created_at_formatted']
    list_filter = ['descargada', 'orden', 'created_at', 'inmueble__ciudad']
    search_fields = ['inmueble__titulo', 'inmueble__ref', 'url', 'url_local']
    autocomplete_fields = ['inmueble']
    
    # Configuración de botones de acción
    save_on_top = True
    save_as = True
    
    ordering = ['inmueble', 'orden', 'created_at']
    list_per_page = 50
    
    readonly_fields = ['imagen_completa', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Información del Inmueble', {
            'fields': ('inmueble',)
        }),
        ('Imagen', {
            'fields': ('imagen_completa', 'url', 'url_local')
        }),
        ('Configuración', {
            'fields': ('orden', 'descargada')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def imagen_miniatura(self, obj):
        """Imagen en miniatura para la lista usando campo url"""
        if obj.url:
            return format_html(
                '<img src="{}" width="60" height="45" '
                'style="border-radius: 6px; object-fit: cover; border: 1px solid #ddd;" />',
                obj.url
            )
        return "🚫"
    
    imagen_miniatura.short_description = 'Imagen'
    
    def imagen_completa(self, obj):
        """Imagen completa para el formulario de detalle usando campo url"""
        if obj.url:
            return format_html(
                '<div style="text-align: center;">'
                '<a href="{}" target="_blank">'
                '<img src="{}" style="max-width: 400px; max-height: 300px; '
                'border-radius: 8px; border: 2px solid #ddd; cursor: pointer;" /></a>'
                '<br><small style="color: #666;">Click para ver en tamaño completo</small>'
                '</div>',
                obj.url, obj.url
            )
        return "Sin URL de imagen disponible"
    
    imagen_completa.short_description = 'Vista Previa'
    
    def inmueble_info(self, obj):
        """Información del inmueble asociado"""
        if obj.inmueble:
            return format_html(
                '<strong>#{}</strong><br><small>{}</small>',
                obj.inmueble.ref,
                obj.inmueble.titulo[:30] + '...' if obj.inmueble.titulo and len(obj.inmueble.titulo) > 30 else obj.inmueble.titulo or 'Sin título'
            )
        return "Sin inmueble"
    
    inmueble_info.short_description = 'Inmueble'
    
    def estado_descarga(self, obj):
        """Estado de descarga visual"""
        if obj.descargada:
            return format_html('<span style="color: #28a745;">✅ Descargada</span>')
        return format_html('<span style="color: #dc3545;">❌ Pendiente</span>')
    
    estado_descarga.short_description = 'Estado'
    
    def created_at_formatted(self, obj):
        """Fecha de creación formateada"""
        if obj.created_at:
            return obj.created_at.strftime('%d/%m/%Y %H:%M')
        return "-"
    
    created_at_formatted.short_description = 'Fecha'
    created_at_formatted.admin_order_field = 'created_at'

# Configuración personalizada para User y Group - Solo superusuarios
class RestrictedUserAdmin(UserAdmin):
    """Admin de usuarios restringido solo a superusuarios"""
    
    def has_module_permission(self, request):
        """Solo superusuarios pueden ver el módulo de usuarios"""
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        """Solo superusuarios pueden ver usuarios"""
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        """Solo superusuarios pueden crear usuarios"""
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Solo superusuarios pueden editar usuarios"""
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """Solo superusuarios pueden eliminar usuarios"""
        return request.user.is_superuser

class RestrictedGroupAdmin(GroupAdmin):
    """Admin de grupos restringido solo a superusuarios"""
    
    def has_module_permission(self, request):
        """Solo superusuarios pueden ver el módulo de grupos"""
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        """Solo superusuarios pueden ver grupos"""
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        """Solo superusuarios pueden crear grupos"""
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Solo superusuarios pueden editar grupos"""
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """Solo superusuarios pueden eliminar grupos"""
        return request.user.is_superuser

# Re-registrar User y Group con las clases restringidas
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, RestrictedUserAdmin)
admin.site.register(Group, RestrictedGroupAdmin)

