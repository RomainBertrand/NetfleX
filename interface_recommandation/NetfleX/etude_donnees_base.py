# -*- codign: utf-8 -*-
"""Definition of the two main functions for movie recommendation and advice

Functions:
meilleure_correlation -- Correlate the user of NetfleX with someone in the database.
For movie recommendation.
advice_movie -- Return movies liked by users that agree with NetfleX' user on the chosen film.
"""

import math
import random
from NetfleX.lecture_csv import init_data, init_tags_movies


def meilleure_correlation(user, with_ratings: bool = False) -> int:
    """Return the id of a movie that may be liked by NetfleX' user

    Look for the most correlate user to NetfleX' user and return a movie he likes.

    Parameters:
    user (list): list of tuples (id of a movie seen by the user, rating of this film)
    with_ratings (bool): If False, ratings are booleans. Else, ratings are floats between 0 and 5.
    (default: False)

    Returns:
    movies_to_recommend[random.randint(0, len(movies_to_recommend))] (int): id of a movie liked
    by the most correlate user to NetfleX' user
    0 if no compatible movie
    """

    # Initialisation
    dictionnary_movies_ratings, dictionnary_users_ratings, dictionnary_views_number, total_views_number = init_data(
        with_ratings)
    # Generation of the list of films seen by NetfleX' user
    list_movies = []
    for movie_rating in user:
        list_movies.append(movie_rating[0])
    # users_ratings: list of tuples. Each tuple contain a movie_id followed by the ids of users
    # that have seen this movie and their rating
    users_rating = []
    # users with at least on movie in common with the user
    for movie in list_movies:
        users_rating.append(dictionnary_movies_ratings[str(movie)])

    users_linked = []
    # list with only the users who have a movie in common
    for user_rating in users_rating:
        for j in range(int(len(user_rating)/2)):
            if user_rating[2*j] not in users_linked:
                users_linked.append(user_rating[2*j])
    # we associate a correlation to each user
    score_correlation = [0 for i in range(len(users_linked))]
    for i in range(len(list_movies)):  # for every movie
        # for every user who saw it
        for j in range(int(len(users_rating[i])/2)):
            if with_ratings:
                gap = abs(user[i][1]-users_rating[i][2*j+1])
                score_correlation[j] += (5-gap) * \
                    (1+math.log(total_views_number /
                                dictionnary_views_number[i]))
            else:
                if user[i][1] == users_rating[i][2*j+1]:  # if they have the same rating
                    score_correlation[j] += 1
                else:
                    score_correlation[j] -= 1
    # user with the best correlation
    user_opti = users_linked[score_correlation.index(
        max(score_correlation))]
    # movies saw by the best correlated user
    possible_movies = dictionnary_users_ratings[user_opti]
    # list of movies whot got the best grade from the most correlated user
    movies_to_recommend = []
    # one on two indew is a movie, the other is a rating
    for ind_movie in range(int(len(possible_movies)/2)):
        # we check whether the user liked the movie
        if possible_movies[2*ind_movie+1]:
            if int(possible_movies[2*ind_movie]) not in list_movies:
                # seen the number of rating for every user (>30), a least be 1 movie is possible
                movies_to_recommend.append(int(possible_movies[2*ind_movie]))
    return movies_to_recommend[random.randint(0, len(movies_to_recommend))]


def advice_movie(movie: int, likes: bool, movie_tag: str, advice_number: int = 5) -> list:
    """Return a list of movies liked by users that agree with NetfleX' user on the chosen film.

    Parameters:
    movie (int): id of the chosen movie
    likes (bool): True if movie is liked by NetfleX' user, else: False
    movie_tag (str): Tag of the films that NetfleX' user would like to see. movie_tag = "No" if no tag selected.
    advice_number (int): Number of movies that NetfleX' user would like to see, between 1 and 10 (default: 5)

    Returns:
    final_movies (list): List of ids of movies liked by users that agree with NetfleX' user on the chosen film
    """
    # Initialisation
    with_ratings = True
    dictionnary_movies_ratings, dictionnary_users_ratings, _, _ = init_data(
        with_ratings)

    dictionnary_tags_movies, list_of_all_tags = init_tags_movies()

    # Selection of users with the same opinion as NetfleX' user
    # users_same_rating: tuples (users, rating of movie)
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

    # Selection of films that may interest NetfleX' user
    # possible_movies: Films liked by users with the same opinion on movie
    possible_movies = []
    users_count = 0
    while users_count < len(users_same_rating):
        # active_user: tuple (movie seen by the user, rating of this movie)
        active_user = dictionnary_users_ratings[users_same_rating[users_count]]
        for ind_movie in range(int(len(active_user)/2)):
            if int(active_user[2 * ind_movie]) != movie:
                # If a tag is selected, in order to be sure to have results, we are more tolerant on the rating
                if movie_tag == "No":
                    if float(active_user[2 * ind_movie + 1]) > 3.5:
                        possible_movies.append(int(active_user[2 * ind_movie]))
                else:
                    if float(active_user[2 * ind_movie + 1]) > 3 and movie_tag in dictionnary_tags_movies[active_user[2 * ind_movie]]:
                        possible_movies.append(int(active_user[2 * ind_movie]))
        users_count += 1

    # Selection of the required number of movies in the list possible_movies
    final_movies = []
    acc = 0
    while acc < min(advice_number, len(possible_movies)):
        potential_movie_id = possible_movies[random.randint(
            0, len(possible_movies) - 1)]
        if potential_movie_id not in final_movies:
            final_movies.append(potential_movie_id)
            acc += 1

    return final_movies
