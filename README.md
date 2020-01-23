# NetfleX
## Presentation
### Authors
Maxime BARAKAT, Romain BERTRAND, Thomas GERBEAUD
### Date
November 2019 to January 2020

### TDLog project
Algorithm to recommend movies, with a web interface

### State of the project
Movie recommendation dataset ml-latest-small downloadable here:
https://grouplens.org/datasets/movielens/latest/

Right now, two main features are available :
- The first one enables the user to choose 1 to 10 movies, and grade them between 1 and 5, and then the algorithm recommends the movie he is most likely to appreciate.
- The second one lets the user choose a movie, and give his opinion on the movie (whether he likes it or not), decides a number of movies he wants, and is able to pick a movie genre (but it's not mandatory). He then gets a movie list and their associated genres.

Algorithms used:
- In the first case, we pick the most correlated user and return a movie he liked.
- In the second case, we pick the users with the same opinion on the movie as the user, and return movies they liked.

## Installation

### Dependencies
To launch the service, `python` 3 and `django` >= 2 are required.

```
apt-get install python
pip install django
```

### Repository
To clone, use
    git clone https://github.com/RomainBertrand/NetfleX

### Set up
Go to the interface_recommandation directory

```
cd interface_recommandation/
```

And launch the main.py file

```
./main.py
```

Alternatively, you can run the manage.py file with the option runserver

```
python manage.py runserver
```

### Use
Open a web browser, and reach the address : http://localhost:8000/NetfleX
