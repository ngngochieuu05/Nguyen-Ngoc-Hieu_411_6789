import sys

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from protocol_navigation import attach_protocol_menu
from ui.rsa import Ui_MainWindow

API_BASE_URL = "http://127.0.0.1:5000/api"


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        attach_protocol_menu(self, "rsa")

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
        try:
            response = requests.get(f"{API_BASE_URL}/rsa/generate_keys", timeout=5)
            if response.status_code == 200:
                self.show_message(QMessageBox.Information, "Success", response.json()["message"])
            else:
                self.show_message(
                    QMessageBox.Critical,
                    "Error",
                    self.get_error_message(response, "Key generation failed!"),
                )
        except requests.RequestException as error:
            self.show_message(QMessageBox.Critical, "Error", f"API connection error: {error}")

    def call_api_encrypt(self):
        payload = {"message": self.ui.txt_plain_text.toPlainText(), "key_type": "public"}

        try:
            response = requests.post(f"{API_BASE_URL}/rsa/encrypt", json=payload, timeout=5)
            if response.status_code == 200:
                self.ui.txt_cipher_text.setText(response.json()["encrypted_message"])
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
        payload = {"ciphertext": self.ui.txt_cipher_text.toPlainText(), "key_type": "private"}

        try:
            response = requests.post(f"{API_BASE_URL}/rsa/decrypt", json=payload, timeout=5)
            if response.status_code == 200:
                self.ui.txt_plain_text.setText(response.json()["decrypted_message"])
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
        payload = {"message": self.ui.txt_info.toPlainText()}

        try:
            response = requests.post(f"{API_BASE_URL}/rsa/sign", json=payload, timeout=5)
            if response.status_code == 200:
                self.ui.txt_sign.setText(response.json()["signature"])
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
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText(),
        }

        try:
            response = requests.post(f"{API_BASE_URL}/rsa/verify", json=payload, timeout=5)
            if response.status_code == 200:
                verified = response.json()["is_verified"]
                text = "Verified Successfully" if verified else "Verified Fail"
                icon = QMessageBox.Information if verified else QMessageBox.Warning
                self.show_message(icon, "Success" if verified else "Warning", text)
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
