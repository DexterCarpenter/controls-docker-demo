# Industrial Automation Controls Demo with Docker

This repository demonstrates how Docker can simplify the workflow of industrial automation controls engineers. It showcases the use of various services such as MQTT for communication, InfluxDB for data storage, and Python for automation tasks, all running inside Docker containers. This setup is ideal for building modular, scalable, and easy-to-deploy systems in an industrial setting.

## Services Overview

### 1. **Mosquitto (MQTT Broker)**

- **Image:** `eclipse-mosquitto:latest`
- **Description:** Mosquitto is an open-source MQTT broker that allows devices to communicate with each other using the MQTT protocol. In this setup, it's used for publishing and subscribing to messages across devices and services.
- **Ports:**
  - `1883`: MQTT port
  - `9001`: WebSocket port (optional for web-based clients)
- **Volumes:** Persistent configuration, data, and log storage.

### 2. **InfluxDB**

- **Image:** `influxdb:latest`
- **Description:** InfluxDB is a time-series database that's perfect for storing high-frequency data from automation systems, like sensor readings and machine states. This service is configured with an initial setup including a user, organization, bucket, and admin token.
- **Port:** `8086`
- **Volumes:** Persistent data storage for the database.

### 3. **Telegraf**

- **Image:** `telegraf:latest`
- **Description:** Telegraf is a plugin-driven agent for collecting, processing, and sending metrics and events. In this setup, it subscribes to the MQTT broker (Mosquitto) and writes data to InfluxDB.
- **Depends on:** `mosquitto`, `influxdb`
- **Volumes:** Configuration directory for Telegraf.

### 4. **Python Services**

- **Python 3.8, 3.10, and 3.12 Environments**
- **Description:** These Python services are examples of using Python to interface with MQTT and InfluxDB. They demonstrate how different Python versions can run in containers, helping you ensure compatibility across environments.
- **Build Contexts:** Each Python service builds from its respective Dockerfile and installs dependencies defined in a `requirements.txt` file, including FastAPI, paho-mqtt, and influxdb-client.

## Prerequisites

You need Docker and Docker Compose installed on your machine to run this project. Follow the instructions for your platform:

- [Install Docker on Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Install Docker on macOS](https://docs.docker.com/desktop/install/mac-install/)
- [Install Docker on Linux](https://docs.docker.com/engine/install/)

To check if Docker is installed, run:

```bash
docker --version
```

To check if Docker Compose is installed, run:

```bash
docker-compose --version
```

## How to Launch the Project

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/nnbutler/controls-docker-demo.git
   cd controls-docker-demo
   ```

2. **Build and Start the Services:**
   Use Docker Compose to build and run all services.

   ```bash
   docker-compose up --build
   ```

   This will:

   - Start the Mosquitto MQTT broker.
   - Start InfluxDB with an initial setup.
   - Launch Telegraf, which listens to MQTT and writes to InfluxDB.
   - Build and run Python services for versions 3.8, 3.10, and 3.12.

3. **Verify the Services:**

   - You can verify that Mosquitto is running by publishing a message to the MQTT topic:
     ```bash
     docker exec -it <container_name> mosquitto_pub -h localhost -t test -m "{"message": "ping"}"
     ```
   - Access InfluxDB via the browser at `http://localhost:8086` and log in with the credentials provided in the `docker-compose.yml` file.

4. **Stop the Services:**
   To stop the services, simply run:

   ```bash
   docker-compose down
   ```

## Customization

You can customize the configurations of Mosquitto, InfluxDB, and Telegraf by modifying the configuration files in the respective directories (`./mosquitto/config`,and `./telegraf`). You can also adjust the Python services by modifying the `main.py` script or adding additional scripts.

## Why Docker?

- **Isolation:** Each service runs in its container, eliminating the "it works on my machine" problem.
- **Scalability:** Easily add or remove services as needed.
- **Version Control:** Test your code across multiple Python versions with minimal effort.
- **Reproducibility:** Ensure that everyone on your team uses the same environment.

## Useful Links

- [Docker Documentation](https://docs.docker.com/)
- [MQTT Protocol](https://mqtt.org/)
- [InfluxDB Documentation](https://docs.influxdata.com/influxdb/latest/)
- [Telegraf Documentation](https://docs.influxdata.com/telegraf/latest/)
