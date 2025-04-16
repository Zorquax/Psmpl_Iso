from bs4 import BeautifulSoup
import requests
import re 
import tkinter as tk

class ISO:

    def __init__(self, link):
        self.soup = None 
        self.iso = []


def getHTMLdocument(url): 
      
    response = requests.get(url) 
    return response.text 

def extract():
    users = input("Enter the users you would like to see, separated by commas: ")
    user_arr = users.split(",")
    print("You entered: ")
    for i in range(len(user_arr)):
        user_arr[i] = user_arr[i].strip()
        print(user_arr[i], end=",")
    return user_arr


def scrape(url):
    html = getHTMLdocument(url)
    soup = BeautifulSoup(html, 'html.parser') 
    all_msgs = soup.find_all("p")
    users = extract()

    output = []
    #x = re.findall(pattern, html, re.IGNORECASE)
    for msg in all_msgs: 
        text = msg.text
        poster = re.compile(fr'^\[\d\d:\d\d:\d\d\] (?:[+%*@#])?({'|'.join(user for user in users)}):\s*(.+)', re.IGNORECASE)
        if poster.match(text):
            output.append(text.replace('\xa0', ' '))

    return output

link = 'https://docs.google.com/document/d/e/2PACX-1vTTqbQh7tu9Cnu_Bvc1Halgp54WXgteBq7rw_U-KvRRVYiyyodXXwp7dWEiO4RM9S89CmsxRzC_RcmH/pub'
endarray = scrape(link)
print(endarray)

# text = "[17:19:56] motogp: I have been assigned the role of Vanilla Townie in the game of PS Mafia.I will assist in town's victory to the best of my abilities. /mafia vote Kaif☆彡Plays"
# poster = r'\[\d{2}:\d{2}:\d{2}\] (?:[+%*@#])?(\w+):\s*(.+)'
# match = re.search(poster, text)

users = ['motogp', 'creamykitty']
poster = re.compile(fr'^\[\dd:\dd:\dd\] (?:[+%*@#])?({'|'.join(user for user in users)}):\s*(.+)', re.IGNORECASE)
print(poster)