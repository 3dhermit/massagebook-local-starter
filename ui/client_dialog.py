from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTextEdit, QMessageBox
)
from database.models import Client
from datetime import datetime

class ClientDialog(QDialog):
    def __init__(self, session, client=None):
        super().__init__()
        self.session = session
        self.client = client
        self.setWindowTitle("Add/Edit Client")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Form fields
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.email = QLineEdit()
        self.phone = QLineEdit()
        self.address = QTextEdit()
        self.address.setMaximumHeight(80)
        
        layout.addWidget(QLabel("First Name*"))
        layout.addWidget(self.first_name)
        layout.addWidget(QLabel("Last Name*"))
        layout.addWidget(self.last_name)
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email)
        layout.addWidget(QLabel("Phone"))
        layout.addWidget(self.phone)
        layout.addWidget(QLabel("Address / Notes"))
        layout.addWidget(self.address)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_client)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        if client:
            self.populate_fields()

    def populate_fields(self):
        self.first_name.setText(self.client.first_name)
        self.last_name.setText(self.client.last_name)
        self.email.setText(self.client.email or '')
        self.phone.setText(self.client.phone or '')
        self.address.setPlainText(self.client.notes or '')

    def save_client(self):
        if not self.first_name.text() or not self.last_name.text():
            QMessageBox.warning(self, "Validation", "First and Last name are required.")
            return
        
        if self.client:  # Edit
            self.client.first_name = self.first_name.text()
            self.client.last_name = self.last_name.text()
            self.client.email = self.email.text() or None
            self.client.phone = self.phone.text() or None
            self.client.notes = self.address.toPlainText() or None
        else:  # New
            new_client = Client(
                first_name=self.first_name.text(),
                last_name=self.last_name.text(),
                email=self.email.text() or None,
                phone=self.phone.text() or None,
                notes=self.address.toPlainText() or None
            )
            self.session.add(new_client)
        
        try:
            self.session.commit()
            self.accept()
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to save client: {str(e)}")