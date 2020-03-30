import requests
from bs4 import BeautifulSoup

url = "https://finance.yahoo.com/quote/AMZN/balance-sheet?p=AMZN"
page = requests.get(url)

page_content = page.content

soup = BeautifulSoup(page_content,'html.parser')

tabl = soup.find_all({'table':})