# Projet_Architecture_Distribue

## Présentation :

Ceci est un projet d'Intelligence Artificielle, il consiste à récupérer des commentaires sur le site d'Imdb, ces commentaires seront ensuite traité et classifier selon leur note (Commentaire positif, Commentaire négatif), pour entrainer nos IA. Pour en finalité, prédire si le commentaire est positif ou négatif, prédire une note a ce commentaire,...
Plusieurs modèles d'IA sont intégré dans le projet et l'utilisateur pourra ensuite écrire des commentaires sur une interface Streamlit.

## Lancement :

1. Lancement du Docker :

A la racine du projet, entrez la commande suivante :

`docker-compose up --build`

2. Lancement du Scrapper :

Toujours à la racine du projet, executez le fichier suivant :

`python imdb_movie_scrapper.py`

Celui-i va s'occuper de récupérer tous les commentaires sur un certains nombre de films données et tout stocker dans un ficher Json.

3. Lancement de la Base de donnée :

A partir de cette étape, il faudra ouvrir un autre terminal et entrer les commandes suivantes :

`docker exec -it pyspark_notebook bash`

Avec cette commande vous vous connectez à l'image docker de Pyspark Notebook. Une fois connecté faites :

`cd ../work`

Puis :

`python fill_database.py`

Vous pouvez désormais consulter la Base de donnée a partir de `localhost:8081/` ou sur MongoDB Compass.

4. Visualisation :

C'est depuis cette interface que vous pouvez entrer un commentaire et jouer avec les differents modèles d'IA intégrés.
Connectez-vous a l'url `localhost:8501/` pour y accéder.
