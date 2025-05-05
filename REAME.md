
# MQTT-Based Disaster Relief System

This GitHub repo simulates how MQTT communications would take place in a disaster environment. It includes a publisher that broadcasts private data to a subscriber and another publisher with privacy-enhancing technologies (PETs) such as tokenization and optional payload encryption, which the subscriber can decrypt.
---

## Tools Used

| Tool              | Purpose                                      |
|------------------|----------------------------------------------|
| Python 3         | Primary programming language                 |
| Paho-MQTT        | Python MQTT client library for pub/sub       |
| Eclipse Mosquitto| MQTT Broker for message routing              |
| cryptography     | Fernet encryption for message confidentiality|
| Homebrew (macOS) | Installing Mosquitto broker                  |

---

## Installation Guide

### 1. Install Python (if not already installed)
Download Python from: https://www.python.org/downloads/

### 2. Clone this repository
```bash
git clone https://github.com/hzainal/cyse587extra
```

### 3. Install required Python packages
```bash
pip install -r requirements.txt
```


### 4. Install Mosquitto MQTT broker

#### macOS:
```bash
brew install mosquitto
brew services start mosquitto
```


---

## How to Run the Scenario

### Step 1: Start the Mosquitto broker
Ensure Mosquitto is running locally on port 1883:
```bash
mosquitto
```

### Step 2: Run the Subscriber
In a new terminal:
```bash
cd subscriber
python3 subscriber.py
```

### Step 3: Run the Publisher
In another terminal:
```bash
cd publisher
python3 publisher.py
```

All messages from the publisher have no PETs

### Step 4: Stop the Publisher execution

### Step 5: Run the PET Publisher
In another terminal:
```bash
cd publisher
python3 publisherPET.py
```

The publisher sends pseudonymized and optionally encrypted messages to the subscriber over MQTT.

---

## Interpreting the Results

- **Before PETs**: Messages contained data such as the victim's GPS coordinates in plaintext
- **After PETs**: Messages use tokenized victim IDs and location zones instead of raw GPS and can be encrypted using Fernet.
- The improvement is measured using a **Sensitive Field Exposure Metric**:
  - **Before**: 5 sensitive fields exposed (Victim ID, GPS, IP, Temp, Severity)
  - **After**: Only two exposed (Temp, Severity) — IDs and location are anonymized/encrypted

This shows a measurable privacy improvement and supports threat mitigation for linkability, identifiability, and disclosure.
---

Code Adapter from specific files in https://github.com/kabartsjc/disaster_project/tree/main

