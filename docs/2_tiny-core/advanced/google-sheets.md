# How to write data to Google Sheets

## :construction:  **THIS ZONE IS UNDER CONSTRUCTION**  :construction:

```cpp linenums="1"
/*
  Adapted from Rui Santos
  
  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files.
  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
  Adapted from the examples of the Library Google Sheet Client Library for Arduino devices: https://github.com/mobizt/ESP-Google-Sheet-Client
*/

#include <Arduino.h>
#include <WiFi.h>
#include <Adafruit_LSM6DSOX.h>
#include "time.h"
#include <ESP_Google_Sheet_Client.h>

// For SD/SD_MMC mounting helper
#include <GS_SDHelper.h>

#define WIFI_SSID "YOUR-SSID-HERE"
#define WIFI_PASSWORD "YOUR-PASSWORD-HERE"

// Google Project ID
#define PROJECT_ID "YOUR-PROJECT-ID-HERE"

// Service Account's client email
#define CLIENT_EMAIL "YOUR-CLIENT-EMAIL-HERE"

// Service Account's private key
const char PRIVATE_KEY[] PROGMEM = "-----BEGIN PRIVATE KEY-----\nYOUR KEY HERE\n-----END PRIVATE KEY-----\n";

// The ID of the spreadsheet where you'll publish the data
const char spreadsheetId[] = "YOUR-SPREADSHEET-ID-HERE";

// Timer variables
unsigned long lastTime = 0;  
unsigned long timerDelay = 5000;  // Log every 30 seconds (same as original)

// Token Callback function
void tokenStatusCallback(TokenInfo info);

// LSM6DSOX IMU
Adafruit_LSM6DSOX lsm6dso;

// Variables to hold sensor readings
float temp;
float accelX;
float accelY;
float accelZ;

// NTP server to request epoch time
const char* ntpServer = "pool.ntp.org";

// Variable to save current epoch time
unsigned long epochTime; 

// Function that gets current epoch time
unsigned long getTime() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    //Serial.println("Failed to obtain time");
    return(0);
  }
  time(&now);
  return now;
}

void setup(){

    Serial.begin(115200);
    Serial.println();
    Serial.println();

    //Configure time
    configTime(0, 0, ntpServer);

    // Initialize IMU-related pins
    pinMode(6, OUTPUT);
    digitalWrite(6, HIGH);
    
    // Initialize I2C
    Wire.begin(3, 4);
    delay(100);

    // Initialize LSM6DSOX IMU sensor 
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

    GSheet.printf("ESP Google Sheet Client v%s\n\n", ESP_GOOGLE_SHEET_CLIENT_VERSION);

    // Connect to Wi-Fi
    WiFi.setAutoReconnect(true);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
    Serial.print("Connecting to Wi-Fi");
    while (WiFi.status() != WL_CONNECTED) {
      Serial.print(".");
      delay(1000);
    }
    Serial.println();
    Serial.print("Connected with IP: ");
    Serial.println(WiFi.localIP());
    Serial.println();

    // Set the callback for Google API access token generation status (for debug only)
    GSheet.setTokenCallback(tokenStatusCallback);

    // Set the seconds to refresh the auth token before expire (60 to 3540, default is 300 seconds)
    GSheet.setPrerefreshSeconds(10 * 60);

    // Begin the access token generation for Google API authentication
    GSheet.begin(CLIENT_EMAIL, PROJECT_ID, PRIVATE_KEY);
}

void loop(){
    // Call ready() repeatedly in loop for authentication checking and processing
    bool ready = GSheet.ready();

    if (ready && millis() - lastTime > timerDelay){
        lastTime = millis();

        FirebaseJson response;

        Serial.println("\nAppend spreadsheet values...");
        Serial.println("----------------------------");

        FirebaseJson valueRange;

        // Get new IMU sensor readings
        sensors_event_t accel;
        sensors_event_t gyro;
        sensors_event_t tempEvent;
        lsm6dso.getEvent(&accel, &gyro, &tempEvent);
        
        // Extract the data we want to log
        temp = tempEvent.temperature;
        accelX = accel.acceleration.x;
        accelY = accel.acceleration.y;
        accelZ = accel.acceleration.z;
        
        // Get timestamp
        epochTime = getTime();

        // Print readings to serial for debugging
        Serial.print("Temperature: "); Serial.print(temp); Serial.println(" °C");
        Serial.print("Accel X: "); Serial.print(accelX); Serial.println(" m/s²");
        Serial.print("Accel Y: "); Serial.print(accelY); Serial.println(" m/s²");
        Serial.print("Accel Z: "); Serial.print(accelZ); Serial.println(" m/s²");

        valueRange.add("majorDimension", "COLUMNS");
        valueRange.set("values/[0]/[0]", epochTime);
        valueRange.set("values/[1]/[0]", temp);
        valueRange.set("values/[2]/[0]", accelX);
        valueRange.set("values/[3]/[0]", accelY);
        valueRange.set("values/[4]/[0]", accelZ);

        // For Google Sheet API ref doc, go to https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append
        // Append values to the spreadsheet
        bool success = GSheet.values.append(&response /* returned response */, spreadsheetId /* spreadsheet Id to append */, "Sheet1!A1" /* range to append */, &valueRange /* data range to append */);
        if (success){
            response.toString(Serial, true);
            valueRange.clear();
        }
        else{
            Serial.println(GSheet.errorReason());
        }
        Serial.println();
        Serial.println(ESP.getFreeHeap());
    }
}

void tokenStatusCallback(TokenInfo info){
    if (info.status == token_status_error){
        GSheet.printf("Token info: type = %s, status = %s\n", GSheet.getTokenType(info).c_str(), GSheet.getTokenStatus(info).c_str());
        GSheet.printf("Token error: %s\n", GSheet.getTokenError(info).c_str());
    }
    else{
        GSheet.printf("Token info: type = %s, status = %s\n", GSheet.getTokenType(info).c_str(), GSheet.getTokenStatus(info).c_str());
    }
}
```