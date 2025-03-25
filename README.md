<img align="center" src="https://media.licdn.com/dms/image/v2/D4D16AQGUNxQ7NSC05A/profile-displaybackgroundimage-shrink_350_1400/profile-displaybackgroundimage-shrink_350_1400/0/1738695150340?e=1744243200&v=beta&t=oXX-ixT9bR3dJcYCLv4KBs5wjKFoeP0524kFGHQMYmQ" alt="gabriellugo" />

# TELEGRAM BOT

<a href="https://github.com/GabrielLugooo/Telegram-Bot-Public" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.shields.io/badge/English%20Telegram%20Bot-000000" alt="English Telegram Bot" /></a>
<a href="https://github.com/GabrielLugooo/Telegram-Bot-Public/blob/main/README%20Spanish.md" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.shields.io/badge/Spanish%20Telegram%20Bot-green" alt="Spanish Telegram Bot" /></a>

### Objective

The Telegram Bot is designed to provide up-to-date information on popular, top-rated, currently playing, and upcoming movies. Its main objective is to make it easier for users to access details such as synopses, ratings, and movie trailers from The Movie Database (TMDb), all within the Telegram platform.

In addition, the bot allows for interactive navigation using buttons, improving the user experience when exploring film content quickly and easily.

### Skills Learned

- Use of the Telegram API for bot creation.
- Use of REST API (TMDb) to obtain movie information.
- Handling encryption with the `cryptography` library.
- Use of `dotenv` to securely manage environment variables.
- Creation of interactive interfaces with `InlineKeyboardMarkup`.
- Handling HTTP requests with `requests`.
- Asynchronous programming with `asyncio` to avoid blocking during bot execution.
- Managing and storing users in JSON files.
- Implementing interactive pagination in Telegram.
- Handling errors in requests to external APIs.

### Tools Used

![Static Badge](https://img.shields.io/badge/Python-000000?logo=python&logoSize=auto)
![Static Badge](https://img.shields.io/badge/Requests-000000?logo=requests&logoSize=auto)
![Static Badge](https://img.shields.io/badge/Asyncio-000000?logo=asyncio&logoSize=auto)
![Static Badge](https://img.shields.io/badge/Cryptography%20Fernet-000000?logo=cryptography&logoSize=auto)
![Static Badge](https://img.shields.io/badge/venv-000000?logo=venv&logoSize=auto)
![Static Badge](https://img.shields.io/badge/.ENV-000000?logo=dotenv&logoSize=auto)
![Static Badge](https://img.shields.io/badge/JSON-000000?logo=json&logoSize=auto)
![Static Badge](https://img.shields.io/badge/Telegram-000000?logo=telegram&logoSize=auto)
![Static Badge](https://img.shields.io/badge/TMDB-000000?logo=themoviedatabase&logoSize=auto)

- Python: Main programming language used for bot development.
- `python-telegram-bot`: Library used to interact with the Telegram API.
- `requests`: Used to make HTTP requests to the TMDB API.
- TMDB API: Data source for retrieving movie information.
- `cryptography (Fernet)`: Used for encrypting sensitive data and improving security.
- `JSON`: For structured data storage and management.
- `dotenv`: Loads environment variables to manage credentials securely.
- `asyncio`: Handles asynchronous tasks within the bot.
- Telegram Bot API: Enables communication between the bot and users.

### Project

#### Preview

<p align= left>
<img align="center" src="https://i.imgur.com/7GXWLHd.jpeg" alt="Bot01" width=400 /> <img align="center" src="https://i.imgur.com/xlMrMYO.jpeg" alt="Bot02" width=400 />

<img align="center" src="https://i.imgur.com/OGITxpr.jpeg" alt="Bot03" width=400 /> <img align="center" src="https://i.imgur.com/KGTVCIG.jpeg" alt="Bot04" width=400 />

<img align="center" src="https://i.imgur.com/sA9bLpD.jpeg" alt="Bot05" width=400 /> <img align="center" src="https://i.imgur.com/oNQH8Vk.jpeg" alt="Bot06" width=400 />

<img align="center" src="https://i.imgur.com/XhD1Qjc.jpeg" alt="Bot07" width=800/>
</p>

#### Code with Comments (English)

```python
# Movie Nerds Bot
# Import the necessary libraries

import sys
import you
import io
import requests
import json
import asyncio
import time
from dotenv import load_dotenv
from cryptography.fernet import Fernet

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Generate a key for encryption (this only needs to be done once)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt and save data
with open('users.json', 'rb') as file:
      data = file.read()
encrypted_data = cipher_suite.encrypt(data)

with open('encrypted_users.json', 'wb') as file:
      file.write(encrypted_data)

# List of allowed chat_ids, the Ids are stored in the users.json
allowed_users = [-100123456789]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
      chat_id = update.message.chat.id
      if chat_id not in allowed_users:
           await update.message.reply_text("You do not have permissions to interact with this bot.")
      return

# Set standard output to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load the variables from the .env file
load_dotenv()

# TMDB API Key & Telegram Token
api_key = os.getenv("TMDB_API_KEY") # API TMDB Key
tmdb_base_url = 'https://api.themoviedb.org/3/movie/' # TMDB Movie API URL
image_base_url = "https://image.tmdb.org/t/p/w500" # TMDB Image Database URL
telegram_token = os.getenv("TELEGRAM_TOKEN") # Telegram Token
users_file = "users.json" # JSON file where Telegram group user IDs are stored

# Load users from file
def load_users():
      try:
           with open(users_file, "r") as file:
           return json.load(file)
      except (FileNotFoundError, json.JSONDecodeError):
           return []

# Save users to file
def save_users(users):
      with open(users_file, "w") as file:
           json.dump(users, file)

# Save user if new
def save_user(chat_id):
      users = load_users()
      if chat_id not in users:
           users.append(chat_id)
           save_users(users)

# Get movie categories
def get_movie_categories():
      return {
           "🎬 Popular": 'popular',
           "⭐ Top Rated": 'top_rated',
           "🎥 Now Playing": 'now_playing',
           "🔜 Coming Soon": 'upcoming'
      }

# Get movies by category with error handling
def get_movies_by_category(category, page=1):
     try:
           tmdb_url = f'{tmdb_base_url}{category}?page={page}&api_key={api_key}&language=es&region=AR'
           response = requests.get(tmdb_url)
           response.raise_for_status() # Check if there was an error in the request
           return response.json()
     except requests.exceptions.RequestException as e:
           print(f"Error getting movies from TMDB: {e}")
           return {"results": []} # Return an empty result on error

# Get a movie trailer with error handling
def get_movie_trailer(movie_id):
      try:
           tmdb_url = f'{tmdb_base_url}{movie_id}/videos?api_key={api_key}&language=es'
           response = requests.get(tmdb_url)
           response.raise_for_status() # Check if there was an error in the request
           json_data = response.json()
           return f'https://www.youtube.com/watch?v={json_data["results"][0]["key"]}' if json_data.get("results") else "Not available"
      except requests.exceptions.RequestException as e:
           print(f"Error getting movie trailer for {movie_id}: {e}")
           return "Not available"

# Create an interactive keyboard for the main menu
def create_category_keyboard():
      keyboard = [[InlineKeyboardButton(cat, callback_data=key)] for cat, key in get_movie_categories().items()]
      return InlineKeyboardMarkup(keyboard)

# Create an interactive keyboard for pagination and returning to the menu
def create_pagination_keyboard(page, total_pages):
     keyboard = []
      if page > 1:
           keyboard.append([InlineKeyboardButton("⬅️ Previous Page", callback_data=f"page_{page-1}")])
      if page < total_pages:
           keyboard.append([InlineKeyboardButton("➡️ Next Page", callback_data=f"page_{page+1}")])
           keyboard.append([InlineKeyboardButton(f"Page {page}/{total_pages}", callback_data="none")])
           keyboard.append([InlineKeyboardButton("🏠 Return to main menu", callback_data="menu")])
      return InlineKeyboardMarkup(keyboard)

# Send category menu
async def send_category_menu(chat_id, context: ContextTypes.DEFAULT_TYPE):
     message = "🎞️ *Select a category to get movies:*"
     keyboard = create_category_keyboard()
           await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard, parse_mode="Markdown")

# Send movies to user with pagination
async def send_movies_to_telegram(movies, chat_id, context: ContextTypes.DEFAULT_TYPE, page=1):
     total_pages = len(movies) // 10 + (1 if len(movies) % 10 > 0 else 0) # Calculate the total number of pages
     start, end = (page - 1) * 10, page * 10
      for movie in movies[start:end]:
         title, votes, description, poster_path = movie['title'], movie['vote_average'], movie['overview'], movie.get('poster_path')
         trailer_url = get_movie_trailer(movie['id'])
         message = f"*🎬 Title:* {title}\n⭐ *Votes:* {votes}\n📖 *Synopsis:* {description}\n🎥 *Trailer:* {trailer_url}"
           if poster_path:
                await context.bot.send_photo(chat_id=chat_id, photo=image_base_url + poster_path, caption=message, parse_mode="Markdown")
           else:
                await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

await asyncio.sleep(2) # Prevent spam

# Show navigation buttons after sending movies
keyboard = create_pagination_keyboard(page, total_pages)
     await context.bot.send_message(chat_id=chat_id, text="Navigate between pages or return to the main menu.", reply_markup=keyboard)

# Handle user responses when selecting a category or browsing
async def handle_user_response(update: Update, context: ContextTypes. DEFAULT_TYPE):
     query = update.callback_query
     category = query.data
     # Store the current chat state
     chat_id = query.message.chat_id
     user_data = context.user_data
     # If the user clicks the main menu
     if category == "menu":
         await send_category_menu(chat_id, context)
         user_data['category'] = None # Reset category
         user_data['page'] = 1 # Reset page
     return
     # If the user selects a category
     if category in ['popular', 'top_rated', 'now_playing', 'upcoming']:
           user_data['category'] = category
           user_data['page'] = 1 # Start from page 1
           movies_data = get_movies_by_category(category, 1)
           if 'results' in movies_data:
                await send_movies_to_telegram(movies_data['results'], chat_id, context, page=1)
           else:
                await query.message.reply_text('❌ No movies found in this category.')
     return
     # If the user navigates between pages
     if category.startswith("page_"):
           page = int(category.split("_")[1])
           category_name = user_data.get('category')
           if category_name:
                movies_data = get_movies_by_category(category_name, page)
                if 'results' in movies_data:
                    await send_movies_to_telegram(movies_data['results'], chat_id, context, page)
                else:
                    await query.message.reply_text('❌ No movies found in this category.')
           else:
                await query.message.reply_text('❌ No category has been selected.')
     return

# Send menu when starting chat
async def start(update: Update, context: ContextTypes. DEFAULT_TYPE):
     chat_id = update.message.chat.id
     save_user(chat_id)
     await send_category_menu(chat_id, context)

# Main function
def Movies_Nerd_Bot():
     application = Application.builder().token(telegram_token).build()
     # Send menu when the user interacts with the bot
     application.add_handler(MessageHandler(filters.TEXT | filters.COMMAND | filters.PHOTO | filters.VIDEO | filters.AUDIO, start))
     # Handle user responses
     application.add_handler(CallbackQueryHandler(handle_user_response))
     # Start the bot
     application.run_polling()

Movies_Nerd_Bot()
```

#### Secure handling of Telegram group user IDs:

User IDs are stored in the `users.json` file:

- Don't post it publicly.

Avoid uploading it to public GitHub repositories. Add it to `.gitignore`.
(This is for educational purposes, and the stored ID is a sample.)

- Use appropriate permissions.

On Linux: `chmod 600 users.json` (Only the owner can read/write).

On Windows: Set permissions so that only the bot user has access.

- Encrypt sensitive data.

If you store tokens, keys, or private information, encrypt them with `cryptography` or `fernet`.

Python example:

```python
from cryptography.fernet import Fernet

key = Fernet.generate_key() # Store this key securely
cipher = Fernet(key)

data = '{"user_id": 12345, "username": "Gaby"}'
encrypted_data = cipher.encrypt(data.encode())

print(encrypted_data) # Save this to users.json
```

- Don't process the file directly

Instead of constantly uploading and saving the file, use a database like SQLite or MongoDB with authentication.

- Validation and Sanitization

Prevent malicious users from injecting malicious JSON code.
Use `json.load()` with `try-except` to handle errors:

```python
import json

try:
     with open("users.json", "r") as file:
         data = json.load(file)
except (json.JSONDecodeError, FileNotFoundError) as e:
     print(f"Error loading JSON: {e}")
```

#### Secure API Key Handling:

**DO NOT** store API keys in your source code. It's important not to leave API keys (such as those for TMDB and Telegram) directly in your code. Use a `.env` file to securely store them or use secret management tools such as AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault.

1. Install python-dotenv

Before we begin, let's install the `python-dotenv` library, which allows us to read variables from an `.env` file.

Open a terminal and run:

```bash
pip install python-dotenv
```

This will install the library in your Python environment.

2. Create the .env file

The `.env` file is used to store sensitive variables such as API keys or tokens.

In the same folder as your Python script, create a file named `.env` (no extension).

Example of `.env` (create it with a text editor or VS Code):

```ini
TMDB_API_KEY=your_api_key_here
TELEGRAM_TOKEN=your_token_here
```

Important:

Do not use quotes around variables (= must be attached to the value).
Do not upload this file to GitHub. To avoid this, add it to a `.gitignore` file:

```bash
.env
```

3. Load the variables in Python

Now, in your Python script, you need to import `dotenv` and `os` to read the variables from the `.env` file.

Example in your code:

```python
from dotenv import load_dotenv
import os

# Load the variables from the .env file
load_dotenv()

# Get the keys
tmdb_api_key = os.getenv("TMDB_API_KEY")
telegram_token = os.getenv("TELEGRAM_TOKEN")

# Verify that they loaded correctly
print(f"TMDB API Key: {tmdb_api_key}")
print(f"Telegram Token: {telegram_token}")
```

If you configured everything correctly, when you run the script, you should see the keys you put in the `.env` in the console.

4. Using variables in your code

Now that the variables are loaded, you can use them in your Telegram bot:

```python
import telegram

bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
print("Bot started successfully.")
```

Or when making a request to the TMDB API:

```python
import requests

api_key = os.getenv("TMDB_API_KEY")
url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=es-ES"

response = requests.get(url)
print(response.json())
```

5. Protecting the .env file

To ensure you don't expose the keys:

- Add it to `.gitignore` if you're using Git.
- Don't share this file directly.
- If you upload the project to a server like HEROKU (see explanation below), use environment variables instead of `.env`.

#### Steps to deploy your bot to Heroku:

1. Prepare your project

Before uploading to Heroku, make sure your project is ready to run in the cloud.

Make sure you have a `requirements.txt` file. This file should contain all your project's dependencies. If you don't have one, create one by running:

```bash
pip freeze > requirements.txt
```

This will generate a list of all the dependencies installed in your local environment.

Create a `Procfile` file. This file tells Heroku how to run your bot. Create a file named `Procfile` (no extension) in your project's root directory and add this line:

```makefile
worker: python bot.py
```

Where `bot.py` is the name of your bot's main file. If your file has a different name, change it accordingly.

Add a `runtime.txt` file (optional). If you want to specify the version of Python you want to use on Heroku, you can create a file called `runtime.txt` and add the version, for example:

```txt
python-3.9.7
```

2. Create a Heroku account

If you don't have a Heroku account yet, create one now. Once you have one, log in from the terminal:

```bash
heroku login
```

This will open a window in your browser so you can log in with your Heroku account.

2. Initialize a Git repository

If you don't have a Git repository in your project, initialize it by running these commands in the root of your project:

```bash
git init
git add .
git commit -m "First commit to Heroku"
```

3. Create a new app on Heroku

Now, create a new app on Heroku:

```bash
heroku create your-app-name
```

This command will create a new app on Heroku with the name you choose (your-app-name), and will automatically associate the Git repository with your Heroku app.

4. Push your project to Heroku

Push your code to Heroku with the following commands:

```bash
git push heroku master
```

This command pushes your code to the Heroku server. If this is your first time doing this, Heroku will install all the dependencies you defined in `requirements.txt` and deploy the bot.

5. Verify that the bot is running

Once the deployment is complete, you can check the logs to ensure the bot is running correctly:

```bash
heroku logs --tail
```

6. Enable the bot 24/7

Heroku has a free plan with certain limitations (such as sleeping the app after 30 minutes of non-use). If you want to prevent your bot from shutting down, you'll need to upgrade to a paid plan. However, there are ways to keep it active by using services like Uptime Robot, which send periodic pings to your app to prevent it from going down.

7. Optional: Configure the bot with environment variables

If you need environment variables, such as your Telegram token or your TMDB API, you can configure them on Heroku:

```bash
heroku config:set TELEGRAM_TOKEN=your_token TELEGRAM_USER=your_username
```

You can access these variables in your Python code using:

```python
import os
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
```

8. Done!

Your bot should now be running 24/7 on Heroku! You can invoke the bot from Telegram and start interacting with it.

### Limitations

Telegram Bot it's just for educational purpose under the MIT License.

---

<h3 align="left">Connect with me</h3>

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
<a href="https://github.com/GabrielLugooo/GabrielLugooo/blob/main/README.md" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.shields.io/badge/English%20Version-000000" alt="English Version" /></a>
<a href="https://github.com/GabrielLugooo/GabrielLugooo/blob/main/Readme%20Spanish.md" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.shields.io/badge/Spanish%20Version-Green" alt="Spanish Version" /></a>
</p>

<a href="https://linktr.ee/gabriellugooo" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.shields.io/badge/Credits-Gabriel%20Lugo-green" alt="Credits" /></a>
<img align="center" src="https://komarev.com/ghpvc/?username=GabrielLugoo&label=Profile%20views&color=green&base=2000" alt="GabrielLugooo" />
<a href="" target="_blank" rel="noreferrer noopener"> <img align="center" src="https://img.shields.io/badge/License-MIT-green" alt="MIT License" /></a>
