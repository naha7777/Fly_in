Brain storming :

Dans l'exercice on doit faire avancer les drones de zones en zones pour arriver jusqu'a la zone d'arrivee (depuis le start).

Je peux donc recuperer mon parsing pour y trouver les infos necessaires :

Creation des drones
- creer tant de drones - create drone
- les mettre sur la zone start - add drone start_hub
- leur donner le pouvoir de se deplacer - move drone
-> Classe drone avec ID

Creer les zones ou pas besoin ?
-> Classe zone avec nom, couleur etc (avec metadatas en mode None si ya rien, autre si y'a)

Creer les connexions ?
-> Classe connexion ?????????????????

Creer algo

Creer l'output:
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
- d'une liste avec de listes avec les max_link_capacity (matrice C)
- index de start
- index de end
On obtient a la fin la quantite de drones pouvant avancer en meme temps
Il manque :
- la prise en compte des max_drones dans chaque zone
- la gestion des couts de deplacement (restricted = 2 tours)
Ce code est la base pure. Il faut y ajouter :
- Le node splitting pour les max_drones des zones
- La gestion des coûts de déplacement (restricted=2 turns) dans la simulation tour par tour
- La conversion des noms de zones en indices de matrice

Si max_link_capacity pas precisee alors c'est 1, si ya pas de lien entre les zones c'est donc 0

Si max_drones pas precise c'est 1 par defaut

Si zone pas precise c'est normal par defaut

Idees creation de la matrice C:
- si une zone est bloquee on met les liens avec elle a 0 comme ca personne n'y va jamais
- class Matrice, check les connexions entre les zones, cree une liste avec les liens

Le manager cree la Matrice en envoyant en param les configs de la map : connexions et types des zones avec leurs noms, puis return la liste des listes que le manager envoie en param quand il appelle l'algo

Mon algo doit me renvoyer, en + du nombre de drones a bouger simultanement, ma matrice F qui detiens les chemins que jaurai juste a assigner a chaque drone

Et la matrice doit etre doublee et chaque zone va etre splittee en 2 pour gerer et le max_link_capacity et le max_drones

start --3--> A(max_drones=2) --2--> end

start  → index 0  → start_in=0,  start_out=1
A      → index 1  → A_in=2,      A_out=3
end    → index 2  → end_in=4,    end_out=5

C[start_in][start_out]  = C[0][1] = 25  (nb_drones, pas de limite)
C[A_in][A_out]          = C[2][3] = 2   (max_drones=2)
C[end_in][end_out]      = C[4][5] = 25  (nb_drones, pas de limite)

C[start_out][A_in]  = C[1][2] = 3  (max_link_capacity=3)
C[A_out][start_in]  = C[3][0] = 3  (bidirectionnel)
C[A_out][end_in]    = C[3][4] = 2  (max_link_capacity=2)
C[end_out][A_in]    = C[5][2] = 2  (bidirectionnel)

s_in s_out A_in A_out e_in e_out
s_in  [  0,  25,   0,    0,   0,    0 ]
s_out [  0,   0,   3,    0,   0,    0 ]
A_in  [  0,   0,   0,    2,   0,    0 ]
A_out [  3,   0,   0,    0,   2,    0 ]
e_in  [  0,   0,   0,    0,   0,   25 ]
e_out [  0,   0,   2,    0,   0,    0 ]


DU COUP
- je vais creer une classe Manager pour gerer chaque transmission a chaque bon endroit
- cette classe prendra en param ma map validee par mon parsing (dict)
- elle va tout extraire ce dont on a besoin
- elle va creer les drones en appelant directement la classe dans son fichier
- elle va creer les zones aussi en appelant leur classe
- elle va aussi creer la matrice C a envoyer a l'algo (classe Matrice?)

Pour creer la matrice, on va avoir besoin des connections, des max_links, des noms des zones, leurs types (car si type blocked on mettra le link a 0), et si elles ont des max_drones
Du coup peut etre avant il faut creer la classe zone et creer toutes les zones?

Et plus tard creer les drones quand l'algo sera fini pour justement effectuer les mouvements trouves par l'algo renvoyes dans la matrice F

1 - parsing qui renvoie un dict DONE
-> creer la classe Manager qui recup le dict et creer les zones a partir de leur classe DONE
2 - creer les zones dans une classe Zone DONE
-> je sais pas trop quoi faire de ma classe zone par contre
3.5- Classe connection ? DONE
ou j'envoie mes connections a ma classe Zone

methodes check les connections pour les mettres dans une liste

3 - Construire la matrice C depuis les zones
4 - lancer l'algo pour obtenir matrice F
5 - extraire les chemins de F
6 - creer les drones
7 - assigner les chemins aux drones
8 - simulation tour par tour

Creer un file d'ou prendre mes couleurs

Tout ca dans gere par la classe Manager


Output visuel exemple :
Affichage couleur sur un terminal indiquant les mouvements des drones et l’état des zones ->

[ start: D1 ] [ waypoint1: empty ] [ waypoint2: empty ] [ goal: empty ]

Turn 1 : D1-waypoint1
[ start: empty ] [ waypoint1: D1 ] [ waypoint2: empty ] [ goal: empty ]

Turn 2 : D1-waypoint2
[ start: empty ] [ waypoint1: empty ] [ waypoint2: D1 ] [ goal: empty ]

Turn 3 : D1-goal
[ start: empty ] [ waypoint1: empty ] [ waypoint2: empty ] [ goal: D1 ]




jai trouve un truc oublie du parsing si je rajoute une metadata : [color=blue] [zone=normal] en les separant ca la prend pas en compte mais ca renvoie pas d'erreur donc renvoyer erreur

sinon continuer la matrice car si bloque on veut 0 lien par exemple
