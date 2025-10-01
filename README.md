
# Bancowo - Django + Postgres

Este proyecto es una API construida con **Django REST Framework** y **PostgreSQL**.  
Se puede ejecutar de forma local (con entorno virtual) o mediante **Docker Compose**.


## 🚀 Requisitos previos

- [Python 3.14+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/) (solo si corres en local)
- [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/)


## ⚙️ Instalación local (sin Docker)

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/knameless27/bancowo.git
   cd bancowo

2. **Crear entorno virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   
   Crea un archivo `.env` en la raíz del proyecto en base al `.env.example`

5. **Ejecutar migraciones**

   ```bash
   python manage.py migrate
   ```

6. **Levantar servidor**

   ```bash
   python manage.py runserver
   ```

El proyecto estará disponible en: [http://localhost:8000](http://localhost:8000)

---

## 🐳 Instalación con Docker

1. **Clonar repositorio**

   ```bash
   git clone https://github.com/knameless27/bancowo.git
   cd bancowo
   ```

2. **Configurar `.env`**
   
    Crea un archivo `.env` en la raiz del proyecto en base al `.env.example`

3. **Levantar servicios**

   ```bash
   docker compose up --build
   ```

4. **Ejecutar migraciones dentro del contenedor**

   ```bash
   docker compose exec django python manage.py migrate
   ```

5. **Crear superusuario (opcional)**

   ```bash
   docker compose exec django python manage.py createsuperuser
   ```

El proyecto estará disponible en: [http://localhost:8000](http://localhost:8000)

---

## 📂 Estructura básica del proyecto

```
bancowo/
│── bancowo/             # Código principal de Django
│── requirements.txt     # Dependencias del proyecto
│── docker-compose.yml   # Configuración de servicios
│── Dockerfile           # Imagen del contenedor web
│── .env                 # Variables de entorno
│── manage.py            # Script de gestión de Django
```

---

## 🔧 Comandos útiles

* Parar contenedores:

  ```bash
  docker compose down
  ```
* Ver logs:

  ```bash
  docker compose logs -f
  ```
* Reconstruir:

  ```bash
  docker compose up --build
  ```

---

## ✅ Notas

* Si corres en **local**, asegúrate de tener PostgreSQL corriendo y con un usuario/contraseña válidos.
* Si corres con **Docker**, el servicio de base de datos está preconfigurado en `docker-compose.yml`.
