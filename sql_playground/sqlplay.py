import psycopg2

conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="iphixli",
                        port="5432")
conn.autocommit = True
#cursor = conn.cursor()

# Open a database cursor

dbCursor = conn.cursor();

 
check="DROP TABLE IF EXISTS dramas";
dbCursor.execute(check);
# SQL statement to create a table

sqlCreateTable  = "CREATE TABLE dramas(name text, genre text[])"

# Execute CREATE TABLE command

dbCursor.execute(sqlCreateTable);

 

# Insert statements

sqlInsertRow1  = "INSERT INTO dramas values('Extraordinary Attorney Woo', {'law', 'romance', 'life', 'drama'})";

sqlInsertRow2  = "INSERT INTO dramas values('Squid Game', '{'action', 'thriller', 'mystery', 'drama'}')";

 

# Insert statement

dbCursor.execute(sqlInsertRow1);

dbCursor.execute(sqlInsertRow2);
sql3 = '''select * from dramas;'''
dbCursor.execute(sql3)
for i in dbCursor.fetchall():
    print(i)
conn.commit()
conn.close()