Brain storming :

Dans l'exercice on doit faire avancer les drones de zones en zones pour arriver jusqu'a la zone d'arrivee (depuis le start).

D'abord on a une map nous indiquant :
- le nombre de drone a creer
- la zone start avec son nom, ses coordonnees et sa couleur/la capacite/type de zone
- d'autres zones avec pareil
- la zone de fin avec pareil
- puis les connections pour nous indiquer les deplacements possibles des drones

On doit creer autant de drones que le nombre indique. Il doit y en avoir au moins 1 sinon ERROR. DONE

verif .txt DONE

On doit ignorer les commentaires DONE

Il y a des keys obligatoires DONE

Il y a plusieurs types de zones : restricted, normal, priority, blocked DONE

Une fois la map parsée et validée, on crée les drones et on les mets sur la zone de depart.
On fait l'algo pour trouver le chemin le plus court

- Premiere ligne de la map doit etre le nombre de drones ! DONE
- Un seul start_hub et un seul end_hub DONE
- chaque zone a un nom unique DONE
- chaque zone a des coordonnees valides DONE JE CROIS
- les noms des zones peuvent utiliser n'importe quel caractere sauf les - et espaces DONE
- les connections doivent relier des zones prealablement  DONE
- pas la meme connection 2 fois DONE
- les metadatas doivent etre syntaxiquement correctes DONE
- les types de zones doivent etre parmi : normal, blocked, restricted, priority sinon error DONE
- max_drones DONE et MAX_LINK_CAPACITYYYYYYY doivent etre des int positifs DONE
- n'importe quelle autre erreur de parsing doit stopper le programe et retourner un message clair indiquant la ligne et la cause

PARSING FINIT :
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
- https://www.datacamp.com/tutorial/dijkstra-algorithm-in-python
- https://rich.readthedocs.io/en/latest/introduction.html

- le main appelle la classe Maps avec en parametre l'argument c'est a dire le fichier .txt donne.
- on arrive dans notre classe Maps qu'on initialise avec en param un fichier.
- on cree un dict self.config dans lequel on va pouvoir enregistrer la config de notre map
-- il faudrait peut etre un manager de map qui a un dictionnaire pour chaque map en mode {"01.txt": "sa map validee donc sa config"}
- on initialise un i, un j, une liste pour mettre notre premiere key et verif que c'est pas nb_drones en premier, une variable pour compter le nombre de start_hub, une pour le nombre de end_hub, une pour le nombre de lignes, et une liste des keys obligatoires.
- on ouvre le fichier qu'on splite a chaque fin de ligne et qu'on stocke dans la variable map_content.
- on cree deux listes : une pour savoir a quelles lignes sont les hubs et une autre pour savoir a quelles lignes sont les connexions.
- ensuite pour chaque ligne de notre map on l'ignore si elle commence par # ou si elle est vide, si elle commence par start_hub on augmente le compte du start, pareil pour end_hub, si il y a 2 start_hub ou 2 end_hub alors on renvoie une erreur
- ensuite, si il n'y a encore rien dans la liste first_key, on regarde qu'elle est la premiere key de la map, si ce n'est pas nb_drones, on met la key dans la liste comme ca quand nb_drones arrivera et que la liste aura deja un element, on saura que nb_drones n'etait pas la premiere key et donc on renverra une erreur
- une fois qu'on a fait ces verifs de base, on va diviser notre ligne en deux pour separer la key de sa valeur dans une variable s'appelant param. Si la taille du param n'est pas deux, cela veut dire que la key n'avait pas de valeur et donc on renvoie une erreur.
- ensuite on met au propre la key et la valeur qu'on separe dans des variables a ces noms, ensuite on check que la key fait bien partie des key obligatoires, si elle est bien ecrite etc. SI ce n'est pas le cas on renvoie une erreur : key invalide.
- si la key est hub ou connection, vu qu'on ne veut pas que les hubs s'ecrasent les uns les autres, on ajoute un numero au nom de la key puis on ajoute la key et sa value dans le self.config
- ensuite on compte la ligne a laquelle apparait chaque cle pour pouvoir return des erreurs plus precises.
- enfin on regarde si toutes les keys sont presentes dans la map, si il y a une key obligatoire qui est manquante, on renvoie une erreur.
- une fois ces premieres verif de faites, on les envoie a notre classe MapConfig qui va gerer les field etc.
- une fois les verifs de base faites, des methodes appellent une fonction validate qui va verifier precisement si les values des clefs sont correctes : syntaxe, coordonnees, pas de double nom, pas de double connexion, etc.
- si il n'y a aucune erreur alors on met tout dans un dictionnaire map_valid



Du coup pour commencer dans mon main jappelle ma fonction manager qui recupere les donnees de la config validee.

Je regarde le nombre de drones a creer et je les cree dans le manager avec ma classe Drones dans drones.py
Mon manager doit pouvoir gerer tous les drones. = Classe Manager ?

Je dois compter les tours aussi
