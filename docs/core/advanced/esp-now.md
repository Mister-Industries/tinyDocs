---
title: ESP-NOW
publish: true
date: 2025-01-27 12:00:00
update: 2025-01-27 12:00:00
description: Learn how to use ESP-NOW for device-to-device communication with tinyCore
categories:
  - advanced
  - connectivity
---

# ESP-NOW 🔗

ESP-NOW is a wireless communication protocol developed by Espressif that allows direct device-to-device communication without requiring a WiFi router. Perfect for creating networks of tinyCore devices!

## What is ESP-NOW?

ESP-NOW is a connectionless communication protocol that enables:
- **Direct communication** - No WiFi router required
- **Low latency** - Fast data transmission
- **Low power** - Efficient for battery-powered devices
- **Mesh networks** - Multiple device communication
- **Encryption** - Secure data transmission

## Key Features

### ✅ **What ESP-NOW Can Do**

- **Device-to-Device** - Direct tinyCore to tinyCore communication
- **Sensor Networks** - Multiple sensor nodes reporting to a central device
- **Remote Control** - Control one tinyCore from another
- **Data Broadcasting** - Send data to multiple devices simultaneously
- **Mesh Networks** - Create complex network topologies

### 🔗 **Common Use Cases**

- **Sensor Networks** - Environmental monitoring across multiple locations
- **Remote Controls** - Control devices from a central controller
- **Data Logging** - Collect data from multiple sensors
- **Home Automation** - Control lights, appliances, and sensors
- **IoT Networks** - Internet of Things device networks

## Getting Started

### Prerequisites

1. **Multiple tinyCore Boards** - At least 2 for testing
2. **Arduino IDE** - With ESP32 board support
3. **WiFi Library** - ESP-NOW requires WiFi initialization

### Basic ESP-NOW Example

```cpp
#include <esp_now.h>
#include <WiFi.h>

// ESP-NOW peer info
esp_now_peer_info_t peerInfo;

// Data structure for messages
typedef struct struct_message {
    int id;
    int x;
    int y;
    String message;
} struct_message;

struct_message myData;
struct_message incomingData;

// Callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
    char macStr[18];
    snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
             mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
    Serial.print("Last Packet Sent to: ");
    Serial.println(macStr);
    Serial.print("Last Packet Send Status: ");
    Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}

// Callback when data is received
void OnDataRecv(const uint8_t *mac, const uint8_t *incomingData, int len) {
    memcpy(&incomingData, incomingData, sizeof(incomingData));
    Serial.print("Bytes received: ");
    Serial.println(len);
    Serial.print("ID: ");
    Serial.println(incomingData.id);
    Serial.print("X: ");
    Serial.println(incomingData.x);
    Serial.print("Y: ");
    Serial.println(incomingData.y);
    Serial.print("Message: ");
    Serial.println(incomingData.message);
}

void setup() {
    Serial.begin(115200);
    
    // Set device as a Wi-Fi Station
    WiFi.mode(WIFI_STA);

    // Init ESP-NOW
    if (esp_now_init() != ESP_OK) {
        Serial.println("Error initializing ESP-NOW");
        return;
    }

    // Set up callbacks
    esp_now_register_send_cb(OnDataSent);
    esp_now_register_recv_cb(OnDataRecv);

    // Register peer
    memcpy(peerInfo.peer_addr, broadcastAddress, 6);
    peerInfo.channel = 0;
    peerInfo.encrypt = false;

    // Add peer
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        Serial.println("Failed to add peer");
        return;
    }
}

void loop() {
    // Prepare data
    myData.id = 1;
    myData.x = random(0, 100);
    myData.y = random(0, 100);
    myData.message = "Hello from tinyCore!";

    // Send data
    esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));
    if (result == ESP_OK) {
        Serial.println("Sent with success");
    } else {
        Serial.println("Error sending the data");
    }
    delay(2000);
}
```

## Advanced Features

### Peer Management

Manage multiple ESP-NOW peers:

```cpp
// Add multiple peers
void addPeer(uint8_t* macAddress) {
    esp_now_peer_info_t peerInfo;
    memcpy(peerInfo.peer_addr, macAddress, 6);
    peerInfo.channel = 0;
    peerInfo.encrypt = false;
    
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        Serial.println("Failed to add peer");
    }
}

// Remove peer
void removePeer(uint8_t* macAddress) {
    if (esp_now_del_peer(macAddress) != ESP_OK) {
        Serial.println("Failed to delete peer");
    }
}
```

### Encryption

Enable encryption for secure communication:

```cpp
// Set up encrypted communication
void setupEncryptedPeer(uint8_t* macAddress) {
    esp_now_peer_info_t peerInfo;
    memcpy(peerInfo.peer_addr, macAddress, 6);
    peerInfo.channel = 0;
    peerInfo.encrypt = true;
    
    // Set encryption key (16 bytes)
    uint8_t key[16] = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
                       0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10};
    memcpy(peerInfo.lmk, key, 16);
    
    esp_now_add_peer(&peerInfo);
}
```

### Channel Hopping

Improve reliability with channel hopping:

```cpp
// Switch channels periodically
int currentChannel = 1;
const int maxChannel = 13;

void switchChannel() {
    currentChannel = (currentChannel % maxChannel) + 1;
    WiFi.channel(currentChannel);
    
    // Update all peers to new channel
    esp_now_peer_info_t peerInfo;
    for (int i = 0; i < esp_now_get_peer_num(); i++) {
        esp_now_get_peer_info(i, &peerInfo);
        peerInfo.channel = currentChannel;
        esp_now_mod_peer(&peerInfo);
    }
}
```

## Project Examples

### 1. Sensor Network

Create a network of sensor nodes reporting to a central device:

```cpp
// Sensor Node Code
typedef struct {
    int nodeId;
    float temperature;
    float humidity;
    int lightLevel;
    unsigned long timestamp;
} sensor_data_t;

sensor_data_t sensorData;

void setup() {
    // Initialize sensors
    // Setup ESP-NOW
    // Register with central node
}

void loop() {
    // Read sensors
    sensorData.nodeId = 1;
    sensorData.temperature = readTemperature();
    sensorData.humidity = readHumidity();
    sensorData.lightLevel = readLight();
    sensorData.timestamp = millis();
    
    // Send to central node
    esp_now_send(centralNodeMac, (uint8_t*)&sensorData, sizeof(sensorData));
    delay(5000);
}
```

### 2. Remote Control System

Control multiple devices from a central controller:

```cpp
// Controller Code
typedef struct {
    int deviceId;
    int command;
    int value;
} control_message_t;

void sendCommand(int deviceId, int command, int value) {
    control_message_t msg;
    msg.deviceId = deviceId;
    msg.command = command;
    msg.value = value;
    
    // Send to specific device or broadcast
    esp_now_send(targetMac, (uint8_t*)&msg, sizeof(msg));
}

// Device Code
void OnDataRecv(const uint8_t *mac, const uint8_t *data, int len) {
    control_message_t msg;
    memcpy(&msg, data, sizeof(msg));
    
    if (msg.deviceId == MY_DEVICE_ID) {
        switch(msg.command) {
            case CMD_LED_ON:
                digitalWrite(LED_PIN, HIGH);
                break;
            case CMD_LED_OFF:
                digitalWrite(LED_PIN, LOW);
                break;
            case CMD_SET_BRIGHTNESS:
                analogWrite(LED_PIN, msg.value);
                break;
        }
    }
}
```

### 3. Mesh Network

Create a mesh network for data routing:

```cpp
// Mesh node with routing capability
typedef struct {
    int sourceId;
    int targetId;
    int hopCount;
    String data;
} mesh_message_t;

void routeMessage(mesh_message_t msg) {
    if (msg.targetId == MY_DEVICE_ID) {
        // Process message for this device
        processMessage(msg);
    } else {
        // Forward message to next hop
        msg.hopCount++;
        if (msg.hopCount < MAX_HOPS) {
            forwardMessage(msg);
        }
    }
}
```

## Network Topologies

### Star Network
```
    Central Node
    /     |     \
Node1   Node2   Node3
```

### Mesh Network
```
Node1 ---- Node2 ---- Node3
  |         |         |
  |         |         |
Node4 ---- Node5 ---- Node6
```

### Chain Network
```
Node1 -> Node2 -> Node3 -> Node4
```

## Performance Optimization

### Power Management

```cpp
// Reduce power consumption
void setupLowPower() {
    // Set WiFi to low power mode
    WiFi.setSleep(true);
    
    // Use deep sleep between transmissions
    esp_sleep_enable_timer_wakeup(5000000); // 5 seconds
}

void loop() {
    // Send data
    sendData();
    
    // Enter deep sleep
    esp_deep_sleep_start();
}
```

### Data Throughput

```cpp
// Optimize for high data rates
void setupHighThroughput() {
    // Use larger packets
    esp_now_set_pmk((uint8_t*)"pmk1234567890123", 16);
    
    // Reduce transmission intervals
    // Use multiple channels
}
```

## Troubleshooting

### Common Issues

1. **Devices Not Connecting**
   - Check MAC addresses are correct
   - Ensure devices are on same channel
   - Verify WiFi mode is set correctly

2. **Data Loss**
   - Reduce transmission distance
   - Check for interference
   - Implement acknowledgment system

3. **High Latency**
   - Optimize data structures
   - Reduce network size
   - Use channel hopping

### Debug Tools

```cpp
// Enable debugging
#define ESP_NOW_DEBUG 1

// Monitor network status
void printNetworkStatus() {
    Serial.print("Number of peers: ");
    Serial.println(esp_now_get_peer_num());
    
    Serial.print("WiFi channel: ");
    Serial.println(WiFi.channel());
}
```

## Best Practices

### Security
- Use encryption for sensitive data
- Implement authentication
- Regularly rotate encryption keys

### Reliability
- Implement acknowledgment systems
- Use multiple channels
- Add error checking

### Scalability
- Design for network growth
- Use efficient data structures
- Implement routing protocols

## Next Steps

- **Explore WiFi** - For internet connectivity
- **Learn about Mesh Networks** - For complex topologies
- **Check out User Projects** - See real-world examples
- **Join the Community** - Get help on Discord

---

*Ready to build device networks? Start with the [Sensor Network Tutorial](../../get-started/collects-data) or explore [other connectivity options](../../get-started/index)!* 