from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QStyleFactory, QDialog

import config as cfg

class C_PVSystem_ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.titleWindow = "PVSystem Settings"
        self.iconWindow = cfg.sipla_icon
        self.stylesheet = cfg.sipla_stylesheet

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.titleWindow)
        self.setWindowIcon(QIcon(self.iconWindow))  # ícone da janela
        self.setStyle(QStyleFactory.create('Cleanlooks'))  # Estilo da Interface

