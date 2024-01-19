import sqlite3
from MainProject import kategorilerVeAdetleri, linkYorumAdetYildiz, yorumlarDizisi, markaListesi

conn = sqlite3.connect('Python_Projem.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS "Kategori" (
	"kategori_id"	INTEGER,
	"kategori_adi"	TEXT NOT NULL,
	PRIMARY KEY("kategori_id" AUTOINCREMENT)
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS "Urun" (
	"urun_id"	INTEGER,
	"urun_adi"	TEXT NOT NULL,
	"urun_linki" TEXT NOT NULL,
	"urun_yorum_adet" INTEGER,
	"urun_ort_yildiz"	REAL,
	PRIMARY KEY("urun_id" AUTOINCREMENT)
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS "Marka" (
	"marka_id"	INTEGER,
	"marka_adi"	TEXT NOT NULL,
	PRIMARY KEY("marka_id" AUTOINCREMENT)
);
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS "Yorum" (
	"yorum_id"	INTEGER,
	"urun_id"	INTEGER,
	"yorum_metni"	TEXT,
	"yildiz"	REAL,
	"tarih"	TEXT,
	PRIMARY KEY("yorum_id" AUTOINCREMENT)
    );
""")
conn.commit()


for i,item in enumerate(markaListesi):
    cursor.execute(f"INSERT INTO Marka (marka_adi) VALUES ('{item}')")
conn.commit()
for i,item in enumerate(kategorilerVeAdetleri):
    cursor.execute(f"INSERT INTO Kategori (kategori_adi) VALUES ('{item[0]}')")
conn.commit()
for i,item in enumerate(linkYorumAdetYildiz):
    cursor.execute(f"INSERT INTO Urun (urun_adi,urun_linki,urun_yorum_adet,urun_ort_yildiz) VALUES ('{item[1]}','{item[0]}',{item[2]},{item[3]})")
for i, yorumlarYildizlarTarihleri in enumerate(yorumlarDizisi):
    for yorum in yorumlarYildizlarTarihleri:
        urun_id = i + 1  # Ürünlerin indeksi 1'den başladığı için
        cursor.execute('INSERT INTO yorum (urun_id,yorum_metni,yildiz,tarih) VALUES (?, ?, ?, ?)',(urun_id,yorum[0],yorum[1],yorum[2]))
        conn.commit()

conn.commit()
conn.close()
