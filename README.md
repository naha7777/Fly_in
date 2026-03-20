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
- https://www.datacamp.com/tutorial/dijkstra-algorithm-in-python
- https://rich.readthedocs.io/en/latest/introduction.html

- creer l'algo pour 1 drone + l'output
- ensuite creer classe Drones que le manager (classe) va appeler pour creer le nombre de drones dans create_drones avec un ID, le meilleur chemin
- les drones ont une methode avancer
