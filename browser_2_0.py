import sys
import socket
import platform
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QStatusBar, QToolBar, QAction

class SystemInfoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.computer_name = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.computer_name)
        self.os_details = platform.system() + " " + platform.release()

        
        self.initUI()

    def initUI(self):
     
        self.setWindowTitle("AnBrowser 2.0")
        self.setFixedSize(300, 250) 

        self.computer_name_label = QLabel(f"Sys Name: {self.computer_name}")
        self.ip_address_label = QLabel(f"IPv4: {self.ip_address}")
        self.os_details_label = QLabel(f"OS: {self.os_details}")

        label_style = "font-weight: bold; letter-spacing: 2px;"
        self.computer_name_label.setStyleSheet(label_style)
        self.ip_address_label.setStyleSheet(label_style)
        self.os_details_label.setStyleSheet(label_style)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP address here")
        self.ip_input.setText("192.168.1.33")  
        self.ip_input.setStyleSheet("font-weight: bold; letter-spacing: 2px;")

        self.launch_button = QPushButton("Launch")
        self.launch_button.setStyleSheet("font-weight: bold; background-color: green; color: white; padding: 10px;")
        self.launch_button.clicked.connect(self.launch_action) 

        self.shutdown_button = QPushButton("Shutdown")
        self.shutdown_button.setStyleSheet("font-weight: bold; background-color: red; color: white; padding: 10px;")
        self.shutdown_button.clicked.connect(self.shutdown_action)

        self.footer_label = QLabel("Designed & Developed By Anish R. | Version 2.0")
        self.footer_label.setStyleSheet("font-weight: bold; color: gray;")
        self.footer_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)  

        layout.addWidget(self.computer_name_label)
        layout.addWidget(self.ip_address_label)
        layout.addWidget(self.os_details_label)

        layout.addWidget(self.ip_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch() 
        button_layout.addWidget(self.launch_button)
        button_layout.addWidget(self.shutdown_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        layout.setSpacing(25)

        layout.addWidget(self.footer_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def launch_action(self):

        entered_ip = self.ip_input.text()
        if entered_ip:
            #print(f"Launching browser with IP address: {entered_ip}")
            self.open_browser(entered_ip)  
        else:
            print("No IP address entered.")

    def shutdown_action(self):
        print("Shutting down the application")
        QApplication.quit()

    def open_browser(self, server_ip):

        self.browser_window = BrowserWindow(server_ip)
        self.browser_window.show()


class BrowserWindow(QMainWindow):
    def __init__(self, server_ip, *args, **kwargs):
        super(BrowserWindow, self).__init__(*args, **kwargs)

        self.server_ip = server_ip
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(f"http://{self.server_ip}/onlineexam/"))
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)
        self.setCentralWidget(self.browser)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        self.menuBar().setHidden(True)  
        navtb.setHidden(True) 
        self.urlbar.setHidden(True) 

        self.showFullScreen() 

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(f"{title} - Online Exam")

    def navigate_home(self):
        self.browser.setUrl(QUrl(f"http://{self.server_ip}/onlineexam/"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SystemInfoApp()
    
    window.show()

    sys.exit(app.exec_())
