import sqlite3
import json
from pathlib import Path

# SQLite database connection
database_path = "data/ShootoutRanking.db"
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

# Execute SQL query to obtain list of current years
cursor.execute("SELECT DISTINCT year FROM Rankings")
years = cursor.fetchall()

for year in years:
    year = year[0]

    # Execute SQL query to select data for current year
    cursor.execute('''
                   WITH previous_year AS (
                    SELECT r.ranking, r.team, r.points
                    FROM Rankings r
                    LEFT JOIN Teams t ON (r.team = t.team)
                    WHERE year = ? - 1 AND month = 12 AND day = 31
                   )
                    SELECT r.ranking, t.tricode || '.png' AS flag, r.team, r.points, t.confederation, (p.ranking - r.ranking) AS ranking_change, (r.points - p.points) AS points_change
                    FROM Rankings r
                    LEFT JOIN Teams t ON (r.team = t.team)
                    LEFT JOIN previous_year p ON (r.team = p.team)
                    WHERE year = ? AND month = 12 AND day = 31
                   ''', (year,year))

    # Data recovery
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    data = [dict(zip(column_names, row)) for row in rows]

    # JSON file name
    json_path = Path(f"data/json/{year}Rankings.json")

    # Check if the file already exists
    if not json_path.exists():
        # Export data to a JSON file
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=2)

        print(f"Data successfully extracted and exported to {json_path}.")
    else:
        print(f"The {json_path} file already exists. No action required.")


# Generate last date file
# Execute SQL query to select all table rows
cursor.execute('''
                WITH max_date AS (
                    SELECT MAX(date) as max_date, strftime('%Y', MAX(date)) AS year FROM Rankings
                ),
               previous_year AS (
                    SELECT r.ranking, r.team, r.points
                    FROM Rankings r
                    LEFT JOIN Teams t ON (r.team = t.team)
                    WHERE year = (SELECT year FROM max_date) - 1 AND month = 12 AND day = 31
                   )
                SELECT r.ranking, t.tricode || '.png' AS flag, r.team, r.points, t.confederation, (p.ranking - r.ranking) AS ranking_change, (r.points - p.points) AS points_change
                FROM Rankings r
                LEFT JOIN previous_year p ON (r.team = p.team)
                LEFT JOIN Teams t ON (r.team = t.team)
                WHERE date = (SELECT MAX(date) FROM Rankings)
               '''
)

rows = cursor.fetchall()
column_names = [description[0] for description in cursor.description]
data = [dict(zip(column_names, row)) for row in rows]

# Export data to a JSON file
json_path = "data/json/LastRankings.json"
with open(json_path, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=2)

print(f"Data successfully extracted and exported to {json_path}.")

connection.close()
