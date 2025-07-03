import os, time, requests
from bs4 import BeautifulSoup
from telegram import Bot

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
URL = "https://pokezentrum.de/kategorie/pokemon-karten-news/"

bot = Bot(token=BOT_TOKEN)
last_sent = None

def get_latest():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    art = soup.find("article")
    title = art.find("h2").get_text(strip=True)
    link = art.find("a")["href"]
    return title, link

def send(title, link):
    bot.send_message(chat_id=CHAT_ID, text=f"📰 Neue Pokémon-News:\n\n{title}\n🔗 {link}")

if __name__ == "__main__":
    while True:
        try:
            title, link = get_latest()
            if link != last_sent:
                send(title, link)
                last_sent = link
            else:
                print("Keine neue News.")
        except Exception as e:
            print("Fehler:", e)
        time.sleep(1800)
