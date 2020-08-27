import sqlite3
conn = sqlite3.connect('example.sqlite')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS country(id integer primary key, country_name text)''')

result = c.execute('SELECT * FROM country')

if result.rowcount < 1:
    with open("countries.txt", "r") as filename:
        for data in filename:
            country = data.split("|")
            country[1] = country[1].rstrip('\n')
            country.pop(0)
            c.execute('INSERT INTO country (country_name) VALUES (?)', country)

conn.commit()
conn.close()
