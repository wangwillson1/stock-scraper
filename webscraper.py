# Importing files for web scraping
import os
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup
from time import sleep
from twilio.rest import Client

# Function to grab prices
def getPrice():
    # Setting URL variables
    page_url = 'https://finance.yahoo.com/quote/FB?p=FB'
    urlClient = urlReq(page_url)
    page_html = urlClient.read()
    urlClient.close()
    
    # Parsing HTML
    page_soup = soup(page_html, "html.parser")

    # Grabbing current price
    curr_price = page_soup.find('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    return curr_price

# Function to find percentage difference
def percentageDifference(new, old):
    return ( (new - old) / old ) * 100

# Twilio information
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# Infinite loop to grab prices in real time
first_itr = True;
prev_price = 0;
send_text = 0;

while True:
    prev_price = 0
    curr_price = float(getPrice())

    if first_itr:
        prev_price = float(getPrice())
        first_itr = False;

    else:
        prev_price = curr_price

    # Print information to console
    print('The current price is: ' + str(curr_price))
    print('The previous price was: ' + str(prev_price))

    percentage_change = percentageDifference(curr_price, prev_price)
    print('The percentage change is: ' + str(percentage_change) + '%\n\n')

    # Send text message if percentage is greater than specified
    if (percentage_change >= send_text):
        message = client.messages.create(
            body='Hey! Your stock changed by ' + str(percentage_change) + "%",
            from_='+16476938905',
            to='+16479186806'
        )

        print(message.sid)

    sleep(5)
