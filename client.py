import sys
import socket
import res
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5 import uic
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class myclass(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        loadUi('client.ui', self)
        self.setGeometry(700, 50, 400, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.connectButton.clicked.connect(self.connectServer)
        self.sendButton.clicked.connect(self.onsend)
        self.closeButton.clicked.connect(self.close)

    def connectServer(self):
        SERVER = self.ipBox.toPlainText()
        ADDR = (SERVER, PORT)
        client.connect(ADDR)
        self.chatBox.insertPlainText(f'[CONNECTED] connect with {SERVER}\n')

    def onsend(self):
        msg = self.sendtext.toPlainText()
        message = msg.encode(FORMAT)
        #msg_length = len(message)
        #send_length = str(msg_length).encode(FORMAT)
        #send_length += b' ' * (HEADER - len(send_length))
        #client.send(send_length)
        client.send(message)
        #feedback = client.recv(2048).decode(FORMAT)
        self.sendtext.clear()
        self.chatBox.insertPlainText(f'sent : {msg}\n')

    def mousePressEvent(self, QMouseEvent):
        self.oldPosition = QMouseEvent.globalPos()

    def mouseMoveEvent(self, QMouseEvent):
        delta = QPoint(QMouseEvent.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = QMouseEvent.globalPos()


app = QApplication(sys.argv)
widget = myclass()
widget.show()
sys.exit(app.exec_())
#soc.close()