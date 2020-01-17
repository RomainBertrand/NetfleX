# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 22:01:12 2019

@author: maxime
"""

# Objectif: Lecture de fichiers .csv

import csv
#
# Ouverture du fichier source.
#


def init_data(with_ratings: bool = False) -> (dict, dict, dict, int):
    """
        Construction des deux dictionnaires de base:
            Celui qui à un movie associe les users l'ayant vu et leur rating
            Celui qui à un user associe les movies qu'il a vu et leur rating
        Passer l'argument avec_rating = True pour obtenir les ratings et non les rating

        Compte également le nombre de vues total et le nombre de vues par movie
    """

    dictionnary_movies_ratings = {}
    dictionnary_users_ratings = {}

    total_view_count = 0
    dictionnary_views_number = {}

    file_name = "ml-latest-small/ratings.csv"
    with open(file_name, newline='') as file_ratings:

        reader = csv.reader(file_ratings)

        first_line = True
        for row in reader:
            if not first_line:

                movie_id = row[1]
                user_id = row[0]
                rating = float(row[2])

                if not with_ratings:
                    rating = bool(rating > 3)

                if str(movie_id) not in dictionnary_movies_ratings.keys():
                    dictionnary_movies_ratings[str(movie_id)] = (user_id, rating)
                    dictionnary_views_number[str(movie_id)] = 1

                else:
                    # On concatène les users si plusieurs ont vu le movie
                    dictionnary_movies_ratings[str(movie_id)] += (user_id, rating)
                    dictionnary_views_number[str(movie_id)] += 1

                if str(user_id) not in dictionnary_users_ratings.keys():
                    dictionnary_users_ratings[str(user_id)] = (
                        movie_id, rating)
                else:
                    # On concatène les movies si l'user en a vu plusieurs
                    dictionnary_users_ratings[str(
                        user_id)] += (movie_id, rating)

                total_view_count += 1

            first_line = False

    file_ratings.close()
    return dictionnary_movies_ratings, dictionnary_users_ratings, dictionnary_views_number, total_view_count


def init_movies_names() -> (dict, dict):
    """
        Initialisation du dico movie_ids / noms_movies
    """

    dictionnary_names_movies = {}
    dictionnary_movies_names = {}

    file_name = "ml-latest-small/movies.csv"
    with open(file_name, newline='', encoding='utf-8') as file_names:

        reader = csv.reader(file_names)

        first_line = True
        for row in reader:

            if not first_line:

                movie_id = row[0]
                movie_name = row[1]

                dictionnary_names_movies[str(movie_id)] = movie_name
                dictionnary_movies_names[movie_name] = str(movie_id)
            first_line = False

    file_names.close()
    return dictionnary_names_movies, dictionnary_movies_names


def init_tags_moviess() -> dict:
    """
        Initialisation du dico movie_ids / tags du movie
        Les tags sont une liste de string
    """

    dictionnary_tags_movies = {}

    file_name = "ml-latest-small/movies.csv"
    with open(file_name, newline='', encoding='utf-8') as file_names:

        reader = csv.reader(file_names)

        first_line = True
        for row in reader:

            if not first_line:

                movie_id = row[0]
                # tags_moviess est du format "tag_1|tag_2|...|tag_n"
                tags_movies = row[2]

                tags_movies = tags_movies.split("|")

                dictionnary_tags_movies[str(movie_id)] = tags_movies
            first_line = False

    file_names.close()
    return dictionnary_tags_movies
