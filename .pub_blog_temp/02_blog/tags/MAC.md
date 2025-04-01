---
publish: 'true'
search:
  exclude: true
slug: mac
title: Tag - MAC

---

<!--
  ~ MIT License
  ~
  ~ Copyright (c) 2023-2025 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
  ~
  ~ Permission is hereby granted, free of charge, to any person obtaining a copy
  ~ of this software and associated documentation files (the "Software"), to deal
  ~ in the Software without restriction, including without limitation the rights
  ~ to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  ~ copies of the Software, and to permit persons to whom the Software is
  ~ furnished to do so, subject to the following conditions:
  ~
  ~ The above copyright notice and this permission notice shall be included in all
  ~ copies or substantial portions of the Software.
  ~
  ~ THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  ~ IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  ~ FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  ~ AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  ~ LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  ~ OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  ~ SOFTWARE.
  -->


## [ESP-NOW Test](http://127.0.0.1:8000/blog/2024-11-06-12:00/)

<!--suppress LongLine -->
<div class="post-extra">
    <div class="col">
        <p class="post-date">2024-11-06 12:00:00</p>
    </div>
    <div class="col">
    
        <a href="http://127.0.0.1:8000/blog/tags/testing/">#testing</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/example/">#example</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/code/">#code</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/ESP-NOW/">#ESP-NOW</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/MAC/">#MAC</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/WiFi/">#WiFi</a>
    
    </div>
</div>

Had to find the MAC Addresses of the devices first, so I used this program:

```cpp
#include <WiFi.h>
#include <esp_wifi.h>

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Initialize WiFi properly
  WiFi.mode(WIFI_MODE_APSTA);  // Set to AP+STA mode
  delay(100);  // Give it some time to initialize
  
  // Print Station MAC
  Serial.print("Station MAC Address: ");
  Serial.println(WiFi.macAddress());
  
  // Print AP MAC
  Serial.print("AP MAC Address: ");
  Serial.println(WiFi.softAPmacAddress());
  
  // Additional info about relationship
  Serial.println("\nTypically, the AP MAC is the Station MAC with");
  Serial.println("the last byte incremented by 1");
}

void loop() {
  // Empty loop
}
```

Then you can use the ESPNOW Serial Example to test coms

I set it up to send IMU Data through via the Station device, to the AP device and graph it onto the serial plotter:

First, I used the ESP-NOW Serial Example as a basis for checking the ESP-NOW connection:

```
/*
    ESP-NOW Serial Example - Unicast transmission
    Lucas Saavedra Vaz - 2024
    Send data between two ESP32s using the ESP-NOW protocol in one-to-one (unicast) configuration.
    Note that different MAC addresses are used for different interfaces.
    The devices can be in different modes (AP or Station) and still communicate using ESP-NOW.
    The only requirement is that the devices are on the same Wi-Fi channel.
    Set the peer MAC address according to the device that will receive the data.

    Example setup:
    - Device 1: AP mode with MAC address F6:12:FA:42:B6:E8
                Peer MAC address set to the Station MAC address of Device 2 (F4:12:FA:40:64:4C)
    - Device 2: Station mode with MAC address F4:12:FA:40:64:4C
                Peer MAC address set to the AP MAC address of Device 1 (F6:12:FA:42:B6:E8)

    The device running this sketch will also receive and print data from any device that has its MAC address set as the peer MAC address.
    To properly visualize the data being sent, set the line ending in the Serial Monitor to "Both NL & CR".
*/

#include "ESP32_NOW_Serial.h"
#include "MacAddress.h"
#include "WiFi.h"

#include "esp_wifi.h"

// 0: AP mode, 1: Station mode
#define ESPNOW_WIFI_MODE_STATION 0

// Channel to be used by the ESP-NOW protocol
#define ESPNOW_WIFI_CHANNEL 1

#if ESPNOW_WIFI_MODE_STATION          // ESP-NOW using WiFi Station mode
#define ESPNOW_WIFI_MODE WIFI_STA     // WiFi Mode
#define ESPNOW_WIFI_IF   WIFI_IF_STA  // WiFi Interface
#else                                 // ESP-NOW using WiFi AP mode
#define ESPNOW_WIFI_MODE WIFI_AP      // WiFi Mode
#define ESPNOW_WIFI_IF   WIFI_IF_AP   // WiFi Interface
#endif

// Set the MAC address of the device that will receive the data
// For example: F4:12:FA:40:64:4C
const MacAddress peer_mac({0xF0, 0xF5, 0xBD, 0x50, 0xB0, 0x80});

ESP_NOW_Serial_Class NowSerial(peer_mac, ESPNOW_WIFI_CHANNEL, ESPNOW_WIFI_IF);

void setup() {
  Serial.begin(115200);

  Serial.print("WiFi Mode: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? "AP" : "Station");
  WiFi.mode(ESPNOW_WIFI_MODE);

  Serial.print("Channel: ");
  Serial.println(ESPNOW_WIFI_CHANNEL);
  WiFi.setChannel(ESPNOW_WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);

  while (!(WiFi.STA.started() || WiFi.AP.started())) {
    delay(100);
  }

  Serial.print("MAC Address: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? WiFi.softAPmacAddress() : WiFi.macAddress());

  // Start the ESP-NOW communication
  Serial.println("ESP-NOW communication starting...");
  NowSerial.begin(115200);
  Serial.println("You can now send data to the peer device using the Serial Monitor.\n");
}

void loop() {
  while (NowSerial.available()) {
    Serial.write(NowSerial.read());
  }

  while (Serial.available() && NowSerial.availableForWrite()) {
    if (NowSerial.write(Serial.read()) <= 0) {
      Serial.println("Failed to send data");
      break;
    }
  }

  delay(1);
}
```

```cpp
/*
    ESP-NOW Serial Example - Unicast transmission
    Lucas Saavedra Vaz - 2024
    Send data between two ESP32s using the ESP-NOW protocol in one-to-one (unicast) configuration.
    Note that different MAC addresses are used for different interfaces.
    The devices can be in different modes (AP or Station) and still communicate using ESP-NOW.
    The only requirement is that the devices are on the same Wi-Fi channel.
    Set the peer MAC address according to the device that will receive the data.

    Example setup:
    - Device 1: AP mode with MAC address F6:12:FA:42:B6:E8
                Peer MAC address set to the Station MAC address of Device 2 (F4:12:FA:40:64:4C)
    - Device 2: Station mode with MAC address F4:12:FA:40:64:4C
                Peer MAC address set to the AP MAC address of Device 1 (F6:12:FA:42:B6:E8)

    The device running this sketch will also receive and print data from any device that has its MAC address set as the peer MAC address.
    To properly visualize the data being sent, set the line ending in the Serial Monitor to "Both NL & CR".
*/

#include "ESP32_NOW_Serial.h"
#include "MacAddress.h"
#include "WiFi.h"

#include "esp_wifi.h"

// 0: AP mode, 1: Station mode
#define ESPNOW_WIFI_MODE_STATION 1

// Channel to be used by the ESP-NOW protocol
#define ESPNOW_WIFI_CHANNEL 1

#if ESPNOW_WIFI_MODE_STATION          // ESP-NOW using WiFi Station mode
#define ESPNOW_WIFI_MODE WIFI_STA     // WiFi Mode
#define ESPNOW_WIFI_IF   WIFI_IF_STA  // WiFi Interface
#else                                 // ESP-NOW using WiFi AP mode
#define ESPNOW_WIFI_MODE WIFI_AP      // WiFi Mode
#define ESPNOW_WIFI_IF   WIFI_IF_AP   // WiFi Interface
#endif

// Set the MAC address of the device that will receive the data
// For example: F4:12:FA:40:64:4C
const MacAddress peer_mac({0xF2, 0xF5, 0xBD, 0x50, 0xB0, 0x10});

ESP_NOW_Serial_Class NowSerial(peer_mac, ESPNOW_WIFI_CHANNEL, ESPNOW_WIFI_IF);

void setup() {
  Serial.begin(115200);

  Serial.print("WiFi Mode: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? "AP" : "Station");
  WiFi.mode(ESPNOW_WIFI_MODE);

  Serial.print("Channel: ");
  Serial.println(ESPNOW_WIFI_CHANNEL);
  WiFi.setChannel(ESPNOW_WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);

  while (!(WiFi.STA.started() || WiFi.AP.started())) {
    delay(100);
  }

  Serial.print("MAC Address: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? WiFi.softAPmacAddress() : WiFi.macAddress());

  // Start the ESP-NOW communication
  Serial.println("ESP-NOW communication starting...");
  NowSerial.begin(115200);
  Serial.println("You can now send data to the peer device using the Serial Monitor.\n");
}

void loop() {
  while (NowSerial.available()) {
    Serial.write(NowSerial.read());
  }

  while (Serial.available() && NowSerial.availableForWrite()) {
    if (NowSerial.write(Serial.read()) <= 0) {
      Serial.println("Failed to send data");
      break;
    }
  }

  delay(1);
}
```

This worked great, and I was able to send characters/messages through Serial Monitor between the devices!

Then for the station device, I used Claude to generate an interface which allowed the user to choose between a throughput test, streaming data the IMU, and stopping all actions, based on character commands sent from the AP device. This was the final output of working code:

```cpp
#include "ESP32_NOW_Serial.h"
#include "MacAddress.h"
#include "WiFi.h"
#include "esp_wifi.h"
#include <Adafruit_LSM6DS3TRC.h>

// ESP-NOW Configuration
#define ESPNOW_WIFI_MODE_STATION 1
#define ESPNOW_WIFI_CHANNEL 1

#if ESPNOW_WIFI_MODE_STATION
#define ESPNOW_WIFI_MODE WIFI_STA
#define ESPNOW_WIFI_IF   WIFI_IF_STA
#else
#define ESPNOW_WIFI_MODE WIFI_AP
#define ESPNOW_WIFI_IF   WIFI_IF_AP
#endif

// Set your receiver's MAC address here
const MacAddress peer_mac({0xF2, 0xF5, 0xBD, 0x50, 0xB0, 0x10});

ESP_NOW_Serial_Class NowSerial(peer_mac, ESPNOW_WIFI_CHANNEL, ESPNOW_WIFI_IF);
Adafruit_LSM6DS3TRC lsm6ds3trc;

// Buffer for formatting IMU data
char dataBuffer[100];

// Throughput test variables
unsigned long startTime;
unsigned long bytesTransmitted = 0;
unsigned long packetsTransmitted = 0;
bool isRunning = false;
bool inThroughputTest = false;
const unsigned long THROUGHPUT_TEST_DURATION = 5000; // 5 seconds test

void setup() {
  Serial.begin(115200);
  
  // Initialize IMU-related pins
  pinMode(6, OUTPUT);
  digitalWrite(6, HIGH);
  
  // Initialize I2C
  Wire.begin(3, 4);
  delay(100);

  // Initialize WiFi for ESP-NOW
  Serial.print("WiFi Mode: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? "AP" : "Station");
  WiFi.mode(ESPNOW_WIFI_MODE);

  Serial.print("Channel: ");
  Serial.println(ESPNOW_WIFI_CHANNEL);
  WiFi.setChannel(ESPNOW_WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);

  while (!(WiFi.STA.started() || WiFi.AP.started())) {
    delay(100);
  }

  Serial.print("MAC Address: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? WiFi.softAPmacAddress() : WiFi.macAddress());

  // Initialize ESP-NOW
  Serial.println("ESP-NOW communication starting...");
  NowSerial.begin(115200);

  // Initialize LSM6DS3TR-C
  Serial.println("Initializing LSM6DS3TR-C...");
  if (!lsm6ds3trc.begin_I2C()) {
    Serial.println("Failed to find LSM6DS3TR-C chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("LSM6DS3TR-C Found!");

  // Configure IMU settings
  lsm6ds3trc.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);
  lsm6ds3trc.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);
  lsm6ds3trc.setAccelDataRate(LSM6DS_RATE_104_HZ);
  lsm6ds3trc.setGyroDataRate(LSM6DS_RATE_104_HZ);

  lsm6ds3trc.configInt1(false, false, true);  // accelerometer DRDY on INT1
  lsm6ds3trc.configInt2(false, true, false);  // gyro DRDY on INT2

  Serial.println("Waiting for command from AP...");
  Serial.println("Commands:");
  Serial.println("'s' - Start IMU data transmission");
  Serial.println("'t' - Run throughput test");
  Serial.println("'x' - Stop current operation");
}

void performThroughputTest() {
  const char testData[] = "THROUGHPUT_TEST_PACKET";
  startTime = millis();
  bytesTransmitted = 0;
  packetsTransmitted = 0;
  
  Serial.println("Starting throughput test for 5 seconds...");
  
  while (millis() - startTime < THROUGHPUT_TEST_DURATION) {
    if (NowSerial.availableForWrite()) {
      // Send test packet
      for (size_t i = 0; i < strlen(testData); i++) {
        NowSerial.write(testData[i]);
      }
      NowSerial.write('\n');
      
      bytesTransmitted += strlen(testData) + 1;  // +1 for newline
      packetsTransmitted++;
    }
    
    // Check for stop command
    if (NowSerial.available()) {
      char cmd = NowSerial.read();
      if (cmd == 'x') {
        break;
      }
    }
  }
  
  // Calculate and display results
  unsigned long duration = millis() - startTime;
  float throughputKBps = (bytesTransmitted * 1000.0) / (duration * 1024.0);  // KB/s
  float packetsPerSecond = (packetsTransmitted * 1000.0) / duration;
  
  Serial.println("\nThroughput Test Results:");
  Serial.printf("Duration: %lu ms\n", duration);
  Serial.printf("Bytes transmitted: %lu\n", bytesTransmitted);
  Serial.printf("Packets transmitted: %lu\n", packetsTransmitted);
  Serial.printf("Throughput: %.2f KB/s\n", throughputKBps);
  Serial.printf("Packets per second: %.2f\n", packetsPerSecond);
  
  inThroughputTest = false;
}

void sendIMUData() {
  // Read IMU data
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t temp;
  lsm6ds3trc.getEvent(&accel, &gyro, &temp);

  // Format the data into a string
  snprintf(dataBuffer, sizeof(dataBuffer), "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f",
           temp.temperature,
           accel.acceleration.x,
           accel.acceleration.y,
           accel.acceleration.z,
           gyro.gyro.x,
           gyro.gyro.y,
           gyro.gyro.z);

  // Send the data over ESP-NOW
  if (NowSerial.availableForWrite()) {
    for (size_t i = 0; i < strlen(dataBuffer); i++) {
      NowSerial.write(dataBuffer[i]);
    }
    NowSerial.write('\n');
  }

  // Also print to Serial for debugging
  Serial.println(dataBuffer);
}

void loop() {
  // Check for incoming commands
  while (NowSerial.available()) {
    char cmd = NowSerial.read();
    
    switch (cmd) {
      case 's':
        if (!isRunning && !inThroughputTest) {
          Serial.println("Starting IMU data transmission...");
          isRunning = true;
        }
        break;
        
      case 't':
        if (!isRunning && !inThroughputTest) {
          inThroughputTest = true;
          performThroughputTest();
        }
        break;
        
      case 'x':
        if (isRunning || inThroughputTest) {
          Serial.println("Stopping current operation...");
          isRunning = false;
          inThroughputTest = false;
        }
        break;
    }
  }

  // Send IMU data if running
  if (isRunning) {
    sendIMUData();
    delay(100);  // Adjust this delay based on your needs
  }
}
```

After running the throughput test, I got around 57KB/s. This is about 0.46 Mbps!

The data also transferred cleanly, and I was able to view it through the serial plotter.

<aside>
Note: The AP device is still running the example ESP-NOW Serial program in this configuriation.
</aside>

### Update 11/23/24:

---

Since adding a custom board library, we no longer need to specify the I2C PWR pins, so these lines have been removed from the example:

```cpp
  // Initialize IMU-related pins
  ~~pinMode(6, OUTPUT);
	digitalWrite(6, HIGH);~~
```

Also, I2C pins have been written in the board specification, so we can remove those parameters from I2C.begin():

```cpp
  // Initialize I2C
  Wire.begin(~~3, 4~~);
  delay(100);

```



<div class="post-link">

    &nbsp;

</div>

