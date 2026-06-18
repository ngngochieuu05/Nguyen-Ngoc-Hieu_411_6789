import sys
from PyQt5 import QtWidgets
from ui.transposition import Ui_MainWindow
from transposition_cipher import encrypt, decrypt


class TranspositionWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_en.clicked.connect(self.on_encrypt)
        self.ui.btn_de.clicked.connect(self.on_decrypt)
        self.ui.btn_clear.clicked.connect(self.clear_all)
        # compatibility attributes to mirror ex01's API names
        # ex01 expects widgets named input_text, output_text, key_entry and methods encrypt_text/decrypt_text
        self.input_text = self.ui.txt_plain
        self.output_text = self.ui.txt_cipher
        self.key_entry = self.ui.txt_key
        self.status_label = self.ui.status_label

    def on_encrypt(self):
        plain = self.ui.txt_plain.toPlainText()
        key = self.ui.txt_key.text()
        try:
            ct = encrypt(plain, key)
            self.ui.txt_cipher.setPlainText(ct)
            self.ui.status_label.setText(f"✓ Encrypted")
        except Exception as e:
            self.show_output(f"Error: {e}")

    def on_decrypt(self):
        ct = self.ui.txt_cipher.toPlainText()
        key = self.ui.txt_key.text()
        try:
            pt = decrypt(ct, key)
            self.ui.txt_plain.setPlainText(pt)
            self.ui.status_label.setText(f"✓ Decrypted")
        except Exception as e:
            self.show_output(f"Error: {e}")

    def show_output(self, message: str):
        # show message in output area for errors; update status label
        try:
            self.output_text.setPlainText(message)
        except Exception:
            # fallback
            self.ui.txt_cipher.setPlainText(message)
        self.status_label.setText("Error")

    # Methods named to match ex01's API
    def encrypt_text(self):
        # called by ex01-style integrations
        self.on_encrypt()

    def decrypt_text(self):
        self.on_decrypt()

    def clear_all(self):
        self.ui.txt_plain.clear()
        self.ui.txt_cipher.clear()
        self.ui.txt_key.clear()
        self.ui.status_label.setText("Cleared")


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = TranspositionWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
