import sqlite3
import pandas as pd

database_path = 'data/ShootoutRanking.db'

# Database connection
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Tables creations 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Teams (
        team_id INTEGER PRIMARY KEY AUTOINCREMENT,
        team VARCHAR(50) NOT NULL,
        tricode VARCHAR(3),
        confederation VARCHAR(10),
        startDate DATE,
        endDate DATE,
        member BOOLEAN NOT NULL,
        base INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rankings (
        ranking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        day INTEGER NOR NULL,
        team VARCHAR(50) NOT NULL,
        points INTEGER NOT NULL,
        ranking INTEGER NOT NULL
    );
''')


# Load Teams data from Excel to Table
excel_file_path = 'data/teams_db.xlsx'
df_teams = pd.read_excel(excel_file_path)
df_teams.to_sql('Teams', conn, index=False, if_exists='replace')

# Validez et fermez la connexion à la base de données
conn.commit()
conn.close()