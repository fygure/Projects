import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

AV_API_KEY = "2VZV482F02KE9ZFA"  # Alpha Vantage API key for stock price checking
NEWS_API_KEY = "002b377f4bff4abba9739167ce97fc9d"  # News Api key

TWILIO_ACCOUNT_SID = "AC3fa72350bf0e146666797644fb0a1d04"
TWILIO_AUTH_TOKEN = "c063cfe0db5c837411830faeaba5eef0"

MY_NUMBER = "+18323222997"
TWILIO_NUMBER = "+19414515537"

stock_parameters = {
    "function":"TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "outputsize": "compact",
    "apikey": AV_API_KEY
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()
yesterday_closing_price = stock_data["Time Series (Daily)"]
#print(yesterday_closing_price["2021-12-31"]["4. close"])
closing_prices = [float(value["4. close"]) for (key, value) in yesterday_closing_price.items()]
#print(closing_prices)
positive_difference = round(float(abs(closing_prices[0] - closing_prices[1])), 2)
#print(positive_difference)
difference = round(float(closing_prices[0] - closing_prices[1]), 2)
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
percentage_difference = round((positive_difference/closing_prices[1] * 100), 2)
#print(percentage_difference)
dates = [key for (key, value) in yesterday_closing_price.items()]

news_parameters = {
    "q": COMPANY_NAME,
    "from": dates[1],
    "to": dates[0],
    "apiKey": NEWS_API_KEY
}

news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()
first_three_articles = news_data["articles"][:3]

headlines = [first_three_articles[i]["title"] for i, value in enumerate(first_three_articles)]
descriptions = [first_three_articles[i]["description"] for i, value in enumerate(first_three_articles)]
#print(headlines)
#print(first_three_articles)

account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

for i in range(0, 3):
    if percentage_difference > 3:
        client = Client(account_sid, auth_token)
        message = client.messages \
                .create(
                     body=f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline: {headlines[i]}\n\nDescription: {descriptions[i]}",
                     from_=TWILIO_NUMBER,
                     to=MY_NUMBER
                 )
        print(message.status)
    
    # else:
    #     client = Client(account_sid, auth_token)
    #     message = client.messages \
    #             .create(
    #                  body=f"{STOCK_NAME} did not have an increase or decrease by 5% within the past day.",
    #                  from_=TWILIO_NUMBER,
    #                  to=MY_NUMBER
    #              )
    #     print(message.status)