from django.db import models
from django.conf import settings
import os


class Assesor(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    foto = models.ImageField(
        upload_to='asesores/', 
        blank=True, 
        null=True, 
        help_text='Selecciona una imagen para el asesor'
    )
    activo = models.BooleanField(default=True, db_comment='Indica si el asesor está activo o no')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.nombre
    
    def telefono_formateado(self):
        """Devuelve el teléfono formateado de manera legible"""
        if self.telefono:
            # Limpiar el número de espacios y caracteres especiales
            telefono = ''.join(filter(str.isdigit, self.telefono))
            
            # Formatear según la longitud del número
            if len(telefono) == 10:  # Número colombiano: 3XX XXX XXXX
                return f"({telefono[:3]}) {telefono[3:6]}-{telefono[6:]}"
            elif len(telefono) == 7:  # Número local: XXX XXXX
                return f"{telefono[:3]}-{telefono[3:]}"
            else:
                return self.telefono
        return "Sin teléfono"
    
    def get_foto_url(self):
        """Devuelve la URL completa de la foto usando ImageField"""
        if self.foto:
            return self.foto.url
        return None
    
    def tiene_foto(self):
        """Verifica si el asesor tiene foto"""
        return bool(self.foto)
        return None
        return "Sin teléfono"

    class Meta:
        db_table = 'asesores'
        verbose_name = 'Asesor'
        verbose_name_plural = 'Asesores'


class Barrios(models.Model):
    nombre = models.CharField(max_length=255)
    ciudad = models.ForeignKey('City', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'barrios'


class Caracteristica(models.Model):
    TIPO_CHOICES = [
        ('texto', 'Texto'),
        ('numerico', 'Numérico')
    ]
    
    nombre = models.CharField(unique=True, max_length=255)
    tipo = models.CharField(max_length=8, blank=True, null=True)
    unidad = models.CharField(max_length=255, choices=TIPO_CHOICES, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'caracteristicas'
        verbose_name = 'Característica'
        verbose_name_plural = 'Características'
        

class City(models.Model):
    nombre = models.CharField(max_length=255)
    departamento = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'ciudades'
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'


class EstadosInmueble(models.Model):
    nombre = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'estados_inmueble'


class Etiquetas(models.Model):
    nombre = models.CharField(unique=True, max_length=255, db_comment='Nombre de la etiqueta')
    color = models.CharField(max_length=255, blank=True, null=True, db_comment='Color en formato hexadecimal')
    descripcion = models.TextField(blank=True, null=True, db_comment='Descripción de la etiqueta')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'etiquetas'        
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        

class Imagenes(models.Model):
    inmueble = models.ForeignKey('Inmuebles', models.DO_NOTHING, blank=True, null=True)
    url = models.CharField(max_length=255, help_text='URL de la imagen externa')
    url_local = models.CharField(max_length=255, blank=True, null=True, help_text='Ruta local de la imagen')
    orden = models.IntegerField(blank=True, null=True, default=0, help_text='Orden de visualización (menor número = primera)')
    descargada = models.IntegerField(blank=True, null=True, default=0, help_text='0=No descargada, 1=Descargada')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        inmueble_info = f"Inmueble #{self.inmueble.ref}" if self.inmueble else "Sin inmueble"
        orden_info = f"Orden {self.orden}" if self.orden is not None else "Sin orden"
        return f"{inmueble_info} - {orden_info}"
    
    def get_imagen_display_url(self):
        """Devuelve la URL principal para mostrar la imagen"""
        return self.url
    
    def esta_descargada(self):
        """Indica si la imagen está descargada localmente"""
        return bool(self.descargada)

    class Meta:
        managed = True
        db_table = 'imagenes'
        verbose_name = 'Imagen del Inmueble'
        verbose_name_plural = 'Imágenes del Inmueble'
        ordering = ['orden', 'created_at']


class InmuebleCaracteristicas(models.Model):
    inmueble = models.ForeignKey('Inmuebles', models.DO_NOTHING, blank=True, null=True)
    caracteristica = models.ForeignKey(Caracteristica, models.DO_NOTHING, blank=True, null=True)
    valor_texto = models.CharField(max_length=255, blank=True, null=True)
    valor_numerico = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    valor_booleano = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        caracteristica_nombre = self.caracteristica.nombre if self.caracteristica else "Sin característica"
        if self.valor_texto:
            return f"{caracteristica_nombre}: {self.valor_texto}"
        elif self.valor_numerico:
            return f"{caracteristica_nombre}: {self.valor_numerico}"
        elif self.valor_booleano is not None:
            valor = "Sí" if self.valor_booleano else "No"
            return f"{caracteristica_nombre}: {valor}"
        return f"{caracteristica_nombre}: Sin valor"

    class Meta:
        managed = True
        db_table = 'inmueble_caracteristicas'
        verbose_name = 'Característica del Inmueble'
        verbose_name_plural = 'Características del Inmueble'


class Inmuebles(models.Model):
    ref = models.IntegerField(unique=True)
    codigo_sincronizacion = models.CharField(max_length=255, blank=True, null=True)
    titulo = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    descripcion_corta = models.TextField(blank=True, null=True)
    ciudad = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    ciudad_nombre = models.CharField(max_length=255, blank=True, null=True)
    barrio = models.ForeignKey(Barrios, models.DO_NOTHING, blank=True, null=True)
    barrio_nombre = models.CharField(max_length=255, blank=True, null=True)
    tipo_inmueble = models.ForeignKey('TiposInmueble', models.DO_NOTHING, blank=True, null=True)
    tipo_inmueble_nombre = models.CharField(max_length=255, blank=True, null=True)
    uso_inmueble = models.ForeignKey('UsosInmueble', models.DO_NOTHING, blank=True, null=True)
    uso_inmueble_nombre = models.CharField(max_length=255, blank=True, null=True)
    estado_inmueble = models.ForeignKey(EstadosInmueble, models.DO_NOTHING, blank=True, null=True)
    estado_inmueble_nombre = models.CharField(max_length=255, blank=True, null=True)
    tipo_consignacion = models.ForeignKey('TipoConsignacion', models.DO_NOTHING, blank=True, null=True)
    tipo_consignacion_nombre = models.CharField(max_length=255, blank=True, null=True)
    asesor = models.ForeignKey(Assesor, models.DO_NOTHING, blank=True, null=True)
    asesor_nombre = models.CharField(max_length=255, blank=True, null=True)
    area_construida = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    area_privada = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    area_terreno = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    area = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    habitaciones = models.IntegerField(blank=True, null=True)
    banos = models.IntegerField(blank=True, null=True)
    garajes = models.IntegerField(blank=True, null=True)
    estrato = models.IntegerField(blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    precio_canon = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    precio_administracion = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    precio_total = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    latitud = models.CharField(max_length=255, blank=True, null=True)
    longitud = models.CharField(max_length=255, blank=True, null=True)
    activo = models.IntegerField(blank=True, null=True)
    destacado = models.IntegerField(blank=True, null=True)
    en_caliente = models.IntegerField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_sincronizacion = models.DateTimeField(blank=True, null=True)
    hash_datos = models.TextField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True, db_comment='URL amigable para el inmueble')

    def __str__(self):
        titulo = self.titulo or f"Inmueble #{self.ref}"
        ciudad = self.ciudad.nombre if self.ciudad else self.ciudad_nombre or "Sin ciudad"
        barrio = self.barrio.nombre if self.barrio else self.barrio_nombre or "Sin barrio"
        return f"{titulo} - {ciudad} - {barrio}"
    
    def get_imagen_principal(self):
        """Obtiene la imagen principal (orden 0) del inmueble"""
        try:
            # Buscar imagen con orden 0 o la primera imagen disponible
            imagen = self.imagenes_set.filter(orden=0).first()
            if not imagen:
                # Si no hay imagen con orden 0, tomar la primera disponible
                imagen = self.imagenes_set.order_by('orden', 'created_at').first()
            return imagen
        except:
            return None
    
    def tiene_imagenes(self):
        """Verifica si el inmueble tiene imágenes"""
        return self.imagenes_set.exists()
    
    class Meta:
        managed = False
        db_table = 'inmuebles'
        verbose_name = 'Inmueble'
        verbose_name_plural = 'Inmuebles'


class InmueblesEstados(models.Model):
    inmueble_ref = models.IntegerField(db_comment='Referencia del inmueble (campo ref de la tabla inmuebles)')
    codigo_sincronizacion = models.CharField(max_length=255, db_comment='Código de sincronización del inmueble')
    activo = models.IntegerField(blank=True, null=True, db_comment='Estado del campo activo que debe mantenerse entre sincronizaciones')
    destacado = models.IntegerField(blank=True, null=True, db_comment='Estado del campo destacado que debe mantenerse entre sincronizaciones')
    en_caliente = models.IntegerField(blank=True, null=True, db_comment='Estado del campo en_caliente que debe mantenerse entre sincronizaciones')
    fecha_modificacion = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inmuebles_estados'


class InmueblesEtiquetas(models.Model):
    inmueble = models.ForeignKey(Inmuebles, models.DO_NOTHING)
    etiqueta = models.ForeignKey(Etiquetas, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inmuebles_etiquetas'
        unique_together = (('inmueble', 'etiqueta'),)


class TipoConsignacion(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'tipo_consignacion'
        verbose_name = 'Tipo de Consignación'
        verbose_name_plural = 'Tipos de Consignación'


class TiposInmueble(models.Model):
    nombre = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'tipos_inmueble'
        verbose_name = 'Tipo de Inmueble'
        verbose_name_plural = 'Tipos de Inmuebles'


class UsosInmueble(models.Model):
    nombre = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'usos_inmueble'
        verbose_name = 'Uso de Inmueble'
        verbose_name_plural = 'Usos de Inmuebles'
