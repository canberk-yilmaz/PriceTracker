#Importing Libraries
import requests
from bs4 import BeautifulSoup
import smtplib
import time
from datetime import datetime
#adding URL links
URL1 = "https://www.epey.com/akilli-telefonlar/apple-iphone-11.html"
URL2 = 'https://www.epey.com/akilli-telefonlar/apple-iphone-12.html'
URL3 = 'https://www.epey.com/akilli-telefonlar/apple-iphone-12-mini.html'
UserAgent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:85.0) Gecko/20100101 Firefox/85.0"}
EMAIL_ADDRESS = "cyilmaz089@gmail.com" #use your own email address here
#defining functions
def getPrice(URL): #listing prices
    page = requests.get(URL, headers=UserAgent)
    soup = BeautifulSoup(page.content, 'html.parser')
    prices = soup.find_all(class_='urun_fiyat')
    price_list = []
    for price in prices:
        price_list.append(price.get_text().strip('\n').split(' TL')[0].replace('.', '').replace(',','.'))
    return price_list

def trackPrices(URL): #tracking minimum price
    price_list = getPrice(URL)
    minPrice = price_list[0]
    for price in price_list:
        if price < minPrice:
            minPrice = price
    return float(minPrice.strip(''))

def sendEmail(): #email sending function
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_ADDRESS, 'temporary_password') #use your own password here
    server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, mailtext)

currentMinPrice11 = trackPrices(URL1)
currentMinPrice12 = trackPrices(URL2)
currentMinPrice12mini = trackPrices(URL3)

while True:
    if trackPrices(URL1) < currentMinPrice11:
        print('iPhone 11 got cheaper')
        currentMinPrice11 = trackPrices(URL1)
        subject = "iPhone 11 Fiyati Dustu!"
        mailtext = 'Subject:' + subject + '\n\n' + URL1
        sendEmail()

    if trackPrices(URL2) < currentMinPrice12:
        print('iphone 12 got cheaper')
        currentMinPrice12 = trackPrices(URL2)
        subject = "iPhone 12 Fiyati Dustu!"
        mailtext = 'Subject:' + subject + '\n\n' + URL2
        sendEmail()

    if trackPrices(URL3) < currentMinPrice12mini:
        print('iphone 12 mini got cheaper')
        currentMinPrice12mini = trackPrices(URL3)
        subject = "iPhone 12 mini Fiyati Dustu!"
        mailtext = 'Subject:' + subject + '\n\n' + URL3
        sendEmail()
    print(f'iPhone11: {currentMinPrice11} TL\niPhone12: {currentMinPrice12} TL\niPhone12 Mini: {currentMinPrice12mini} TL')

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    print('')
    time.sleep(75)


