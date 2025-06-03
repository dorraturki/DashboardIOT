# Projet IOT - Dossier Cloud

## Fichiers principaux

- **main.py** : Ce script lit les données des capteurs via MQTT et les envoie directement vers InfluxDB Cloud.
- **dashboard.json** : Fichier de configuration permettant d'importer un tableau de bord Grafana Cloud connecté à InfluxDB Cloud.

## Utilisation

1. Exécutez `main.py` pour lancer l’abonnement MQTT et envoyer les données vers InfluxDB Cloud.

2. Connectez-vous à Grafana Cloud, ajoutez InfluxDB Cloud comme source de données (via l’interface `Connections > Data Sources`), puis :

   - Cliquez sur `+ > Import`,
   - Chargez le fichier `dashboard.json`,
   - Sélectionnez votre source InfluxDB configurée.

Le tableau de bord vous permettra de visualiser les données électriques (courant, tension, puissance, énergie, facteur de puissance) en temps réel, directement depuis le cloud.

