import json, pandas ,requests, os, random, kivy.logger
from bs4 import BeautifulSoup
from collections import OrderedDict

def fetch_crime_news():
    NEWS_SOURCES = [
        "https://www.the-star.co.ke/news/",
        "https://www.theeastafrican.co.ke/tea/news",
        "https://www.pulselive.co.ke/news/local"
    ]
    news_data = []

    for url in NEWS_SOURCES:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            articles = soup.find_all("article")
            for article in articles:
                headline_tag = article.find("h2") or article.find("h3")
                summary_tag = article.find("p")
                link_tag = article.find("a")

                if headline_tag and link_tag:
                    news_item = {
                        "headline": headline_tag.text.strip(),
                        "summary": summary_tag.text.strip() if summary_tag else "No summary available",
                        "link": link_tag["href"] if "http" in link_tag["href"] else url + link_tag["href"]
                    }
                    news_data.append(news_item)
        else:
            kivy.logger.Logger.info(f"Failed to fetch data from {url}")

    pandas.DataFrame(news_data).to_json('Utility/Alerts.json', orient='records')


def load_news():
    try:
        with open('Utility/Alerts.json', "r", encoding="utf-8") as json_reader:
            news_data = json.load(json_reader)

            if isinstance(news_data, list):
                random.shuffle(news_data)
                return news_data

            return []

    except json.JSONDecodeError as e:
        kivy.logger.Logger.info(f"[ERROR] JSONDecodeError: {e}")
        return []

