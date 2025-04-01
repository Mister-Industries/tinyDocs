---
title: I2S Audio Test
slug: 2024-11-24-12:00
publish: true
date: 2024-11-24 12:00:00
update: 2024-11-24 12:00:00
description: Testing I2S Audio on the tinyCore
categories:
  - Testing
tags:
  - example
  - code
  - I2S
  - Audio
hide:
  - toc
  - navigation
---
I had Claude write up an I2S Test for a speaker, specifically the MAX98357A. Here's the program it wrote:

<!-- more -->

```cpp
#include <driver/i2s.h>

// I2S pins for ESP32-S3 Feather
#define I2S_BCLK_PIN       8  // Bit clock
#define I2S_LRCLK_PIN      9  // Left/Right clock (Word Select)
#define I2S_DATA_PIN       10  // Data pin

// I2S configuration
#define SAMPLE_RATE     44100  // Audio sample rate in Hz
#define BITS_PER_SAMPLE    16  // Bits per sample
#define CHANNEL_NUM         2  // Number of channels (stereo)

// DMA buffer parameters
#define DMA_BUF_COUNT      8  // Number of DMA buffers
#define DMA_BUF_LEN      256  // Size of each DMA buffer

void setup() {
    Serial.begin(115200);
    
    // Configure I2S
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
        .sample_rate = SAMPLE_RATE,
        .bits_per_sample = (i2s_bits_per_sample_t)BITS_PER_SAMPLE,
        .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = DMA_BUF_COUNT,
        .dma_buf_len = DMA_BUF_LEN,
        .use_apll = false,
        .tx_desc_auto_clear = true,
        .fixed_mclk = 0
    };
    
    // Configure I2S pins
    i2s_pin_config_t pin_config = {
        .mck_io_num = I2S_PIN_NO_CHANGE,
        .bck_io_num = I2S_BCLK_PIN,
        .ws_io_num = I2S_LRCLK_PIN,
        .data_out_num = I2S_DATA_PIN,
        .data_in_num = I2S_PIN_NO_CHANGE
    };
    
    // Install and start I2S driver
    esp_err_t result = i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
    if (result != ESP_OK) {
        Serial.println("Error installing I2S driver");
        return;
    }
    
    result = i2s_set_pin(I2S_NUM_0, &pin_config);
    if (result != ESP_OK) {
        Serial.println("Error setting I2S pins");
        return;
    }
    
    Serial.println("I2S initialized successfully");
}

// Example function to write a sine wave to I2S
void writeSineWave() {
    // Generate a 440 Hz sine wave
    const float frequency = 440.0;  // A4 note
    const float amplitude = 32000;  // Volume (max is 32767 for 16-bit)
    
    // Buffer for audio samples
    int16_t samples[DMA_BUF_LEN * 2];  // *2 for stereo
    
    static float phase = 0.0;
    const float phase_increment = 2.0 * PI * frequency / SAMPLE_RATE;
    
    // Fill the buffer with sine wave samples
    for (int i = 0; i < DMA_BUF_LEN * 2; i += 2) {
        int16_t sample = (int16_t)(amplitude * sin(phase));
        samples[i] = sample;      // Left channel
        samples[i + 1] = sample;  // Right channel
        
        phase += phase_increment;
        if (phase >= 2.0 * PI) {
            phase -= 2.0 * PI;
        }
    }
    
    // Write the samples to I2S
    size_t bytes_written;
    i2s_write(I2S_NUM_0, samples, sizeof(samples), &bytes_written, portMAX_DELAY);
}

void loop() {
    // Continuously output the sine wave
    writeSineWave();
}
```

It worked right away! This program will play a 440 Hz tone. 

<aside>
Note: Install the ESP8266 Library before compiling.

</aside>

I then had Claude update the code to read an MP3 file from the SD Card. Here's the functioning code:

```cpp
#include <Arduino.h>
#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include <driver/i2s.h>
#include "AudioFileSourceSD.h"
#include "AudioFileSourceID3.h"
#include "AudioGeneratorMP3.h"
#include "AudioOutputI2S.h"

// Pin definitions
#define I2S_BCLK_PIN       8  // Bit clock
#define I2S_LRCLK_PIN      9  // Left/Right clock (Word Select)
#define I2S_DATA_PIN       10  // Data pin

// Audio objects
AudioFileSourceSD *file;
AudioFileSourceID3 *id3;
AudioGeneratorMP3 *mp3;
AudioOutputI2S *out;

void setup() {
    Serial.begin(115200);
    while (!Serial) {
        delay(10);
    }
    Serial.println("Initializing...");

    // Initialize SD card using the working method
    if (!SD.begin()) {
        Serial.println("Card Mount Failed");
        return;
    }

    uint8_t cardType = SD.cardType();
    if (cardType == CARD_NONE) {
        Serial.println("No SD card attached");
        return;
    }

    Serial.print("SD Card Type: ");
    if (cardType == CARD_MMC) {
        Serial.println("MMC");
    } else if (cardType == CARD_SD) {
        Serial.println("SDSC");
    } else if (cardType == CARD_SDHC) {
        Serial.println("SDHC");
    } else {
        Serial.println("UNKNOWN");
    }

    // Check if test.mp3 exists
    if (!SD.exists("/test.mp3")) {
        Serial.println("Can't find /test.mp3");
        return;
    }
    Serial.println("Found test.mp3");

    // Set up I2S output
    out = new AudioOutputI2S();
    out->SetPinout(I2S_BCLK_PIN, I2S_LRCLK_PIN, I2S_DATA_PIN);
    out->SetGain(0.5); // Set volume (0.0-1.0)

    // Set up MP3 decoder
    file = new AudioFileSourceSD("/test.mp3");
    id3 = new AudioFileSourceID3(file);
    mp3 = new AudioGeneratorMP3();

    Serial.println("Starting MP3...");
    mp3->begin(id3, out);
}

void loop() {
    if (mp3->isRunning()) {
        if (!mp3->loop()) {
            // File is finished playing
            mp3->stop();
            Serial.println("MP3 playback completed");
            delay(1000);

            // Restart playback
            Serial.println("Restarting playback...");
            file->open("/test.mp3");
            mp3->begin(id3, out);
        }
    } else {
        Serial.println("MP3 not running, attempting to restart...");
        delay(1000);
        file->open("/test.mp3");
        mp3->begin(id3, out);
    }
}
```

This one took a few tries, but next I generated some code to record via a microphone and then play it back over the speaker:

```cpp
#include <Arduino.h>
#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include <driver/i2s.h>

// Pin Definitions
// Microphone (SPH0645)
#define I2S_MIC_SCK     8
#define I2S_MIC_WS      9
#define I2S_MIC_SD      10

// Speaker
#define I2S_SPKR_BCLK   8
#define I2S_SPKR_LRC    9
#define I2S_SPKR_DIN    10

// Constants for recording
const int RECORD_TIME = 5;  // seconds to record
const int SAMPLE_RATE = 44100;
const int SAMPLE_BITS = 32;
const int WAV_HEADER_SIZE = 44;
const char* RECORD_FILE = "/recording.wav";
const int BINARY_BUFFER_SIZE = 1024;

// Global flag to track I2S state
bool i2s_initialized = false;

// WAV header structure
struct WavHeader {
    char riff[4] = {'R', 'I', 'F', 'F'};
    uint32_t fileSize = 0;
    char wave[4] = {'W', 'A', 'V', 'E'};
    char fmt[4] = {'f', 'm', 't', ' '};
    uint32_t fmtSize = 16;
    uint16_t audioFormat = 1;
    uint16_t numChannels = 1;
    uint32_t sampleRate = SAMPLE_RATE;
    uint32_t byteRate = SAMPLE_RATE * 2;
    uint16_t blockAlign = 2;
    uint16_t bitsPerSample = 16;
    char data[4] = {'d', 'a', 't', 'a'};
    uint32_t dataSize = 0;
};

void cleanup_i2s() {
    if (i2s_initialized) {
        i2s_stop(I2S_NUM_0);
        i2s_driver_uninstall(I2S_NUM_0);
        i2s_initialized = false;
        delay(100);
    }
}

void i2s_mic_init() {
    cleanup_i2s();
    
    // Configuration for SPH0645
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
        .sample_rate = SAMPLE_RATE,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 4,
        .dma_buf_len = 1024,
        .use_apll = false,
        .tx_desc_auto_clear = false,
        .fixed_mclk = 0
    };
    
    i2s_pin_config_t pin_config = {
        .mck_io_num = I2S_PIN_NO_CHANGE,
        .bck_io_num = I2S_MIC_SCK,
        .ws_io_num = I2S_MIC_WS,
        .data_out_num = I2S_PIN_NO_CHANGE,
        .data_in_num = I2S_MIC_SD
    };
    
    esp_err_t err = i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
    if (err != ESP_OK) {
        Serial.printf("Failed to install I2S driver for mic: %d\n", err);
        return;
    }
    
    err = i2s_set_pin(I2S_NUM_0, &pin_config);
    if (err != ESP_OK) {
        Serial.printf("Failed to set I2S pins for mic: %d\n", err);
        return;
    }
    
    i2s_initialized = true;
    delay(100);
}

void i2s_speaker_init() {
    cleanup_i2s();
    
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
        .sample_rate = SAMPLE_RATE,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 8,
        .dma_buf_len = 1024,
        .use_apll = false,
        .tx_desc_auto_clear = true,
        .fixed_mclk = 0
    };
    
    i2s_pin_config_t pin_config = {
        .mck_io_num = I2S_PIN_NO_CHANGE,
        .bck_io_num = I2S_SPKR_BCLK,
        .ws_io_num = I2S_SPKR_LRC,
        .data_out_num = I2S_SPKR_DIN,
        .data_in_num = I2S_PIN_NO_CHANGE
    };
    
    esp_err_t err = i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
    if (err != ESP_OK) {
        Serial.printf("Failed to install I2S driver for speaker: %d\n", err);
        return;
    }
    
    err = i2s_set_pin(I2S_NUM_0, &pin_config);
    if (err != ESP_OK) {
        Serial.printf("Failed to set I2S pins for speaker: %d\n", err);
        return;
    }
    
    i2s_initialized = true;
    delay(100);
}

void writeWavHeader(File file, size_t dataSize) {
    WavHeader header;
    header.fileSize = dataSize + WAV_HEADER_SIZE - 8;
    header.dataSize = dataSize;
    file.write((const uint8_t*)&header, WAV_HEADER_SIZE);
}

void startRecording() {
    Serial.println("Starting recording...");
    
    i2s_mic_init();
    
    if (!i2s_initialized) {
        Serial.println("Failed to initialize I2S for recording");
        return;
    }
    
    if (SD.exists(RECORD_FILE)) {
        SD.remove(RECORD_FILE);
    }
    
    File file = SD.open(RECORD_FILE, FILE_WRITE);
    if (!file) {
        Serial.println("Failed to open file for recording");
        return;
    }
    
    // Write placeholder header
    WavHeader header;
    file.write((const uint8_t*)&header, WAV_HEADER_SIZE);
    
    size_t bytesWritten = 0;
    unsigned long startTime = millis();
    int32_t samples[BINARY_BUFFER_SIZE/4];
    
    Serial.println("Recording...");
    
    while ((millis() - startTime) < (RECORD_TIME * 1000)) {
        size_t bytesRead = 0;
        esp_err_t result = i2s_read(I2S_NUM_0, samples, sizeof(samples), &bytesRead, portMAX_DELAY);
        
        if (result == ESP_OK && bytesRead > 0) {
            // Process SPH0645 data: 24-bit signed integer in MSB format
            int16_t converted[BINARY_BUFFER_SIZE/8];
            for (int i = 0; i < bytesRead/4; i++) {
                // Convert 24-bit to 16-bit with proper scaling
                converted[i] = (int16_t)(samples[i] >> 14);
            }
            file.write((const uint8_t*)converted, bytesRead/2);
            bytesWritten += bytesRead/2;
        }
    }
    
    // Update WAV header with final size
    file.seek(0);
    writeWavHeader(file, bytesWritten);
    file.close();
    
    cleanup_i2s();
    Serial.println("Recording finished!");
}

void playRecording() {
    Serial.println("Playing recording...");
    
    // Initialize speaker
    i2s_speaker_init();
    if (!i2s_initialized) {
        Serial.println("Failed to initialize I2S for playback");
        return;
    }
    
    // Open WAV file
    File file = SD.open(RECORD_FILE);
    if (!file) {
        Serial.println("Failed to open file for playback");
        return;
    }
    
    // Skip WAV header
    file.seek(WAV_HEADER_SIZE);
    
    // Read and play file
    uint8_t buffer[1024];
    size_t bytes_read;
    Serial.println("Starting playback...");
    
    while (file.available()) {
        bytes_read = file.read(buffer, sizeof(buffer));
        if (bytes_read > 0) {
            size_t bytes_written = 0;

            // Amplify the signal
            int16_t *samples = (int16_t*)buffer;
            for(int i=0; i < bytes_read/2; i++) {
              samples[i] = samples[i] * 4;  // Multiply by 2-8 for more volume
            }
            
            esp_err_t result = i2s_write(I2S_NUM_0, buffer, bytes_read, &bytes_written, portMAX_DELAY);
            if (result != ESP_OK) {
                Serial.printf("Failed to write I2S data: %d\n", result);
            }
        }
    }
    
    file.close();
    cleanup_i2s();
    Serial.println("Playback finished!");
}

void setup() {
    Serial.begin(115200);
    while (!Serial) delay(10);
    
    Serial.println("Initializing...");
    
    // Initialize SD card
    if (!SD.begin()) {
        Serial.println("Card Mount Failed");
        return;
    }
    
    // Make sure I2S is clean at startup
    cleanup_i2s();
    
    Serial.println("Ready! Send 'R' to start recording.");
}

void loop() {
    if (Serial.available()) {
        char cmd = Serial.read();
        if (cmd == 'R' || cmd == 'r') {
            startRecording();
            delay(500);
            playRecording();
        }
    }
}
```

And it works great! I'm able to record a short message and play it back over the speaker!