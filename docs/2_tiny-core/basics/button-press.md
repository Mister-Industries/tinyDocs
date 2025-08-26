# How to Read a Button Press (Digital Input)

Time to flip the script. We've been making the tinyCore control things like LEDs and buzzers, but what if we want to control the tinyCore instead? Buttons are the most basic way to give your device some input, and understanding how they work opens the door to interactive projects.

!!! warning "Are you skipping ahead?"

    Make sure you have already setup your Arduino IDE using the [previous tutorial](../get-started/arduino-ide.md)!

## Digital input vs output

Remember when we made an LED blink? That was **digital output** - the tinyCore was sending signals out to control something else. Now we're doing the opposite: **digital input** means the tinyCore is listening for signals coming in from the outside world.

A button is basically just a switch that connects two wires when you press it. When pressed, it completes a circuit. When released, it breaks the circuit. Your job is to detect whether the circuit is complete or broken.

## The floating pin problem

Here's where things get a bit weird. If you just connect a button between a GPIO pin and ground, something strange happens when the button isn't pressed - the pin doesn't read HIGH or LOW, it just... floats around randomly. This is called a "floating input" and it'll drive you crazy with random false readings.

The solution is something called a **pull-up resistor**. Think of it like this: when the button isn't pressed, the resistor "pulls" the pin up to HIGH (3.3V). When you press the button, it connects the pin directly to ground, overriding the resistor and making the pin read LOW.

The good news? The ESP32 has built-in pull-up resistors, so you don't need any extra components.

## What you'll need

- Your tinyCore ESP32-S3

- A momentary push button (the kind that springs back when you let go)

- A couple of jumper wires

The beauty of this tutorial is that we'll use the tinyCore's built-in LED, so you don't need any external LEDs or resistors.

## Step 1: Simple button wiring

This couldn't be simpler:

1. **One side of button** → **GPIO pin 4** on tinyCore
2. **Other side of button** → **GND** on tinyCore

That's it. No resistors, no complicated circuits. The ESP32's internal pull-up does all the heavy lifting.

![Button Wiring](images/button-wiring.png)

## Step 2: Basic button reading

Let's start with code that just tells you when the button is pressed:

```cpp
// Simple Button Reading

const int buttonPin = 4;

void setup() {
  Serial.begin(115200);
  
  // Configure the pin as input with internal pull-up
  pinMode(buttonPin, INPUT_PULLUP);
  
  Serial.println("Button reader ready");
  Serial.println("Press the button and watch what happens");
}

void loop() {
  // Read the button state
  int buttonState = digitalRead(buttonPin);
  
  // Print the state (remember: pull-up logic is inverted)
  if (buttonState == LOW) {
    Serial.println("Button is PRESSED");
  } else {
    Serial.println("Button is NOT pressed");
  }
  
  delay(100);  // Don't spam the serial monitor
}
```

Upload this and open the Serial Monitor. You'll see it constantly telling you whether the button is pressed or not.

Notice something important: when you press the button, it reads LOW, not HIGH. That's because of the pull-up resistor - it inverts the logic.

## Step 3: Detecting button events

Constantly checking if a button is pressed gets annoying fast. What we really want is to detect the moment when the button changes state - when it goes from not-pressed to pressed, or vice versa.

```cpp
// Button Press Detection

const int buttonPin = 4;

int lastButtonState = HIGH;    // Previous button state
int currentButtonState;        // Current button state

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
  
  Serial.println("Button event detector ready");
  Serial.println("Try pressing and releasing the button");
}

void loop() {
  // Read the current state
  currentButtonState = digitalRead(buttonPin);
  
  // Check if the state has changed
  if (currentButtonState != lastButtonState) {
    
    // Determine what kind of change it was
    if (currentButtonState == LOW) {
      Serial.println("🔽 Button PRESSED");
    } else {
      Serial.println("🔼 Button RELEASED");
    }
    
    // Update the last state
    lastButtonState = currentButtonState;
  }
  
  delay(10);  // Small delay for stability
}
```

This is much cleaner. Now you only get a message when something actually happens, not a constant stream of status updates.

## Step 4: Understanding NOT logic

Here's where we can explore some basic digital logic. Let's make the built-in LED turn on when the button is NOT pressed, and turn off when it IS pressed. This demonstrates a NOT gate in action:

```cpp
// NOT Gate Logic with Built-in LED

const int buttonPin = 4;

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);  // Use the built-in LED
  
  Serial.println("NOT gate demo ready");
  Serial.println("LED will be ON when button is NOT pressed");
}

void loop() {
  int buttonState = digitalRead(buttonPin);
  
  // This is the NOT gate logic:
  // If button is NOT pressed (HIGH), LED is ON
  // If button IS pressed (LOW), LED is OFF
  digitalWrite(LED_BUILTIN, buttonState);
  
  delay(50);  // Small delay for stability
}
```

Upload this and watch what happens. The LED should be glowing when you're not touching the button, and turn off the moment you press it. You've just built a NOT gate using a button and LED.

## Step 5: Toggle behavior vs direct control

Let's contrast that with toggle behavior, where each button press switches the LED state:

```cpp
// LED Toggle with Built-in LED

const int buttonPin = 4;

int lastButtonState = HIGH;
int ledState = LOW;        // Keep track of LED state

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  
  // Start with LED off
  digitalWrite(LED_BUILTIN, ledState);
  
  Serial.println("LED toggle ready");
  Serial.println("Press button to toggle LED on/off");
}

void loop() {
  int currentButtonState = digitalRead(buttonPin);
  
  // If button state changed AND button is now pressed
  if (currentButtonState != lastButtonState && currentButtonState == LOW) {
    
    // Toggle the LED state
    ledState = !ledState;
    digitalWrite(LED_BUILTIN, ledState);
    
    // Give some feedback
    Serial.print("LED is now ");
    Serial.println(ledState ? "ON" : "OFF");
  }
  
  lastButtonState = currentButtonState;
  delay(10);
}
```

Now each button press switches the LED between on and off. This is like a light switch in your house - press once for on, press again for off.

## Step 6: Multiple buttons, multiple behaviors

Why stop at one button? Let's use two buttons to control the built-in LED in different ways:

```cpp
// Multiple Button Control

const int button1Pin = 4;
const int button2Pin = 5;

int lastButton1State = HIGH;
int lastButton2State = HIGH;
int ledState = LOW;

void setup() {
  Serial.begin(115200);
  
  // Setup buttons
  pinMode(button1Pin, INPUT_PULLUP);
  pinMode(button2Pin, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.println("Multi-button control ready");
  Serial.println("Button 1 (GPIO 4): Toggle LED on/off");
  Serial.println("Button 2 (GPIO 5): Flash LED while pressed");
}

void loop() {
  // Check button 1 (toggle behavior)
  int currentButton1State = digitalRead(button1Pin);
  if (currentButton1State != lastButton1State && currentButton1State == LOW) {
    ledState = !ledState;
    digitalWrite(LED_BUILTIN, ledState);
    Serial.println(ledState ? "💡 LED toggled ON" : "💡 LED toggled OFF");
  }
  lastButton1State = currentButton1State;
  
  // Check button 2 (flash while pressed)
  int currentButton2State = digitalRead(button2Pin);
  if (currentButton2State == LOW) {
    // Flash the LED rapidly while button 2 is held
    digitalWrite(LED_BUILTIN, HIGH);
    delay(50);
    digitalWrite(LED_BUILTIN, LOW);
    delay(50);
  }
  
  // If button 2 is not pressed, restore the toggle state from button 1
  if (currentButton2State == HIGH) {
    digitalWrite(LED_BUILTIN, ledState);
  }
  
  lastButton2State = currentButton2State;
  delay(10);
}
```

This gives you two different interaction modes: button 1 toggles the LED state permanently, while button 2 makes it flash rapidly but only while you hold it down.

## Understanding pull-up logic

The trickiest part about buttons with pull-up resistors is remembering that the logic is inverted:

- Button **not pressed** = pin reads **HIGH**

- Button **pressed** = pin reads **LOW**

This feels backwards at first, but you'll get used to it. The benefit is that you don't need any external resistors.

## Why use `INPUT_PULLUP`?

You might wonder why we don't just use `INPUT` mode. Here's what happens:


- `INPUT`: Pin floats randomly when button isn't pressed (unreliable)

- `INPUT_PULLUP`: Pin is held at HIGH when button isn't pressed (reliable)

- `INPUT_PULLDOWN`: Pin is held at LOW when button isn't pressed (less common)

The ESP32 supports all three, but `INPUT_PULLUP` is the most commonly used for buttons.

## Common issues

**Button readings seem random or inconsistent**
- Make sure you're using `INPUT_PULLUP` mode
- Check your wiring - one side to GPIO, other side to GND
- Try a different button (they do break sometimes)

**Multiple triggers from single button press**
- This is called "bouncing" - mechanical buttons aren't perfect
- The delay(10) in our code helps with this
- For more precise applications, look into "debouncing" techniques

**Button doesn't seem to work**
- Try testing with a simple multimeter or even just a wire
- Some buttons have multiple pins that aren't all connected
- Make sure you're connecting to the right GPIO pin in both hardware and software

## What's next?

Now you understand both digital output (controlling LEDs) and digital input (reading buttons). This is huge - you can now create interactive devices that respond to user input.

Some project ideas:

- **Password entry system** - Different button combinations unlock things

- **Game controller** - Use buttons to control games or robots  

- **Menu system** - Navigate through options with button presses

- **Security system** - Arm/disarm with button combinations

- **Musical instrument** - Different buttons play different notes on a buzzer

- **Smart lighting** - Complex lighting patterns controlled by button sequences

The combination of inputs and outputs is where electronics gets really interesting. You're no longer just making things blink - you're creating devices that can think and respond.

!!! tip "Debouncing deep dive"

    If you're building something that needs to count every single button press perfectly (like a voting machine), you'll want to learn about debouncing. It's a technique to handle the fact that mechanical buttons "bounce" when pressed, causing multiple readings from a single press.

!!! warning "Having trouble?"

    Send us an email at [support@mr.industries](mailto:support@mr.industries) or join our [Discord](https://discord.gg/hvJZhwfQsF) for help!