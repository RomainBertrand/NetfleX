# -*- coding: utf-8 -*-
"""Initialisation of all the dictionnaries needed to deal with films and users data

Functions:
init_data -- Creation of the dictionnary that links movies to all the users that have seen them and
their rating, and of the dictionnary that links users to the films they have seen and their ratings
init_movies_names -- Creation of the dictionnary that links movies to their ids
init_tags_movies -- Creation of the dictionnary that links movies to their tags
"""

import csv


def init_data(with_ratings: bool = False) -> (dict, dict, dict, int):
    """Return dictionnaries that link users, movies and ratings as well as the number of views
    of each and all movies

    Parameters:
    with_ratings (bool): If False, ratings are bools. Else, ratings are floats between 0 and 5.
    (default: False)

    Returns:
    dictionnary_movies_ratings (dict): Keys: id of movies (str),
    values: tuple (id_user_1, rating_1, id_user_2, rating_2, ...)
    dictionnary_users_ratings (dict): Keys: id of users (int),
    values: tuple (id_movie_1, rating_1, id_movie_2, rating_2, ...)
    dictionnary_views_number (dict): Keys: movie_id (str), values: total views of this movie (int)
    total_view_count (int): Number of films watched by all the users of the database
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
                    # If the movie is not already in the dictionnary:
                    dictionnary_movies_ratings[str(
                        movie_id)] = (user_id, rating)
                    dictionnary_views_number[str(movie_id)] = 1

                else:
                    # All the users that have seen this movie are concatenated
                    dictionnary_movies_ratings[str(
                        movie_id)] += (user_id, rating)
                    dictionnary_views_number[str(movie_id)] += 1

                if str(user_id) not in dictionnary_users_ratings.keys():
                    # If the user is not already in the dictionnary:
                    dictionnary_users_ratings[str(user_id)] = (
                        movie_id, rating)
                else:
                    # All the movies seen seen by this user are concatenated
                    dictionnary_users_ratings[str(
                        user_id)] += (movie_id, rating)

                total_view_count += 1

            first_line = False

    file_ratings.close()
    return dictionnary_movies_ratings, dictionnary_users_ratings, dictionnary_views_number, total_view_count


def init_movies_names() -> (dict, dict):
    """Return the dictionnary that links a movie to its id, and its reversed version

    Returns:
    dictionnary_names_movies (dict): Keys: movies id (str), values: movies_name (str)
    dictionnary_movies_names (dict); Keys: movies name (str), values: movies_id (str)

    NB: Having both these dictionnaries is redondant but makes the code easier to follow later
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


def init_tags_movies() -> (dict, set):
    """Return the dictionnariy that links a movie to its tags

    Returns:
    dictionnary_tags_movies (dict): Keys: movie_id (str), values: movie_tags (list of string)
    list_of_all_tags (set): Set of all the tags (str) that appear in the database.
    No tag is: '(no genres listed)'
    """
    dictionnary_tags_movies = {}
    list_of_all_tags = set()

    file_name = "ml-latest-small/movies.csv"
    with open(file_name, newline='', encoding='utf-8') as file_names:

        reader = csv.reader(file_names)

        first_line = True
        for row in reader:

            if not first_line:

                movie_id = row[0]
                # Format of tag_movies is: "tag_1|tag_2|...|tag_n"
                tags_movies = row[2]

                tags_movies = tags_movies.split("|")

                dictionnary_tags_movies[str(movie_id)] = tags_movies
                for elem in tags_movies:
                    list_of_all_tags.add(elem)
            first_line = False

    file_names.close()
    return dictionnary_tags_movies, list_of_all_tags
