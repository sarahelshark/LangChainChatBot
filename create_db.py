import sqlite3

# Creazione del database e della tabella prodotti
conn = sqlite3.connect('fakeEcommerce.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        price NUMERIC(10, 2),
        image_url TEXT
    )
''')
# Inserimento di alcuni prodotti di esempio
products = [
    ('Laptop', 'Un potente laptop con 16GB di RAM e 512GB SSD.', 1200.00, 'https://via.placeholder.com/150'),
    ('Smartphone', 'Un moderno smartphone con una fotocamera eccellente.', 800.00, 'https://via.placeholder.com/150'),
    ('Cuffie', 'Cuffie wireless con cancellazione del rumore.', 200.00, 'https://via.placeholder.com/150'),
    ('Tablet', 'Tablet con display da 10 pollici e 64GB di memoria.', 300.00, 'https://via.placeholder.com/150'),
    ('Smartwatch', 'Smartwatch con monitoraggio della frequenza cardiaca.', 150.00, 'https://via.placeholder.com/150'),
    ('Televisore', 'Televisore 4K da 55 pollici.', 600.00, 'https://via.placeholder.com/150'),
    ('Fotocamera', 'Fotocamera DSLR con obiettivo da 18-55mm.', 700.00, 'https://via.placeholder.com/150'),
    ('Stampante', 'Stampante multifunzione con scanner.', 120.00, 'https://via.placeholder.com/150'),
    ('Mouse', 'Mouse wireless ergonomico.', 25.00, 'https://via.placeholder.com/150'),
    ('Tastiera', 'Tastiera meccanica retroilluminata.', 80.00, 'https://via.placeholder.com/150'),
    ('Monitor', 'Monitor da 24 pollici Full HD.', 180.00, 'https://via.placeholder.com/150'),
    ('Altoparlanti', 'Altoparlanti Bluetooth portatili.', 60.00, 'https://via.placeholder.com/150'),
    ('Router', 'Router Wi-Fi dual band.', 90.00, 'https://via.placeholder.com/150'),
    ('Hard Disk Esterno', 'Hard disk esterno da 1TB.', 70.00, 'https://via.placeholder.com/150'),
    ('SSD', 'SSD da 500GB.', 100.00, 'https://via.placeholder.com/150'),
    ('Chiavetta USB', 'Chiavetta USB da 32GB.', 15.00, 'https://via.placeholder.com/150'),
    ('Scheda di Memoria', 'Scheda di memoria SD da 64GB.', 20.00, 'https://via.placeholder.com/150'),
    ('Caricatore Portatile', 'Caricatore portatile da 10000mAh.', 35.00, 'https://via.placeholder.com/150'),
    ('Adattatore USB-C', 'Adattatore da USB-C a HDMI.', 25.00, 'https://via.placeholder.com/150'),
    ('Cavo HDMI', 'Cavo HDMI da 2 metri.', 10.00, 'https://via.placeholder.com/150'),
    ('Microfono', 'Microfono a condensatore per registrazioni.', 90.00, 'https://via.placeholder.com/150'),
    ('Webcam', 'Webcam Full HD con microfono integrato.', 50.00, 'https://via.placeholder.com/150'),
    ('Cuffie da Gioco', 'Cuffie da gioco con microfono.', 70.00, 'https://via.placeholder.com/150')
]
cursor.executemany('INSERT INTO products (name, description, price, image_url) VALUES (?, ?, ?, ?)', products)
conn.commit()
conn.close()
