from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QLineEdit, QTextEdit, QMessageBox)
from PyQt5.QtGui import QIcon

import requests
import re 
import sys 

cache = {}

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PSMPL ISO Tool")
        self.setGeometry(400, 150, 750, 750)
        self.setWindowIcon(QIcon("rampage.jpeg"))

        self.document = ""
        self.doc_label = QLabel(self)
        self.doc_tbox = QLineEdit(self)

        self.player_string = ""
        self.player_label = QLabel(self)
        self.player_tbox = QLineEdit(self)

        self.iso_button = QPushButton("ISO!", self)

        self.output = QTextEdit(self)

        self.initUI()

    def initUI(self):

        self.doc_label.setGeometry(35, 75, 500, 50)
        self.doc_label.setText("Enter PUBLISHED document link: ")

        self.doc_tbox.setGeometry(300, 75, 300, 50)
        self.doc_tbox.setPlaceholderText("https://docs.google.com/document/d/e/2PACX-1vTTqbQh7tu9Cnu_Bvc1Halgp54WXgteBq7rw_U-KvRRVYiyyodXXwp7dWEiO4RM9S89CmsxRzC_RcmH/pub")

        self.player_label.setGeometry(35, 150, 500, 50)
        self.player_label.setText("Enter users, separated by commas: ")
        self.player_tbox.setPlaceholderText("e.g. motogp, Kaif☆彡Plays♗, Schiavetto ♫♪♫♪")

        self.player_tbox.setGeometry(300, 150, 300, 50)

        self.iso_button.setGeometry(275, 
                                    250, 200, 75)
        self.iso_button.setStyleSheet("font-size: 30px;")

        self.output.setReadOnly(True)
        self.output.setGeometry(10, 350, 730, 350)

        self.iso_button.clicked.connect(self.compileISO)


    def compileISO(self):
        self.output.clear()
        self.document = self.doc_tbox.text()
        self.player_string = self.player_tbox.text()
        if not self.document:
            QMessageBox.warning(self, "Error", "No document selected")
            return
        if not self.player_string:
            QMessageBox.warning(self, "Error", "No player string entered")
            return 
        iso = ISO(self.document, self.player_string)
        logs = iso.scrape()

        for line in logs: 
            self.output.append(line)

class ISO:

    def __init__(self, link, player_string):
        self.soup = None 
        self.link = link
        self.player_string = player_string

        self.html = self.getHTMLdocument(link)
        if not self.html:
            raise ValueError("Failed to retrieve html document")
        if not self.extract():
            raise ValueError("No names detected?")

    def getHTMLdocument(self, url): 
        
        if url in cache: 
            return cache[url]
        response = requests.get(url) 
        cache[url] = response.text
        return cache[url]

    def extract(self):
        user_arr = self.player_string.split(",")
        for i in range(len(user_arr)):
            user_arr[i] = user_arr[i].strip()
        return user_arr


    def scrape(self):
        html = self.getHTMLdocument(self.link)
        soup = BeautifulSoup(html, 'html.parser') 
        all_msgs = soup.find_all(["p", "h3"])
        users = self.extract()

        output = []

        user_string = '|'.join(user for user in users)
        poster = re.compile(fr'^\[\d\d:\d\d:\d\d\] (?:[+%*@#^])?({user_string}):\s*(.+)', re.IGNORECASE)
        voter = re.compile(fr'^\[\d\d:\d\d:\d\d\] \|c:\|\d{{9,11}}\|~\|({user_string})', re.IGNORECASE)
        eliminated = re.compile(fr'({user_string}) was eliminated!', re.IGNORECASE)
        role = re.compile(fr'({user_string})\'s role was .*', re.IGNORECASE)

        daycheck = re.compile(r'^Day .*')

        for msg in all_msgs: 
            text = msg.text

            if poster.match(text):
                output.append(text.replace('\xa0', ' '))
            elif voter.match(text):
                output.append(re.sub(r'\|c:\|\d{9,11}\|~\|', '', text))
            elif daycheck.match(text):
                output.append("\n" + text + "\n")
            elif role.match(text):
                output.append(text)
            elif eliminated.match(text):
                output.append(text)

        return output

# link = 'https://docs.google.com/document/d/e/2PACX-1vTTqbQh7tu9Cnu_Bvc1Halgp54WXgteBq7rw_U-KvRRVYiyyodXXwp7dWEiO4RM9S89CmsxRzC_RcmH/pub'
# endarray = scrape(link)
# print(endarray)

# text = "[17:19:56] motogp: I have been assigned the role of Vanilla Townie in the game of PS Mafia.I will assist in town's victory to the best of my abilities. /mafia vote Kaif☆彡Plays"
# poster = r'\[\d{2}:\d{2}:\d{2}\] (?:[+%*@#])?(\w+):\s*(.+)'
# match = re.search(poster, text)

# users = ['motogp', 'creamykitty']
# poster = re.compile(fr'^\[\dd:\dd:\dd\] (?:[^+%*@#])?({'|'.join(user for user in users)}):\s*(.+)', re.IGNORECASE)

# msgs = ["[17:20:02] |c:|1744564802|~|CreamyKitty has voted articoo ☾.",
#         '[17:22:15] |c:|1744564935|~|motogp has shifted their vote from articoo ☾ to Aziziller',
#         '[17:20:28] Prodigu: roderickisamazing gl',
#         '[17:20:31] |c:|1744564831|~|NightEmerald has shifted their vote from roderickisamazing to DkKoba',
#         '[17:32:05] |c:|1744565525|~|CreamyKitty has voted motogp.', 
#         '[17:35:42] |c:|1744565742|~|CreamyKitty has shifted their vote from motogp to SlowthePoke',
#         '[17:38:49] |c:|1744565928|~|motogp has voted SlowthePoke.',
#         '[18:12:11] |c:|1744567931|~|motogp has shifted their vote from commander¿awesome to strateg1c',
#         '[18:28:43] |c:|1744568923|~|CreamyKitty has shifted their vote from Spiderz to roderickisamazing',
#         '[18:30:15] |c:|1744569015|~|motogp has unvoted CreamyKitty.']


# user_string = '|'.join(user for user in users)
# #voted = re.compile(fr'^\[\d\d:\d\d:\d\d\] \|c:\|\d{{9,11}}\|~\|({user_string}) has (?:un)?voted (.+)', re.IGNORECASE)
# print(user_string)
# voted = re.compile(fr'^\[\d\d:\d\d:\d\d\] \|c:\|\d{{9,11}}\|~\|({user_string})', re.IGNORECASE)
# for msg in msgs: 
#     if voted.match(msg):
#         print(re.sub(r'\|c:\|\d{9,11}\|~\|', '', msg))
#         #print(re.sub('motogp', 'clown', msg))

# shiftvoted = re.compile(fr'^\[\d\d:\d\d:\d\d\] \|c:\|\d{{9,11}}\|~\|({user_string}) has shifted their vote from (.+) to (.+)', re.IGNORECASE)
# for msg in msgs: 
#     if (b:= shiftvoted.match(msg)) != None:
#         print(b.group(1), b.group(2), b.group(3))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()