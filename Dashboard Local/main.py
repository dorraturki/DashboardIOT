import paho.mqtt.client as mqtt
import time
import socket
import sqlite3
from datetime import datetime

# Paramètres MQTT
BROKER = "" #Replace with broker name
PORT = 1883
TOPICS = [
    ("/Courant1", 0),
    ("/Tension1", 0),
    ("/Power1", 0),
    ("/Energy1", 0),
    ("/Power_Factor1", 0)
]

# Variables de données
courant = None
tension = None
puissance = None
energie = None
facteur_puissance = None
is_connected = False

# Connexion SQLite
conn = sqlite3.connect("mesures_mqtt.db", check_same_thread=False)
cursor = conn.cursor()

# Création de la table
cursor.execute("""
CREATE TABLE IF NOT EXISTS mesures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    courant REAL,
    tension REAL,
    puissance REAL,
    energie REAL,
    facteur_puissance REAL
)
""")
conn.commit()

# Vérifie la connexion internet
def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

# Callback de connexion MQTT
def on_connect(client, userdata, flags, rc):
    global is_connected
    if rc == 0:
        print("Client MQTT connecté")
        is_connected = True
        client.subscribe(TOPICS)
    else:
        print("Erreur de connexion MQTT:", rc)

# Callback de réception MQTT
def on_message(client, userdata, msg):
    global courant, tension, puissance, energie, facteur_puissance

    topic = msg.topic
    value = float(msg.payload.decode())

    if topic == "/Courant1":
        courant = value
    elif topic == "/Tension1":
        tension = value
    elif topic == "/Power1":
        puissance = value
    elif topic == "/Energy1":
        energie = value
    elif topic == "/Power_Factor1":
        facteur_puissance = value

    # Vérifie si toutes les valeurs sont présentes avant insertion
    if None not in (courant, tension, puissance, energie, facteur_puissance):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Courant: {courant} A | Tension: {tension} V | Puissance: {puissance} W | Énergie: {energie} Wh | FP: {facteur_puissance}")

        cursor.execute("""
        INSERT INTO mesures (timestamp, courant, tension, puissance, energie, facteur_puissance)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, courant, tension, puissance, energie, facteur_puissance))
        conn.commit()

# Callback de déconnexion
def on_disconnect(client, userdata, rc):
    global is_connected
    is_connected = False
    print("Client MQTT déconnecté")

# Configuration du client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

# Boucle principale
try:
    while True:
        if check_internet():
            print("Réseau OK")
        else:
            print("Pas d'accès réseau")

        if not is_connected and check_internet():
            try:
                print("Tentative de reconnexion MQTT...")
                client.reconnect()
            except Exception as e:
                print("Erreur:", e)

        time.sleep(5)

except KeyboardInterrupt:
    print("Arrêt du programme...")
    client.loop_stop()
    client.disconnect()
    conn.close()

    
