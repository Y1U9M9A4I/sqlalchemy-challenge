import sqlite3
import pandas as pd

from pathlib import Path

database_path = "Resources/hawaiii.sqlite"
Path(database_path).touch()

conn = sqlite3.connect(database_path)
c = conn.cursor()

c.execute('''CREATE TABLE climate (ID int, station, date, prcp, tobs, name, latitude, longitude, elevation)''')

csv_meas = pd.read_csv("Resources/hawaii_measurements.csv")  
csv_stat = pd.read_csv("Resources/hawaii_stations.csv")  
climate_csv = csv_stat.merge(csv_meas, how='inner', on='station' )      

climate_csv.to_sql("climate", conn, if_exists='append', index=False)