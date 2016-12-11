from qtpy.QtWidgets import *

from utils import clear_layout
from view.base_view import BaseView


class KeyPairsDialog(QDialog, BaseView):
    def __init__(self, controller):
        super().__init__(controller=controller)
        
        self._init_ui()
    
    def _init_ui(self):
        main_layout = QVBoxLayout()
        self._grid_layout = QGridLayout()
        main_layout.addLayout(self._grid_layout)
        
        generate_pair_btn = QPushButton("Сгенерировать новую пару")
        generate_pair_btn.pressed.connect(self._controller.create_key_pair)
        main_layout.addWidget(generate_pair_btn)
        
        self._controller.load_keys()
        self.setLayout(main_layout)
        self.setMinimumWidth(300)
        self.setWindowTitle('Пары ключей')
        self.setModal(True)
        self.show()
        self._center()
    
    def set_rows(self, rows):
        clear_layout(self._grid_layout)
        
        for index, address in enumerate(rows):
            self._grid_layout.addWidget(QLabel(address), index, 0)
            export_public_btn = QPushButton("Экспортировать публичный ключ")
            export_public_btn.setProperty("address", address)
            export_public_btn.pressed.connect(self._controller.export_public)
            self._grid_layout.addWidget(export_public_btn, index, 1)
            export_private_btn = QPushButton("Экспортировать приватный ключ")
            export_private_btn.setProperty("address", address)
            export_private_btn.pressed.connect(self._controller.export_private)
            self._grid_layout.addWidget(export_private_btn, index, 2)
        
        self._center()
    
    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
