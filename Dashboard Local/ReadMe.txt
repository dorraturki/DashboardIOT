# Projet IOT - Documentation

## Fichiers principaux

- **main.py** : Ce script lit les données des capteurs et les enregistre dans la base de données `mesures_mqtt.db`.
- **mesures_mqtt.db** : Base de données SQLite contenant les mesures collectées.
- **dashboard.json** : Fichier de configuration pour le dashboard Grafana d'affichage des données.

## Utilisation

1. Exécutez `main.py` pour collecter et stocker les données.
2. Utilisation de `dashboard.json` pour visualiser les données de `mesures_mqtt.db` :

Ouvrez Grafana en local, ajoutez une source de données de type SQLite pointant vers le fichier `mesures_mqtt.db`. Ensuite, importez le fichier `dashboard.json` depuis le menu Import de Grafana. Lors de l'import, associez-le à la source SQLite créée.

Cela permettra d’afficher le tableau de bord complet avec les graphiques des mesures électriques (courant, tension, puissance, énergie, facteur de puissance), mis à jour en temps réel à partir de la base locale.
