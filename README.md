# Dashboard IOT - Local & Cloud Data Visualization

This project implements a complete IoT data collection and visualization chain, enabling monitoring of electrical parameters (current, voltage, power, etc.) via both local and cloud-based dashboards.

It demonstrates techniques for real-time data acquisition, storage, and visualization using MQTT, SQLite, InfluxDB, and Grafana.

## Project Objectives

- Set up an MQTT client to receive sensor data.
- Store data locally using SQLite for offline analysis.
- Visualize measurements with a Grafana dashboard (locally).
- Migrate to a cloud-based system using InfluxDB Cloud & Grafana Cloud.
- Compare local and cloud solutions for accessibility, scalability, and maintenance.

## Technologies Used

- **Python**: Main logic for MQTT client, data parsing, and database integration.
- **MQTT (Mosquitto)**: Protocol for receiving sensor data.
- **SQLite**: Local lightweight database to store time-series measurements.
- **Grafana (Local)**: Dashboarding tool to visualize data from SQLite.
- **InfluxDB Cloud**: Time-series database in the cloud.
- **Grafana Cloud**: For remote visualization from anywhere.

## Dashboards Preview

Local and cloud dashboards feature:
- Time-series plots (current, voltage, power, energy)
- Gauges for instant values
- Real-time data updates
