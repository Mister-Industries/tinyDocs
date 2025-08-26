# Using ChatGPT and TTS

```cpp
#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <driver/i2s.h>
#include "AudioOutputI2S.h"
#include "AudioGeneratorMP3.h"
#include "AudioFileSourceBuffer.h"
#include "AudioFileSourceHTTPStream.h"

// Pin definitions
#define I2S_BCLK_PIN       8  // Bit clock
#define I2S_LRCLK_PIN      9  // Left/Right clock (Word Select)
#define I2S_DATA_PIN       10 // Data pin

// Network credentials
const char* ssid = "YOURSSIDHERE";
const char* password = "YOURPASSWORDHERE";

// OpenAI API configuration
const char* openai_api_key = "YOURAPIKEYHERE";
const char* openai_endpoint = "https://api.openai.com/v1/chat/completions";

// VoiceRSS TTS configuration
const char* tts_endpoint = "http://api.voicerss.org/";
const char* tts_api_key = "YOURAPIKEYHERE";

// Audio objects
AudioOutputI2S *out;
AudioGeneratorMP3 *mp3;
AudioFileSourceHTTPStream *file;
AudioFileSourceBuffer *buff;

// Buffer for audio streaming
uint8_t* audio_buffer;
const int BUFFER_SIZE = 8192;

// Initialize I2S configuration
void initI2S() {
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
        .sample_rate = 16000,  // Match the TTS audio sample rate
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,  // Stereo
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 8,
        .dma_buf_len = 64,
        .use_apll = false,
        .tx_desc_auto_clear = true,
        .fixed_mclk = 0
    };

    // ... rest of the function remains unchanged
}

void setup() {
    Serial.begin(115200);
    
    // Connect to WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to WiFi");

    // Initialize I2S
    initI2S();
    out = new AudioOutputI2S();
    out->SetPinout(I2S_BCLK_PIN, I2S_LRCLK_PIN, I2S_DATA_PIN);
    out->SetGain(0.5);

    // Initialize audio buffer
    audio_buffer = (uint8_t*)malloc(BUFFER_SIZE);
    mp3 = new AudioGeneratorMP3();
}

String urlencode(String str) {
    String encodedString = "";
    char c;
    char code0;
    char code1;
    for (int i = 0; i < str.length(); i++){
        c = str.charAt(i);
        if (isalnum(c)){
            encodedString += c;
        } else {
            encodedString += '%';
            code0 = (c >> 4) & 0xF;
            code1 = c & 0xF;
            code0 += code0 > 9 ? 'A' - 10 : '0';
            code1 += code1 > 9 ? 'A' - 10 : '0';
            encodedString += code0;
            encodedString += code1;
        }
    }
    return encodedString;
}

String getChatGPTResponse(String userInput) {
    if (WiFi.status() != WL_CONNECTED) {
        return "WiFi not connected";
    }

    HTTPClient http;
    http.begin(openai_endpoint);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", String("Bearer ") + openai_api_key);

    // Prepare the request payload
    StaticJsonDocument<2048> doc;  // Increase size if necessary
    doc["model"] = "gpt-3.5-turbo";  // Update model as needed
    JsonArray messages = doc.createNestedArray("messages");
    
    // You can add previous conversation turns to maintain context
    JsonObject userMessage = messages.createNestedObject();
    userMessage["role"] = "user";
    userMessage["content"] = userInput;

    String requestBody;
    serializeJson(doc, requestBody);

    int httpResponseCode = http.POST(requestBody);
    String response = "";

    if (httpResponseCode == HTTP_CODE_OK) {
        response = http.getString();
        // Parse the response
        StaticJsonDocument<6144> responseDoc;  // Adjust size as needed
        DeserializationError error = deserializeJson(responseDoc, response);
        if (!error) {
            response = responseDoc["choices"][0]["message"]["content"].as<String>();
        } else {
            Serial.println("Error parsing response");
            response = "Error parsing response";
        }
    } else {
        Serial.printf("OpenAI API request failed with code %d\n", httpResponseCode);
        response = "Error in API request";
    }

    http.end();
    return response;
}

bool textToSpeech(String text) {
    if (WiFi.status() != WL_CONNECTED) {
        return false;
    }

    // URL encode the text
    String encodedText = urlencode(text);

    // Construct the URL for the TTS request
    String url = String(tts_endpoint) +
                 "?key=" + tts_api_key +
                 "&hl=en-us" +   // Language
                 "&c=MP3" +      // Codec
                 "&f=16khz_16bit_stereo" +  // Format
                 "&src=" + encodedText;

    Serial.println("TTS Request URL: " + url);

    // Clean up previous audio sources
    if (file != nullptr) {
        delete file;
        file = nullptr;
    }
    if (buff != nullptr) {
        delete buff;
        buff = nullptr;
    }

    // Create audio source from the TTS URL
    file = new AudioFileSourceHTTPStream(url.c_str());
    buff = new AudioFileSourceBuffer(file, audio_buffer, BUFFER_SIZE);
    mp3->begin(buff, out);
    return true;
}

void loop() {
    if (Serial.available()) {
        String userInput = Serial.readStringUntil('\n');
        Serial.println("You: " + userInput);

        // Get ChatGPT response
        String response = getChatGPTResponse(userInput);
        Serial.println("ChatGPT: " + response);

        // Convert response to speech and play
        if (textToSpeech(response)) {
            Serial.println("Playing audio response...");
        } else {
            Serial.println("Failed to get audio response");
        }
    }

    // Handle audio playback
    if (mp3->isRunning()) {
        if (!mp3->loop()) {
            mp3->stop();

            if (buff != nullptr) {
                delete buff;
                buff = nullptr;
            }

            if (file != nullptr) {
                file->close();
                delete file;
                file = nullptr;
            }
        }
    }

    // Add a small delay to prevent watchdog timer issues
    delay(1);
}
```