import sys
import socket
import res
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
#from serv import Server

SERVER = socket.gethostbyname(socket.gethostname())

class Server(QObject):
    clientReadyToRead = pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = 0

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {self.addr} connected.")
        connected = True
        while connected:
            msg = self.conn.recv(1024).decode('utf-8')
            self.clientReadyToRead.emit(msg)
            print(f"[{addr}] {msg}")
            if msg == " ":
                connected = False
        self.conn.close()

    def start(self):
        SERVER = socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        PORT = 5050
        self.server.bind((SERVER, PORT))
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            self.conn, self.addr = self.server.accept()
            self.thread = threading.Thread(target=self.handle_client, args=(self.conn, self.addr))
            self.thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

class AThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        self.sock = Server()
        self.sock.start()
        self.sock.clientReadyToRead.connect(self.MainWindow.onClientReadyToRead)
        return sock

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("serv.ui", self)
        self.setGeometry(100, 50, 400, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.makeServer()
        self.makeConnections()
        self.ipadd.setText(f'{SERVER}')

    def makeServer(self):
        self.aa = AThread()
        self.aa.start()

    def makeConnections(self):
        self.startButton.clicked.connect(self.onstartButtonClicked)
        self.closeButton.clicked.connect(self.close)

    def onClientReadyToRead(self, msg):
        self.messagetext.appendPlainText(msg)

    def onstartButtonClicked(self):
        self.messagetext.appendPlainText(f"[LISTENING] Server is listening on {SERVER}\n")

    def mousePressEvent(self, QMouseEvent):
        self.oldPosition = QMouseEvent.globalPos()

    def mouseMoveEvent(self, QMouseEvent):
        delta = QPoint(QMouseEvent.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = QMouseEvent.globalPos()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())