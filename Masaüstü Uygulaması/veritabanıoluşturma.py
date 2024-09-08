import mysql.connector
from mysql.connector import Error

try:
    # Veritabanı bağlantısını oluşturma
    VeriTabani1 = mysql.connector.connect(
        host="localhost",   # Default olarak 'localhost'
        user="root",        # MySQL kullanıcı adı
        password="1234"     # MySQL WorkBench kurarken belirlediğiniz şifre
    )

    if VeriTabani1.is_connected():
        # Cursor oluşturma ve veritabanı yaratma komutu
        secilenVT = VeriTabani1.cursor()

        # PROJE3 veritabanını oluşturma
        secilenVT.execute("CREATE DATABASE IF NOT EXISTS PROJE3")
        print("PROJE3 veritabanı başarıyla oluşturuldu veya zaten mevcut.")

        # PROJE3 veritabanını seçme
        secilenVT.execute("USE PROJE3")

        # rehber tablosunu oluşturma
        secilenVT.execute("""
            CREATE TABLE IF NOT EXISTS rehber (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(15) NOT NULL
            )
        """)
        print("rehber tablosu başarıyla oluşturuldu veya zaten mevcut.")
    
except Error as e:
    # Hata durumunda hatayı yazdırma
    print("İşlem sırasında bir hata oluştu:", e)

finally:
    # Veritabanı bağlantısını kapatma
    if VeriTabani1.is_connected():
        secilenVT.close()
        VeriTabani1.close()
        print("Veritabanı bağlantısı kapatıldı.")

