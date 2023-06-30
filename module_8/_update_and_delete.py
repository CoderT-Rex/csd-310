import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "root",
    "password": "Purplepig92",
    "host": "127.0.0.1",
    "database": "movies",
    "raise_on_warnings": True
}
db = None  # Define db variable outside the try block

try:
    db = mysql.connector.connect(**config)
    print("\nDatabase user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)



def display_film_records(cursor, title):
    # Execute the select statement to fetch film records with genre and studio details
    select_query = """
        SELECT film_name AS Name, genre_name AS Genre, studio_name AS 'Studio Name'
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id
    """
    cursor.execute(select_query)
    film_records = cursor.fetchall()

    print("\n--- {} ---".format(title))
    for record in film_records:
        print("Film Name: {}\n Genre: {}\n Studio: {}\n".format(record[0], record[1], record[2]))

cursor = db.cursor()
display_film_records(cursor, "DISPLAYING Film RECORDS")

insert_query = """
INSERT INTO film (film_name, film_director, genre_id, studio_id, film_runtime, film_releaseDate)
VALUES ('ET the Extra-Terrestrial', 'Steven Spielberg', 2, 3, 114, '1982')
"""
cursor.execute(insert_query)
db.commit()

cursor = db.cursor()
display_film_records(cursor, "DISPLAYING FILMS AFTER INSERT")

update_query = """
UPDATE film
SET genre_id = 1
WHERE film_name = 'Alien'
"""
cursor = db.cursor()
cursor.execute(update_query)
db.commit()

display_film_records(cursor, "DISPLAYING FILMS AFTER UPDATE Changed ALien to Horror")

delete_query = """
DELETE FROM film
WHERE film_name = 'Gladiator'
"""
cursor = db.cursor()
cursor.execute(delete_query)
db.commit()

display_film_records(cursor, "DISPLAYING FILMS AFTER DELETE")

cursor.close()
db.close()


