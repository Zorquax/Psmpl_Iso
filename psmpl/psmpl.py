from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, 
                             QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
                             QLineEdit, QTextEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt 
import requests
import re 
import sys 

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("My cool second GUI")
#         self.setGeometry(250,100,1000,800)
#         self.setWindowIcon(QIcon("virus_img.jpg"))

#         self.button = QPushButton("ISO", self)
#         self.line_edit = QLineEdit(self)

#         label2 = QLabel(self)
#         label2.setGeometry(0,0,100,100)

#         pixmap = QPixmap("virus_img.jpg")
#         label2.setPixmap(pixmap)

#         label2.setScaledContents(True)

#         label = QLabel("Hello", self)
#         label.setFont(QFont("Times New Roman", 30))
#         label.setGeometry(0, 0, 1000, 100)
#         label.setStyleSheet("color: #292929;" 
#                             "background-color: #6fdcf7;"
#                             "font-weight: bold;"
#                             "text-decoration: underline;")
        
#         label.setGeometry((self.width() - label.width()) // 2,
#                           (self.height() - label.height()),
#                           label.width(),
#                           label.height())
        
#         # label.setAlignment(Qt.AlignTop) # Vertically top
#         # label.setAlignment(Qt.AlignBottom) # Vertically bottom
#         # label.setAlignment(Qt.AlignVCenter) # Vertically center
#         # label.setAlignment(Qt.AlignRight) # Horizontally Right
#         # label.setAlignment(Qt.AlignLeft) # Horizontally left

#         label.setAlignment(Qt.AlignHCenter | Qt.AlignTop) # Blah blah

#         self.initUI()

#     def initUI(self):
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
    
#         self.button.setGeometry(150, 200, 200, 200)
#         self.button.setStyleSheet("font-size: 30px;")
#         self.button.clicked.connect(self.on_click)

#         self.line_edit.setGeometry(500, 500, 20, 40)

#     def on_click(self):
#         print("Button clicked!")
#         self.button.setText("Clicked!")

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PSMPL ISO Tool")
        self.setGeometry(400, 150, 750, 750)

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
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

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


    def compileISO(self):
        pass


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

# link = 'https://docs.google.com/document/d/e/2PACX-1vTTqbQh7tu9Cnu_Bvc1Halgp54WXgteBq7rw_U-KvRRVYiyyodXXwp7dWEiO4RM9S89CmsxRzC_RcmH/pub'
# endarray = scrape(link)
# print(endarray)

# text = "[17:19:56] motogp: I have been assigned the role of Vanilla Townie in the game of PS Mafia.I will assist in town's victory to the best of my abilities. /mafia vote Kaif☆彡Plays"
# poster = r'\[\d{2}:\d{2}:\d{2}\] (?:[+%*@#])?(\w+):\s*(.+)'
# match = re.search(poster, text)

users = ['motogp', 'creamykitty']
poster = re.compile(fr'^\[\dd:\dd:\dd\] (?:[+%*@#])?({'|'.join(user for user in users)}):\s*(.+)', re.IGNORECASE)
print(poster)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()