# 🐍 Guía de Uso - Entorno Virtual Tradicional

## 🎯 Migración completada: Poetry → venv + pip

El proyecto ha sido migrado exitosamente de Poetry a entorno virtual tradicional para mayor estabilidad y simplicidad.

## 🚀 Comandos principales

### **Activar entorno virtual**
```bash
source venv/bin/activate
```

### **Desactivar entorno virtual**
```bash
deactivate
```

### **Ejecutar Django**
```bash
# Con entorno activado
source venv/bin/activate
python manage.py runserver

# O en una línea
source venv/bin/activate && python manage.py runserver
```

### **Ejecutar migraciones**
```bash
source venv/bin/activate && python manage.py migrate
```

### **Crear superusuario**
```bash
source venv/bin/activate && python manage.py createsuperuser
```

### **Ejecutar comandos Django**
```bash
source venv/bin/activate && python manage.py <comando>
```

## 📦 Gestión de dependencias

### **Instalar nueva dependencia**
```bash
source venv/bin/activate
pip install nombre-paquete
pip freeze > requirements.txt  # Actualizar requirements
```

### **Reinstalar todas las dependencias**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### **Actualizar dependencias**
```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## 🔧 Desarrollo diario

### **Flujo de trabajo típico**
```bash
# 1. Activar entorno
source venv/bin/activate

# 2. Ejecutar servidor
python manage.py runserver

# 3. En otra terminal (para comandos adicionales)
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### **Scripts útiles**
```bash
# Crear archivo run.sh para facilitar inicio
echo '#!/bin/bash
source venv/bin/activate
python manage.py runserver' > run.sh
chmod +x run.sh

# Ejecutar con: ./run.sh
```

## ✅ Ventajas de venv + pip

1. **Simplicidad**: Comandos estándar de Python
2. **Estabilidad**: Sin problemas de metadata corrupta
3. **Compatibilidad**: Funciona en cualquier entorno
4. **Velocidad**: Activación instantánea
5. **Debugging**: Más fácil de diagnosticar problemas

## 📁 Estructura del proyecto

```
Backend/
├── venv/                    # Entorno virtual (no subir a git)
├── requirements.txt         # Dependencias del proyecto
├── manage.py               # Django management
├── core/                   # Configuración Django
├── inmobiliaria/          # App principal
├── media/                 # Archivos media
├── .gitignore            # Configurado para ignorar venv/
└── GUIA_VENV.md          # Esta guía
```

## 🚨 Importantes

1. **Siempre activar venv** antes de ejecutar comandos Django
2. **No subir venv/ a git** (ya está en .gitignore)
3. **Actualizar requirements.txt** cuando instales nuevas dependencias
4. **Usar Python 3.10+** como especificado originalmente

## 🌟 ¡Django funcionando en Español!

El admin ya está configurado para mostrar:
- ✅ "AHOInmobiliaria Administración"
- ✅ Interfaz completamente en español
- ✅ Formato de fecha dd/mm/yyyy
- ✅ Zona horaria de Colombia
- ✅ Formato de moneda colombiano

**¡El proyecto está listo para desarrollo!**