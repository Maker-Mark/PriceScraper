import requests
import smtplib
import os
import time
from bs4 import BeautifulSoup
from smtplib import SMTPException
from dotenv import load_dotenv
load_dotenv()
##Bring in environment variables 
email = os.getenv('LOGIN_EMAIL')
password = os.getenv('GENERATED_PW')
email_from = os.getenv('FROM_EMAIL')
to_email = os.getenv('TO_EMAIL')
##Using amazon.de, it seems as if amazon.com is not allowing this method of scraping.
URL = 'https://www.amazon.de/Chemex-Drip-Coffee-Maker-Cup/dp/B004BEQFVY/ref=sr_1_5?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=coffee&qid=1561565539&s=gateway&sr=8-5'

headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

def check_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id="productTitle").get_text().strip()
    price = float(soup.find(id="priceblock_ourprice").get_text().strip()[0:2]) #Shriks price and converts into float
    if(price < 50):
         send_mail()
    print(price)

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, password)
    subject = "Price is DOWN!"
    body = "Check out the link! https://www.amazon.de/Chemex-Drip-Coffee-Maker-Cup/dp/B004BEQFVY/ref=sr_1_5?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=coffee&qid=1561565539&s=gateway&sr=8-5"
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        email_from, to_email, msg
    )
    print("MSG SENT")
    server.quit()

#Set to check the price every 40k seconds (roughly 12 hours)
while(True):
    check_price()
    time.sleep(43200)
