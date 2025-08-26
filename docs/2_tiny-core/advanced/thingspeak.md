# How to log data to Thingspeak

## :construction:  **THIS ZONE IS UNDER CONSTRUCTION**  :construction:

```cpp linenums="1"
/*
  Adapted from WriteSingleField Example from ThingSpeak Library (Mathworks) and Random Nerd Tutorials
  
  Updated to use LSM6DSOX IMU instead of BME280 sensor
  Logs temperature from IMU sensor in Fahrenheit
*/

#include <WiFi.h>
#include "ThingSpeak.h"
#include <Adafruit_LSM6DSOX.h>
#include <Adafruit_Sensor.h>

const char* ssid = "YOUR-SSID-HERE";   // your network SSID (name) 
const char* password = "YOUR-PASSWORD-HERE";   // your network password

WiFiClient  client;

unsigned long myChannelNumber = 1;
const char * myWriteAPIKey = "YOUR-WRITE-API-KEY-HERE";

// Timer variables
unsigned long lastTime = 0;
unsigned long timerDelay = 30000;

// Variable to hold temperature readings
float temperatureF;

// Create IMU sensor object
Adafruit_LSM6DSOX lsm6dso;

void initIMU(){
  // Initialize IMU-related pins
  pinMode(6, OUTPUT);
  digitalWrite(6, HIGH);
  
  // Initialize I2C
  Wire.begin(3, 4);
  delay(100);

  Serial.println("Attempting to initialize LSM6DSOX...");
  if (!lsm6dso.begin_I2C()) {
    Serial.println("Failed to find LSM6DSOX chip");
    Serial.println("Check your wiring!");
    while (1) {
      delay(10);
    }
  }

  Serial.println("LSM6DSOX Found!");

  // Configure IMU settings
  lsm6dso.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);
  lsm6dso.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);
  lsm6dso.setAccelDataRate(LSM6DS_RATE_104_HZ);
  lsm6dso.setGyroDataRate(LSM6DS_RATE_104_HZ);
}

void setup() {
  Serial.begin(115200);  //Initialize serial
  initIMU();
  
  WiFi.mode(WIFI_STA);   
  
  ThingSpeak.begin(client);  // Initialize ThingSpeak
}

void loop() {
  if ((millis() - lastTime) > timerDelay) {
    
    // Connect or reconnect to WiFi
    if(WiFi.status() != WL_CONNECTED){
      Serial.print("Attempting to connect");
      while(WiFi.status() != WL_CONNECTED){
        WiFi.begin(ssid, password); 
        delay(5000);     
      } 
      Serial.println("\nConnected.");
    }

    // Get new IMU sensor readings
    sensors_event_t accel;
    sensors_event_t gyro;
    sensors_event_t tempEvent;
    lsm6dso.getEvent(&accel, &gyro, &tempEvent);
    
    // Get temperature in Fahrenheit
    temperatureF = (tempEvent.temperature * 1.8) + 32;
    Serial.print("Temperature (ºF): ");
    Serial.println(temperatureF);
    
    // Write to ThingSpeak. There are up to 8 fields in a channel, allowing you to store up to 8 different
    // pieces of information in a channel.  Here, we write to field 1.
    int x = ThingSpeak.writeField(myChannelNumber, 1, temperatureF, myWriteAPIKey);

    if(x == 200){
      Serial.println("Channel update successful.");
    }
    else{
      Serial.println("Problem updating channel. HTTP error code " + String(x));
    }
    lastTime = millis();
  }
}
```