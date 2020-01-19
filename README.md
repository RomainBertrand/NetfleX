# NetfleX

## Auteurs: 
Maxime BARAKAT, Romain BERTRAND, Thomas GERBEAUD
## Date: 
Novembre 2019 à Janvier 2020


## Projet de TDLog:
Algorithme de recommandation de films, site web

## Etat du projet:

Recommandation de films utilisant la base de données ml-latest-small téléchargeable ici:
https://grouplens.org/datasets/movielens/latest/

Sont actuellement disponibles deux services de recommandations:
- Un premier où l'utilisateur choisit entre 1 et 10 films, les note entre 1 et 5 et se voit proposé le film le plus adapté pour lui. (Onglet "Recommandation" du site)
- Un second où l'utilisateur choisit un film, indique s'il l'a aimé ou pas, et décide combien de films il veut se voir proposer (et éventuellement de quel genre). Il obtient alors une liste de films et les genres associés. (Onglet "Conseil" du site)

Algorithmes utilisés:
- Dans le premier cas, sélectionne l'utilisateur le plus corrélé avec vous et renvoie un film qu'il a aimé
- Dans le second cas, sélectionne les utilisateurs du même avis que vous sur votre film, et renvoie des films qu'ils ont apprécié.


## Mise en place : 
Nécessite uniquement Python 3 et le framework Django, version > 1.

## Lancement
Après téléchargement du projet, pour le lancer:

1. Se placer dans le répertoire contenant main.py
2. L'exécuter: 


    python main.py

OU:

1. Se placer dans le répertoire contenant le fichier manage.py ( NetfleX/interface_recommandation )
2. Utiliser la commande 


    python manage.py runserver

Puis:

3. Se rendre à l'adresse http://localhost:8000/NetfleX/


## Remerciements
?
