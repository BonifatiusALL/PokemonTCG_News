from flask import Flask
import threading, time, requests
from bs4 import BeautifulSoup
from telegram import Bot
import os

app = Flask(__name__)
bot = Bot(token=os.environ["BOT_TOKEN"])
CHAT_ID = os.environ["CHAT_ID"]
URL = "https://pokezentrum.de/kategorie/pokemon-karten-news/"
last_sent = None

def task():
    global last_sent
    while True:
        try:
            r = requests.get(URL)
            soup = BeautifulSoup(r.text, "html.parser")
            art = soup.find("article")
            title = art.find("h2").get_text(strip=True)
            link = art.find("a")["href"]
            if link != last_sent:
                bot.send_message(chat_id=CHAT_ID,
                    text=f"📰 Neue Pokémon-News:\n\n{title}\n🔗 {link}")
                last_sent = link
        except Exception as e:
            print("Fehler:", e)
        time.sleep(1800)

@app.route("/healthz")
def health():
    return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=task, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
