# 🏢 AHO Inmobiliaria Backend

Sistema completo de gestión inmobiliaria desarrollado en Django con interfaces administrativas profesionales, gestión de galerías de imágenes, formateo de moneda automático y editor de texto enriquecido.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación Local](#-instalación-local)
- [Configuración](#-configuración)
- [Uso del Sistema](#-uso-del-sistema)
- [Deploy en Hosting Compartido](#-deploy-en-hosting-compartido)
- [Deploy en VPS](#-deploy-en-vps)
- [Deploy en PaaS (Railway, Render, etc.)](#-deploy-en-paas)
- [Base de Datos](#-configuración-de-base-de-datos)
- [Mantenimiento](#-mantenimiento)
- [Troubleshooting](#-troubleshooting)
- [Contribución](#-contribución)

## 🚀 Características

### Funcionalidades Principales
- **Gestión completa de inmuebles** con todos los detalles necesarios
- **Galería de imágenes profesional** con ordenamiento y previsualizaciones
- **Formateo automático de moneda** para precios (COP)
- **Editor de texto enriquecido** (TinyMCE) para descripciones
- **Interfaz administrativa avanzada** con autocomplete y filtros
- **Gestión de categorías, ciudades, barrios y características**
- **Sistema de etiquetas** con colores personalizables
- **Relaciones many-to-many** para características de inmuebles

### Características Técnicas
- Django 5.2+ con Python 3.10+
- Base de datos MySQL optimizada
- Gestión de dependencias con Poetry
- Archivos estáticos y media organizados
- Configuración mediante variables de entorno
- Sistema de migraciones completo

## 🛠 Tecnologías

- **Backend**: Django 5.2+
- **Base de Datos**: MySQL 8.0+
- **Manejo de Imágenes**: Pillow
- **Editor de Texto**: TinyMCE
- **Gestión de Dependencias**: Poetry
- **Variables de Entorno**: python-dotenv
- **Conector DB**: PyMySQL

## 💻 Instalación Local

### Prerrequisitos
```bash
# Python 3.10 o superior
python --version

# Poetry (instalación)
curl -sSL https://install.python-poetry.org | python3 -

# MySQL Server 8.0+
# Descargar desde: https://dev.mysql.com/downloads/mysql/
```

### Instalación Paso a Paso

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd Backend
```

2. **Configurar Poetry y dependencias**
```bash
# Configurar Poetry para usar .venv local
poetry config virtualenvs.in-project true

# Instalar dependencias
poetry install
```

3. **Activar entorno virtual**
```bash
# Opción 1: Con Poetry
poetry shell

# Opción 2: Activación manual
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows
```

4. **Configurar variables de entorno**
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
nano .env
```

5. **Configurar base de datos**
```sql
-- Conectar a MySQL y crear base de datos
mysql -u root -p
CREATE DATABASE inmuebles CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'inmuebles_user'@'localhost' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON inmuebles.* TO 'inmuebles_user'@'localhost';
FLUSH PRIVILEGES;
```

6. **Ejecutar migraciones**
```bash
poetry run python manage.py migrate
```

7. **Crear superusuario**
```bash
poetry run python manage.py createsuperuser
```

8. **Ejecutar servidor de desarrollo**
```bash
poetry run python manage.py runserver
```

## ⚙️ Configuración

### Variables de Entorno (.env)

```bash
# Base de datos
DB_NAME=inmuebles
DB_USER=inmuebles_user
DB_PASSWORD=tu_password_seguro
DB_HOST=localhost
DB_PORT=3306

# Django
SECRET_KEY=tu-clave-secreta-muy-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Archivos
MEDIA_URL=/media/
MEDIA_ROOT=media
STATIC_URL=/static/
STATIC_ROOT=staticfiles
```

### Configuraciones Importantes

- **Archivos Media**: Se almacenan en `media/` para desarrollo
- **Archivos Estáticos**: Se recolectan en `staticfiles/` para producción
- **TinyMCE**: Configurado con dos modos (completo y simple)
- **Admin**: Optimizado con autocomplete y previsualizaciones

## 📖 Uso del Sistema

### Acceso al Admin
```
http://localhost:8000/admin/
```

### Funcionalidades Principales

1. **Gestión de Inmuebles**
   - Crear, editar y eliminar propiedades
   - Galería de imágenes con ordenamiento
   - Formateo automático de precios
   - Descripciones con editor de texto enriquecido

2. **Organización de Datos**
   - Ciudades y barrios
   - Categorías de inmuebles
   - Características personalizables
   - Etiquetas con colores

3. **Gestión de Imágenes**
   - Subida múltiple de imágenes
   - Ordenamiento por drag & drop
   - Previsualizaciones en admin
   - Gestión de imagen principal (orden 0)

## 🌐 Deploy en Hosting Compartido

### Proveedores Recomendados (Económicos)
- **Hostinger** ($2-5/mes)
- **Namecheap** ($3-8/mes)
- **SiteGround** ($4-10/mes)
- **A2 Hosting** ($3-7/mes)

### Requisitos del Hosting
- Python 3.10+
- Acceso SSH o cPanel con Python
- MySQL 8.0+ o compatible
- Al menos 1GB RAM
- 10GB almacenamiento SSD

### Pasos de Deployment

1. **Preparar archivos para producción**
```bash
# Generar requirements.txt desde Poetry
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Recolectar archivos estáticos
poetry run python manage.py collectstatic --noinput
```

2. **Configurar settings para producción**
```python
# En settings.py o crear production_settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# Base de datos del hosting
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cpanel_user_dbname',
        'USER': 'cpanel_user',
        'PASSWORD': 'password_del_hosting',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

3. **Subir archivos al hosting**
```bash
# Via FTP/SFTP o cPanel File Manager
# Subir todo excepto:
# - .venv/
# - __pycache__/
# - .git/
# - *.log
```

4. **Configurar en cPanel**
```bash
# Instalar dependencias (si tienes SSH)
pip install -r requirements.txt

# O crear app Python en cPanel
# Seleccionar Python 3.10+
# Apuntar a manage.py
```

5. **Configurar .htaccess (si es necesario)**
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /wsgi.py/$1 [QSA,L]
```

### Hosting Específico - Hostinger

```bash
# 1. Crear aplicación Python en hPanel
# 2. Seleccionar Python 3.10
# 3. Subir código a public_html/
# 4. Instalar dependencias
cd public_html
pip install -r requirements.txt

# 5. Configurar variables de entorno en hPanel
# 6. Ejecutar migraciones
python manage.py migrate

# 7. Crear superusuario
python manage.py createsuperuser
```

## 🖥 Deploy en VPS

### Proveedores Recomendados
- **DigitalOcean** ($5-10/mes)
- **Vultr** ($5-10/mes) 
- **Linode** ($5-10/mes)
- **Contabo** ($4-8/mes)
- **Hetzner** ($4-8/mes)

### Configuración VPS (Ubuntu 22.04)

1. **Configuración inicial del servidor**
```bash
# Conectar al VPS
ssh root@tu-ip-del-vps

# Actualizar sistema
apt update && apt upgrade -y

# Instalar dependencias básicas
apt install -y python3.10 python3.10-venv python3-pip mysql-server nginx supervisor git
```

2. **Configurar MySQL**
```bash
# Configuración segura de MySQL
mysql_secure_installation

# Crear base de datos
mysql -u root -p
```
```sql
CREATE DATABASE inmuebles CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'inmuebles'@'localhost' IDENTIFIED BY 'password_muy_seguro';
GRANT ALL PRIVILEGES ON inmuebles.* TO 'inmuebles'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

3. **Configurar aplicación**
```bash
# Crear usuario para la aplicación
adduser inmobiliaria
usermod -aG sudo inmobiliaria
su - inmobiliaria

# Clonar repositorio
git clone <url-repositorio> /home/inmobiliaria/app
cd /home/inmobiliaria/app

# Configurar Poetry
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/inmobiliaria/.local/bin:$PATH"
poetry config virtualenvs.in-project true
poetry install --only=main

# Configurar variables de entorno
cp .env.example .env
nano .env  # Configurar con datos de producción
```

4. **Configurar Gunicorn**
```bash
# Crear archivo de configuración
nano /home/inmobiliaria/app/gunicorn.conf.py
```
```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
```

5. **Configurar Supervisor**
```bash
# Como root
sudo nano /etc/supervisor/conf.d/inmobiliaria.conf
```
```ini
[program:inmobiliaria]
command=/home/inmobiliaria/app/.venv/bin/gunicorn core.wsgi:application -c /home/inmobiliaria/app/gunicorn.conf.py
directory=/home/inmobiliaria/app
user=inmobiliaria
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/inmobiliaria.log
environment=PATH="/home/inmobiliaria/app/.venv/bin"
```

6. **Configurar Nginx**
```bash
sudo nano /etc/nginx/sites-available/inmobiliaria
```
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    
    client_max_body_size 50M;
    
    location /static/ {
        alias /home/inmobiliaria/app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /home/inmobiliaria/app/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

7. **Activar y ejecutar servicios**
```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/inmobiliaria /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Ejecutar migraciones y recolectar estáticos
cd /home/inmobiliaria/app
poetry run python manage.py migrate
poetry run python manage.py collectstatic --noinput
poetry run python manage.py createsuperuser

# Iniciar supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start inmobiliaria
```

8. **Configurar SSL con Certbot (Opcional pero recomendado)**
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

## ☁️ Deploy en PaaS

### Railway (Recomendado - $5-10/mes)

1. **Configurar archivos para Railway**
```bash
# Crear railway.toml
nano railway.toml
```
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn core.wsgi:application"
restartPolicyType = "always"
restartPolicyMaxRetries = 10
```

2. **Crear Procfile**
```bash
echo "web: gunicorn core.wsgi:application" > Procfile
```

3. **Configurar variables de entorno en Railway**
```bash
# En el dashboard de Railway
SECRET_KEY=tu-clave-secreta-super-segura
DEBUG=False
ALLOWED_HOSTS=*.railway.app,tu-dominio.com
DATABASE_URL=postgresql://user:pass@host:port/db  # Railway provee esto
```

4. **Deploy**
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login y deploy
railway login
railway link
railway up
```

### Render (Alternativa - $7/mes)

1. **Configurar build script**
```bash
# En render.yaml
services:
  - type: web
    name: inmobiliaria
    env: python
    buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --noinput"
    startCommand: "python manage.py migrate && gunicorn core.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
```

### Heroku (Más caro - $7+/mes)

1. **Configurar archivos Heroku**
```bash
# Procfile
echo "web: gunicorn core.wsgi:application" > Procfile

# runtime.txt
echo "python-3.10.12" > runtime.txt

# requirements.txt (generar desde Poetry)
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

2. **Deploy**
```bash
# Instalar Heroku CLI y login
heroku login

# Crear app
heroku create tu-app-inmobiliaria

# Configurar base de datos
heroku addons:create heroku-postgresql:mini

# Configurar variables
heroku config:set SECRET_KEY=tu-clave-secreta
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Ejecutar migraciones
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## 🗄 Configuración de Base de Datos

### MySQL en Producción

#### Optimizaciones recomendadas
```sql
-- En /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
innodb_buffer_pool_size = 512M  # Para VPS de 1-2GB RAM
max_connections = 100
query_cache_type = 1
query_cache_size = 32M
tmp_table_size = 64M
max_heap_table_size = 64M
```

#### Backup automático
```bash
# Crear script de backup
nano /home/inmobiliaria/backup_db.sh
```
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u inmuebles -p'password' inmuebles > /home/inmobiliaria/backups/backup_$DATE.sql
find /home/inmobiliaria/backups/ -name "backup_*.sql" -mtime +7 -delete
```

```bash
# Agregar a crontab
crontab -e
# Backup diario a las 2 AM
0 2 * * * /home/inmobiliaria/backup_db.sh
```

### PostgreSQL (Para PaaS)

Si usas Railway, Render o Heroku, generalmente usan PostgreSQL:

```bash
# Instalar psycopg2
poetry add psycopg2-binary

# En settings.py para producción con PostgreSQL
import dj_database_url
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

## 🔧 Mantenimiento

### Comandos Útiles

```bash
# Backup de archivos media
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/

# Limpiar archivos estáticos antiguos
python manage.py collectstatic --clear --noinput

# Verificar estado de la aplicación
python manage.py check --deploy

# Ver logs en VPS
sudo tail -f /var/log/inmobiliaria.log
sudo journalctl -u nginx -f

# Reiniciar servicios en VPS
sudo supervisorctl restart inmobiliaria
sudo systemctl restart nginx
```

### Monitoreo

#### Configurar alertas básicas
```bash
# Crear script de monitoreo
nano /home/inmobiliaria/monitor.sh
```
```bash
#!/bin/bash
# Verificar que la aplicación responda
if ! curl -f http://localhost:8000/admin/ > /dev/null 2>&1; then
    echo "ALERTA: Aplicación no responde" | mail -s "Error Inmobiliaria" admin@tu-dominio.com
    sudo supervisorctl restart inmobiliaria
fi
```

### Actualizaciones

```bash
# Proceso de actualización en VPS
cd /home/inmobiliaria/app
git pull origin main
poetry install
poetry run python manage.py migrate
poetry run python manage.py collectstatic --noinput
sudo supervisorctl restart inmobiliaria
```

## 🚨 Troubleshooting

### Problemas Comunes

#### 1. Error de conexión a base de datos
```bash
# Verificar conexión MySQL
mysql -u inmuebles -p inmuebles
# Verificar configuración en .env
cat .env | grep DB_
```

#### 2. Archivos estáticos no cargan
```bash
# Verificar permisos
ls -la staticfiles/
# Recolectar estáticos
python manage.py collectstatic --noinput
# Verificar configuración Nginx
sudo nginx -t
```

#### 3. Error 500 en producción
```bash
# Ver logs específicos
tail -f /var/log/inmobiliaria.log
# Verificar configuración Django
python manage.py check --deploy
```

#### 4. Problemas con Poetry
```bash
# Limpiar cache
poetry cache clear pypi --all
# Reinstalar dependencias
rm poetry.lock
poetry install
```

#### 5. Imágenes no se suben
```bash
# Verificar permisos de media
sudo chown -R inmobiliaria:inmobiliaria /home/inmobiliaria/app/media/
chmod -R 755 /home/inmobiliaria/app/media/
```

### Logs Útiles

```bash
# Django logs
tail -f /var/log/inmobiliaria.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# MySQL logs
sudo tail -f /var/log/mysql/error.log

# Sistema
sudo journalctl -f
```

## 💰 Estimación de Costos

### Hosting Compartido (Pequeña empresa)
- **Hostinger Business**: $3.99/mes
- **Namecheap Stellar**: $4.88/mes
- **Total anual**: ~$50-60

### VPS (Empresa en crecimiento)
- **DigitalOcean Droplet**: $6/mes (1GB RAM)
- **Vultr Regular**: $6/mes (1GB RAM)
- **Total anual**: ~$72-80

### PaaS (Fácil de gestionar)
- **Railway**: $5/mes + uso
- **Render**: $7/mes
- **Total anual**: ~$60-100

### Recomendación por Tamaño de Empresa

1. **Startup/Pequeña (1-10 usuarios)**: Hostinger Business
2. **Mediana (10-50 usuarios)**: DigitalOcean VPS
3. **Grande (50+ usuarios)**: VPS con load balancer

## 🤝 Contribución

### Desarrollo Local
```bash
# Instalar dependencias de desarrollo
poetry install --with dev

# Formatear código
poetry run black .

# Crear nueva migración
poetry run python manage.py makemigrations

# Ejecutar tests (cuando se implementen)
poetry run python manage.py test
```

### Estructura del Proyecto
```
Backend/
├── core/                 # Configuración Django
├── inmobiliaria/         # App principal
│   ├── models.py        # Modelos de datos
│   ├── admin.py         # Configuración admin
│   ├── forms.py         # Formularios personalizados
│   └── static/          # Archivos estáticos
├── media/               # Archivos subidos
├── staticfiles/         # Archivos estáticos recolectados
├── .env.example         # Variables de entorno ejemplo
├── CLAUDE.md           # Documentación para IA
└── README.md           # Este archivo
```

## 📞 Soporte

Para soporte técnico o consultas:

1. **Documentación**: Revisar este README y CLAUDE.md
2. **Logs**: Verificar logs del sistema en `/var/log/`
3. **Issues**: Crear issue en el repositorio
4. **Email**: contacto@ahoinmobiliaria.com

---

**Desarrollado con ❤️ para AHO Inmobiliaria**

*Sistema de gestión inmobiliaria profesional, optimizado para empresas pequeñas y medianas con presupuestos accesibles.*