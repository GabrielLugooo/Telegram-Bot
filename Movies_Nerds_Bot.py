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
