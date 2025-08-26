# How to Link tinyCores (ESP-NOW)

Want to make two tinyCores talk to each other **without WiFi**? Let's use ESP-NOW, a wireless communication protocol that lets your tinyCores send messages to each other like walkie-talkies!

!!! warning "Are you skipping ahead?"

    Make sure you have already setup your Arduino IDE using the [getting started guide](../get-started/arduino-ide.md)!

## What is ESP-NOW?

ESP-NOW is a fast communication protocol that can be used to exchange small messages (up to 250 bytes) between ESP32 boards. No router, no WiFi network needed - just direct device-to-device communication up to 200+ meters away.

ESP-NOW offers several advantages: devices talk directly to each other without needing WiFi infrastructure, it has millisecond-level delay for fast communication, works over long distances in open areas, uses low power which is great for battery projects, and setup is straightforward once you know each device's MAC address(1).
{ .annotate }

1.  MAC stands for Media Access Control. It's a unique identifier assigned to every network device. It's like a serial number for all wireless devices. No two devices will have the same one. (Yours should be located on a sticker on the back of your tinyCore kit)

![Types of Network Topologies Supported by ESP-NOW](images/espnow-concept.png)

(One-way, Two-way, One to Many, Many to One. ESP-NOW + WiFi)

## What you'll need

You'll need two tinyCore ESP32-S3 devices, USB-C cables for both, your computer, and about 30 minutes. For the advanced section, you might want a breadboard and LED.

## Step 1: Install the ESP-NOW library

First, we need to install the library that makes ESP-NOW communication easy.

1. Open Arduino IDE
2. Go to **Tools → Manage Libraries**
3. Search for `ESP32_NOW_Serial`
4. Install the library by **yoursunny**

![ESP-NOW Library Installation](images/espnow-library.png)

## Step 2: Get your MAC addresses

Every tinyCore has a unique MAC address that identifies it on the network. We need to find these addresses so the devices know who to talk to.

Check the sticker on your kit box first - your tinyCore's MAC address should be printed there. If you can't find it, upload this code to get the MAC address:

```cpp linenums="1"
#include "WiFi.h"

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("tinyCore ESP32-S3 MAC Address Display");
  Serial.println("=====================================");
  
  // Initialize WiFi (required to access MAC address)
  WiFi.mode(WIFI_MODE_STA);
  delay(100);

  // Get and print MAC address
  String macAddress = WiFi.macAddress();
  Serial.print("MAC Address: ");
  Serial.println(macAddress);
  
  // Print additional device info
  Serial.println("\nDevice Info:");
  Serial.print("Chip Model: ");
  Serial.println(ESP.getChipModel());
  Serial.print("Flash Size: ");
  Serial.print(ESP.getFlashChipSize() / 1024 / 1024);
  Serial.println(" MB");
}

void loop() {
  // Print MAC address every 10 seconds
  delay(10000);
  Serial.print("MAC Address: ");
  Serial.println(WiFi.macAddress());
}
```

Write down both MAC addresses - they'll look like: `AA:BB:CC:DD:EE:FF`

![MAC Address Display](images/mac-address-output.png)

## Step 3: Setup two-way communication

Now we'll use code that lets both devices send and receive messages. This code can store the other device's address and remember it even after power cycling.

Upload this code to both devices:

```cpp linenums="1"
#include "ESP32_NOW_Serial.h"
#include "MacAddress.h"
#include "WiFi.h"
#include "esp_wifi.h"
#include <EEPROM.h>

// Configuration options
#define EEPROM_SIZE 64
#define MAC_ADDRESS_SIZE 6
#define EEPROM_MAC_ADDR 0
#define EEPROM_INIT_FLAG 48  // Location to store initialization flag

// WiFi Configuration
// 0: AP mode, 1: Station mode
#define ESPNOW_WIFI_MODE_STATION 1
#define ESPNOW_WIFI_CHANNEL 1

#if ESPNOW_WIFI_MODE_STATION          // ESP-NOW using WiFi Station mode
#define ESPNOW_WIFI_MODE WIFI_STA     // WiFi Mode
#define ESPNOW_WIFI_IF   WIFI_IF_STA  // WiFi Interface
#else                                 // ESP-NOW using WiFi AP mode
#define ESPNOW_WIFI_MODE WIFI_AP      // WiFi Mode
#define ESPNOW_WIFI_IF   WIFI_IF_AP   // WiFi Interface
#endif

// Global variables
uint8_t peerMacAddress[6];
bool macAddressSet = false;
bool nowSerialActive = false;
ESP_NOW_Serial_Class* NowSerial = nullptr;
String receivedMessage = "";  // Buffer for incoming message

// Function to print MAC address in readable format
void printMacAddress(uint8_t* mac) {
  for (int i = 0; i < 6; i++) {
    if (mac[i] < 16) Serial.print("0");
    Serial.print(mac[i], HEX);
    if (i < 5) Serial.print(":");
  }
  Serial.println();
}

// Function to save MAC address to EEPROM
void saveMacToEEPROM(uint8_t* mac) {
  for (int i = 0; i < MAC_ADDRESS_SIZE; i++) {
    EEPROM.write(EEPROM_MAC_ADDR + i, mac[i]);
  }
  EEPROM.write(EEPROM_INIT_FLAG, 0xAA);  // Set initialization flag
  EEPROM.commit();
  Serial.println("MAC address saved to EEPROM!");
}

// Function to load MAC address from EEPROM
bool loadMacFromEEPROM(uint8_t* mac) {
  if (EEPROM.read(EEPROM_INIT_FLAG) != 0xAA) {
    return false;  // Not initialized
  }
  
  for (int i = 0; i < MAC_ADDRESS_SIZE; i++) {
    mac[i] = EEPROM.read(EEPROM_MAC_ADDR + i);
  }
  return true;
}

// Function to parse MAC address from string (format: AA:BB:CC:DD:EE:FF)
bool parseMacAddress(String macStr, uint8_t* mac) {
  macStr.replace(":", "");
  macStr.toUpperCase();
  
  if (macStr.length() != 12) {
    return false;
  }
  
  for (int i = 0; i < 6; i++) {
    String byteStr = macStr.substring(i * 2, i * 2 + 2);
    mac[i] = strtol(byteStr.c_str(), NULL, 16);
  }
  return true;
}

// Function to initialize ESP-NOW Serial with new peer MAC
bool initializeNowSerial(uint8_t* mac) {
  // Clean up existing instance
  if (NowSerial != nullptr) {
    delete NowSerial;
    NowSerial = nullptr;
    nowSerialActive = false;
  }
  
  // Create MacAddress object from uint8_t array
  MacAddress peer_mac({mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]});
  
  // Create new ESP_NOW_Serial instance
  NowSerial = new ESP_NOW_Serial_Class(peer_mac, ESPNOW_WIFI_CHANNEL, ESPNOW_WIFI_IF);
  
  // Start ESP-NOW communication
  if (NowSerial->begin(115200)) {
    Serial.print("ESP-NOW communication started with peer: ");
    printMacAddress(mac);
    memcpy(peerMacAddress, mac, 6);
    macAddressSet = true;
    nowSerialActive = true;
    return true;
  } else {
    Serial.println("Failed to start ESP-NOW communication");
    delete NowSerial;
    NowSerial = nullptr;
    return false;
  }
}

// Function to configure MAC address
void configureMacAddress() {
  Serial.println("\n=== MAC ADDRESS CONFIGURATION ===");
  Serial.println("Enter peer MAC address (format: AA:BB:CC:DD:EE:FF):");
  Serial.println("Or type 'show' to display current MAC, 'clear' to reset");
  
  while (true) {
    if (Serial.available()) {
      String input = Serial.readStringUntil('\n');
      input.trim();
      
      if (input.equalsIgnoreCase("show")) {
        if (macAddressSet) {
          Serial.print("Current peer MAC: ");
          printMacAddress(peerMacAddress);
        } else {
          Serial.println("No MAC address set");
        }
        continue;
      }
      
      if (input.equalsIgnoreCase("clear")) {
        EEPROM.write(EEPROM_INIT_FLAG, 0x00);
        EEPROM.commit();
        Serial.println("MAC address cleared from EEPROM");
        macAddressSet = false;
        nowSerialActive = false;
        if (NowSerial != nullptr) {
          delete NowSerial;
          NowSerial = nullptr;
        }
        continue;
      }
      
      uint8_t newMac[6];
      if (parseMacAddress(input, newMac)) {
        if (initializeNowSerial(newMac)) {
          saveMacToEEPROM(newMac);
          Serial.print("Peer MAC address set to: ");
          printMacAddress(newMac);
          Serial.println("Configuration saved!\n");
          break;
        }
      } else {
        Serial.println("Invalid MAC address format. Use AA:BB:CC:DD:EE:FF");
      }
    }
    delay(10);
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n=== ESP32 ESP-NOW Two-Way Communication ===");
  
  // Initialize EEPROM
  EEPROM.begin(EEPROM_SIZE);
  
  // Setup WiFi
  Serial.print("WiFi Mode: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? "AP" : "Station");
  WiFi.mode(ESPNOW_WIFI_MODE);

  Serial.print("Channel: ");
  Serial.println(ESPNOW_WIFI_CHANNEL);
  WiFi.setChannel(ESPNOW_WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);

  while (!(WiFi.STA.started() || WiFi.AP.started())) {
    delay(100);
  }
  
  // Print this device's MAC address
  Serial.print("This device MAC Address: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? WiFi.softAPmacAddress() : WiFi.macAddress());
  
  // Try to load MAC from EEPROM
  uint8_t storedMac[6];
  if (loadMacFromEEPROM(storedMac)) {
    Serial.print("Loaded peer MAC from EEPROM: ");
    printMacAddress(storedMac);
    initializeNowSerial(storedMac);
  } else {
    Serial.println("No MAC address found in EEPROM");
  }
  
  Serial.println("\nCommands:");
  Serial.println("- Type any message to send it to peer");
  Serial.println("- Type 'config' to configure peer MAC address");
  Serial.println("- Type 'status' to show current configuration");
  Serial.println("- Type 'reset' to restart the device");
  
  if (!macAddressSet) {
    Serial.println("\nNo peer MAC address configured!");
    Serial.println("Type 'config' to set up communication");
  } else if (nowSerialActive) {
    Serial.println("ESP-NOW communication ready!");
  }
  
  Serial.println("\nEnter message to send (or 'config' to change MAC): ");
}

void loop() {
  // Handle incoming ESP-NOW messages
  if (nowSerialActive && NowSerial != nullptr && NowSerial->available()) {
    while (NowSerial->available()) {
      char receivedChar = NowSerial->read();
      
      if (receivedChar == '\n') {
        // Complete message received
        if (receivedMessage.length() > 0) {
          Serial.print("R: ");
          Serial.println(receivedMessage);
          receivedMessage = "";  // Clear buffer
        }
      } else if (receivedChar != '\r') {
        // Add character to buffer (ignore carriage returns)
        receivedMessage += receivedChar;
      }
    }
  }
  
  // Handle serial input
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    
    if (input.equalsIgnoreCase("config")) {
      configureMacAddress();
    }
    else if (input.equalsIgnoreCase("status")) {
      Serial.println("\n=== DEVICE STATUS ===");
      Serial.print("This device MAC: ");
      Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? WiFi.softAPmacAddress() : WiFi.macAddress());
      Serial.print("WiFi Mode: ");
      Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? "AP" : "Station");
      Serial.print("WiFi Channel: ");
      Serial.println(ESPNOW_WIFI_CHANNEL);
      if (macAddressSet) {
        Serial.print("Peer MAC: ");
        printMacAddress(peerMacAddress);
        Serial.print("ESP-NOW Status: ");
        Serial.println(nowSerialActive ? "Active" : "Inactive");
        Serial.println("Status: Ready for communication");
      } else {
        Serial.println("Peer MAC: Not set");
        Serial.println("Status: Configuration required");
      }
      Serial.println("====================\n");
      Serial.println("Enter message to send (or 'config' to change MAC): ");
    }
    else if (input.equalsIgnoreCase("reset")) {
      Serial.println("Restarting device...");
      ESP.restart();
    }
    else if (input.length() > 0) {
      if (nowSerialActive && NowSerial != nullptr) {
        // Send message via ESP-NOW
        Serial.print("S: ");
        Serial.println(input);
        
        for (int i = 0; i < input.length(); i++) {
          if (NowSerial->write(input.charAt(i)) <= 0) {
            Serial.println("Failed to send");
            break;
          }
        }
        
        // Send newline to mark end of message
        NowSerial->write('\n');

      } else {
        Serial.println("Please configure peer MAC address first (type 'config')");
      }
    }
  }
  
  delay(1);
}
```

## Step 4: Configure the devices to talk to each other

Now we'll get the devices talking to each other.

On Device #1, open the Serial Monitor at 115200 baud, type `config` and press Enter. When prompted, enter Device #2's MAC address (the one you wrote down or from the sticker). You should see "Configuration saved!"

On Device #2, open the Serial Monitor at 115200 baud, type `config` and press Enter, then enter Device #1's MAC address. You should see "Configuration saved!"

![Configuration Process](images/espnow-config.png)

## Step 5: Test it out

Now you can try typing messages in either Serial Monitor - they should appear on both devices.

Type `Hello from Device 1!` on the first device, then type `Hey there Device 2!` on the second device. Watch the messages appear on both screens with `R:` and `S:` prefixes.

You can also try these commands: `status` shows current configuration, `show` displays the peer MAC address, and `reset` restarts the device.

![ESP-NOW Messages](images/espnow-messages.png)

!!! example "Challenge: Secret Messages"

    Can you send a secret coded message? Try creating your own simple cipher - like replacing every letter with the next one in the alphabet (A→B, B→C, etc.). Send coded messages and decode them on the other device.

## Step 6: Control an LED wirelessly

Let's make this more interesting by controlling the built-in LEDs wirelessly. We'll modify one device to control the other device's LEDs.

Add this code to the top of your program (after the includes):

```cpp linenums="3"
// LED control pins
const int ledBoot = 21;    // Built-in LED_BOOT
const int ledSig = 33;     // Built-in LED_SIG
```

Add this to your `setup()` function (after EEPROM initialization):

```cpp linenums="75"
  // Initialize LED pins
  pinMode(ledBoot, OUTPUT);
  pinMode(ledSig, OUTPUT);
  digitalWrite(ledBoot, LOW);
  digitalWrite(ledSig, LOW);
```

Add this LED control function before your `setup()`:

```cpp linenums="70"
// Function to handle LED commands
void handleLEDCommand(String command) {
  if (command.startsWith("LED:")) {
    String ledCommand = command.substring(4);
    
    if (ledCommand == "BOOT_ON") {
      digitalWrite(ledBoot, HIGH);
      Serial.println("BOOT LED turned ON");
    }
    else if (ledCommand == "BOOT_OFF") {
      digitalWrite(ledBoot, LOW);
      Serial.println("BOOT LED turned OFF");
    }
    else if (ledCommand == "SIG_ON") {
      digitalWrite(ledSig, HIGH);
      Serial.println("SIG LED turned ON");
    }
    else if (ledCommand == "SIG_OFF") {
      digitalWrite(ledSig, LOW);
      Serial.println("SIG LED turned OFF");
    }
    else if (ledCommand == "BOTH_ON") {
      digitalWrite(ledBoot, HIGH);
      digitalWrite(ledSig, HIGH);
      Serial.println("Both LEDs turned ON");
    }
    else if (ledCommand == "BOTH_OFF") {
      digitalWrite(ledBoot, LOW);
      digitalWrite(ledSig, LOW);
      Serial.println("Both LEDs turned OFF");
    }
  }
}
```

Finally, modify the message receiving section in your `loop()` to call the LED function. Replace this part:

```cpp linenums="180"
        if (receivedMessage.length() > 0) {
          Serial.print("R: ");
          Serial.println(receivedMessage);
          receivedMessage = "";  // Clear buffer
        }
```

With this:

```cpp linenums="180"
        if (receivedMessage.length() > 0) {
          Serial.print("R: ");
          Serial.println(receivedMessage);
          
          // Check if it's an LED command
          handleLEDCommand(receivedMessage);
          
          receivedMessage = "";  // Clear buffer
        }
```

Upload this modified code to both devices, then try these commands: `LED:BOOT_ON` turns on the BOOT LED, `LED:BOOT_OFF` turns it off, `LED:SIG_ON` and `LED:SIG_OFF` control the SIG LED, while `LED:BOTH_ON` and `LED:BOTH_OFF` control both LEDs together.

You should see the LEDs on the receiving device light up when you send these commands from the other device.

![LED Control Demo](images/espnow-led-control.png)

## Step 7: Send motion data between devices

Now we'll use the built-in IMU(1) to send motion data from one device to another.
{ .annotate }

1.  IMU stands for Inertial Measurement Unit. It's a sensor that can detect motion, orientation, and acceleration. The tinyCore has a built-in LSM6DSOX IMU that can measure acceleration and rotation.

First, install the IMU library if you haven't already. Go to **Tools → Manage Libraries**, search for `Adafruit LSM6DS`, and install the **Adafruit LSM6DS library**.

Add these includes at the top:

```cpp linenums="1"
#include <Adafruit_LSM6DSOX.h>
#include <Wire.h>
```

Add these variables after your other global variables:

```cpp linenums="25"
// IMU variables
Adafruit_LSM6DSOX lsm6dsox;
unsigned long lastIMUSample = 0;
const unsigned long IMU_INTERVAL = 200; // Send IMU data every 200ms
bool imuInitialized = false;
```

Add this IMU setup function before your `setup()`:

```cpp linenums="80"
// Function to initialize the built-in IMU
void setupIMU() {
  // Initialize IMU power pin (GPIO6 controls IMU power)
  pinMode(6, OUTPUT);
  digitalWrite(6, HIGH);
  delay(100);
  
  // Initialize I2C for IMU (SDA=GPIO3, SCL=GPIO4)
  Wire.begin(3, 4);
  delay(100);

  Serial.println("Initializing built-in IMU...");
  if (!lsm6dsox.begin_I2C()) {
    Serial.println("Failed to find LSM6DSOX IMU");
    imuInitialized = false;
    return;
  }

  Serial.println("LSM6DSOX IMU Found!");
  
  // Configure IMU settings
  lsm6dsox.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);
  lsm6dsox.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);
  lsm6dsox.setAccelDataRate(LSM6DS_RATE_104_HZ);
  lsm6dsox.setGyroDataRate(LSM6DS_RATE_104_HZ);
  
  imuInitialized = true;
  Serial.println("IMU configured and ready!");
}
```

Add this to your `setup()` function (after LED initialization):

```cpp linenums="90"
  // Initialize the built-in IMU
  setupIMU();
```

Add this IMU data sending function before your `setup()`:

```cpp linenums="120"
// Function to send IMU data
void sendIMUData() {
  unsigned long currentTime = millis();
  
  if (currentTime - lastIMUSample >= IMU_INTERVAL && nowSerialActive && imuInitialized) {
    sensors_event_t accel, gyro, temp;
    lsm6dsox.getEvent(&accel, &gyro, &temp);
    
    // Format IMU data as a string
    String imuData = "IMU:";
    imuData += String(accel.acceleration.x, 2) + ",";
    imuData += String(accel.acceleration.y, 2) + ",";  
    imuData += String(accel.acceleration.z, 2) + ",";
    imuData += String(gyro.gyro.x, 2) + ",";
    imuData += String(gyro.gyro.y, 2) + ",";
    imuData += String(gyro.gyro.z, 2);
    
    // Send it via ESP-NOW
    if (NowSerial != nullptr) {
      for (int i = 0; i < imuData.length(); i++) {
        NowSerial->write(imuData.charAt(i));
      }
      NowSerial->write('\n');
      
      Serial.println("Sent IMU data");
    }
    
    lastIMUSample = currentTime;
  }
}
```

Add this to your `loop()` function (right before the final `delay(1);`):

```cpp linenums="250"
  // Send IMU data automatically
  sendIMUData();
```

Upload this enhanced code to both devices.

Now shake, tilt, or move Device #1 around. On Device #2, watch the Serial Monitor - you should see IMU data streaming in like:

```
R: IMU:0.15,-0.23,9.81,0.01,-0.02,0.00
Sent IMU data
R: IMU:0.22,-0.18,9.79,0.05,-0.01,0.03
```

The numbers represent acceleration in X, Y, Z directions (m/s²) for the first three values, and rotation rate in X, Y, Z directions (rad/s) for the last three values.

Try shaking Device #1 and watch the numbers change dramatically on Device #2.

![IMU Data Streaming](images/espnow-imu-data.png)

!!! example "Challenge: Motion-Controlled LEDs"

    Can you combine both features? Try modifying the code so that when Device #1 detects strong motion (acceleration > 2.0), it automatically sends `LED:BOTH_ON` to Device #2, and when it's still, it sends `LED:BOTH_OFF`. This creates a motion-activated remote LED controller.

## Common Issues

If you see "Failed to start ESP-NOW communication", double-check the MAC address format (AA:BB:CC:DD:EE:FF), make sure both devices are powered on, and try typing `reset` to restart both devices.

If you see "No MAC address found in EEPROM", this is normal on first run - just type `config` to set it up. The device will remember the MAC address for next time.

If messages aren't getting through, check that both devices are configured with each other's MAC addresses, make sure you're on the same WiFi channel (code sets this to 1), and try moving the devices closer together (within a few meters for testing).

For LED command issues, make sure you're typing the exact command like `LED:BOOT_ON` (case sensitive), check that both devices have the LED control code uploaded, and try the `status` command to verify ESP-NOW is active.

If the IMU isn't working, make sure the Adafruit LSM6DS library is installed, check the Serial Monitor for "LSM6DSOX IMU Found!" message, and if you see "Failed to find LSM6DSOX IMU", try restarting the device. The IMU is built into the tinyCore, so no wiring is needed.

If IMU data looks wrong, the Z-axis acceleration should read around 9.8 m/s² when the device is sitting flat (that's gravity). If all values are zero, the IMU might not be initialized properly - try the `reset` command.

## Understanding the Code

The `ESP_NOW_Serial_Class` creates a wireless serial connection between devices. `NowSerial->write()` sends data to the peer device while `NowSerial->read()` receives data from the peer device.

For storage, `EEPROM.write()` saves data to permanent memory and `EEPROM.read()` loads data from permanent memory. The tinyCore remembers the peer MAC address even after power off.

The IMU sensor uses `lsm6dsox.getEvent()` to read acceleration and rotation data. The `sensors_event_t` is a data structure containing sensor readings. The IMU runs on I2C bus(1) using pins GPIO3 (SDA) and GPIO4 (SCL).
{ .annotate }

1.  I2C (Inter-Integrated Circuit) is a communication protocol that allows multiple devices to share the same two wires. Think of it like a party line telephone where devices take turns talking.

## What's next?

Now you have two tinyCore devices talking wirelessly. Some project ideas include remote sensor monitoring where you place one device outside to monitor temperature and send data inside, wireless game controllers using IMU data to control games or robots wirelessly, home automation sending commands between rooms without WiFi infrastructure, motion alarms that detect motion on one device and trigger alerts on another, or data logging networks where multiple sensors report to one central device.

Want to learn more? Try [connecting to WiFi and the Internet](connect-wifi.md), [using the Serial Monitor and Plotter](../core/serial-monitor-plotter.md), or [advanced IMU motion detection](../core/detect-motion.md).

!!! warning "Having trouble?"

    Join our [Discord](https://discord.gg/hvJZhwfQsF) or email [support@mr.industries](mailto:support@mr.industries) for help!