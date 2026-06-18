from PyQt5.QtWidgets import QAction


def _open_protocol_window(current_window, protocol_name):
    window_class = get_protocol_window_class(protocol_name)
    next_window = window_class()
    next_window.show()
    current_window._next_window = next_window
    current_window.close()


def get_protocol_window_class(protocol_name):
    if protocol_name == "menu":
        from main_menu import MainMenuWindow

        return MainMenuWindow
    if protocol_name == "caesar":
        from caesar_cipher import MyApp as CaesarWindow

        return CaesarWindow
    if protocol_name == "rsa":
        from rsa_cipher import MyApp as RSAWindow

        return RSAWindow
    if protocol_name == "ecc":
        from ecc_cipher import MyApp as ECCWindow

        return ECCWindow
    raise ValueError(f"Unsupported protocol: {protocol_name}")


def attach_protocol_menu(window, current_protocol):
    protocol_menu = window.menuBar().addMenu("Protocol")
    labels = [
        ("menu", "Main Menu"),
        ("rsa", "RSA"),
        ("ecc", "ECC"),
    ]

    for protocol_name, label in labels:
        action = QAction(label, window)
        action.setCheckable(True)
        action.setChecked(protocol_name == current_protocol)
        action.triggered.connect(
            lambda checked=False, name=protocol_name: _open_protocol_window(window, name)
            if name != current_protocol
            else None
        )
        protocol_menu.addAction(action)
