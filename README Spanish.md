<img align="center" src="https://media.licdn.com/dms/image/v2/D4D16AQGUNxQ7NSC05A/profile-displaybackgroundimage-shrink_350_1400/profile-displaybackgroundimage-shrink_350_1400/0/1738695150340?e=1744243200&v=beta&t=oXX-ixT9bR3dJcYCLv4KBs5wjKFoeP0524kFGHQMYmQ" alt="gabriellugo" />

# BOT DE TELEGRAM

<a href="https://github.com/GabrielLugooo/Telegram-Bot-Public/blob/main/README%20Spanish.md" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.shields.io/badge/Bot%20de%20Telegram%20Español-000000" alt="Bot de Telegram Español" /></a>
<a href="https://github.com/GabrielLugooo/Telegram-Bot-Public" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.shields.io/badge/Bot%20de%20Telegram%20Inglés-green" alt="Bot de Telegram Inglés" /></a>

### Objetivos

Bot de Telegram esta diseñado para proporcionar información actualizada sobre películas populares, mejor calificadas, en cartelera y próximas a estrenarse. Su objetivo principal es facilitar a los usuarios el acceso a detalles como sinopsis, calificaciones y tráilers de películas de The Movie Database (TMDb), todo dentro de la plataforma de Telegram.

Además, el bot permite la navegación interactiva mediante botones, lo que mejora la experiencia del usuario al explorar contenido cinematográfico de manera rápida y sencilla.

### Habilidades Aprendidas

- Uso de la API de Telegram para la creación de bots.
- Consumo de API REST (TMDb) para obtener información sobre películas.
- Manejo de cifrado con la librería `cryptography`.
- Uso de `dotenv` para manejar variables de entorno de forma segura.
- Creación de interfaces interactivas con `InlineKeyboardMarkup`.
- Manejo de solicitudes HTTP con `requests`.
- Programación asíncrona con `asyncio` para evitar bloqueos en la ejecución del bot.
- Gestión y almacenamiento de usuarios en archivos JSON.
- Implementación de paginación interactiva en Telegram.
- Manejo de errores en solicitudes a APIs externas.

### Herramientas Usadas

![Static Badge](https://img.shields.io/badge/Python-000000?logo=python&logoSize=auto)
![Static Badge](https://img.shields.io/badge/Requests-000000?logo=requests&logoSize=auto)
![Static Badge](https://img.shields.io/badge/Asyncio-000000?logo=asyncio&logoSize=auto)
![Static Badge](https://img.shields.io/badge/Cryptography%20Fernet-000000?logo=cryptography&logoSize=auto)
![Static Badge](https://img.shields.io/badge/venv-000000?logo=venv&logoSize=auto)
![Static Badge](https://img.shields.io/badge/.ENV-000000?logo=dotenv&logoSize=auto)
![Static Badge](https://img.shields.io/badge/JSON-000000?logo=json&logoSize=auto)
![Static Badge](https://img.shields.io/badge/Telegram-000000?logo=telegram&logoSize=auto)
![Static Badge](https://img.shields.io/badge/TMDB-000000?logo=themoviedatabase&logoSize=auto)

- Python: Lenguaje principal para el desarrollo del bot.
- `python-telegram-bot`: Biblioteca utilizada para interactuar con la API de Telegram.
- `requests`: Para realizar solicitudes HTTP a la API de TMDB.
- TMDB API: Fuente de datos para obtener información de películas.
- `cryptography (Fernet)`: Para cifrar datos sensibles y mejorar la seguridad.
- `JSON`: Para el almacenamiento y manejo de datos estructurados.
- `dotenv`: Para cargar variables de entorno y manejar credenciales de manera segura.
- `asyncio`: Para manejar tareas asincrónicas dentro del bot.
- Telegram Bot API: Para la comunicación entre el bot y los usuarios.

### Proyecto

#### Vista Previa

<img align="center" src="https://i.imgur.com/7GXWLHd.jpeg" alt="Bot01" height=300 />
<img align="center" src="https://i.imgur.com/xlMrMYO.jpeg" alt="Bot02" height=300 />
<img align="center" src="https://i.imgur.com/OGITxpr.jpeg" alt="Bot03" height=300 />
<img align="center" src="https://i.imgur.com/KGTVCIG.jpeg" alt="Bot04" height=300 />
<img align="center" src="https://i.imgur.com/sA9bLpD.jpeg" alt="Bot05" height=300 />
<img align="center" src="https://i.imgur.com/oNQH8Vk.jpeg" alt="Bot06" height=300 />
<img align="center" src="https://i.imgur.com/XhD1Qjc.jpeg" alt="Bot07" />

#### Código con Comentarios (Español)

```python
# Movies Nerds Bot
# Importar las librerias necesarias

import sys
import os
import io
import requests
import json
import asyncio
import time
from dotenv import load_dotenv
from cryptography.fernet import Fernet

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Genera una clave para cifrado (esto solo debe hacerse una vez)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Cifrar y guardar datos
with open('users.json', 'rb') as file:
    data = file.read()
encrypted_data = cipher_suite.encrypt(data)

with open('encrypted_users.json', 'wb') as file:
    file.write(encrypted_data)

# Lista de chat_ids permitidos, los Id son almacenados en el users.json
allowed_users = [-100123456789]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    if chat_id not in allowed_users:
        await update.message.reply_text("No tienes permisos para interactuar con este bot.")
        return

# Configurar la salida estándar a UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cargar las variables del archivo .env
load_dotenv()

# API Key de TMDB & Token de Telegram
api_key = os.getenv("TMDB_API_KEY") # API Key de TMDB
tmdb_base_url = 'https://api.themoviedb.org/3/movie/' # URL de la base API de películas de TMDB
image_base_url = "https://image.tmdb.org/t/p/w500" # URL de  la base de imagenes de TMDB
telegram_token = os.getenv("TELEGRAM_TOKEN") # Token de Telegram
users_file = "users.json" # Archivo JSON donde se guardan los ID de los usuarios del grupo de Telegram

# Cargar usuarios desde archivo
def load_users():
    try:
        with open(users_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Guardar usuarios en archivo
def save_users(users):
    with open(users_file, "w") as file:
        json.dump(users, file)

# Guardar usuario si es nuevo
def save_user(chat_id):
    users = load_users()
    if chat_id not in users:
        users.append(chat_id)
        save_users(users)

# Obtener categorías de películas
def get_movie_categories():
    return {
        "🎬 Populares": 'popular',
        "⭐ Mejor calificadas": 'top_rated',
        "🎥 Ahora en cartelera": 'now_playing',
        "🔜 Próximamente": 'upcoming'
    }

# Obtener películas por categoría con manejo de errores
def get_movies_by_category(category, page=1):
    try:
        tmdb_url = f'{tmdb_base_url}{category}?page={page}&api_key={api_key}&language=es&region=AR'
        response = requests.get(tmdb_url)
        response.raise_for_status()  # Verificar si hubo algún error en la solicitud
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener películas de TMDB: {e}")
        return {"results": []}  # Retornar un resultado vacío en caso de error

# Obtener tráiler de película con manejo de errores
def get_movie_trailer(movie_id):
    try:
        tmdb_url = f'{tmdb_base_url}{movie_id}/videos?api_key={api_key}&language=es'
        response = requests.get(tmdb_url)
        response.raise_for_status()  # Verificar si hubo algún error en la solicitud
        json_data = response.json()
        return f'https://www.youtube.com/watch?v={json_data["results"][0]["key"]}' if json_data.get("results") else "No disponible"
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener tráiler de la película {movie_id}: {e}")
        return "No disponible"

# Crear teclado interactivo para el menú principal
def create_category_keyboard():
    keyboard = [[InlineKeyboardButton(cat, callback_data=key)] for cat, key in get_movie_categories().items()]
    return InlineKeyboardMarkup(keyboard)

# Crear teclado interactivo para la paginación y regresar al menú
def create_pagination_keyboard(page, total_pages):
    keyboard = []
    if page > 1:
        keyboard.append([InlineKeyboardButton("⬅️ Página Anterior", callback_data=f"page_{page-1}")])
    if page < total_pages:
        keyboard.append([InlineKeyboardButton("➡️ Página Siguiente", callback_data=f"page_{page+1}")])
    keyboard.append([InlineKeyboardButton(f"Página {page}/{total_pages}", callback_data="none")])
    keyboard.append([InlineKeyboardButton("🏠 Volver al menú principal", callback_data="menu")])
    return InlineKeyboardMarkup(keyboard)

# Enviar menú de categorías
async def send_category_menu(chat_id, context: ContextTypes.DEFAULT_TYPE):
    message = "🎞️ *Selecciona una categoría para obtener películas:*"
    keyboard = create_category_keyboard()
    await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard, parse_mode="Markdown")

# Enviar películas al usuario con paginación
async def send_movies_to_telegram(movies, chat_id, context: ContextTypes.DEFAULT_TYPE, page=1):
    total_pages = len(movies) // 10 + (1 if len(movies) % 10 > 0 else 0)  # Calcular el número total de páginas
    start, end = (page - 1) * 10, page * 10
    for movie in movies[start:end]:
        title, votes, description, poster_path = movie['title'], movie['vote_average'], movie['overview'], movie.get('poster_path')
        trailer_url = get_movie_trailer(movie['id'])
        message = f"*🎬 Título:* {title}\n⭐ *Votos:* {votes}\n📖 *Sinópsis:* {description}\n🎥 *Tráiler:* {trailer_url}"

        if poster_path:
            await context.bot.send_photo(chat_id=chat_id, photo=image_base_url + poster_path, caption=message, parse_mode="Markdown")
        else:
            await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

        await asyncio.sleep(2)  # Evitar spam

    # Mostrar botones de navegación después de enviar las películas
    keyboard = create_pagination_keyboard(page, total_pages)
    await context.bot.send_message(chat_id=chat_id, text="Navega entre las páginas o vuelve al menú principal.", reply_markup=keyboard)

# Manejar respuestas de usuario al seleccionar una categoría o navegar
async def handle_user_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    category = query.data

    # Almacenar el estado actual del chat
    chat_id = query.message.chat_id
    user_data = context.user_data

    # Si el usuario hace clic en el menú principal
    if category == "menu":
        await send_category_menu(chat_id, context)
        user_data['category'] = None  # Resetear categoría
        user_data['page'] = 1  # Resetear página
        return

    # Si el usuario selecciona una categoría
    if category in ['popular', 'top_rated', 'now_playing', 'upcoming']:
        user_data['category'] = category
        user_data['page'] = 1  # Empezar desde la página 1
        movies_data = get_movies_by_category(category, 1)
        if 'results' in movies_data:
            await send_movies_to_telegram(movies_data['results'], chat_id, context, page=1)
        else:
            await query.message.reply_text('❌ No se encontraron películas en esta categoría.')
        return

    # Si el usuario navega entre páginas
    if category.startswith("page_"):
        page = int(category.split("_")[1])
        category_name = user_data.get('category')

        if category_name:
            movies_data = get_movies_by_category(category_name, page)
            if 'results' in movies_data:
                await send_movies_to_telegram(movies_data['results'], chat_id, context, page)
            else:
                await query.message.reply_text('❌ No se encontraron películas en esta categoría.')
        else:
            await query.message.reply_text('❌ No se ha seleccionado una categoría.')
        return

# Enviar menú al iniciar chat
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    save_user(chat_id)
    await send_category_menu(chat_id, context)

# Función principal
def Movies_Nerd_Bot():
    application = Application.builder().token(telegram_token).build()
    # Enviar menú cuando el usuario interactúe con el bot
    application.add_handler(MessageHandler(filters.TEXT | filters.COMMAND | filters.PHOTO | filters.VIDEO | filters.AUDIO, start))
    # Manejar las respuestas de usuario
    application.add_handler(CallbackQueryHandler(handle_user_response))
    # Iniciar el bot
    application.run_polling()

Movies_Nerd_Bot()
```

#### Manejo seguro de Id´s de usuarios del grupo de Telegram:

Los Id's de usuarios se almacenan en el archivo `users.json`:

- No lo expongas públicamente

Evitá subirlo a repositorios públicos de GitHub. Agregalo a `.gitignore`.
(Aqui se subió por motivos educativos y el Id almacenado es de muestra).

- Usá permisos adecuados

En Linux: `chmod 600 users.json` (Solo el dueño puede leer/escribir).

En Windows: Configurá los permisos para que solo el usuario del bot tenga acceso.

- Encriptación de datos sensibles.

Si guardás tokens, claves o información privada, encriptalos con `cryptography` o `fernet`.
Ejemplo en Python:

```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()  # Guardá esta clave de forma segura
cipher = Fernet(key)

data = '{"user_id": 12345, "username": "Gaby"}'
encrypted_data = cipher.encrypt(data.encode())

print(encrypted_data)  # Guardá esto en users.json
```

- No proceses el archivo directamente

En lugar de cargar y guardar el archivo constantemente, usá una base de datos como SQLite o MongoDB con autenticación.

- Validación y Sanitización

Evitá que usuarios malintencionados inyecten código JSON malicioso.
Usá `json.load()` con `try-except` para manejar errores:

```python
import json

try:
    with open("users.json", "r") as file:
        data = json.load(file)
except (json.JSONDecodeError, FileNotFoundError) as e:
    print(f"Error al cargar JSON: {e}")
```

#### Manejo seguro de las claves API:

_NO_ almacenar claves API en el código fuente, Es importante no dejar las claves de API (como la de TMDB y Telegram) directamente en el código. Usa un archivo `.env` para almacenarlas de manera segura o herramientas de gestión de secretos, como AWS Secrets Manager, Azure Key Vault o HashiCorp Vault.

1. Instalar python-dotenv

Antes de empezar, instalemos la librería `python-dotenv`, que nos permite leer variables de un archivo `.env`.

Abrí una terminal y ejecutá:

```bash
pip install python-dotenv
```

Esto instalará la librería en tu entorno de Python.

2. Crear el archivo .env

El archivo `.env` se usa para guardar variables sensibles como claves de API o tokens.
En la misma carpeta donde está tu script Python, creá un archivo llamado `.env` (sin extensión).

Ejemplo de `.env` (crealo con un editor de texto o VS Code):

```ini
TMDB_API_KEY=tu_clave_api_aqui
TELEGRAM_TOKEN=tu_token_aqui
```

Importante:

No uses comillas en las variables (= debe estar pegado al valor).
No subas este archivo a GitHub. Para evitarlo, agregalo a un `.gitignore`:

```bash
.env
```

3. Cargar las variables en Python

Ahora, en tu script Python, tenés que importar `dotenv` y `os` para leer las variables del archivo `.env`.

Ejemplo en tu código:

```python
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# Obtener las claves
tmdb_api_key = os.getenv("TMDB_API_KEY")
telegram_token = os.getenv("TELEGRAM_TOKEN")

# Verificar que se cargaron bien
print(f"TMDB API Key: {tmdb_api_key}")
print(f"Telegram Token: {telegram_token}")
```

Si configuraste todo bien, cuando ejecutes el script, deberías ver en la consola las claves que pusiste en el `.env`.

4. Usar las variables en tu código

Ahora que las variables están cargadas, podés usarlas en tu bot de Telegram:

```python
import telegram

bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
print("Bot iniciado correctamente.")
```

O cuando hagas una petición a la API de TMDB:

```python
import requests

api_key = os.getenv("TMDB_API_KEY")
url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=es-ES"

response = requests.get(url)
print(response.json())
```

5. Proteger el archivo .env

Para asegurarte de no exponer las claves:

- Agregalo al `.gitignore si usás Git`.
- No compartas este archivo directamente.
- Si subís el proyecto a un servidor como HEROKU (ver explicacion abajo), usá variables de entorno en lugar de `.env`.

#### Pasos para desplegar tu bot en Heroku:

1. Prepara tu proyecto

Antes de subirlo a Heroku, asegúrate de que tu proyecto esté listo para ejecutarse en la nube.

Asegúrate de tener un archivo `requirements.txt`. Este archivo debe contener todas las dependencias de tu proyecto. Si no lo tienes, crea uno ejecutando:

```bash
pip freeze > requirements.txt
```

Esto generará una lista de todas las dependencias instaladas en tu entorno local.

Crea un archivo `Procfile`. Este archivo le indica a Heroku cómo ejecutar tu bot. Crea un archivo llamado `Procfile` (sin extensión) en el directorio raíz de tu proyecto y añade esta línea:

```makefile
worker: python bot.py
```

Donde `bot.py` es el nombre del archivo principal de tu bot. Si tu archivo tiene otro nombre, cámbialo en consecuencia.

Añadir archivo `runtime.txt` (opcional). Si deseas especificar la versión de Python que quieres usar en Heroku, puedes crear un archivo llamado `runtime.txt` y añadir la versión, por ejemplo:

```txt
python-3.9.7
```

2. Crea una cuenta en Heroku

Si aún no tienes una cuenta en Heroku, crea una ahora. Una vez que tengas la cuenta, inicia sesión desde la terminal:

```bash
heroku login
```

Esto abrirá una ventana en tu navegador para que puedas iniciar sesión con tu cuenta de Heroku.

2. Inicializa un repositorio Git

Si no tienes un repositorio Git en tu proyecto, inicialízalo ejecutando estos comandos en la raíz de tu proyecto:

```bash
git init
git add .
git commit -m "Primer commit para Heroku"
```

3. Crea una nueva aplicación en Heroku

Ahora, crea una nueva aplicación en Heroku:

```bash
heroku create nombre-de-tu-app
```

Este comando creará una nueva aplicación en Heroku con el nombre que elijas (nombre-de-tu-app), y automáticamente asociará el repositorio Git con tu aplicación de Heroku.

4. Sube tu proyecto a Heroku

Sube tu código a Heroku con los siguientes comandos:

```bash
git push heroku master
```

Este comando sube tu código al servidor de Heroku. Si es la primera vez que lo haces, Heroku instalará todas las dependencias que definiste en `requirements.txt` y desplegará el bot.

5. Verifica que el bot esté corriendo

Una vez que se haya completado el despliegue, puedes verificar los logs para asegurarte de que el bot esté funcionando correctamente:

```bash
heroku logs --tail
```

6. Habilitar el bot 24/7

Heroku tiene un plan gratuito con ciertas limitaciones (como dormir la app después de 30 minutos sin uso). Si quieres evitar que tu bot se apague, tendrás que optar por un plan de pago. Sin embargo, hay formas de mantenerlo activo utilizando servicios como Uptime Robot que envían pings periódicos a tu app para evitar que entre en inactividad.

7. Opcional: Configura el bot con variables de entorno

Si necesitas variables de entorno, como tu token de Telegram o tu API de TMDB, puedes configurarlas en Heroku:

```bash
heroku config:set TELEGRAM_TOKEN=tu_token TELEGRAM_USER=tu_usuario
```

Puedes acceder a estas variables en tu código Python utilizando:

```python
import os
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
```

8. Listo!

¡Tu bot ya debería estar funcionando 24/7 en Heroku! Puedes invocar el bot desde Telegram y comenzar a interactuar con él.

### Limitaciones

El Bot de Telegram es solo para fines educativos bajo la licencia MIT.

---

<h3 align="left">Conecta Conmigo</h3>

<p align="left">
<a href="https://www.youtube.com/@gabriellugooo" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.icons8.com/?size=50&id=55200&format=png" alt="@gabriellugooo" height="40" width="40" /></a>
<a href="http://www.tiktok.com/@gabriellugooo" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.icons8.com/?size=50&id=118638&format=png" alt="@gabriellugooo" height="40" width="40" /></a>
<a href="https://instagram.com/lugooogabriel" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.icons8.com/?size=50&id=32309&format=png" alt="lugooogabriel" height="40" width="40" /></a>
<a href="https://twitter.com/gabriellugo__" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.icons8.com/?size=50&id=phOKFKYpe00C&format=png" alt="gabriellugo__" height="40" width="40" /></a>
<a href="https://www.linkedin.com/in/hernando-gabriel-lugo" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.icons8.com/?size=50&id=8808&format=png" alt="hernando-gabriel-lugo" height="40" width="40" /></a>
<a href="https://github.com/GabrielLugooo" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.icons8.com/?size=80&id=AngkmzgE6d3E&format=png" alt="gabriellugooo" height="34" width="34" /></a>
<a href="mailto:lugohernandogabriel@gmail.com"> <img align="center" src="https://img.icons8.com/?size=50&id=38036&format=png" alt="lugohernandogabriel@gmail.com" height="40" width="40" /></a>
<a href="https://linktr.ee/gabriellugooo" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://simpleicons.org/icons/linktree.svg" alt="gabriellugooo" height="40" width="40" /></a>
</p>

<p align="left">
<a href="https://github.com/GabrielLugooo/GabrielLugooo/blob/main/Readme%20Spanish.md" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.shields.io/badge/Versión%20Español-000000" alt="Versión Español" /></a>
<a href="https://github.com/GabrielLugooo/GabrielLugooo/blob/main/README.md" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.shields.io/badge/Versión%20Inglés-Green" alt="Versión Inglés" /></a>

</p>

<a href="https://linktr.ee/gabriellugooo" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.shields.io/badge/Créditos-Gabriel%20Lugo-green" alt="Créditos" /></a>
<img align="center" src="https://komarev.com/ghpvc/?username=GabrielLugoo&label=Vistas%20del%20Perfil&color=green&base=2000" alt="GabrielLugooo" />
<a href="" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.shields.io/badge/License-MIT-green" alt="MIT License" /></a>
