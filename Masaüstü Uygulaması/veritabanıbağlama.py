import mysql.connector
try:
    bağlantı = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "1234"
    )
    print("Veri Tabanına Bağlandı")
except:
      print("Veri Tabanına Bağlanılamadı")