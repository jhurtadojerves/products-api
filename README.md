# 🛍️ Products API

Products API es una plataforma RESTful desarrollada con Django y Django REST Framework para gestionar productos, marcas y usuarios. Soporta autenticación JWT, tareas en segundo plano con Celery, y despliegue vía Docker. Ideal para pruebas técnicas o proyectos reales con necesidades escalables.

---

## Requisitos

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos en tu máquina:

- **Python 3.10 o superior**
- **Docker** y **Docker Compose**
- **Redis** (para Celery)
- **PostgreSQL** (si no usas Docker para la base de datos)

---

## Configuración del entorno local

### 1. Clonar el repositorio

Clona este repositorio en tu máquina local:

```bash
git clone git@github.com:jhurtadojerves/products-api.git
cd products-api
```

### 2. Crear un archivo `.env`

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:

```bash
# ¡NO compartas este archivo en producción!
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=products
DATABASE_USER=root
DATABASE_PASS=root
DATABASE_HOST=db
DATABASE_PORT=5432
CELERY_BROKER_URL=redis://redis:6379/0
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
FROM_EMAIL=no-reply@example.com
```

### 3. Levantar los servicios con Docker Compose

Usa Docker Compose para levantar los servicios necesarios (Redis, PostgreSQL y la aplicación):

```bash
docker-compose up --build
```

Esto levantará los siguientes servicios:

- Redis en el puerto 6379
- PostgreSQL en el puerto 5432
- Django en el puerto 8000

### 4. Aplicar migraciones

Ejecuta las migraciones para configurar la base de datos:

```bash
docker-compose exec app python manage.py migrate
```

### 5. Crear un superusuario

Crea un superusuario para administrar el sistema:

```bash
docker-compose exec app python manage.py createsuperuser
```

### 6. Acceder a la aplicación

La API estará disponible en: http://localhost:8080/api/docs

---

## Estructura del proyecto

El proyecto sigue la arquitectura MVC (Modelo-Vista-Controlador), que se implementa en Django de la siguiente manera:

- Modelos (Models): Representan la estructura de los datos y las reglas de negocio. Se encuentran en apps/<nombre_app>/models/.
- Vistas (Views): Gestionan la lógica de la aplicación y responden a las solicitudes HTTP. Se encuentran en apps/<nombre_app>/viewsets/.
- Controladores (Serializers): En Django, los serializers actúan como controladores al transformar los datos entre los modelos y las vistas. Se encuentran en apps/<nombre_app>/serializers/.

## ¿Por qué se eligió la arquitectura MVC?

La arquitectura MVC fue elegida por las siguientes razones:

1. Separación de responsabilidades:

- Facilita el mantenimiento del código al separar la lógica de negocio (Modelos), la lógica de presentación (Vistas) y la transformación de datos (Serializers).
- Permite que diferentes desarrolladores trabajen en distintas partes del sistema sin interferir entre sí.

2. Escalabilidad:

- La separación de responsabilidades permite escalar el proyecto fácilmente, añadiendo nuevas funcionalidades sin afectar otras partes del sistema.

3. Compatibilidad con Django

- Django está diseñado para seguir el patrón MVC (aunque lo llama MTV: Modelo-Template-Vista), lo que facilita su implementación.

4. Facilidad de pruebas

- La separación de responsabilidades facilita la escritura de pruebas unitarias y de integración para cada componente.

---

## Comandos útiles

1. Para ejecutar las pruebas con `coverage`

```
make coverage
```

2. Ejecutar el lintern

```
make lint
```

3. Levantar servidor de desarrollo

```
make runserver
```

---

## Tecnologías utilizadas

- Django: Framework principal para la API.
- Django REST Framework (DRF): Para la creación de APIs RESTful.
- PostgreSQL: Base de datos relacional.
- Redis: Broker para Celery.
- Celery: Para la ejecución de tareas en segundo plano.
- Docker: Para la contenedorización de la aplicación.
- GitHub Actions: Para CI/CD.

---

## Contribuciones

Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad (`git checkout -b feat/nueva-funcionalidad`).
3. Realiza tus cambios y haz un commit (`git commit -m "Añadir nueva funcionalidad"`).
4. Haz push a tu rama (`git push origin feat/nueva-funcionalidad`).
5. Abre un Pull Request.
