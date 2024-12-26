# legos

Site web démo pour les TP de programmation web en BDW.

Prérequis (voir la page de l'UE pour les étapes détaillées) : 

- installer le serveur `bdw-server` (voir page de l'UE)
- installer `legos` (jeu de données, configuration config-bd.toml, déplacement du répertoire)
- lancer legos :
```sh
# activer l'environnement virtuel (déjà créé) dans bdw-server/
source .venv/bin/activate  # ou .venv\Scripts\activate sous windows
# lancer le serveur avec le paramètre DIRECTORY qui contient votre site web
python server.py serial_critique
# si tout est ok, aller sur http://localhost:4242/ (URL par défaut)
```


## Contact

Fabien Duchateau (Université Claude Bernard Lyon 1), <prénom.nom@univ-lyon1.fr>

