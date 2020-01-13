# -*- codign: utf-8 -*-
"""
Created on Sun Nov 10 17:04:37 2019

@author: romain
"""

# Objectif: renvoyer un film corrélé au choix de l'utilisateur

import math
import random
from NetfleX.lecture_csv import init_data


def meilleure_correlation(utilisateur, avec_notes: bool = False) -> int:
    """
    Renvoie l'indice d'un film qui est censé plaire à l'utilisateur, au vu de ses goûts.
    0 si aucun film n'a été trouvé
    Pour cela on utlise simplement l'avis booléen des autres utilisateurs
    """
    # on initialise les dictionnaires
    dico_films_avis, dico_utilisateurs_avis, dico_nombre_vues, nombres_vues_tot = init_data(
        avec_notes)
    liste_films = []
    # on génère la liste des films vus par notre utilisateur
    for film_avis in utilisateur:
        liste_films.append(film_avis[0])
    # une liste de tuples qui contiennent plusieurs utilisateurs ainsi que leur avis
    utilisateurs_avis = []
    for film in liste_films:  # utilisateurs ayant un film en commun avec l'utilisateur
        utilisateurs_avis.append(dico_films_avis[str(film)])
    utilisateurs_lies = []
    # on génère une liste avec uniquement les utilisateurs qui ont vu un des films
    for user_avis in utilisateurs_avis:
        for j in range(int(len(user_avis)/2)):
            if user_avis[2*j] not in utilisateurs_lies:
                utilisateurs_lies.append(user_avis[2*j])
    # on associe à chaque utilisateur une corrélation
    score_correlation = [0 for i in range(len(utilisateurs_lies))]
    for i in range(len(liste_films)):  # pour chaque film
        # pour chaque utilisateur qui l'a vu
        for j in range(int(len(utilisateurs_avis[i])/2)):
            if avec_notes:
                ecart = abs(utilisateur[i][1]-utilisateurs_avis[i][2*j+1])
                score_correlation[j] += (5-ecart) * \
                    (1+math.log(nombres_vues_tot/dico_nombre_vues[i]))
            else:
                if utilisateur[i][1] == utilisateurs_avis[i][2*j+1]:  # si ils ont le même avis
                    score_correlation[j] += 1
                else:
                    score_correlation[j] -= 1
    # l'utilisateur avec la meilleure corrélation
    user_opti = utilisateurs_lies[score_correlation.index(
        max(score_correlation))]
    # films vus par l'utilisateur le plus corrélé
    film_possibles = dico_utilisateurs_avis[user_opti]
    # liste des films ayant eu la note maximale chez l'utilisateur optimal
    films_a_recommander = []
    # un indice sur deux est un film, l'autre est un avis
    for ind_film in range(int(len(film_possibles)/2)):
        # on vérifie que l'utilisateur optimal a aimé le film
        if film_possibles[2*ind_film+1]:
            if int(film_possibles[2*ind_film]) not in liste_films:
                # au vu du nombre d'avis de chaque utilisateur (>30), on aura un film en commun
                films_a_recommander.append(int(film_possibles[2*ind_film]))
    return films_a_recommander[random.randint(0, len(films_a_recommander))]


def conseil_film(film: int, aime: bool, nombre_de_conseils: int = 5) -> list:
    """ Renvoie une liste de films aimés par des personnes du même avis que l'utilisateur sur le film saisi """
    # on initialise les dictionnaires
    avec_notes = True
    dico_films_avis, dico_utilisateurs_avis, _, _ = init_data(
        avec_notes)

    # Tuples utilisateurs-avis
    utilisateurs_meme_avis = []
    utilisateurs_ayant_vu = dico_films_avis[str(film)]
    for ind_utilisateur in range(int(len(utilisateurs_ayant_vu) / 2)):
        condition_accord = bool(
            float(utilisateurs_ayant_vu[2 * ind_utilisateur + 1]) > 3.5)
        if not aime:
            condition_accord = bool(
                float(utilisateurs_ayant_vu[2 * ind_utilisateur + 1]) < 2.5)
        if condition_accord:
            utilisateurs_meme_avis.append(
                utilisateurs_ayant_vu[2 * ind_utilisateur])

    # Films aimés par ces utilisateurs de même avis
    films_possibles = []
    compteur_utilisateur = 0
    # while len(films_possibles) < nombre_de_conseils and compteur_utilisateur < len(utilisateurs_meme_avis):
    while compteur_utilisateur < len(utilisateurs_meme_avis):
        # Tuple film-avis
        utilisateur_actif = dico_utilisateurs_avis[utilisateurs_meme_avis[compteur_utilisateur]]
        for ind_film in range(int(len(utilisateur_actif)/2)):
            # if len(films_possibles) < nombre_de_conseils and float(utilisateur_actif[2 * ind_film + 1]) > 3.5:
            if float(utilisateur_actif[2 * ind_film + 1]) > 3.5:
                films_possibles.append(int(utilisateur_actif[2 * ind_film]))
        compteur_utilisateur += 1

    return [films_possibles[random.randint(0, len(films_possibles))] for i in range(min(nombre_de_conseils, len(films_possibles)))]
