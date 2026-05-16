from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTableView, QTabWidget, QLabel, QLineEdit, QMessageBox, QMenuBar,
    QStatusBar, QFileDialog
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QAction
from database.db import get_session, init_db, backup_database
from database.models import Client, Appointment, Service
from datetime import datetime
import os

from .client_dialog import ClientDialog
from .appointment_dialog import AppointmentDialog

class ClientsTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self.headers = ['ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Created']

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = self._data[index.row()]
            col = index.column()
            if col == 0: return row.id
            if col == 1: return row.first_name
            if col == 2: return row.last_name
            if col == 3: return row.email or ''
            if col == 4: return row.phone or ''
            if col == 5: return row.created_at.strftime('%Y-%m-%d') if row.created_at else ''
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle(f"MassageBook Starter - {user.username}")
        self.setGeometry(100, 100, 1200, 800)
        
        init_db()
        self.session = get_session()
        
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        backup_action = QAction("Backup Database", self)
        backup_action.triggered.connect(self.backup_db)
        file_menu.addAction(backup_action)
        
        export_menu = menubar.addMenu("Export")
        export_clients = QAction("Export Clients (CSV)", self)
        export_clients.triggered.connect(self.export_clients)
        export_menu.addAction(export_clients)
        
        export_appts = QAction("Export Appointments (CSV)", self)
        export_appts.triggered.connect(self.export_appointments)
        export_menu.addAction(export_appts)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Dashboard Tab
        dash = QWidget()
        dash_layout = QVBoxLayout(dash)
        dash_layout.addWidget(QLabel(f"Welcome, {self.user.username}! Role: {self.user.role}"))
        dash_layout.addWidget(QLabel("Quick Stats: Use tabs below to manage clients and schedule."))
        self.tabs.addTab(dash, "Dashboard")

        # Clients Tab
        clients_tab = QWidget()
        clients_layout = QVBoxLayout(clients_tab)
        
        clients_toolbar = QHBoxLayout()
        self.add_client_btn = QPushButton("Add Client")
        self.add_client_btn.clicked.connect(self.add_client)
        clients_toolbar.addWidget(self.add_client_btn)
        clients_toolbar.addStretch()
        clients_layout.addLayout(clients_toolbar)
        
        self.clients_table = QTableView()
        clients_layout.addWidget(self.clients_table)
        self.tabs.addTab(clients_tab, "Clients")

        # Schedule Tab
        schedule_tab = QWidget()
        schedule_layout = QVBoxLayout(schedule_tab)
        schedule_toolbar = QHBoxLayout()
        self.book_btn = QPushButton("Book Appointment")
        self.book_btn.clicked.connect(self.book_appointment)
        schedule_toolbar.addWidget(self.book_btn)
        schedule_toolbar.addStretch()
        schedule_layout.addLayout(schedule_toolbar)
        
        self.schedule_table = QTableView()
        schedule_layout.addWidget(self.schedule_table)
        self.tabs.addTab(schedule_tab, "Schedule")

        # Status bar
        self.statusBar().showMessage("Ready. Database initialized.")

    def _load_data(self):
        # Load clients
        clients = self.session.query(Client).order_by(Client.last_name).all()
        self.clients_model = ClientsTableModel(clients)
        self.clients_table.setModel(self.clients_model)
        
        # Load appointments (simple view)
        appts = self.session.query(Appointment).order_by(Appointment.start_time.desc()).limit(50).all()
        # For simplicity, use a basic model or reuse/adapt
        self.appt_data = appts
        # TODO: Create proper AppointmentTableModel similar to ClientsTableModel

    def add_client(self):
        dialog = ClientDialog(self.session)
        if dialog.exec():
            self._load_data()  # Refresh
            self.statusBar().showMessage("Client added successfully.")

    def book_appointment(self):
        dialog = AppointmentDialog(self.session)
        if dialog.exec():
            self._load_data()
            self.statusBar().showMessage("Appointment booked.")

    def backup_db(self):
        try:
            path = backup_database()
            QMessageBox.information(self, "Backup Complete", f"Database backed up to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Backup Failed", str(e))

    def export_clients(self):
        from utils.export import export_clients_csv
        try:
            path = export_clients_csv()
            QMessageBox.information(self, "Export Complete", f"Clients exported to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))

    def export_appointments(self):
        from utils.export import export_appointments_csv
        try:
            path = export_appointments_csv()
            QMessageBox.information(self, "Export Complete", f"Appointments exported to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))

    def closeEvent(self, event):
        self.session.close()
        event.accept()