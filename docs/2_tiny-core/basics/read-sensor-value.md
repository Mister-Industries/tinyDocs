# How to Read Sensor Values (Analog Input)

So far we've been dealing with digital signals - things that are either on or off, like buttons and LEDs. But the real world isn't just on and off. Temperature varies gradually, light gets brighter and dimmer, and sound has volume levels. That's where analog input comes in.

!!! warning "Are you skipping ahead?"

    Make sure you have already setup your Arduino IDE using the [previous tutorial](../get-started/arduino-ide.md)!

## Digital vs analog - what's the difference?

Think of it this way:
- **Digital** = Light switch (on or off, nothing in between)
- **Analog** = Dimmer switch (any brightness level from 0% to 100%)

When you pressed a button in the last tutorial, the tinyCore could only see HIGH or LOW. With analog input, it can see thousands of different levels between 0V and 3.3V.

The magic happens in the **ADC** (Analog-to-Digital Converter). This circuit inside the ESP32-S3 takes analog voltages and converts them to numbers your code can work with. The tinyCore's ADC has 12-bit resolution, which means it can distinguish between 4,096 different voltage levels (that's 2^12).

## How sensors work

Most sensors work by changing their electrical properties based on what they're measuring. For example:
- **Light sensor (LDR)** - Resistance changes with brightness
- **Temperature sensor** - Voltage changes with heat
- **Potentiometer** - Resistance changes when you turn the knob
- **Force sensor** - Resistance changes when you press it

The common thread? They all convert real-world measurements into changing voltages that we can read.

## What you'll need

- Your tinyCore ESP32-S3
- A 10kΩ potentiometer (the kind with three pins)
- A light-dependent resistor (LDR/photoresistor) 
- A 10kΩ regular resistor
- Some jumper wires
- A breadboard (makes connections easier)

## Step 1: Understanding voltage dividers

Before we jump into sensors, let's understand how most of them work. They use something called a **voltage divider** - a simple circuit that splits voltage between two resistors.

Here's the key insight: if one resistor changes (like in a sensor), the voltage in the middle changes too. That middle voltage is what we read with `analogRead()`.

## Step 2: Reading a potentiometer

Let's start with the simplest analog sensor - a potentiometer (variable resistor). Wire it up like this:

1. **Left pin of potentiometer** → **3.3V** on tinyCore
2. **Middle pin of potentiometer** → **GPIO 1** on tinyCore  
3. **Right pin of potentiometer** → **GND** on tinyCore

![Potentiometer Wiring](images/potentiometer-wiring.png)

Now try this code:

```cpp
// Basic Potentiometer Reading

const int potPin = 1;  // ADC pin for potentiometer

void setup() {
  Serial.begin(115200);
  Serial.println("Potentiometer reader ready");
  Serial.println("Turn the knob and watch the values change");
}

void loop() {
  // Read the raw ADC value (0-4095)
  int rawValue = analogRead(potPin);
  
  // Convert to voltage (0-3.3V)
  float voltage = (rawValue / 4095.0) * 3.3;
  
  // Convert to percentage (0-100%)
  int percentage = (rawValue * 100) / 4095;
  
  // Print all three ways of looking at the data
  Serial.print("Raw: ");
  Serial.print(rawValue);
  Serial.print(" | Voltage: ");
  Serial.print(voltage, 2);
  Serial.print("V | Percentage: ");
  Serial.print(percentage);
  Serial.println("%");
  
  delay(100);
}
```

Upload this and open the Serial Monitor. Turn the potentiometer knob and watch the numbers change. You should see values from 0 to 4095 for raw readings, 0V to 3.3V for voltage, and 0% to 100% for percentage.

## Step 3: Visualizing with Serial Plotter

Reading numbers is okay, but seeing the data as a graph is way cooler. Close the Serial Monitor and open **Tools → Serial Plotter** instead.

Try this modified code that's optimized for the plotter:

```cpp
// Potentiometer for Serial Plotter

const int potPin = 1;

void setup() {
  Serial.begin(115200);
  
  // Print headers for the plotter
  Serial.println("Raw_Value,Voltage_x100,Percentage");
}

void loop() {
  int rawValue = analogRead(potPin);
  float voltage = (rawValue / 4095.0) * 3.3;
  int percentage = (rawValue * 100) / 4095;
  
  // Print values separated by commas for plotter
  Serial.print(rawValue);
  Serial.print(",");
  Serial.print(voltage * 100);  // Multiply by 100 so it shows nicely
  Serial.print(",");
  Serial.println(percentage);
  
  delay(50);
}
```

Now when you turn the potentiometer, you'll see beautiful real-time graphs showing how the values change. Try turning it slowly, then quickly, then holding it steady.

## Step 4: Light sensor (photoresistor)

Let's try something more practical - a light sensor that responds to brightness. An LDR (Light Dependent Resistor) changes its resistance based on how much light hits it.

Since the LDR is just a variable resistor, we need to pair it with a fixed resistor to create a voltage divider. Wire it like this:

1. **One side of LDR** → **3.3V** on tinyCore
2. **Other side of LDR** → **GPIO 2** on tinyCore AND one side of 10kΩ resistor
3. **Other side of 10kΩ resistor** → **GND** on tinyCore

![LDR Wiring](images/ldr-wiring.png)

```cpp
// Light Sensor Reader

const int lightPin = 2;

void setup() {
  Serial.begin(115200);
  Serial.println("Light sensor ready");
  Serial.println("Try covering the sensor or shining light on it");
}

void loop() {
  int lightValue = analogRead(lightPin);
  
  // Convert to a light level percentage
  // Note: This might be inverted depending on your LDR
  int lightLevel = map(lightValue, 0, 4095, 0, 100);
  
  Serial.print("Light level: ");
  Serial.print(lightLevel);
  Serial.print("% (raw: ");
  Serial.print(lightValue);
  Serial.println(")");
  
  // Simple threshold detection
  if (lightLevel > 70) {
    Serial.println("  💡 It's bright in here!");
  } else if (lightLevel < 30) {
    Serial.println("  🌙 It's getting dark...");
  }
  
  delay(200);
}
```

Cover the sensor with your hand and watch the values change. Point a flashlight at it and see them jump up.

## Step 5: Multiple sensors at once

The ESP32-S3 has multiple ADC pins, so you can read several sensors simultaneously:

```cpp
// Multiple Analog Sensors

const int potPin = 1;    // Potentiometer on GPIO 1
const int lightPin = 2;  // Light sensor on GPIO 2

void setup() {
  Serial.begin(115200);
  Serial.println("Multi-sensor reader ready");
  
  // Headers for Serial Plotter
  Serial.println("Potentiometer,Light_Sensor");
}

void loop() {
  int potValue = analogRead(potPin);
  int lightValue = analogRead(lightPin);
  
  // Scale both to 0-100 range for easy comparison
  int potPercent = map(potValue, 0, 4095, 0, 100);
  int lightPercent = map(lightValue, 0, 4095, 0, 100);
  
  // Print for Serial Plotter
  Serial.print(potPercent);
  Serial.print(",");
  Serial.println(lightPercent);
  
  delay(50);
}
```

Open the Serial Plotter and you'll see two lines - one tracking your potentiometer, the other tracking the light level. Try changing both at the same time and watch how the graphs respond.

## Step 6: Smart LED control

Let's combine analog input with our previous LED knowledge to create something interactive:

```cpp
// Light-Controlled Auto LED

const int lightPin = 2;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.println("Automatic light controller ready");
  Serial.println("LED will turn on when it gets dark");
}

void loop() {
  int lightValue = analogRead(lightPin);
  
  // Convert to percentage (0-100)
  int lightLevel = map(lightValue, 0, 4095, 0, 100);
  
  // Auto-control LED based on light level
  if (lightLevel < 40) {
    digitalWrite(LED_BUILTIN, HIGH);  // Turn on LED when dark
    Serial.print("🌙 Dark detected (");
    Serial.print(lightLevel);
    Serial.println("%) - LED ON");
  } else {
    digitalWrite(LED_BUILTIN, LOW);   // Turn off LED when bright
    Serial.print("☀️ Light detected (");
    Serial.print(lightLevel);
    Serial.println("%) - LED OFF");
  }
  
  delay(500);
}
```

Now you've built an automatic night light. Cover the sensor to make it "dark" and watch the LED turn on.

## Understanding the numbers

**Raw ADC values (0-4095):**
- 0 = 0V input
- 2047 = ~1.65V input (halfway)
- 4095 = 3.3V input

**Converting to voltage:**
```cpp
float voltage = (rawValue / 4095.0) * 3.3;
```

**Converting to percentage:**
```cpp
int percentage = map(rawValue, 0, 4095, 0, 100);
```

The `map()` function is super useful - it takes a value from one range and converts it to another range proportionally.

## ESP32-S3 ADC specifics

The ESP32-S3 has some important features to know about:

**ADC1 vs ADC2:**
- Use **ADC1 pins** (GPIO 1-10) for most projects
- ADC2 pins can't be used when WiFi is enabled
- Stick to ADC1 and you'll avoid headaches

**Voltage range:**
- Maximum input: **3.3V** (never exceed this!)
- Resolution: **12-bit** (0-4095 values)
- The ESP32-S3 has better accuracy than older ESP32 models

**Recommended pins for tinyCore:**
- GPIO 1, 2, 3, 4, 5 are safe choices for analog input
- Avoid GPIO pins used for other functions (like I2C, SPI, etc.)

## Common issues

**Readings seem random or noisy**
- Analog signals can be noisy - this is normal
- Try averaging multiple readings for stability
- Make sure your wiring connections are solid

**Values don't reach full range (0-4095)**
- Check your voltage divider circuit
- Make sure you're getting 0V to 3.3V range at the input pin
- Some sensors may not use the full voltage range

**Sensor readings are backwards**
- Some sensors (like LDRs) might give higher resistance when you expect lower
- Just flip your logic or use `map(value, 0, 4095, 100, 0)` to invert

**WiFi interferes with readings**
- Use ADC1 pins (GPIO 1-10) instead of ADC2 pins
- If you must use ADC2, disable WiFi first

## What's next?

Now you can read the analog world around you. This opens up massive possibilities:

**Sensor projects:**
- **Weather station** - Temperature, humidity, pressure sensors
- **Security system** - Motion detectors, door sensors
- **Plant monitor** - Soil moisture, light levels
- **Sound visualizer** - Microphone input for audio reactive projects
- **Remote control** - Joysticks, sliders for controlling other devices

**Control projects:**
- **Servo positioning** - Use potentiometer to control servo angle
- **LED brightness** - Analog input controls LED fade level
- **Motor speed** - Variable speed control based on sensor input
- **Audio effects** - Process sound with filters and effects

The combination of analog input with your existing knowledge of digital I/O, PWM output, and wireless communication means you can build sophisticated interactive devices that respond to their environment.

!!! tip "Pro tip: Sensor fusion"

    Try combining multiple sensors for smarter behavior. For example: only turn on automatic lights if it's both dark (light sensor) AND someone is present (motion from IMU). The magic happens when sensors work together.

!!! warning "Having trouble?"

    Send us an email at [support@mr.industries](mailto:support@mr.industries) or join our [Discord](https://discord.gg/hvJZhwfQsF) for help!