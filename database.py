import sqlite3

db = sqlite3.connect('weather.db')

cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weathers(
        weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temp TEXT,
        status TEXT,
        sunrise TEXT, 
        sunset TEXT
    );

''')
db.commit()
db.close()
