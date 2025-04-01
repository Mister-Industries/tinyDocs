---
publish: 'true'
search:
  exclude: true
slug: adc
title: Tag - ADC

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


## [ADC + MCP7428 Test](http://127.0.0.1:8000/blog/adc-mcp/)

<!--suppress LongLine -->
<div class="post-extra">
    <div class="col">
        <p class="post-date">2024-11-19 12:00:00</p>
    </div>
    <div class="col">
    
        <a href="http://127.0.0.1:8000/blog/tags/example/">#example</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/code/">#code</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/ADC/">#ADC</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/MCP7428/">#MCP7428</a>
    
    </div>
</div>

<aside>
Note: This test was run before the custom Arduino library was written. This means we needed to use specific workarounds to remap pins for our ADC Test.

</aside>

```cpp
#include <Adafruit_MCP4728.h>
#include <Wire.h>
#include "driver/adc.h"
#include "esp_adc/adc_oneshot.h"

Adafruit_MCP4728 mcp;

// Constants
const int ANALOG_PIN = 18;  // GPIO18, ADC2_CH7
const unsigned long LIGHT_CHANGE_INTERVAL = 10000;  // 10ms in microseconds
const int LED_VALUE = 310;  // LED brightness value
const unsigned long SAMPLE_INTERVAL = 25;  // 25 microseconds

// Variables for timing
unsigned long lastSampleMicros = 0;
unsigned long lastLightMicros = 0;
uint8_t currentLight = 0;
volatile uint16_t analogBuffer[100];  // Buffer for analog readings
volatile uint8_t bufferIndex = 0;
volatile bool bufferFull = false;

// ADC handles
adc_oneshot_unit_handle_t adc2_handle;
adc_oneshot_unit_init_cfg_t init_config2;
adc_oneshot_chan_cfg_t config;

void setup(void) {
  Serial.begin(2000000);  // Increased baud rate for faster data transmission
  
  // Initialize I2C and LED control
  pinMode(6, OUTPUT);
  digitalWrite(6, HIGH);

  Wire.begin(3, 4);
  Wire.setClock(800000);  // Set I2C clock to 800kHz for faster communication
  delay(100);  // Give I2C time to stabilize

  // Try to initialize MCP4728
  if (!mcp.begin()) {
    Serial.println("Failed to find MCP4728 chip");
    while (1) {
      delay(10);
    }
  }

  // Configure ADC
  init_config2.unit_id = ADC_UNIT_2;  // Using ADC2
  init_config2.ulp_mode = ADC_ULP_MODE_DISABLE;
  init_config2.clk_src = ADC_RTC_CLK_SRC_DEFAULT;
  ESP_ERROR_CHECK(adc_oneshot_new_unit(&init_config2, &adc2_handle));

  // Configure ADC channel
  config.atten = ADC_ATTEN_DB_11;
  config.bitwidth = ADC_BITWIDTH_12;
  ESP_ERROR_CHECK(adc_oneshot_config_channel(adc2_handle, ADC_CHANNEL_7, &config));  // ADC2_CH7 for GPIO18

  // Initialize all channels to 0
  mcp.setChannelValue(MCP4728_CHANNEL_A, 0);
  mcp.setChannelValue(MCP4728_CHANNEL_B, 0);
  mcp.setChannelValue(MCP4728_CHANNEL_C, 0);
  mcp.setChannelValue(MCP4728_CHANNEL_D, 0);

  // Print header for Serial Plotter
  Serial.println("Light_Level Channel_A Channel_B Channel_C Channel_D");
}

void loop() {
  unsigned long currentMicros = micros();
  
  // Sample analog input every 50 microseconds
  if (currentMicros - lastSampleMicros >= SAMPLE_INTERVAL) {
    lastSampleMicros = currentMicros;
    
    // Read ADC
    int adc_value;
    if (adc_oneshot_read(adc2_handle, ADC_CHANNEL_7, &adc_value) == ESP_OK) {
      analogBuffer[bufferIndex] = adc_value;
      
      // Print the values and LED states
      Serial.println(analogBuffer[bufferIndex]);
      // Serial.print(" ");
      // Serial.print(currentLight == 0 ? LED_VALUE : 0);
      // Serial.print(" ");
      // Serial.print(currentLight == 1 ? LED_VALUE : 0);
      // Serial.print(" ");
      // Serial.print(currentLight == 2 ? LED_VALUE : 0);
      // Serial.print(" ");
      // Serial.println(currentLight == 3 ? LED_VALUE : 0);
      
      bufferIndex = (bufferIndex + 1) % 100;
      if (bufferIndex == 0) {
        bufferFull = true;
      }
    }
  }

  // Change lights every 10ms (10,000 microseconds)
  if (currentMicros - lastLightMicros >= LIGHT_CHANGE_INTERVAL) {
    lastLightMicros = currentMicros;
    
    // Turn off all LEDs
    mcp.setChannelValue(MCP4728_CHANNEL_A, 0);
    mcp.setChannelValue(MCP4728_CHANNEL_B, 0);
    mcp.setChannelValue(MCP4728_CHANNEL_C, 0);
    mcp.setChannelValue(MCP4728_CHANNEL_D, 0);

    // If we're not in the "all off" state, turn on the current LED
    if (currentLight < 4) {
      switch(currentLight) {
        case 0:
          mcp.setChannelValue(MCP4728_CHANNEL_A, LED_VALUE);
          break;
        case 1:
          mcp.setChannelValue(MCP4728_CHANNEL_B, LED_VALUE);
          break;
        case 2:
          mcp.setChannelValue(MCP4728_CHANNEL_C, LED_VALUE);
          break;
        case 3:
          mcp.setChannelValue(MCP4728_CHANNEL_D, LED_VALUE);
          break;
      }
    }

    // Increment light counter
    currentLight = (currentLight + 1) % 5;  // 5 states: 4 LEDs + all off
  }
}
```

This code was actually written for the tinyHEG prototype, which uses the MCP4728 DAC to control 4 LEDs. The Analog 0 pin is connected to one photodetector, which was looking at channel C. 

This worked great, and we got good data from the Analog pin. So I threw the program back in to Claude and simplified it to only use one channel:

```cpp
#include <Adafruit_MCP4728.h>
#include <Wire.h>
#include "driver/adc.h"
#include "esp_adc/adc_oneshot.h"

Adafruit_MCP4728 mcp;

// Constants
const int ANALOG_PIN = 18;  // GPIO18, ADC2_CH7
const int LED_VALUE = 400;  // LED brightness value
const unsigned long TOGGLE_INTERVAL = 25;  // 100 microseconds toggle interval
const unsigned long SAMPLE_DELAY = 10;  // Wait 50 microseconds after toggling before sampling
const int BATCH_SIZE = 100;  // Number of samples to collect before printing

// Variables for timing and measurements
unsigned long lastToggleMicros = 0;
unsigned long lastSampleTime = 0;
bool channelCState = false;
int highSample = 0;
int lowSample = 0;

// Batch processing variables
int differenceSum = 0;
unsigned long intervalSum = 0;
int sampleCount = 0;

// ADC handles
adc_oneshot_unit_handle_t adc2_handle;
adc_oneshot_unit_init_cfg_t init_config2;
adc_oneshot_chan_cfg_t config;

void setup(void) {
  Serial.begin(2000000);
  
  // Initialize I2C and LED control
  pinMode(6, OUTPUT);
  digitalWrite(6, HIGH);

  Wire.begin(3, 4);
  Wire.setClock(800000);
  delay(100);

  if (!mcp.begin()) {
    Serial.println("Failed to find MCP4728 chip");
    while (1) {
      delay(10);
    }
  }

  // Configure ADC
  init_config2.unit_id = ADC_UNIT_2;
  init_config2.ulp_mode = ADC_ULP_MODE_DISABLE;
  init_config2.clk_src = ADC_RTC_CLK_SRC_DEFAULT;
  ESP_ERROR_CHECK(adc_oneshot_new_unit(&init_config2, &adc2_handle));

  // Configure ADC channel
  config.atten = ADC_ATTEN_DB_11;
  config.bitwidth = ADC_BITWIDTH_12;
  ESP_ERROR_CHECK(adc_oneshot_config_channel(adc2_handle, ADC_CHANNEL_7, &config));

  // Initialize all channels to 0
  mcp.setChannelValue(MCP4728_CHANNEL_A, 0);
  mcp.setChannelValue(MCP4728_CHANNEL_B, 0);
  mcp.setChannelValue(MCP4728_CHANNEL_C, 0);
  mcp.setChannelValue(MCP4728_CHANNEL_D, 0);

  // Initialize timing variables
  lastSampleTime = micros();

  // Print header
  Serial.println("Average_Difference,Average_Sample_Interval_us");
}

void loop() {
  unsigned long currentMicros = micros();
  
  if (currentMicros - lastToggleMicros >= TOGGLE_INTERVAL) {
    lastToggleMicros = currentMicros;
    
    // Calculate time since last sample
    unsigned long sampleInterval = currentMicros - lastSampleTime;
    lastSampleTime = currentMicros;
    
    // Turn on Channel C
    mcp.setChannelValue(MCP4728_CHANNEL_C, LED_VALUE);
    delayMicroseconds(SAMPLE_DELAY);  // Wait for signal to stabilize
    
    // Take high sample
    if (adc_oneshot_read(adc2_handle, ADC_CHANNEL_7, &highSample) != ESP_OK) {
      highSample = 0;  // In case of error
    }
    
    // Turn off Channel C
    mcp.setChannelValue(MCP4728_CHANNEL_C, 0);
    delayMicroseconds(SAMPLE_DELAY);  // Wait for signal to stabilize
    
    // Take low sample
    if (adc_oneshot_read(adc2_handle, ADC_CHANNEL_7, &lowSample) != ESP_OK) {
      lowSample = 0;  // In case of error
    }
    
    // Calculate difference and add to sum
    int difference = highSample - lowSample;
    differenceSum += difference;
    intervalSum += sampleInterval;
    sampleCount++;
    
    // If we've collected BATCH_SIZE samples, calculate and print averages
    if (sampleCount >= BATCH_SIZE) {
      float avgDifference = (float)differenceSum / BATCH_SIZE;
      float avgInterval = (float)intervalSum / BATCH_SIZE;
      
      // Print averages
      Serial.print(avgDifference);
      Serial.print(",");
      Serial.println(avgInterval);
      
      // Reset counters and sums
      differenceSum = 0;
      intervalSum = 0;
      sampleCount = 0;
    }
  }
}
```

This worked as well, so then I switched to an MCP4725, which is a single channel DAC to control the LED:

```cpp
#include <Adafruit_MCP4725.h>
#include <Wire.h>
#include "driver/adc.h"
#include "esp_adc/adc_oneshot.h"

Adafruit_MCP4725 dac;

// Constants
const int ANALOG_PIN = 18;  // GPIO18, ADC2_CH7
const int LED_VALUE = 400;  // LED brightness value
const unsigned long TOGGLE_INTERVAL = 25;  // 100 microseconds toggle interval
const unsigned long SAMPLE_DELAY = 10;  // Wait 50 microseconds after toggling before sampling
const int BATCH_SIZE = 100;  // Number of samples to collect before printing

// Variables for timing and measurements
unsigned long lastToggleMicros = 0;
unsigned long lastSampleTime = 0;
bool ledState = false;
int highSample = 0;
int lowSample = 0;

// Batch processing variables
int differenceSum = 0;
unsigned long intervalSum = 0;
int sampleCount = 0;

// ADC handles
adc_oneshot_unit_handle_t adc2_handle;
adc_oneshot_unit_init_cfg_t init_config2;
adc_oneshot_chan_cfg_t config;

void setup(void) {
  Serial.begin(2000000);
  
  // Initialize I2C and LED control
  pinMode(6, OUTPUT);
  digitalWrite(6, HIGH);

  Wire.begin(3, 4);
  Wire.setClock(800000);
  delay(100);

  if (!dac.begin(0x62)) {  // Default I2C address for MCP4725
    Serial.println("Failed to find MCP4725 chip");
    while (1) {
      delay(10);
    }
  }

  // Configure ADC
  init_config2.unit_id = ADC_UNIT_2;
  init_config2.ulp_mode = ADC_ULP_MODE_DISABLE;
  init_config2.clk_src = ADC_RTC_CLK_SRC_DEFAULT;
  ESP_ERROR_CHECK(adc_oneshot_new_unit(&init_config2, &adc2_handle));

  // Configure ADC channel
  config.atten = ADC_ATTEN_DB_11;
  config.bitwidth = ADC_BITWIDTH_12;
  ESP_ERROR_CHECK(adc_oneshot_config_channel(adc2_handle, ADC_CHANNEL_7, &config));

  // Initialize DAC to 0
  dac.setVoltage(0, false);

  // Initialize timing variables
  lastSampleTime = micros();

  // Print header
  Serial.println("Average_Difference,Average_Sample_Interval_us");
}

void loop() {
  unsigned long currentMicros = micros();
  
  if (currentMicros - lastToggleMicros >= TOGGLE_INTERVAL) {
    lastToggleMicros = currentMicros;
    
    // Calculate time since last sample
    unsigned long sampleInterval = currentMicros - lastSampleTime;
    lastSampleTime = currentMicros;
    
    // Set DAC output high
    dac.setVoltage(LED_VALUE, false);
    delayMicroseconds(SAMPLE_DELAY);  // Wait for signal to stabilize
    
    // Take high sample
    if (adc_oneshot_read(adc2_handle, ADC_CHANNEL_7, &highSample) != ESP_OK) {
      highSample = 0;  // In case of error
    }
    
    // Set DAC output low
    dac.setVoltage(0, false);
    delayMicroseconds(SAMPLE_DELAY);  // Wait for signal to stabilize
    
    // Take low sample
    if (adc_oneshot_read(adc2_handle, ADC_CHANNEL_7, &lowSample) != ESP_OK) {
      lowSample = 0;  // In case of error
    }
    
    // Calculate difference and add to sum
    int difference = highSample - lowSample;
    differenceSum += difference;
    intervalSum += sampleInterval;
    sampleCount++;
    
    // If we've collected BATCH_SIZE samples, calculate and print averages
    if (sampleCount >= BATCH_SIZE) {
      float avgDifference = (float)differenceSum / BATCH_SIZE;
      float avgInterval = (float)intervalSum / BATCH_SIZE;
      
      // Print averages
      Serial.print(avgDifference);
      Serial.print(",");
      Serial.println(avgInterval);
      
      // Reset counters and sums
      differenceSum = 0;
      intervalSum = 0;
      sampleCount = 0;
    }
  }
}
```



<div class="post-link">

    &nbsp;

</div>

