# Importing files for web scraping
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup
from time import sleep

# Setting URL variables
page_url = 'https://finance.yahoo.com/quote/FB?p=FB'
urlClient = urlReq(page_url)
page_html = urlClient.read()
urlClient.close()

# Function to grab prices
def parsePrice():
    # Parsing HTML
    page_soup = soup(page_html, "html.parser")

    # Grabbing current price
    curr_price = page_soup.find('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text
    return curr_price

# Infinite loop to grab prices in real time
while True:
    print('The current price is: ' + str(parsePrice()))
    sleep(10)
