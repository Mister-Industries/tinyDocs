# How to Control a Buzzer (Analog Output)

Ready to make some noise? Let's learn how to control a buzzer with your tinyCore! This tutorial will teach you about PWM (Pulse Width Modulation) - a super important concept that lets you control not just buzzers, but motors, LED brightness, and tons of other analog devices.

!!! warning "Are you skipping ahead?"

    Make sure you have already setup your Arduino IDE using the [previous tutorial](../get-started/arduino-ide.md)!

## What is PWM?

PWM stands for "Pulse Width Modulation" - think of it like rapidly turning a light switch on and off really fast. By changing how long it stays "on" vs "off", you can control how bright an LED appears, how loud a buzzer sounds, or how fast a motor spins.

For buzzers, we care about two things:
- **Frequency** - How fast we switch (determines the pitch/tone)
- **Duty Cycle** - How long it stays "on" vs "off" (affects volume)

![PWM Diagram](images/pwm-explanation.png)

## What you'll need

- Your tinyCore ESP32-S3
- A **passive buzzer** (the kind that needs a signal to make sound)
- Some jumper wires
- A breadboard (optional)

!!! tip "Passive vs Active Buzzers"

    **Passive buzzers** need you to send a frequency signal - these are what we want! They give you full control over the tone.
    
    **Active buzzers** just make one sound when you give them power - they're boring for this tutorial.
    
    If you're not sure which you have, try connecting it to 3.3V. If it makes a sound, it's active. If it's silent, it's passive (perfect!).

## Step 1: Wire it up

This is super simple - just two wires!

1. **Buzzer positive (+) wire** → **GPIO pin 2** on tinyCore
2. **Buzzer negative (-) wire** → **GND** on tinyCore

![Buzzer Wiring](images/buzzer-wiring.png)

!!! warning "Why not the Arduino `tone()` function?"

    Here's a fun fact: The classic Arduino `tone()` function doesn't work on ESP32! But don't worry - the ESP32's PWM system is actually way more powerful and flexible than the old `tone()` function.

## Step 2: Basic beeping code

Let's start with a simple beep to make sure everything works:

```cpp
// Simple Buzzer Beep for tinyCore ESP32-S3

const int buzzerPin = 2;        // GPIO pin connected to buzzer
const int pwmChannel = 0;       // PWM channel (ESP32 has 16 channels)
const int resolution = 8;       // 8-bit resolution (0-255 values)

void setup() {
  Serial.begin(115200);
  
  // Configure the PWM channel
  ledcSetup(pwmChannel, 1000, resolution);  // 1000 Hz frequency, 8-bit resolution
  
  // Attach the PWM channel to our buzzer pin
  ledcAttachPin(buzzerPin, pwmChannel);
  
  Serial.println("Buzzer ready! Making some noise...");
}

void loop() {
  // Play a 1000 Hz tone
  ledcWriteTone(pwmChannel, 1000);
  delay(500);  // Beep for half a second
  
  // Stop the sound
  ledcWriteTone(pwmChannel, 0);
  delay(500);  // Silence for half a second
}
```

Upload this code and you should hear regular beeping! 🎵

## Step 3: Playing different tones

Now let's get musical! Here's code that plays a simple scale:

```cpp
// Musical Scale with Buzzer

const int buzzerPin = 2;
const int pwmChannel = 0;
const int resolution = 8;

// Musical note frequencies (in Hz)
const int NOTE_C4 = 262;
const int NOTE_D4 = 294;
const int NOTE_E4 = 330;
const int NOTE_F4 = 349;
const int NOTE_G4 = 392;
const int NOTE_A4 = 440;
const int NOTE_B4 = 494;
const int NOTE_C5 = 523;

void setup() {
  Serial.begin(115200);
  ledcSetup(pwmChannel, 2000, resolution);
  ledcAttachPin(buzzerPin, pwmChannel);
  
  Serial.println("Playing musical scale...");
}

void playNote(int frequency, int duration) {
  if (frequency > 0) {
    ledcWriteTone(pwmChannel, frequency);
  } else {
    ledcWriteTone(pwmChannel, 0);  // Rest (silence)
  }
  delay(duration);
  ledcWriteTone(pwmChannel, 0);  // Stop sound
  delay(50);  // Small pause between notes
}

void loop() {
  // Play a C major scale
  playNote(NOTE_C4, 500);
  playNote(NOTE_D4, 500);
  playNote(NOTE_E4, 500);
  playNote(NOTE_F4, 500);
  playNote(NOTE_G4, 500);
  playNote(NOTE_A4, 500);
  playNote(NOTE_B4, 500);
  playNote(NOTE_C5, 500);
  
  delay(1000);  // Pause before repeating
}
```

## Step 4: Play a real song!

Let's play "Twinkle, Twinkle, Little Star":

```cpp
// Twinkle Twinkle Little Star

const int buzzerPin = 2;
const int pwmChannel = 0;
const int resolution = 8;

// Note frequencies
const int NOTE_C4 = 262;
const int NOTE_D4 = 294;
const int NOTE_E4 = 330;
const int NOTE_F4 = 349;
const int NOTE_G4 = 392;
const int NOTE_A4 = 440;
const int NOTE_B4 = 494;
const int REST = 0;

// Twinkle Twinkle melody
int melody[] = {
  NOTE_C4, NOTE_C4, NOTE_G4, NOTE_G4, NOTE_A4, NOTE_A4, NOTE_G4, REST,
  NOTE_F4, NOTE_F4, NOTE_E4, NOTE_E4, NOTE_D4, NOTE_D4, NOTE_C4, REST,
  NOTE_G4, NOTE_G4, NOTE_F4, NOTE_F4, NOTE_E4, NOTE_E4, NOTE_D4, REST,
  NOTE_G4, NOTE_G4, NOTE_F4, NOTE_F4, NOTE_E4, NOTE_E4, NOTE_D4, REST,
  NOTE_C4, NOTE_C4, NOTE_G4, NOTE_G4, NOTE_A4, NOTE_A4, NOTE_G4, REST,
  NOTE_F4, NOTE_F4, NOTE_E4, NOTE_E4, NOTE_D4, NOTE_D4, NOTE_C4, REST
};

// Note durations (in milliseconds)
int noteDurations[] = {
  400, 400, 400, 400, 400, 400, 600, 200,
  400, 400, 400, 400, 400, 400, 600, 200,
  400, 400, 400, 400, 400, 400, 600, 200,
  400, 400, 400, 400, 400, 400, 600, 200,
  400, 400, 400, 400, 400, 400, 600, 200,
  400, 400, 400, 400, 400, 400, 800, 400
};

void setup() {
  Serial.begin(115200);
  ledcSetup(pwmChannel, 2000, resolution);
  ledcAttachPin(buzzerPin, pwmChannel);
  
  Serial.println("Playing Twinkle Twinkle Little Star!");
}

void playSong() {
  int songLength = sizeof(melody) / sizeof(melody[0]);
  
  for (int i = 0; i < songLength; i++) {
    if (melody[i] > 0) {
      ledcWriteTone(pwmChannel, melody[i]);
    } else {
      ledcWriteTone(pwmChannel, 0);  // Rest
    }
    
    delay(noteDurations[i]);
    ledcWriteTone(pwmChannel, 0);  // Stop sound
    delay(50);  // Small pause between notes
  }
}

void loop() {
  playSong();
  delay(2000);  // Wait 2 seconds before playing again
}
```

## Step 5: Interactive buzzer

Let's make it respond to Serial input - type different letters to play different sounds:

```cpp
// Interactive Buzzer Control

const int buzzerPin = 2;
const int pwmChannel = 0;
const int resolution = 8;

void setup() {
  Serial.begin(115200);
  ledcSetup(pwmChannel, 2000, resolution);
  ledcAttachPin(buzzerPin, pwmChannel);
  
  Serial.println("=== Interactive Buzzer Control ===");
  Serial.println("Type letters to make sounds:");
  Serial.println("a-g = Musical notes");
  Serial.println("s = Siren");
  Serial.println("b = Beep");
  Serial.println("r = R2D2 sound");
  Serial.println("x = Stop sound");
}

void playNote(int frequency, int duration) {
  ledcWriteTone(pwmChannel, frequency);
  delay(duration);
  ledcWriteTone(pwmChannel, 0);
}

void playSiren() {
  for (int freq = 400; freq < 2000; freq += 50) {
    ledcWriteTone(pwmChannel, freq);
    delay(20);
  }
  for (int freq = 2000; freq > 400; freq -= 50) {
    ledcWriteTone(pwmChannel, freq);
    delay(20);
  }
  ledcWriteTone(pwmChannel, 0);
}

void playR2D2() {
  for (int i = 0; i < 5; i++) {
    ledcWriteTone(pwmChannel, 1000 + (i * 200));
    delay(100);
    ledcWriteTone(pwmChannel, 800 - (i * 100));
    delay(100);
  }
  ledcWriteTone(pwmChannel, 0);
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    
    switch (command) {
      case 'a': playNote(262, 500); break;  // C
      case 'b': playNote(294, 500); break;  // D
      case 'c': playNote(330, 500); break;  // E
      case 'd': playNote(349, 500); break;  // F
      case 'e': playNote(392, 500); break;  // G
      case 'f': playNote(440, 500); break;  // A
      case 'g': playNote(494, 500); break;  // B
      
      case 's': 
        Serial.println("🚨 Siren!");
        playSiren(); 
        break;
        
      case 'r':
        Serial.println("🤖 R2D2!");
        playR2D2();
        break;
        
      case 'b':
        Serial.println("📢 Beep!");
        playNote(1000, 200);
        break;
        
      case 'x':
        Serial.println("🔇 Stopping sound");
        ledcWriteTone(pwmChannel, 0);
        break;
        
      default:
        Serial.println("Unknown command!");
        break;
    }
  }
}
```

Try typing different letters in the Serial Monitor and listen to the sounds!

## Understanding the code

Let's break down the key functions:

**PWM Setup:**
```cpp
ledcSetup(pwmChannel, 2000, resolution);  // Configure PWM channel
ledcAttachPin(buzzerPin, pwmChannel);     // Connect channel to GPIO pin
```

**Playing tones:**
```cpp
ledcWriteTone(pwmChannel, frequency);  // Play a frequency
ledcWriteTone(pwmChannel, 0);          // Stop sound (frequency = 0)
```

**Key concepts:**
- **Channel** - ESP32 has 16 PWM channels you can use simultaneously
- **Frequency** - Higher numbers = higher pitch (measured in Hz)
- **Resolution** - 8-bit gives you 0-255 levels of control

## Common issues

**No sound from buzzer**
- Check you have a **passive** buzzer (not active)
- Verify wiring: positive to GPIO 2, negative to ground
- Try a different GPIO pin (any output pin works)
- Make sure the buzzer isn't broken - test with 3.3V

**Sound is too quiet**
- Some buzzers are just quieter than others
- You can try adjusting the duty cycle with `ledcWrite(channel, 128)` instead of `ledcWriteTone()`
- Make sure connections are secure

**Code won't compile**
- Make sure you're using ESP32 board package version 3.x
- The functions changed in recent versions - this code is for the latest version

**Buzzer makes noise even when stopped**
- This can happen with some buzzers - try `ledcDetachPin(buzzerPin)` to completely disconnect

## What's next?

Now you understand PWM and analog output! This opens up tons of possibilities:

- **Control LED brightness** - Use PWM to dim/brighten LEDs smoothly
- **Motor speed control** - PWM controls how fast motors spin
- **Servo control** - Precise positioning of servo motors
- **Sound effects** - Create beeps, alarms, and musical instruments
- **Combined projects** - Add sound alerts to your [motion detector](detect-motion.md)

Want to learn more? Check out [What is PWM?](../reference/pwm.md) for the technical deep-dive, or try [Reading a Button Press](button-press.md) to learn about digital inputs!

!!! tip "Fun project idea"

    Try combining this with your [IMU tutorial](detect-motion.md) - make different sounds when you shake or rotate the device in different directions!

!!! warning "Having trouble?"

    Send us an email at [support@mr.industries](mailto:support@mr.industries) or join our [Discord](https://discord.gg/hvJZhwfQsF) for help!