import schedule
import time
from email.message import EmailMessage 
import ssl
import smtplib

import os
from dotenv import load_dotenv
load_dotenv()
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

import yfinance as yf

#------------------------------------------------------------------------------------------------

def get_price():
    quotes = []
    tickers = ['BTC-USD','ETH-USD']
    for x in range(0,len(tickers)):
        ticker_yahoo = yf.Ticker(tickers[x])
        data = ticker_yahoo.history()
        last_quote = data['Close'].iloc[-1]
        print(tickers[x], last_quote)
        quotes.append(last_quote)
    print("quotes: ", quotes)
    send_email(quotes)

#------------------------------------------------------------------------------------------------

def send_email(data):
    email_sender = 'joshua.becker91@gmail.com'
    email_password = EMAIL_PASSWORD
    email_receiver = 'joshua.becker91@gmail.com' # can enter an array with multiple email receivers

    subject = f'Latest Cryptocurrency Prices'

    body = f'''
    This email was sent from python! Robots are hard at work to bring you this data.
    The most recent price of Bitcoin is: {data[0]} 
    The most recent price of Ethereum is: {data[1]} 
    '''

    # html=f'<h1>BTC is trading at {last_quote}</h1>' can also have html code here to customize styling/embeds/links

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        print("email successfully sent")
    except:
        print("error sending email")

schedule.every(60).minutes.do(get_price)

while True:
    schedule.run_pending()
    time.sleep(1)
