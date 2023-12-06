import csv, sqlite3

con = sqlite3.connect("sqlite:///soportes.db.sqlite3") # change to 'sqlite:///your_filename.db'
cur = con.cursor()

with open('agentes.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['legajo'], i['apellidos'], i['nombres'], i['email']) for i in dr]

cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
con.commit()
con.close()