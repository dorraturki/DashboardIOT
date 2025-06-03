import paho.mqtt.client as mqtt
import time
import socket
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Paramètres MQTT
BROKER = "broker.hivemq.com"
PORT = 1883
TOPICS = [
    ("/Courant1", 0),
    ("/Tension1", 0),
    ("/Power1", 0),
    ("/Energy1", 0),
    ("/Power_Factor1", 0)
]

# Paramètres InfluxDB Cloud
INFLUXDB_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"  # Replace with your InfluxDB Cloud region URL
INFLUXDB_TOKEN = "2VMfJddGfWuSNNJbMyz6rSgQD7gCKSvkdnixFei8urFXlkYk18gz2rsP8TiBgwXMJ7BNL0CWIIQMY3w3gDQWhQ=="  # Replace with your InfluxDB Cloud API token
INFLUXDB_ORG = "Study"  # Replace with your InfluxDB organization
INFLUXDB_BUCKET = "electric_data"  # Replace with your bucket name


# Variables de données
courant = None
tension = None
puissance = None
energie = None
facteur_puissance = None
is_connected = False

# Connexion InfluxDB
client_influx = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client_influx.write_api(write_options=SYNCHRONOUS)

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
        timestamp = datetime.utcnow()  # Use UTC for InfluxDB
        print(f"[{timestamp}] Courant: {courant} A | Tension: {tension} V | Puissance: {puissance} W | Énergie: {energie} Wh | FP: {facteur_puissance}")

        # Create InfluxDB point
        point = Point("mesures") \
            .tag("source", "mqtt_client") \
            .field("courant", courant) \
            .field("tension", tension) \
            .field("puissance", puissance) \
            .field("energie", energie) \
            .field("facteur_puissance", facteur_puissance) \
            .time(timestamp, WritePrecision.NS)

        # Write to InfluxDB
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

# Callback de déconnexion
def on_disconnect(client, userdata, rc):
    global is_connected
    is_connected = False
    print("Client MQTT déconnecté")

# Configuration du client MQTT
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
    client_influx.close()
