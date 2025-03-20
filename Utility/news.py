import requests
from bs4 import BeautifulSoup

# Updated list with only Kenya-based news sources
NEWS_SOURCES = [
    #"https://www.the-star.co.ke/news/",
    #"https://www.theeastafrican.co.ke/tea/news",
    #"https://www.pulselive.co.ke/news/local",
    #"https://nation.africa/kenya/news",
    "https://www.kenyanews.go.ke/category/crime/"
]

CRIME_KEYWORDS = ["crime", "robbery", "murder", "theft", "assault", "fraud", "burglary", "homicide"]

def fetch_crime_news():
    news_data = []

    for url in NEWS_SOURCES:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.find_all("article")

            for article in articles:
                headline_tag = article.find("h2") or article.find("h3")
                summary_tag = article.find("p")
                link_tag = article.find("a")

                if headline_tag and link_tag:
                    headline = headline_tag.text.strip()
                    summary = summary_tag.text.strip() if summary_tag else "No summary available"
                    link = link_tag["href"] if "http" in link_tag["href"] else url + link_tag["href"]

                    # Filter only crime-related news
                    if any(keyword in headline.lower() for keyword in CRIME_KEYWORDS):
                        news_data.append({"headline": headline, "summary": summary, "link": link})
        else:
            print(f"❌ Failed to fetch data from {url}")

    return news_data

def display_news(news_data):
    if not news_data:
        print("⚠️ No crime news found.")
        return

    print("\n🔹 Latest Crime News in Kenya 🔹\n")
    for idx, news in enumerate(news_data, start=1):
        print(f"{idx}. {news['headline']}")
        print(f"   Summary: {news['summary']}")
        print(f"   Link: {news['link']}\n")

# Uncomment to test fetching news
news_data = fetch_crime_news()
display_news(news_data)
