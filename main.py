import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.constants import ParseMode
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
URL = "https://pokezentrum.de/kategorie/pokemon-karten-news/"

bot = Bot(token=BOT_TOKEN)

def get_latest_news(count=5):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all("article")[:count]

    news = []
    for article in articles:
        title = article.find("h2").text.strip()
        link = article.find("a")["href"]
        news.append((title, link))
    return news

def send_news():
    news_items = get_latest_news()
    for title, link in news_items:
        message = f"📰 <b>{title}</b>\n🔗 {link}"
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)

if __name__ == "__main__":
    send_news()
