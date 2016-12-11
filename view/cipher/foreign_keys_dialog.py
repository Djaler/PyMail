from qtpy.QtWidgets import *

from utils import clear_layout
from view.base_view import BaseView


class ForeignKeysDialog(QDialog, BaseView):
    def __init__(self, controller):
        super().__init__(controller=controller)
        
        self._init_ui()
    
    def _init_ui(self):
        main_layout = QVBoxLayout()
        self._form_layout = QFormLayout()
        main_layout.addLayout(self._form_layout)
        
        import_btn = QPushButton("Импортировать ключ")
        import_btn.pressed.connect(self._controller.import_)
        main_layout.addWidget(import_btn)
        
        self._controller.load_keys()
        self.setLayout(main_layout)
        self.setMinimumWidth(300)
        self.setWindowTitle('Пары ключей')
        self.setModal(True)
        self.show()
        self._center()
    
    def set_rows(self, rows):
        clear_layout(self._form_layout)
        
        for address in rows:
            export_btn = QPushButton("Экспортировать ключ")
            export_btn.setProperty("address", address)
            export_btn.pressed.connect(self._controller.export)
            self._form_layout.addRow(address, export_btn)
        
        self._center()
    
    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
