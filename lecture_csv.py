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

def init_data(avec_notes=False)->(dict, dict, dict, int):
    """
        Construction des deux dictionnaires de base:
            Celui qui à un film associe les utilisateurs l'ayant vu et leur note
            Celui qui à un utilisateur associe les films qu'il a vu et leur note
        Passer l'argument avec_note = True pour obtenir les notes et non les avis

        Compte également le nombre de vues total et le nombre de vues par film
    """
    nom_fichier = "ml-latest-small/ratings.csv"
    with open(nom_fichier, newline='') as fichier_notes:

        dico_films_avis = {}
        dico_utilisateur_avis = {}

        nombre_vues_tot = 0
        dico_nombre_vues = {}

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
