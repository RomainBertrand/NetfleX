# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 17:34:16 2019

@author: maxime
"""

#NB : La fonction 1 marche, la 2 est débile, la 3 ne marche que s'il n'y a que des int/float dans le fichier (a cause de numpy)

#import lecture_csv
import csv
import sqlite3
import numpy as np

#lien = sqlite3.connect("base_test.db")

#curseur = lien.cursor()
#curseur.execute("""DROP TABLE users""")

##Important pour creer le dico
#curseur.execute("""CREATE TABLE IF NOT EXISTS usersbis(userId,movieId,rating,timestamp); """)
#nom_fichier = "ml-latest-small/ratings.csv"
#with open(nom_fichier, newline='') as fichier_notes:
#    dr = csv.DictReader(fichier_notes)
#    to_db = [( i['userId'], i['movieId'], i['rating'], i['timestamp']) for i in dr ]
#
#curseur.executemany("""INSERT INTO usersbis(userId,movieId,rating,timestamp) VALUES(?,?,?,?)""",
#                    to_db)
#
#lien.commit()


##dico_films_avis, dico_utilisateur_avis, dico_nombre_vues, nombre_vues_tot = lecture_csv.init_data(True)

#curseur.execute("SELECT userID FROM usersbis WHERE movieId='1'")
#print(curseur.fetchall())


#lien.close()

def csv_en_bdd():
    """
        Transforme les fichiers ratings.csv et movies.csv en base de données
    """

    lien_avis = sqlite3.connect("base_avis_film0.db")

    curseur_avis = lien_avis.cursor()
#    curseur_avis.execute("""DROP TABLE users""")

    #Transformation du .csv en .db
    curseur_avis.execute("""CREATE TABLE IF NOT EXISTS avis(userId, movieId, rating); """)
    nom_fichier_avis = "ml-latest-small/ratings.csv"
    with open(nom_fichier_avis, newline='') as fichier_notes:
        dico_avis = csv.DictReader(fichier_notes)
        bdd_avis = [(i['userId'], i['movieId'], i['rating']) for i in dico_avis]

    curseur_avis.executemany("""INSERT INTO avis(userId, movieId, rating) VALUES(?,?,?)""", bdd_avis)

    lien_avis.commit()

    #Test:
    curseur_avis.execute("SELECT DISTINCT userId FROM avis WHERE movieId='17'")
    print(curseur_avis.fetchall())

    lien_avis.close()


    #fichier movies.csv
    lien_noms = sqlite3.connect("base_avis_film0.db")

    curseur_noms = lien_noms.cursor()
#    curseur_avis.execute("""DROP TABLE users""")

    #Transformation du .csv en .db
    curseur_noms.execute("""CREATE TABLE IF NOT EXISTS noms_film(movieId, title); """)
    nom_fichier_noms = "ml-latest-small/movies.csv"
    with open(nom_fichier_noms, newline='', encoding='utf-8') as fichier_noms:
        dico_noms = csv.DictReader(fichier_noms)
        bdd_noms = [(i['movieId'], i['title']) for i in dico_noms]

    curseur_noms.executemany("""INSERT INTO noms_film(movieId, title) VALUES(?,?)""", bdd_noms)

    lien_noms.commit()

    #Test:
    curseur_noms.execute("SELECT DISTINCT title FROM noms_film WHERE movieId='17'")
    print(curseur_noms.fetchall())

    lien_noms.close()



def csv_en_bdd3(fichier_csv, nom_bdd, nom_table, noms_colonnes):
    """
    Test de fonction generique
    """

    lien = sqlite3.connect(nom_bdd)

    curseur = lien.cursor()

    creation = """CREATE TABLE IF NOT EXISTS {}({}); """.format(nom_table, noms_colonnes[0])
    curseur.execute(creation)
#    lien.row_factory = sqlite3.Row
    for col in noms_colonnes[1::]:
#        ajout_col = """ALTER TABLE {} ADD COLUMN {}""".format(nom_table, col)
#        curseur.execute(ajout_col)
        curseur.execute("""ALTER TABLE {} ADD COLUMN {}""".format(nom_table, col))
    nom_fichier = fichier_csv
    with open(nom_fichier, newline='') as fichier_notes:
        dico = csv.DictReader(fichier_notes)
        bdd = np.array([[i[colonne] for colonne in noms_colonnes] for i in dico])
        print(len(bdd[:, 1]))

    test = "?"
    for i in range(len(noms_colonnes) - 1):
        test += ",?"
    print(test)
    curseur.executemany("""INSERT INTO {} VALUES({})""".format(nom_table, test), bdd)

    lien.commit()
    #Test avec le fichier ratings:
#    curseur.execute("SELECT DISTINCT userId FROM avis WHERE movieId='17'")
    #Test avec le fichier movies:
    curseur.execute("SELECT DISTINCT title FROM noms WHERE movieId='17'")
    print(curseur.fetchall())

    lien.close()


#csv_en_bdd3(fichier_csv="ml-latest-small/ratings.csv",
#            nom_bdd="base_avis_film13.db",
#            nom_table="avis",
#            noms_colonnes=("userId", "movieId", "rating"))

#csv_en_bdd3(fichier_csv="ml-latest-small/movies.csv",
#            nom_bdd="base_noms_films.db",
#            nom_table="noms",
#            noms_colonnes=("movieId", "title"))
