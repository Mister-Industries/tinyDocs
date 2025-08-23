---
title: Bluetooth (BLE)
publish: true
date: 2025-01-27 12:00:00
update: 2025-01-27 12:00:00
description: Learn how to use Bluetooth Low Energy with tinyCore
categories:
  - advanced
  - connectivity
---

# Bluetooth Low Energy (BLE) 📱

tinyCore includes built-in Bluetooth Low Energy (BLE) support, allowing you to create wireless projects that connect to phones, computers, and other devices.

## What is BLE?

Bluetooth Low Energy is a wireless communication protocol designed for:
- **Low power consumption** - Perfect for battery-powered projects
- **Short-range communication** - Typically 10-100 meters
- **Simple data exchange** - Ideal for sensors, controllers, and IoT devices

## Key Features

### ✅ **What tinyCore BLE Can Do**

- **Phone Connectivity** - Connect to iOS and Android apps
- **Data Transfer** - Send sensor data to your phone
- **Remote Control** - Control tinyCore from your phone
- **Notifications** - Send alerts and status updates
- **Custom Apps** - Create your own mobile applications

### 📱 **Common Use Cases**

- **Smart Home Devices** - Control lights, sensors, and appliances
- **Wearable Projects** - Fitness trackers, smart watches
- **Remote Sensors** - Environmental monitoring
- **Game Controllers** - Custom input devices
- **IoT Devices** - Internet of Things applications

## Getting Started

### Prerequisites

1. **tinyCore Board** - Any tinyCore variant
2. **Arduino IDE** - With ESP32 board support
3. **Mobile Device** - iOS or Android for testing

### Basic BLE Server Example

```cpp
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

// BLE Service and Characteristic UUIDs
#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;

// Connection callback
class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      Serial.println("Device connected!");
    }

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
      Serial.println("Device disconnected!");
      // Restart advertising
      pServer->getAdvertising()->start();
    }
};

void setup() {
  Serial.begin(115200);
  
  // Initialize BLE
  BLEDevice::init("tinyCore BLE");
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Create BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create BLE Characteristic
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ |
                      BLECharacteristic::PROPERTY_WRITE |
                      BLECharacteristic::PROPERTY_NOTIFY
                    );

  // Add descriptor for notifications
  pCharacteristic->addDescriptor(new BLE2902());

  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0);
  BLEDevice::startAdvertising();
  
  Serial.println("BLE Server ready! Waiting for connections...");
}

void loop() {
  if (deviceConnected) {
    // Send data every second
    String data = "Hello from tinyCore!";
    pCharacteristic->setValue((uint8_t*)data.c_str(), data.length());
    pCharacteristic->notify();
    delay(1000);
  }
}
```

## Advanced Features

### Custom Services and Characteristics

Create your own BLE services for specific applications:

```cpp
// Custom service for sensor data
#define SENSOR_SERVICE_UUID "12345678-1234-1234-1234-123456789abc"
#define TEMPERATURE_CHAR_UUID "87654321-4321-4321-4321-cba987654321"

BLEService* pSensorService;
BLECharacteristic* pTemperatureChar;
```

### Data Formats

Send different types of data:

```cpp
// Send sensor readings
float temperature = 23.5;
uint8_t tempBytes[4];
memcpy(tempBytes, &temperature, 4);
pTemperatureChar->setValue(tempBytes, 4);
pTemperatureChar->notify();
```

### Security Features

Implement pairing and encryption:

```cpp
// Enable security
BLESecurity *pSecurity = new BLESecurity();
pSecurity->setAuthenticationMode(ESP_LE_AUTH_REQ_SC_BOND);
pSecurity->setCapability(ESP_IO_CAP_OUT);
pSecurity->setInitEncryptionKey(ESP_BLE_ENC_KEY_MASK | ESP_BLE_ID_KEY_MASK);
```

## Project Examples

### 1. RGB Mood Light Controller

Control RGB LEDs from your phone:

```cpp
// RGB LED pins
#define RED_PIN 25
#define GREEN_PIN 26
#define BLUE_PIN 27

// BLE characteristic for RGB values
BLECharacteristic* pRGBChar;

void setup() {
  // Initialize RGB pins
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  
  // Setup BLE (similar to basic example)
  // ...
  
  // Create RGB characteristic
  pRGBChar = pService->createCharacteristic(
    RGB_CHAR_UUID,
    BLECharacteristic::PROPERTY_WRITE
  );
}

void loop() {
  // Handle RGB updates in BLE callback
}
```

### 2. Sensor Data Logger

Send sensor data to your phone:

```cpp
// Send IMU data
void sendIMUData() {
  if (deviceConnected) {
    // Read IMU
    float accelX, accelY, accelZ;
    // ... read sensor data ...
    
    // Create JSON-like string
    String data = "{\"accel\":{\"x\":" + String(accelX) + 
                  ",\"y\":" + String(accelY) + 
                  ",\"z\":" + String(accelZ) + "}}";
    
    pCharacteristic->setValue((uint8_t*)data.c_str(), data.length());
    pCharacteristic->notify();
  }
}
```

## Mobile App Development

### Using BLE Scanner Apps

For testing, use these free apps:
- **nRF Connect** (Android/iOS)
- **BLE Scanner** (Android)
- **LightBlue** (iOS)

### Creating Custom Apps

Use these frameworks for custom mobile apps:
- **React Native** with `react-native-ble-plx`
- **Flutter** with `flutter_blue_plus`
- **Native iOS** with CoreBluetooth
- **Native Android** with BluetoothLe

## Troubleshooting

### Common Issues

1. **Device Not Found**
   - Check if BLE is enabled on your phone
   - Ensure tinyCore is advertising
   - Try restarting the BLE stack

2. **Connection Drops**
   - Check signal strength
   - Reduce data transmission frequency
   - Implement reconnection logic

3. **Data Corruption**
   - Use proper data formatting
   - Implement checksums
   - Check characteristic properties

### Debug Tips

```cpp
// Enable BLE debugging
#define CONFIG_BT_NIMBLE_ROLE_PERIPHERAL 1
#define CONFIG_BT_NIMBLE_ROLE_CENTRAL 1

// Monitor connection status
void printConnectionStatus() {
  Serial.print("Connected devices: ");
  Serial.println(deviceConnected ? "1" : "0");
}
```

## Performance Optimization

### Power Management

```cpp
// Reduce power consumption
BLEDevice::setMTU(23); // Use smaller packets
pAdvertising->setMinInterval(0x20); // Slower advertising
pAdvertising->setMaxInterval(0x40);
```

### Data Throughput

```cpp
// Optimize for high data rates
#define BLE_MTU_SIZE 512
BLEDevice::setMTU(BLE_MTU_SIZE);
```

## Next Steps

- **Explore ESP-NOW** - For device-to-device communication
- **Learn WiFi** - For internet connectivity
- **Check out User Projects** - See what others have built
- **Join the Community** - Get help on Discord

---

*Ready to build wireless projects? Start with the [RGB Mood Light Tutorial](../../get-started/lights-up) or explore [other connectivity options](../../get-started/index)!* 