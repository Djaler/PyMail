from qtpy.QtWidgets import *

from view import BaseView


class ExportPublicDialog(QDialog, BaseView):
    def __init__(self, controller):
        super().__init__(controller=controller)
        
        self._init_ui()
    
    def _init_ui(self):
        main_layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)
        
        self._address_edit = QLineEdit()
        form_layout.addRow("Адрес собеседника:", self._address_edit)
        
        export_button = QPushButton("Экспортировать")
        export_button.pressed.connect(self._controller.export)
        main_layout.addWidget(export_button)
        
        self.setLayout(main_layout)
        self.setMinimumWidth(300)
        self.setWindowTitle('Экспорт публичного ключа')
        self.setModal(True)
        self.show()
        self._center()
    
    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    @property
    def address(self):
        return self._address_edit.text()
