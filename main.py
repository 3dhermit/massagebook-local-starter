import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from ui.main_window import MainWindow
from core.auth import authenticate, create_user
from database.db import init_db

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - MassageBook Starter")
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Username"))
        self.username_edit = QLineEdit()
        layout.addWidget(self.username_edit)
        
        layout.addWidget(QLabel("Password"))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_edit)
        
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.try_login)
        layout.addWidget(login_btn)
        
        # Hint for first run
        layout.addWidget(QLabel("Default: admin / admin123"))

    def try_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Login", "Please enter username and password.")
            return
        
        user = authenticate(username, password)
        if user:
            self.user = user
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials. Try admin/admin123 on first run.")

def main():
    app = QApplication(sys.argv)
    init_db()
    
    login = LoginDialog()
    if login.exec() == QDialog.Accepted:
        window = MainWindow(login.user)
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()