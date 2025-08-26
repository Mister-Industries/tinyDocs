# How to Control LEDs with the tinyCore

Ready to light things up? Let's start with the classic "Hello World"(1) of electronics: Blink!
{ .annotate }

1.  In programming, "Hello World" refers to the simplest possible program that demonstrates basic functionality. New students 
    will learn how to print the words "Hello World" in their specific programming language.


We'll start by learning how to flash the built-in LEDs, dim the lights with PWM(1), and then move up to controlling external ones!
{ .annotate }

1.  PWM (Pulse Width Modulation) is a technique that rapidly turns power on and off to simulate different voltage levels. By changing how long the signal stays "on" versus "off," we can make LEDs appear dimmer or brighter, even though they're actually just blinking too fast for your eyes to see (thousands of times per second).

!!! warning "Are you skipping ahead?"

    Make sure you have already setup your Arduino IDE using the [getting started guide](../get-started/arduino-ide.md)!

---

## Part 1: Blink the Onboard LEDs

#### Your tinyCore already has two ***built-in*** LEDs:

- **LED_BOOT** (connected to GPIO21) - Usually indicates boot or error status

- **LED_SIG** (connected to GPIO33) - General purpose signal LED

![tinyCore Pinouts](../core/blink-led/ledsblink.gif)

Let's start by them. No wiring required!

---

### Basic Blink Program

Copy this code into your Arduino IDE:

```cpp linenums="1"
//Basic Blink Example

const int ledBoot = 21;    // LED_BOOT pin
const int ledSig = 33;     // LED_SIG pin

void setup() {
  // Initialize both built-in LEDs as outputs
  pinMode(ledBoot, OUTPUT);
  pinMode(ledSig, OUTPUT);
  
  // Start with both LEDs off
  digitalWrite(ledBoot, LOW);
  digitalWrite(ledSig, LOW);
}

void loop() {
  // Turn LEDs on
  digitalWrite(ledBoot, HIGH);   // Turn on
  digitalWrite(ledSig, HIGH);    // Turn off
  delay(500);
  
  // Turn LEDs off
  digitalWrite(ledBoot, LOW);    // Turn on
  digitalWrite(ledSig, LOW);     // Turn off
  delay(500);
}
```
!!! ai-sparkle "This code was one-shot by [Claude Sonnet 4](claude.ai)"

Both LEDs on your tinyCore should now be flashing On and Off like the GIF above.

---

### Alternating Blink Pattern

Let's try something more interesting. Replace your `loop()` function with this alternating pattern:

```cpp linenums="16"
void loop() {
  // Turn on BOOT, turn off SIG
  digitalWrite(ledBoot, HIGH);
  digitalWrite(ledSig, LOW);
  delay(300);
  
  // Turn off BOOT, turn on SIG
  digitalWrite(ledBoot, LOW);
  digitalWrite(ledSig, HIGH);
  delay(300);
}
```
!!! ai-sparkle "This code was one-shot by [Claude Sonnet 4](claude.ai)"

Now the LEDs should be taking turns blinking! 

!!! example "Challenge: Morse Code"

    **Can you blink "SOS" in Morse code?** 
    
    *Hint:* Try changing the values of the `delay()` functions to create different speeds. Dots can be represented by short flashes (250ms) and Dashes can be represented by long flashes (500ms)

---

## Part 2: PWM Control (Dimming and Brightening)

The ESP32-S3 supports Pulse Width Modulation (PWM)(1) for smooth brightness control. This will let us fade the LEDs in and out!
{ .annotate }

1.  Pulse Width Modulation is a technique that rapidly turns power on and off to simulate different voltage levels. By changing how long the signal stays "on" versus "off," we can make LEDs appear dimmer or brighter, even though they're actually just blinking too fast for your eyes to see (thousands of times per second).

### Smooth Breathing Effect

```cpp linenums="1"
// PWM LED Control Example

const int ledBoot = 21;
const int ledSig = 33;

// PWM settings
const int pwmFreq = 5000;      // 5 KHz frequency
const int pwmResolution = 8;   // 8-bit resolution (0-255)

void setup() {
  // Configure PWM - channel selected automatically
  ledcAttach(ledBoot, pwmFreq, pwmResolution);
  ledcAttach(ledSig, pwmFreq, pwmResolution);
}

void loop() {
  // Breathing effect - fade in
  for(int brightness = 0; brightness <= 255; brightness++) {
    ledcWrite(ledBoot, brightness);
    ledcWrite(ledSig, 255 - brightness);  // Opposite brightness
    delay(10);
  }
  
  // Breathing effect - fade out
  for(int brightness = 255; brightness >= 0; brightness--) {
    ledcWrite(ledBoot, brightness);
    ledcWrite(ledSig, 255 - brightness);  // Opposite brightness
    delay(10);
  }
}
```
!!! ai-sparkle "This code was one-shot by [Claude Sonnet 4](claude.ai)"

You should see your LEDs fading off and on smoothly, almost like two fireflies! (or do you call them lightning bugs??)

---

### Manual Brightness Control

Another option is to manually set the LEDs to specific brightness levels:

```cpp linenums="16"
void loop() {
  // Very dim (10% brightness)
  ledcWrite(ledBoot, 25);
  ledcWrite(ledSig, 25);
  delay(1000);
  
  // Medium brightness (50%)
  ledcWrite(ledBoot, 128);
  ledcWrite(ledSig, 128);
  delay(1000);
  
  // Full brightness (100%)
  ledcWrite(ledBoot, 255);
  ledcWrite(ledSig, 255);
  delay(1000);
  
  // Turn off
  ledcWrite(ledBoot, 0);
  ledcWrite(ledSig, 0);
  delay(1000);
}
```

!!! ai-sparkle "This code was one-shot by [Claude Sonnet 4](claude.ai)"

---

## Part 3: External LED with Breadboard

Now let's add an external LED! The tinyCore has plenty of GPIO pins available for this.

### You'll need

- Your tinyCore
- A breadboard
- A "Gumdrop" LED (any color)
- A 220Ω resistor
- Jumper wires (male-to-male)

??? question "Why do we need a resistor? *Click for the Answer!*"

    Ohm's Law states that the current through a device is inversely proportional to the resistance of that device. Put simply,a very ~small~ resistance equals a very *LARGE* current. LEDs have very little resistance, meaning we have to add a "current-limiting" resistor to protect them from getting fried!

    We calculate the size of this resistor with a simple formula:
    
    $$
    R = \frac{V_s - V_f}{I_f}
    $$
    Where:
    
    - $R$ = Resistor value in Ohms
    
    - $V_s$ = Supply voltage *(3.3V on the tinyCore)**
    
    - $V_f$ = LED forward voltage drop *(typically 1.8-2.0V for red LEDs)*
    
    - $I_f$ = Desired LED current *(typically 10-20mA)*

    **Example calculation for a red LED:**
    $$
    R = \frac{3.3V - 1.8V}{0.02A} = \frac{1.5V}{0.02A} = 75Ω
    $$
    Lucky for us, 75 is a [standard resistor value](https://www.open.edu/openlearn/mod/oucontent/view.php?id=68374&extra=thumbnailfigure_idm547), but if it wasn't, we'd round up to the next higher standard value, which is 100Ω. For extra margin of safety, 220Ω is commonly used and still provides good brightness while ensuring the LED won't be damaged.

**Available GPIO Pins:**

![Available GPIO](../core/blink-led/GPIO.jpg)

You can use any of the GPIO(1) pins for your external LED (pictured in Yellow):
{ .annotate }

1.  "GPIO" stands for General Purpose Input-Output. While labeled as "Digital" and "Analog", all GPIO pins on the tinyCore can actually do both! (with some caveats). The labels simply indicate their primary intended use.

- **Digital pins**: 8, 9, 10, 11, 12, 13

- **Analog pins**: A0, A1, A2, A3, A4, A5

### Wiring the External LED

Let's use GPIO13:

1. **LED short leg (cathode)** → **Pin 13**
2. **LED long leg (anode)** → **220Ω resistor** → **GND Pin**


![External LED Wiring](../core/blink-led/LEDCircuit.jpg)
And here's the circuit on a breadboard:
![External LED Wiring](../core/blink-led/LEDCircuitBreadboard.jpg)

### Code for External LED

Now it's time to program the tinyCore to blink this LED! Here's the code:

```cpp linenums="1"
// External LED Control on tinyCore ESP32-S3

const int externalLed = 13;    // External LED on IO13

void setup() {
  pinMode(externalLed, OUTPUT);
}

void loop() {
  // Light chase effect
  digitalWrite(externalLed, LOW);
  delay(300);
  
  digitalWrite(externalLed, HIGH);
  delay(300);
}
```

!!! ai-sparkle "This code was one-shot by [Claude Sonnet 4](claude.ai)"

---

### PWM Control for All Three LEDs

Let's bring this whole thing home and control ***all three*** LEDs via PWM.

```cpp linenums="1"
// PWM control for built-in and external LEDs

const int ledBoot = 21;
const int ledSig = 33;
const int externalLed = 13;

void setup() {
  // Configure PWM for all LEDs
  ledcAttach(ledBoot, 5000, 8);
  ledcAttach(ledSig, 5000, 8);
  ledcAttach(externalLed, 5000, 8);
}

void loop() {
  // "Wave" effect
  for(int i = 0; i < 256; i++) {
    ledcWrite(ledBoot, (sin(i * 0.02) * 127 + 128));
    ledcWrite(ledSig, (sin(i * 0.02 + 2) * 127 + 128));
    ledcWrite(externalLed, (sin(i * 0.02 + 4) * 127 + 128));
    delay(20);
  }
}
```
!!! ai-sparkle "This code was one-shot by [Claude Sonnet 4](claude.ai)"

---

## Understanding the Code

### Digital Control
- `pinMode(pin, OUTPUT)` - Sets a pin to output mode
- `digitalWrite(pin, HIGH)` - Sends 3.3V to the pin (LED on)
- `digitalWrite(pin, LOW)` - Sends 0V to the pin (LED off)

### PWM Control
- `ledcAttach(channel, frequency, resolution)` - Configures PWM settings
- `ledcWrite(channel, value)` - Sets brightness (0-255 for 8-bit resolution)

### Timer
- `delay(milliseconds)` - Makes the program wait

## Challenge Code

***Spoilers Ahead!***

### SOS Signal

```cpp linenums="1"
//Morse Code "SOS"

const int ledBoot = 21;
const int ledSig = 33;

void setup() {
  // Initialize both built-in LEDs as outputs
  pinMode(ledBoot, OUTPUT);
  pinMode(ledSig, OUTPUT);

  // Start with both LEDs off
  digitalWrite(ledBoot, LOW);
  digitalWrite(ledSig, LOW);
}

void loop() {
  // S (short-short-short)
  for(int i = 0; i < 3; i++) {
    digitalWrite(ledBoot, HIGH);
    delay(200);
    digitalWrite(ledBoot, LOW);
    delay(200);
  }
  delay(300);
  
  // O (long-long-long)
  for(int i = 0; i < 3; i++) {
    digitalWrite(ledBoot, HIGH);
    delay(600);
    digitalWrite(ledBoot, LOW);
    delay(200);
  }
  delay(300);
  
  // S (short-short-short)
  for(int i = 0; i < 3; i++) {
    digitalWrite(ledBoot, HIGH);
    delay(200);
    digitalWrite(ledBoot, LOW);
    delay(200);
  }
  delay(2000);
}
```

## Troubleshooting

**External LED not lighting?**

- Check polarity - long leg (+) goes to Pin 13, short leg (-, flat side) to resistor, resistor to Ground

- Verify your resistor value (220Ω, should be Red, Red, Brown, Gold/Silver)

- Make sure connections are secure on the breadboard

- Could be burnt out, try another LED!

**LED is very dim?**

Check your resistor value - too high resistance dims the LED (For a brighter light, try 150Ω resistor instead)

**Error: 'ledcSetup' was not declared in this scope**

This usually happens with code generated by AI. LLM's tend to hallucinate outdated syntax for the ESP32 board library. ledcSetup was removed in v3.0.7 of Expressif's libraries and combined into ledcAttach. Make sure you use the latest syntax!

---

## What's Next?

Now that you can control LEDs, you can control almost anything: Motors, buzzers, relays - they all use similar `digitalWrite()` commands.

Ready to try:

- [Reading a Button Press?](../core/button-press.md)

- [Using the Serial Monitor?](../core/serial-monitor-plotter.md)

- [Measuring Motion with the IMU?](../core/imu.md)

!!! warning "Need Help?"

    Join our [Discord](https://discord.gg/hvJZhwfQsF) or email [support@mr.industries](mailto:support@mr.industries) for assistance!