---
title: WiFi
publish: true
date: 2025-01-27 12:00:00
update: 2025-01-27 12:00:00
description: Learn how to use WiFi for internet connectivity with tinyCore
categories:
  - advanced
  - connectivity
---

# WiFi 🌐

tinyCore includes built-in WiFi capabilities, allowing you to connect to the internet and create web-enabled projects. Perfect for IoT applications, data logging, and remote monitoring!

## What is WiFi?

WiFi enables tinyCore to:
- **Connect to the Internet** - Access web services and APIs
- **Create Web Servers** - Host web pages and APIs
- **Send Data to Cloud** - Upload sensor data to databases
- **Remote Control** - Control devices from anywhere
- **Real-time Communication** - WebSocket and MQTT support

## Key Features

### ✅ **What tinyCore WiFi Can Do**

- **Internet Access** - Connect to web services and APIs
- **Web Server** - Host web pages and REST APIs
- **Cloud Integration** - Upload data to IoT platforms
- **Remote Monitoring** - Check device status from anywhere
- **Real-time Updates** - Live data streaming

### 🌐 **Common Use Cases**

- **IoT Devices** - Smart home sensors and controllers
- **Data Logging** - Upload sensor data to cloud databases
- **Remote Control** - Control devices via web interface
- **Weather Stations** - Environmental monitoring with web display
- **Home Automation** - Smart home hub functionality

## Getting Started

### Prerequisites

1. **tinyCore Board** - Any tinyCore variant
2. **WiFi Network** - 2.4GHz WiFi network
3. **Arduino IDE** - With ESP32 board support
4. **WiFi Credentials** - Network name and password

### Basic WiFi Connection

```cpp
#include <WiFi.h>

// WiFi credentials
const char* ssid = "YourWiFiNetwork";
const char* password = "YourWiFiPassword";

void setup() {
    Serial.begin(115200);
    
    // Connect to WiFi
    WiFi.begin(ssid, password);
    
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("");
    Serial.println("WiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}

void loop() {
    // Check WiFi connection
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi connection lost. Reconnecting...");
        WiFi.reconnect();
    }
    
    delay(1000);
}
```

## Web Server Examples

### Basic Web Server

```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "YourWiFiNetwork";
const char* password = "YourWiFiPassword";

WebServer server(80);

void setup() {
    Serial.begin(115200);
    
    // Connect to WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("");
    Serial.println("WiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    
    // Setup web server routes
    server.on("/", handleRoot);
    server.on("/led", handleLED);
    server.on("/sensor", handleSensor);
    
    server.begin();
    Serial.println("HTTP server started");
}

void loop() {
    server.handleClient();
}

void handleRoot() {
    String html = "<html><body>";
    html += "<h1>tinyCore Web Server</h1>";
    html += "<p><a href='/led'>Control LED</a></p>";
    html += "<p><a href='/sensor'>Sensor Data</a></p>";
    html += "</body></html>";
    
    server.send(200, "text/html", html);
}

void handleLED() {
    String state = server.hasArg("state") ? server.arg("state") : "";
    
    if (state == "on") {
        digitalWrite(LED_BUILTIN, HIGH);
        server.send(200, "text/plain", "LED ON");
    } else if (state == "off") {
        digitalWrite(LED_BUILTIN, LOW);
        server.send(200, "text/plain", "LED OFF");
    } else {
        server.send(400, "text/plain", "Invalid state");
    }
}

void handleSensor() {
    // Read sensor data
    float temperature = readTemperature();
    float humidity = readHumidity();
    
    String json = "{";
    json += "\"temperature\":" + String(temperature) + ",";
    json += "\"humidity\":" + String(humidity);
    json += "}";
    
    server.send(200, "application/json", json);
}
```

### REST API Server

```cpp
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

WebServer server(80);

void setup() {
    // WiFi setup...
    
    // API endpoints
    server.on("/api/sensors", HTTP_GET, getSensors);
    server.on("/api/led", HTTP_POST, setLED);
    server.on("/api/config", HTTP_PUT, updateConfig);
    
    server.begin();
}

void getSensors() {
    DynamicJsonDocument doc(200);
    
    doc["temperature"] = readTemperature();
    doc["humidity"] = readHumidity();
    doc["light"] = readLight();
    doc["timestamp"] = millis();
    
    String response;
    serializeJson(doc, response);
    
    server.send(200, "application/json", response);
}

void setLED() {
    if (server.hasArg("plain")) {
        DynamicJsonDocument doc(200);
        deserializeJson(doc, server.arg("plain"));
        
        bool state = doc["state"];
        digitalWrite(LED_PIN, state);
        
        server.send(200, "application/json", "{\"status\":\"success\"}");
    } else {
        server.send(400, "application/json", "{\"error\":\"No data\"}");
    }
}
```

## Cloud Integration

### MQTT Client

```cpp
#include <WiFi.h>
#include <PubSubClient.h>

const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "tinycore/sensors";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
    // WiFi setup...
    
    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(callback);
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
    
    // Publish sensor data every 30 seconds
    static unsigned long lastMsg = 0;
    if (millis() - lastMsg > 30000) {
        lastMsg = millis();
        
        String data = "{\"temperature\":" + String(readTemperature()) + "}";
        client.publish(mqtt_topic, data.c_str());
    }
}

void callback(char* topic, byte* payload, unsigned int length) {
    String message = "";
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];
    }
    
    Serial.print("Message received: ");
    Serial.println(message);
}

void reconnect() {
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        String clientId = "tinyCore-";
        clientId += String(random(0xffff), HEX);
        
        if (client.connect(clientId.c_str())) {
            Serial.println("connected");
            client.subscribe("tinycore/commands");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" retrying in 5 seconds");
            delay(5000);
        }
    }
}
```

### HTTP Client

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

void sendDataToCloud() {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        
        // Prepare data
        String data = "{\"temperature\":" + String(readTemperature()) + 
                     ",\"humidity\":" + String(readHumidity()) + "}";
        
        // Send to cloud service
        http.begin("https://api.example.com/data");
        http.addHeader("Content-Type", "application/json");
        http.addHeader("Authorization", "Bearer your-api-key");
        
        int httpResponseCode = http.POST(data);
        
        if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.println("HTTP Response: " + response);
        } else {
            Serial.println("Error on HTTP request");
        }
        
        http.end();
    }
}
```

## Advanced Features

### WebSocket Server

```cpp
#include <WiFi.h>
#include <WebSocketsServer.h>

WebSocketsServer webSocket = WebSocketsServer(81);

void setup() {
    // WiFi setup...
    
    webSocket.begin();
    webSocket.onEvent(webSocketEvent);
}

void loop() {
    webSocket.loop();
    
    // Send real-time sensor data
    static unsigned long lastUpdate = 0;
    if (millis() - lastUpdate > 1000) {
        lastUpdate = millis();
        
        String data = "{\"temperature\":" + String(readTemperature()) + "}";
        webSocket.broadcastTXT(data);
    }
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
    switch(type) {
        case WStype_DISCONNECTED:
            Serial.printf("[%u] Disconnected!\n", num);
            break;
        case WStype_CONNECTED:
            Serial.printf("[%u] Connected!\n", num);
            break;
        case WStype_TEXT:
            // Handle incoming messages
            String message = String((char*)payload);
            Serial.println("Received: " + message);
            break;
    }
}
```

### OTA (Over-the-Air) Updates

```cpp
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <AsyncElegantOTA.h>

AsyncWebServer server(80);

void setup() {
    // WiFi setup...
    
    // Enable OTA updates
    AsyncElegantOTA.begin(&server);
    
    server.begin();
}

void loop() {
    // OTA updates handled automatically
}
```

## Security Features

### HTTPS Support

```cpp
#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>

// For HTTPS requests
void secureRequest() {
    HTTPClient https;
    
    https.begin("https://api.example.com/secure-endpoint");
    https.addHeader("Authorization", "Bearer your-token");
    
    int httpCode = https.GET();
    if (httpCode > 0) {
        String payload = https.getString();
        Serial.println(payload);
    }
    
    https.end();
}
```

### WiFi Security

```cpp
// WPA2 Enterprise (if needed)
void setupEnterpriseWiFi() {
    WiFi.begin(ssid, username, password, identity);
}
```

## Project Examples

### 1. Weather Station

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

void uploadWeatherData() {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        
        // Read sensors
        float temperature = readTemperature();
        float humidity = readHumidity();
        float pressure = readPressure();
        
        // Create JSON payload
        DynamicJsonDocument doc(200);
        doc["temperature"] = temperature;
        doc["humidity"] = humidity;
        doc["pressure"] = pressure;
        doc["timestamp"] = millis();
        
        String payload;
        serializeJson(doc, payload);
        
        // Upload to weather service
        http.begin("https://weather-api.example.com/data");
        http.addHeader("Content-Type", "application/json");
        
        int httpCode = http.POST(payload);
        if (httpCode == 200) {
            Serial.println("Weather data uploaded successfully");
        }
        
        http.end();
    }
}
```

### 2. Smart Home Hub

```cpp
#include <WiFi.h>
#include <WebServer.h>
#include <PubSubClient.h>

WebServer server(80);
PubSubClient mqttClient;

void setup() {
    // WiFi setup...
    
    // Web server routes
    server.on("/", handleHomePage);
    server.on("/api/devices", handleDevices);
    server.on("/api/control", handleControl);
    
    // MQTT setup
    mqttClient.setServer("broker.example.com", 1883);
    mqttClient.setCallback(mqttCallback);
    
    server.begin();
}

void handleHomePage() {
    String html = "<html><body>";
    html += "<h1>Smart Home Hub</h1>";
    html += "<div id='devices'></div>";
    html += "<script>";
    html += "fetch('/api/devices').then(r=>r.json()).then(d=>{";
    html += "  document.getElementById('devices').innerHTML = JSON.stringify(d);";
    html += "});";
    html += "</script>";
    html += "</body></html>";
    
    server.send(200, "text/html", html);
}

void handleDevices() {
    // Return list of connected devices
    String json = "[";
    json += "{\"id\":\"light1\",\"name\":\"Living Room Light\",\"state\":\"on\"},";
    json += "{\"id\":\"sensor1\",\"name\":\"Temperature Sensor\",\"value\":\"23.5°C\"}";
    json += "]";
    
    server.send(200, "application/json", json);
}
```

### 3. Data Logger

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <SD.h>

void logDataToCloud() {
    if (WiFi.status() == WL_CONNECTED) {
        // Read from SD card
        File file = SD.open("/data.csv", FILE_READ);
        if (file) {
            HTTPClient http;
            http.begin("https://data-api.example.com/upload");
            http.addHeader("Content-Type", "text/csv");
            
            // Send file content
            int httpCode = http.POST(file);
            if (httpCode == 200) {
                Serial.println("Data uploaded successfully");
                // Clear file after successful upload
                file.close();
                SD.remove("/data.csv");
            }
            
            http.end();
        }
    }
}
```

## Performance Optimization

### Power Management

```cpp
// Reduce WiFi power consumption
void setupLowPowerWiFi() {
    WiFi.setSleep(true);
    WiFi.setTxPower(WIFI_POWER_MINUS_1dBm);
}

// Deep sleep with WiFi
void deepSleepWithWiFi() {
    esp_sleep_enable_timer_wakeup(30000000); // 30 seconds
    esp_wifi_stop();
    esp_deep_sleep_start();
}
```

### Connection Management

```cpp
// Automatic reconnection
void checkWiFiConnection() {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi connection lost. Reconnecting...");
        WiFi.reconnect();
        delay(5000);
    }
}
```

## Troubleshooting

### Common Issues

1. **Connection Failures**
   - Check WiFi credentials
   - Verify network availability
   - Check signal strength

2. **Web Server Issues**
   - Check port availability
   - Verify HTML syntax
   - Test with different browsers

3. **MQTT Problems**
   - Verify broker address
   - Check authentication
   - Test with MQTT client

### Debug Tools

```cpp
// WiFi diagnostic
void printWiFiStatus() {
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());
    Serial.print("Signal strength: ");
    Serial.println(WiFi.RSSI());
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}
```

## Best Practices

### Security
- Use HTTPS for sensitive data
- Implement authentication
- Regularly update passwords

### Reliability
- Implement reconnection logic
- Use multiple WiFi networks
- Add error handling

### Performance
- Optimize data payloads
- Use appropriate update intervals
- Implement caching

## Next Steps

- **Explore MQTT** - For IoT messaging
- **Learn about WebSockets** - For real-time communication
- **Check out Cloud Platforms** - AWS, Azure, Google Cloud
- **Join the Community** - Get help on Discord

---

*Ready to build internet-connected projects? Start with the [Weather Station Tutorial](../../get-started/collects-data) or explore [other connectivity options](../../get-started/index)!* 