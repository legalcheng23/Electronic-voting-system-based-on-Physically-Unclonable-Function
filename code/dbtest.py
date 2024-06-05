import sqlite3
con = sqlite3.connect('/tmp/mydb')
cursor = con.cursor()


create_table = "CREATE TABLE IF NOT EXISTS employees (id integer PRIMARY KEY, name text NOT NULL, salary integer);"
drop_table = "DROP TABLE IF EXISTS employees"
insert_table = "INSERT INTO employees VALUES(2, 'Ben', 500)"
select_table = "SELECT * FROM employees"

# cursor.execute(create_table)
cursor.execute(select_table)
for row in cursor.fetchall():
    print(row)
con.commit()