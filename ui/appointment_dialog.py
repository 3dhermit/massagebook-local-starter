from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QDateTimeEdit, QTextEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import QDateTime
from database.models import Client, Service, Appointment
from core.scheduler import book_appointment, check_availability
from datetime import datetime, timedelta

class AppointmentDialog(QDialog):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Book Appointment")
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout(self)
        
        # Client selection
        layout.addWidget(QLabel("Client*"))
        self.client_combo = QComboBox()
        clients = self.session.query(Client).order_by(Client.last_name).all()
        for c in clients:
            self.client_combo.addItem(f"{c.last_name}, {c.first_name} (ID: {c.id})", c.id)
        layout.addWidget(self.client_combo)
        
        # Service
        layout.addWidget(QLabel("Service*"))
        self.service_combo = QComboBox()
        services = self.session.query(Service).all()
        for s in services:
            self.service_combo.addItem(f"{s.name} ({s.duration_minutes} min) - ${s.price:.2f}", s.id)
        layout.addWidget(self.service_combo)
        
        # Date/Time
        layout.addWidget(QLabel("Start Time*"))
        self.start_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.start_edit.setCalendarPopup(True)
        layout.addWidget(self.start_edit)
        
        layout.addWidget(QLabel("Duration (minutes)"))
        self.duration_combo = QComboBox()
        self.duration_combo.addItems(["30", "45", "60", "90", "120"])
        self.duration_combo.setCurrentText("60")
        layout.addWidget(self.duration_combo)
        
        # Notes
        layout.addWidget(QLabel("Notes"))
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(60)
        layout.addWidget(self.notes_edit)
        
        # Buttons
        btn_layout = QHBoxLayout()
        book_btn = QPushButton("Book Appointment")
        book_btn.clicked.connect(self.book)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(book_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def book(self):
        client_id = self.client_combo.currentData()
        service_id = self.service_combo.currentData()
        start = self.start_edit.dateTime().toPython()
        duration = int(self.duration_combo.currentText())
        end = start + timedelta(minutes=duration)
        notes = self.notes_edit.toPlainText()
        
        try:
            appt = book_appointment(self.session, client_id, service_id, start, end, notes)
            QMessageBox.information(self, "Success", f"Appointment booked for {start.strftime('%Y-%m-%d %H:%M')}")
            self.accept()
        except ValueError as ve:
            QMessageBox.warning(self, "Conflict", str(ve))
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", f"Booking failed: {str(e)}")