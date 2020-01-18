# -*- codign: utf-8 -*-
"""
Created on Sun Nov 10 17:04:37 2019

@author: romain
"""

# Objectif: renvoyer un movie corrélé au choix de l'user

import math
import random
from NetfleX.lecture_csv import init_data


def meilleure_correlation(user, with_ratings: bool = False) -> int:
    """
    Renvoie l'indice d'un movie qui est censé plaire à l'user, au vu de ses goûts.
    0 si aucun movie n'a été trouvé
    Pour cela on utlise simplement l'rating booléen des autres users
    """
    # on initialise les dictionnaires
    dictionnary_movies_ratings, dictionnary_users_ratings, dictionnary_views_number, total_views_number = init_data(
        with_ratings)
    list_movies = []
    # on génère la liste des movies vus par notre user
    for movie_rating in user:
        list_movies.append(movie_rating[0])
    # une liste de tuples qui contiennent plusieurs users ainsi que leur rating
    users_rating = []
    for movie in list_movies:  # users ayant un movie en commun avec l'user
        users_rating.append(dictionnary_movies_ratings[str(movie)])
    users_linked = []
    # on génère une liste avec uniquement les users qui ont vu un des movies
    for user_rating in users_rating:
        for j in range(int(len(user_rating)/2)):
            if user_rating[2*j] not in users_linked:
                users_linked.append(user_rating[2*j])
    # on associe à chaque user une corrélation
    score_correlation = [0 for i in range(len(users_linked))]
    for i in range(len(list_movies)):  # pour chaque movie
        # pour chaque user qui l'a vu
        for j in range(int(len(users_rating[i])/2)):
            if with_ratings:
                gap = abs(user[i][1]-users_rating[i][2*j+1])
                score_correlation[j] += (5-gap) * \
                    (1+math.log(total_views_number/dictionnary_views_number[i]))
            else:
                if user[i][1] == users_rating[i][2*j+1]:  # si ils ont le même rating
                    score_correlation[j] += 1
                else:
                    score_correlation[j] -= 1
    # l'user avec la meilleure corrélation
    user_opti = users_linked[score_correlation.index(
        max(score_correlation))]
    # movies vus par l'user le plus corrélé
    possible_movies = dictionnary_users_ratings[user_opti]
    # liste des movies ayant eu la rating maximale chez l'user optimal
    movies_to_recommend = []
    # un indice sur deux est un movie, l'autre est un rating
    for ind_movie in range(int(len(possible_movies)/2)):
        # on vérifie que l'user optimal a aimé le movie
        if possible_movies[2*ind_movie+1]:
            if int(possible_movies[2*ind_movie]) not in list_movies:
                # au vu du nombre d'rating de chaque user (>30), on aura un movie en commun
                movies_to_recommend.append(int(possible_movies[2*ind_movie]))
    return movies_to_recommend[random.randint(0, len(movies_to_recommend))]


def advice_movie(movie: int, likes: bool, movie_tag: str, advices_number: int = 5) -> list:
    """ Renvoie une liste de movies aimés par des personnes du même rating que l'user sur le movie saisi """
    # on initialise les dictionnaires
    with_ratings = True
    dictionnary_movies_ratings, dictionnary_users_ratings, _, _ = init_data(
        with_ratings)

    # Tuples users-rating
    users_same_rating = []
    users_who_saw = dictionnary_movies_ratings[str(movie)]
    for ind_user in range(int(len(users_who_saw) / 2)):
        agreement_condition = bool(
            float(users_who_saw[2 * ind_user + 1]) > 3.5)
        if not likes:
            agreement_condition = bool(
                float(users_who_saw[2 * ind_user + 1]) < 2.5)
        if agreement_condition:
            users_same_rating.append(
                users_who_saw[2 * ind_user])

    # Films aimés par ces users de même rating
    possible_movies = []
    users_count = 0
    # while len(possible_movies) < advices_number and users_count < len(users_same_rating):
    while users_count < len(users_same_rating):
        # Tuple movie-rating
        active_user = dictionnary_users_ratings[users_same_rating[users_count]]
        for ind_movie in range(int(len(active_user)/2)):
            # if len(possible_movies) < advices_number and float(active_user[2 * ind_movie + 1]) > 3.5:
            if float(active_user[2 * ind_movie + 1]) > 3.5:
                possible_movies.append(int(active_user[2 * ind_movie]))
        users_count += 1

    final_movies = []
    acc = 0
    while acc < min(advices_number, len(possible_movies)):
        potential_movie_id = possible_movies[random.randint(0, len(possible_movies))]
        if potential_movie_id not in final_movies:
            final_movies.append(potential_movie_id)
            acc += 1


    return final_movies
