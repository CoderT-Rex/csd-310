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

    # Query 1: Select all fields from the studio table
    cursor = db.cursor()
    cursor.execute("SELECT * FROM studio")
    studios = cursor.fetchall()
    print("\n--- DISPLAYING Studio RECORDS ---")
    for studio in studios:
        print("Studio ID: {}".format(studio[0]))
        print("Studio Name: {}".format(studio[1]))


    # Query 2: Select all fields from the genre table
    cursor.execute("SELECT * FROM genre")
    genres = cursor.fetchall()
    print("\n--- DISPLAYING Genre RECORDS ---")
    for genre in genres:
        print("Genre ID: {}".format(genre[0]))
        print("Genre Name: {}".format(genre[1]))

    # Query 3: Select movie names for movies with a runtime of less than two hours
    cursor.execute("SELECT film_name, film_runtime FROM movies.film WHERE film_runtime < 120")
    movies_short_runtime = cursor.fetchall()
    print("\n--- DISPLAYING short film RECORDS ---")
    for movie in movies_short_runtime:
        print("Film Name: {}, Runtime: {}".format(movie[0], movie[1]))

    # Query 4: Get film names and directors ordered by director
    cursor.execute("SELECT film_name, film_director FROM movies.film ORDER BY film_director")
    movies_directors_ordered = cursor.fetchall()
    print("\n--- Movies and Directors Ordered by Director ---")
    for movie in movies_directors_ordered:
        print("Film Name: {}, Director: {}".format(movie[0], movie[1]))



except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)

finally:
    if db is not None:
        db.close()

