import sys

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from protocol_navigation import attach_protocol_menu
from ui.caesar import Ui_MainWindow

API_BASE_URL = "http://127.0.0.1:5000/api"


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        attach_protocol_menu(self, "caesar")
        self.ui.btn_en.clicked.connect(self.call_api_encrypt)
        self.ui.btn_de.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = f"{API_BASE_URL}/caesar/encrypt"
        payload = {
            "plain_text": self.ui.txt_banro.toPlainText(),
            "key": self.ui.txt_key.text(),
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                encrypted_text = data.get("encrypted_text", "")
                self.ui.txt_banma.setPlainText(encrypted_text)
                self.show_message(QMessageBox.Information, "Success", "Encryption successful!")
            else:
                self.show_message(
                    QMessageBox.Critical,
                    "Error",
                    self.get_error_message(response, "Encryption failed!"),
                )
        except requests.RequestException as error:
            self.show_message(QMessageBox.Critical, "Error", f"API connection error: {error}")

    def call_api_decrypt(self):
        url = f"{API_BASE_URL}/caesar/decrypt"
        payload = {
            "encrypted_text": self.ui.txt_banma.toPlainText(),
            "key": self.ui.txt_key.text(),
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                decrypted_text = data.get("decrypted_text", "")
                self.ui.txt_banro.setPlainText(decrypted_text)
                self.show_message(QMessageBox.Information, "Success", "Decryption successful!")
            else:
                self.show_message(
                    QMessageBox.Critical,
                    "Error",
                    self.get_error_message(response, "Decryption failed!"),
                )
        except requests.RequestException as error:
            self.show_message(QMessageBox.Critical, "Error", f"API connection error: {error}")

    def get_error_message(self, response, fallback):
        try:
            return response.json().get("error", fallback)
        except ValueError:
            return fallback

    def show_message(self, icon, title, text):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
