from qtpy.QtWidgets import *

from utils import clear_layout
from view import BaseView


class ForeignKeysDialog(QDialog, BaseView):
    def __init__(self, controller):
        super().__init__(controller=controller)
        
        self._init_ui()
    
    def _init_ui(self):
        main_layout = QVBoxLayout()
        self._grid_layout = QGridLayout()
        main_layout.addLayout(self._grid_layout)
        
        import_btn = QPushButton("Импортировать ключ")
        import_btn.pressed.connect(self._controller.import_)
        main_layout.addWidget(import_btn)
        
        self._controller.load_keys()
        self.setLayout(main_layout)
        self.setMinimumWidth(300)
        self.setWindowTitle('Импортированные ключи')
        self.setModal(True)
        self.show()
        self._center()
    
    def set_rows(self, rows):
        clear_layout(self._grid_layout)
    
        for index, address in enumerate(rows):
            self._grid_layout.addWidget(QLabel(address), index, 0)
            export_btn = QPushButton("Экспортировать ключ")
            export_btn.setProperty("address", address)
            export_btn.pressed.connect(self._controller.export)
            self._grid_layout.addWidget(export_btn, index, 1)
        
            delete_btn = QPushButton("Удалить")
            delete_btn.setProperty("address", address)
            delete_btn.pressed.connect(self._controller.delete)
            self._grid_layout.addWidget(delete_btn, index, 2)
        
        self._center()
    
    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
