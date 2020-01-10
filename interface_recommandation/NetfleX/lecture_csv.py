# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 22:01:12 2019

@author: maxime
"""

###Objectif: Lecture de fichiers .csv

import csv
#
# Ouverture du fichier source.
#

def init_data(avec_notes: bool = False)->(dict, dict, dict, int):
    """
        Construction des deux dictionnaires de base:
            Celui qui à un film associe les utilisateurs l'ayant vu et leur note
            Celui qui à un utilisateur associe les films qu'il a vu et leur note
        Passer l'argument avec_note = True pour obtenir les notes et non les avis

        Compte également le nombre de vues total et le nombre de vues par film
    """

    dico_films_avis = {}
    dico_utilisateur_avis = {}

    nombre_vues_tot = 0
    dico_nombre_vues = {}

    nom_fichier = "ml-latest-small/ratings.csv"
    with open(nom_fichier, newline='') as fichier_notes:

        reader = csv.reader(fichier_notes)

        premiere_ligne = True
        for row in reader:
            if not premiere_ligne:

                id_film = row[1]
                id_utilisateur = row[0]
                avis = float(row[2])

                if not avec_notes:
                    avis = bool(avis > 3)

                if str(id_film) not in dico_films_avis.keys():
                    dico_films_avis[str(id_film)] = (id_utilisateur, avis)
                    dico_nombre_vues[str(id_film)] = 1

                else:
                    #On concatène les utilisateurs si plusieurs ont vu le film
                    dico_films_avis[str(id_film)] += (id_utilisateur, avis)
                    dico_nombre_vues[str(id_film)] += 1


                if str(id_utilisateur) not in dico_utilisateur_avis.keys():
                    dico_utilisateur_avis[str(id_utilisateur)] = (id_film, avis)
                else:
                    #On concatène les films si l'utilisateur en a vu plusieurs
                    dico_utilisateur_avis[str(id_utilisateur)] += (id_film, avis)

                nombre_vues_tot += 1

            premiere_ligne = False

    fichier_notes.close()
    return dico_films_avis, dico_utilisateur_avis, dico_nombre_vues, nombre_vues_tot


def init_noms_films()->(dict, dict):
    """
        Initialisation du dico id_films / noms_films
    """

    dico_noms_films = {}
    dico_films_noms = {}

    nom_fichier = "ml-latest-small/movies.csv"
    with open(nom_fichier, newline='', encoding='utf-8') as fichier_noms:


        reader = csv.reader(fichier_noms)

        premiere_ligne = True
        for row in reader:

            if not premiere_ligne:

                id_film = row[0]
                nom_film = row[1]

                dico_noms_films[str(id_film)] = nom_film
                dico_films_noms[nom_film] = str(id_film)
            premiere_ligne = False

    fichier_noms.close()
    return dico_noms_films, dico_films_noms


def init_tags_films()->dict:
    """
        Initialisation du dico id_films / tags du film
        Les tags sont une liste de string
    """

    dico_tags_films = {}

    nom_fichier = "ml-latest-small/movies.csv"
    with open(nom_fichier, newline='', encoding='utf-8') as fichier_noms:


        reader = csv.reader(fichier_noms)

        premiere_ligne = True
        for row in reader:

            if not premiere_ligne:

                id_film = row[0]
                #tags_films est du format "tag_1|tag_2|...|tag_n"
                tags_film = row[2]

                tags_film = tags_film.split("|")

                dico_tags_films[str(id_film)] = tags_film
            premiere_ligne = False

    fichier_noms.close()
    return dico_tags_films
