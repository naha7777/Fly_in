Brain storming :

Dans l'exercice on doit faire avancer les drones de zones en zones pour arriver jusqu'a la zone d'arrivee (depuis le start).

Creation des drones
- creer tant de drones - create drone
- les mettre sur la zone start - add drone start_hub
- leur donner le pouvoir de se deplacer - move drone
-> Classe drone avec ID

Creer algo

Renvoyer l'output dans un .txt:
L'output se fait en une ligne et indique juste les deplacements d'un drone vers une zone de cette maniere D1-roof1 = le drone 1 s'est deplace vers la zone roof1 puis un espace et D2-roof2 par exemple, on ecrit que les deplacements quoi

# Fly_in

## Resources :
Algo dijkstra :
- https://www.datacamp.com/tutorial/dijkstra-algorithm-in-python

Couleurs :
- https://rich.readthedocs.io/en/latest/introduction.html

Algorithme d'Edmonds-Karp :
- https://www.youtube.com/watch?v=eLcdEcIjijs
- https://cp-algorithms.com/graph/edmonds_karp.html#:~:text=Edmonds%2DKarp%20algorithm%20is%20just,independently%20of%20the%20maximal%20flow.
- https://fr.wikipedia.org/wiki/Algorithme_d%27Edmonds-Karp
- https://www.youtube.com/watch?v=M6Mq_jRqblQ

Deque :
- https://www.geeksforgeeks.org/python/deque-in-python/

Algo en python a completer :
- https://github.com/anxiaonong/Maxflow-Algorithms/blob/master/Edmonds-Karp%20Algorithm.py


L'algo a besoin:
- matrice C
- index de start
- index de end
On obtient a la fin la quantite de drones pouvant avancer en meme temps
Il manque :
- la gestion des couts de deplacement (restricted = 2 tours)
- La conversion des noms de zones en indices de matrice

Mon algo doit me renvoyer, en + du nombre de drones a bouger simultanement, ma matrice F qui detiens les chemins que jaurai juste a assigner a chaque drone

Et plus tard creer les drones quand l'algo sera fini pour justement effectuer les mouvements trouves par l'algo renvoyes dans la matrice F


6 - creer les drones
7 - assigner les chemins aux drones
8 - simulation tour par tour (classe et fichier simulation)



Creer un file d'ou prendre mes couleurs



Output visuel exemple :
Affichage couleur sur un terminal indiquant les mouvements des drones et l’état des zones ->

[ start: D1 ] [ waypoint1: empty ] [ waypoint2: empty ] [ goal: empty ]

Turn 1 : D1-waypoint1
[ start: empty ] [ waypoint1: D1 ] [ waypoint2: empty ] [ goal: empty ]

Turn 2 : D1-waypoint2
[ start: empty ] [ waypoint1: empty ] [ waypoint2: D1 ] [ goal: empty ]

Turn 3 : D1-goal
[ start: empty ] [ waypoint1: empty ] [ waypoint2: empty ] [ goal: D1 ]


OU MATPLOTLIB CA A L'AIR FUN

la simulation a les drones sur start
doit prendre le nombre de drones a bouger simultanement + le chemin et envoyer le nombre de drones faire un mouv du chemin, une fois le mouv fait on envoit d'autres drones
a chaque fois on compte un tour
si la zone suivante est restricted on se deplace sur connection (on va a la zone en 2 tours)

du coup faut ptete analyser le path d'abord
on regarde chaque path et on regarde le type de zone
==
pour chaque zone (1 sur 2 dans notre path) on regarde son type
----- d'abord on check si ya une priority parmi toutes, vu que l'algo me sort des chemins opti (minimum de tours) si dans un des chemins il y a la zone prioritaire alors je vais choisir ce chemin plus qu'un autre.
- si type normal on s'en blc
- si type restricted on va sur connection
