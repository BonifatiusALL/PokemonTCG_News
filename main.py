from flask import Flask
import threading, time, requests, os
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.constants import ParseMode

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
bot = Bot(token=BOT_TOKEN)
URL = "https://pokezentrum.de/kategorie/pokemon-karten-news/"
last_sent = None

def get_latest():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find("article")
    title = article.find("h2").text.strip()
    link = article.find("a")["href"]
    return title, link

def send_news(title, link):
    message = f"📰 <b>Neue Pokémon-News</b>\n\n{title}\n🔗 {link}"
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)

def check_loop():
    global last_sent
    while True:
        try:
            title, link = get_latest()
            if link != last_sent:
                send_news(title, link)
                last_sent = link
            else:
                print("Keine neue News.")
        except Exception as e:
            print("Fehler:", e)
        time.sleep(1800)

@app.route("/")
def home():
    return "Bot läuft", 200

if __name__ == "__main__":
    threading.Thread(target=check_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
