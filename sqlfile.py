import sqlite3
import pandas as pd
from pprint import pprint as pp


# connecting to the database
connection = sqlite3.connect("kdrama.db")
 
# cursor
crsr = connection.cursor()
 
# SQL command to create a table in the database
drop_command="""DROP TABLE main_pd"""
sql_command = """CREATE TABLE emp (
drama_name VARCHAR(60) PRIMARY KEY,
genre VARCHAR(60),
tags VARCHAR(60),
episodes VARCHAR(60),
start_airing VARCHAR(60),
end_airing VARCHAR(60),
aired_on VARCHAR(200),
original_network VARCHAR(200),
duration VARCHAR(60),
score VARCHAR(60),
scored_by VARCHAR(60),
ranked VARCHAR(60),
popularity VARCHAR(60),
content_rating VARCHAR(60),
watchers VARCHAR(60),
actors VARCHAR(700),
platforms VARCHAR(200),
imdb_rating VARCHAR(60),
imdb_users VARCHAR(60),
imdb_description VARCHAR(800));"""

main_pd=pd.read_csv('normalized_tables/main_descriptors.csv')
main_pd.to_sql('main_pd',connection,if_exists='append',index=False)

cols_main=['Kdrama_name','Episodes','start airing','end airing', 'Duration', 'score', 'scored by','Ranked',
         'Popularity', 'Content Rating','Watchers']
results=crsr.execute('''SELECT * FROM main_pd  where Episodes<20 and Episodes>6 order by Ranked desc limit 5''').fetchall()
pp(results)
# close the connection
connection.close()