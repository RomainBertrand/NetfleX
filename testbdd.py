""" Création des bases de données """

import csv
import sqlite3


def csv_en_bdd():
    """
        Transforme les fichiers ratings.csv et movies.csv en base de données
        Cree directement les fichiers .db associes
    """

    lien_avis = sqlite3.connect("base_avis_film.db")

    curseur_avis = lien_avis.cursor()
#    curseur_avis.execute("""DROP TABLE users""")

    # Transformation du .csv en .db
    curseur_avis.execute(
        """CREATE TABLE IF NOT EXISTS avis(userId, movieId, rating); """)
    nom_fichier_avis = "ml-latest-small/ratings.csv"
    with open(nom_fichier_avis, newline='') as fichier_notes:
        dico_avis = csv.DictReader(fichier_notes)
        bdd_avis = [(i['userId'], i['movieId'], i['rating'])
                    for i in dico_avis]

    curseur_avis.executemany(
        """INSERT INTO avis(userId, movieId, rating) VALUES(?,?,?)""", bdd_avis)

    lien_avis.commit()

    # Test:
    curseur_avis.execute("SELECT DISTINCT userId FROM avis WHERE movieId='17'")
    print(curseur_avis.fetchall())

    lien_avis.close()

    # fichier movies.csv
    lien_noms = sqlite3.connect("base_noms_film.db")

    curseur_noms = lien_noms.cursor()
#    curseur_avis.execute("""DROP TABLE users""")

    # Transformation du .csv en .db
    curseur_noms.execute(
        """CREATE TABLE IF NOT EXISTS noms_film(movieId, title); """)
    nom_fichier_noms = "ml-latest-small/movies.csv"
    with open(nom_fichier_noms, newline='', encoding='utf-8') as fichier_noms:
        dico_noms = csv.DictReader(fichier_noms)
        bdd_noms = [(i['movieId'], i['title']) for i in dico_noms]

    curseur_noms.executemany(
        """INSERT INTO noms_film(movieId, title) VALUES(?,?)""", bdd_noms)

    lien_noms.commit()

    # Test:
    curseur_noms.execute(
        "SELECT DISTINCT title FROM noms_film WHERE movieId='17'")
    print(curseur_noms.fetchall())

    lien_noms.close()
