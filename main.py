import os
import requests
from twilio.rest import Client

# Variables // Constants
GOOGLE_SYMBOL = "GOOG"
API_KEY_ALPHA_VANTAGE = os.environ["ALPHA_VANTAGE_API_KEY"]
FUNCTION = "TIME_SERIES_DAILY_ADJUSTED"
NEWS_API_KEY = os.environ["NEWS_API_KEY"]

AUTH_TOKEN = os.environ["AUTH_TOKEN"]
ACCOUNT_SID = os.environ["ACCOUNT_SID"]
PHONE_NUMBER = os.environ["TWILIO_PHONE_NUMBER"]

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def stock_prices_alpha_vantage(function, symbol, apikey):
    """Returns data from the Alpha Vantage API."""
    parameters = {
        "function": f"{function}",
        "symbol": f"{symbol}",
        "apikey": f"{apikey}"
    }
    URL = "https://www.alphavantage.co/query"
    alpha_vantage_response = requests.get(url=URL, params=parameters)
    stock_price_data = alpha_vantage_response.json()
    return stock_price_data


def news_api_articles(query, apikey):
    """Returns a list of dictionaries that contains the articles from the News API."""
    news_parameters = {
        "apiKey": f"{apikey}",
        "q": f"{query}"
    }
    URL = "https://newsapi.org/v2/everything"
    news_response = requests.request("GET", url=URL, params=news_parameters)
    articles = news_response.json()["articles"]
    return articles


def positive_number(number):
    """If a number is bigger than zero return an up emoji."""
    if number > 0:
        return "🔺"
    else:
        return "🔻"


stock_prices = stock_prices_alpha_vantage(function=FUNCTION,
                                          symbol=GOOGLE_SYMBOL,
                                          apikey=API_KEY_ALPHA_VANTAGE)["Time Series (Daily)"]
days = list(stock_prices)

yesterday_close_price = float(stock_prices[days[0]]['4. close'])
day_after_yesterday_close_price = float(stock_prices[days[1]]['4. close'])
total_difference = round(((yesterday_close_price - day_after_yesterday_close_price) / 100) * 100, 2)

latest_articles = news_api_articles(query=GOOGLE_SYMBOL, apikey=NEWS_API_KEY)[::-1]
sign = positive_number(total_difference)

for article in latest_articles[:2]:
    title = article["title"]
    description = article["description"]
    url = article["url"]
    message = client.messages.create(to="",
                                     from_=PHONE_NUMBER,
                                     body=f"{positive_number(total_difference)} {total_difference}%\n"
                                          f"{title}\n"
                                          f"{description}\n"
                                          f"{url}")
