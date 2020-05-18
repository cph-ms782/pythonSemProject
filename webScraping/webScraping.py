import requests
import urllib.request
import time
from bs4 import BeautifulSoup


def webscraping(): 
    url = 'https://www.ssi.dk/aktuelt/sygdomsudbrud/coronavirus/covid-19-i-danmark-epidemiologisk-overvaagningsrapport'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    list_of_A = soup.select('blockquote div a')
    link_list = []
    for link in list_of_A:
        link_list.append(link.get('href'))
    return link_list

print(webscraping())


