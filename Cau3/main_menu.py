import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

from protocol_navigation import attach_protocol_menu, get_protocol_window_class


class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainMenuWindow")
        self.resize(860, 520)
        self.setMinimumSize(860, 520)
        self.setWindowTitle("Cipher Protocol Menu")

        attach_protocol_menu(self, "menu")

        self.btn_rsa = QPushButton("RSA", self)
        self.btn_rsa.setGeometry(220, 200, 420, 48)
        self.btn_rsa.clicked.connect(lambda: self.open_protocol("rsa"))

        self.btn_ecc = QPushButton("ECC", self)
        self.btn_ecc.setGeometry(220, 280, 420, 48)
        self.btn_ecc.clicked.connect(lambda: self.open_protocol("ecc"))

    def open_protocol(self, protocol_name):
        window_class = get_protocol_window_class(protocol_name)
        next_window = window_class()
        next_window.show()
        self._next_window = next_window
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenuWindow()
    window.show()
    sys.exit(app.exec_())
