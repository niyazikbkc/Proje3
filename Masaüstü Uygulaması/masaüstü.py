import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QTableWidget, 
    QTableWidgetItem
)

# Veritabanı bağlantısı
def create_connection():
    connection = mysql.connector.connect(
        host="localhost",  
        user="root",      
        password="1234",  
        database="PROJE3"  
    )
    return connection

# Giriş ekranı
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Giriş")
        self.setGeometry(100, 100, 300, 200)
        
        # Kullanıcı adı ve şifre alanları
        self.username_label = QLabel("Kullanıcı Adı:")
        self.username_input = QLineEdit()
        
        self.password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Giriş butonu
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.check_login)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "1234":
            QMessageBox.information(self, "Başarılı", "Giriş Başarılı!")
            # Giriş başarılı olduğunda rehber ekranını başlat
            self.open_rehber_window()
        else:
            QMessageBox.warning(self, "Hata", "Yanlış kullanıcı adı veya şifre")

    def open_rehber_window(self):
        self.rehber_window = RehberWindow()
        self.rehber_window.show()
        self.close()

# Rehber ekranı
class RehberWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rehber Uygulaması")
        self.setGeometry(100, 100, 600, 400)
        self.connection = create_connection()
        self.init_ui()

    def init_ui(self):
        self.name_label = QLabel("Ad:")
        self.name_input = QLineEdit()

        self.phone_label = QLabel("Telefon:")
        self.phone_input = QLineEdit()

        # Ekleme, silme ve güncelleme butonları
        self.add_button = QPushButton("Ekle")
        self.add_button.clicked.connect(self.add_person)

        self.delete_button = QPushButton("Sil")
        self.delete_button.clicked.connect(self.delete_person)

        self.update_button = QPushButton("Güncelle")
        self.update_button.clicked.connect(self.update_person)

        # Kişileri listeleme alanı
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Ad", "Telefon"])
        self.load_data()

        # Layout
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.phone_label)
        form_layout.addWidget(self.phone_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.update_button)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)

        self.setLayout(layout)

    # Veritabanından veri yükleme
    def load_data(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, phone FROM rehber")
        rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            self.table.setItem(row_idx, 0, QTableWidgetItem(row_data[0]))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data[1]))

    # Kişi ekleme
    def add_person(self):
        name = self.name_input.text()
        phone = self.phone_input.text()

        if name and phone:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO rehber (name, phone) VALUES (%s, %s)", (name, phone))
            self.connection.commit()
            QMessageBox.information(self, "Başarılı", "Kişi Eklendi!")
            self.load_data()
        else:
            QMessageBox.warning(self, "Hata", "Ad ve Telefon alanları boş olamaz.")

    # Kişi silme
    def delete_person(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            name = self.table.item(selected_row, 0).text()

            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM rehber WHERE name=%s", (name,))
            self.connection.commit()
            QMessageBox.information(self, "Başarılı", "Kişi Silindi!")
            self.load_data()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen silmek için bir kişi seçin.")

    # Kişi güncelleme
    def update_person(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            name = self.table.item(selected_row, 0).text()
            new_name = self.name_input.text()
            new_phone = self.phone_input.text()

            if new_name and new_phone:
                cursor = self.connection.cursor()
                cursor.execute("UPDATE rehber SET name=%s, phone=%s WHERE name=%s", (new_name, new_phone, name))
                self.connection.commit()
                QMessageBox.information(self, "Başarılı", "Kişi Güncellendi!")
                self.load_data()
            else:
                QMessageBox.warning(self, "Hata", "Ad ve Telefon alanları boş olamaz.")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen güncellemek için bir kişi seçin.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
