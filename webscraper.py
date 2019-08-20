# Importing files for web scraping
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup

# Setting URL variables
test_url = 'https://www.newegg.ca/LCD-LED-Monitors/SubCategory/ID-20?Tid=166428'
urlClient = urlReq(test_url)
page_html = urlClient.read()
urlClient.close()

# Parsing HTML
page_soup = soup(page_html, "html.parser")

# Finding desired content
containers = page_soup.findAll("div", {"class":"item-container"})

filename = "products.csv"
f = open(filename, "w")

headers = "brand, title, total_price, old_price, percent_saved, ship_cost\n"
f.write(headers)

# Find elements with classes function
def findClass(contain, elem, class_name, index):
    return contain.findAll(elem, {"class": class_name})[index]

# Find total price of item
def totalPrice(contain):
    price_container = findClass(contain, "li", "price-current", 0)
    price_dollar = price_container.findAll("strong")[0].text
    price_cents = price_container.findAll("sup")[0].text
    return float((price_dollar + price_cents).replace(',',''))

# Find percentage difference
def percentageDifference(new, old):
    return ( (new - old) / old ) * 100

# Loop through all containers
for container in containers:
    brand = findClass(container, "a", "item-title", 0).text.split()[0]
    title = findClass(container, "a", "item-title", 0).text.replace(",", "|")

    info_container = findClass(container, "div", "item-action", 0).ul

    # Getting price of item
    total_price = totalPrice(info_container)

    # Getting shipping cost of item
    ship_cost = findClass(info_container, "li", "price-ship", 0).text.split()[0].replace("$","")

    # Getting old cost of item
    old_price_li = findClass(info_container, "li", "price-was", 0).text
    old_price = total_price

    if old_price_li != "\n":
        old_price = float((old_price_li.split()[1]).replace(',',''))

    # Getting percentage saved
    percent_saved = abs(percentageDifference(total_price, old_price))

    # Print data
    print("brand: " + brand)
    print("product_name: " + title)
    print("price: " + str(total_price))
    print("old_price: " + str(old_price))
    print("percentage_saved: " + str(percent_saved) + "%")
    print("shipping: " + ship_cost)

    f.write(brand + "," + title + "," + str(total_price) + "," + str(old_price)
    + "," + str(percent_saved) + "," + ship_cost + "\n")

f.close()
