import sys

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from protocol_navigation import attach_protocol_menu
from ui.ecc import Ui_MainWindow

API_BASE_URL = "http://127.0.0.1:5000/api"


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        attach_protocol_menu(self, "ecc")

        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

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

    def call_api_gen_keys(self):
        url = f"{API_BASE_URL}/ecc/generate_keys"

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.show_message(QMessageBox.Information, "Success", data["message"])
            else:
                self.show_message(
                    QMessageBox.Critical,
                    "Error",
                    self.get_error_message(response, "Key generation failed!"),
                )
        except requests.RequestException as error:
            self.show_message(QMessageBox.Critical, "Error", f"API connection error: {error}")

    def call_api_encrypt(self):
        url = f"{API_BASE_URL}/ecc/encrypt"
        payload = {
            "message": self.ui.txt_plain_text.toPlainText(),
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data["encrypted_message"])
                self.show_message(QMessageBox.Information, "Success", "Encrypted Successfully")
            else:
                self.show_message(
                    QMessageBox.Critical,
                    "Error",
                    self.get_error_message(response, "Encryption failed!"),
                )
        except requests.RequestException as error:
            self.show_message(QMessageBox.Critical, "Error", f"API connection error: {error}")

    def call_api_decrypt(self):
        url = f"{API_BASE_URL}/ecc/decrypt"
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setText(data["decrypted_message"])
                self.show_message(QMessageBox.Information, "Success", "Decrypted Successfully")
            else:
                self.show_message(
                    QMessageBox.Critical,
                    "Error",
                    self.get_error_message(response, "Decryption failed!"),
                )
        except requests.RequestException as error:
            self.show_message(QMessageBox.Critical, "Error", f"API connection error: {error}")

    def call_api_sign(self):
        url = f"{API_BASE_URL}/ecc/sign"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setText(data["signature"])
                self.show_message(QMessageBox.Information, "Success", "Signed Successfully")
            else:
                self.show_message(
                    QMessageBox.Critical,
                    "Error",
                    self.get_error_message(response, "Sign failed!"),
                )
        except requests.RequestException as error:
            self.show_message(QMessageBox.Critical, "Error", f"API connection error: {error}")

    def call_api_verify(self):
        url = f"{API_BASE_URL}/ecc/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText(),
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data["is_verified"]:
                    self.show_message(QMessageBox.Information, "Success", "Verified Successfully")
                else:
                    self.show_message(QMessageBox.Warning, "Warning", "Verified Fail")
            else:
                self.show_message(
                    QMessageBox.Critical,
                    "Error",
                    self.get_error_message(response, "Verify failed!"),
                )
        except requests.RequestException as error:
            self.show_message(QMessageBox.Critical, "Error", f"API connection error: {error}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
