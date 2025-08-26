# How to use the Serial Monitor and Serial Plotter

If you've been following along with the tutorials, you've probably noticed `Serial.println()` scattered throughout the code. These aren't just random lines - they're your window into what's happening inside your tinyCore. The Serial Monitor and Serial Plotter are two of the most valuable debugging and visualization tools you'll use as a maker.

!!! warning "Are you skipping ahead?"

    Make sure you have already setup your Arduino IDE using the [previous tutorial](../get-started/arduino-ide.md)!

## Why serial communication matters

Your tinyCore is constantly thinking, measuring, and making decisions, but most of the time you can't see what's going on inside. Serial communication is like giving your device a voice - it can tell you what it's seeing, what it's thinking, and what's going wrong.

Think of it like this: imagine trying to debug a program on your computer if the screen was permanently turned off. That's what programming microcontrollers would be like without serial communication.

## Understanding baud rate

Before we dive in, let's talk about **baud rate** - the speed at which data travels between your tinyCore and computer. It's measured in bits per second (bps).

Common baud rates you'll encounter:
- **9600 bps** - Slow but reliable, good for simple data
- **57600 bps** - Medium speed, good balance  
- **115200 bps** - Fast, great for lots of data or debugging

Here's the crucial part: **both your code and the Serial Monitor must use the same baud rate**. If your code says `Serial.begin(115200)` but the Serial Monitor is set to 9600, you'll see garbled text that looks like alien hieroglyphics.

Think of baud rate like language speed - if one person is speaking slowly and the other is listening for rapid speech, nothing makes sense.

## Serial Monitor basics

The Serial Monitor is your primary debugging tool. Let's explore what it can do.

### Basic output example

```cpp
// Basic Serial Monitor Output

void setup() {
  // Initialize serial communication at 115200 bps
  Serial.begin(115200);
  
  // Wait a moment for the serial connection to stabilize
  delay(1000);
  
  Serial.println("=== tinyCore System Starting ===");
  Serial.println("Firmware version: 1.0");
  Serial.print("Compiled on: ");
  Serial.print(__DATE__);
  Serial.print(" at ");
  Serial.println(__TIME__);
  Serial.println("System ready for commands");
}

void loop() {
  static int counter = 0;
  
  // Print different types of data
  Serial.print("Loop iteration: ");
  Serial.println(counter);
  
  // Print sensor-like data with labels
  float fakeTemperature = 20.5 + (counter % 10);
  Serial.print("Temperature: ");
  Serial.print(fakeTemperature, 1);  // 1 decimal place
  Serial.println("°C");
  
  // Print system status
  Serial.print("Free memory: ");
  Serial.print(ESP.getFreeHeap());
  Serial.println(" bytes");
  
  Serial.println("---");
  
  counter++;
  delay(2000);  // Update every 2 seconds
}
```

Upload this code, then open **Tools → Serial Monitor**. Make sure the baud rate dropdown (bottom right) is set to **115200** to match your code.

You'll see a running log of what your tinyCore is doing. This is invaluable for understanding program flow and diagnosing issues.

### Reading input from Serial Monitor

The Serial Monitor isn't just for output - you can send commands to your tinyCore too.

```cpp
// Interactive Serial Commands

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.println("=== Interactive tinyCore Controller ===");
  Serial.println("Available commands:");
  Serial.println("  'on'    - Turn LED on");
  Serial.println("  'off'   - Turn LED off");
  Serial.println("  'blink' - Blink LED once");
  Serial.println("  'status'- Show current status");
  Serial.println("  'help'  - Show this menu");
  Serial.println("Type a command and press Enter:");
}

void loop() {
  // Check if data is available to read
  if (Serial.available()) {
    // Read the entire line until newline character
    String command = Serial.readStringUntil('\n');
    command.trim();  // Remove any extra whitespace
    
    // Convert to lowercase for easier comparison
    command.toLowerCase();
    
    Serial.print("Received command: '");
    Serial.print(command);
    Serial.println("'");
    
    // Process the command
    if (command == "on") {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("✓ LED turned ON");
      
    } else if (command == "off") {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("✓ LED turned OFF");
      
    } else if (command == "blink") {
      Serial.println("✓ Blinking LED...");
      digitalWrite(LED_BUILTIN, HIGH);
      delay(300);
      digitalWrite(LED_BUILTIN, LOW);
      delay(300);
      Serial.println("✓ Blink complete");
      
    } else if (command == "status") {
      Serial.println("=== System Status ===");
      Serial.print("LED state: ");
      Serial.println(digitalRead(LED_BUILTIN) ? "ON" : "OFF");
      Serial.print("Uptime: ");
      Serial.print(millis() / 1000);
      Serial.println(" seconds");
      Serial.print("Free memory: ");
      Serial.print(ESP.getFreeHeap());
      Serial.println(" bytes");
      
    } else if (command == "help") {
      Serial.println("Available commands: on, off, blink, status, help");
      
    } else {
      Serial.print("❌ Unknown command: '");
      Serial.print(command);
      Serial.println("'");
      Serial.println("Type 'help' for available commands");
    }
    
    Serial.println("Enter next command:");
  }
}
```

Try this code and experiment with typing different commands in the text box at the top of the Serial Monitor. Make sure the dropdown next to the text box is set to **"Newline"** so the tinyCore knows when you've finished typing a command.

## Serial Plotter for data visualization

While the Serial Monitor is great for text, the Serial Plotter excels at visualizing changing data over time. It's perfect for sensors, signals, and any data that varies.

### Single variable plotting

```cpp
// Basic Serial Plotter Demo

void setup() {
  Serial.begin(115200);
  Serial.println("Starting signal generation...");
  delay(1000);  // Give plotter time to start
}

void loop() {
  // Generate a simple sine wave
  static float angle = 0;
  
  float sineValue = 50 + 30 * sin(angle);  // Sine wave from 20 to 80
  
  // For Serial Plotter, just print the value
  Serial.println(sineValue);
  
  angle += 0.1;
  delay(50);  // Update rate affects how fast the wave moves
}
```

Upload this, then close the Serial Monitor and open **Tools → Serial Plotter**. You'll see a beautiful sine wave scrolling across the screen in real-time.

### Multiple variable plotting

The real power comes from plotting multiple signals simultaneously:

```cpp
// Multiple Signals for Serial Plotter

void setup() {
  Serial.begin(115200);
  delay(1000);
}

void loop() {
  static float time = 0;
  
  // Generate different waveforms
  float signal1 = 50 + 20 * sin(time);           // Sine wave
  float signal2 = 50 + 15 * sin(time * 2);       // Faster sine wave  
  float signal3 = 30 + 10 * sin(time * 0.5);     // Slower sine wave
  float signal4 = 20 + time * 2;                 // Rising ramp
  
  // For multiple plots, separate with tabs or spaces
  Serial.print(signal1);
  Serial.print("\t");    // Tab character
  Serial.print(signal2);
  Serial.print("\t");
  Serial.print(signal3);
  Serial.print("\t");
  Serial.println(signal4);  // Last value uses println
  
  time += 0.05;
  
  // Reset the ramp periodically
  if (time > 10) {
    time = 0;
  }
  
  delay(30);
}
```

This creates four different colored lines on the plotter. The plotter automatically scales the Y-axis to fit all the data and assigns different colors to each signal.

**Key formatting rules for Serial Plotter:**
- Separate multiple values with **tab (`\t`)** or **space (` `)** characters
- End the line with **`Serial.println()`** for the last value
- All values on one line get plotted at the same time point
- Don't include text labels in the data (save those for Serial Monitor)

### Real sensor data visualization

Let's combine the plotter with actual sensor readings:

```cpp
// Real Sensor Data Plotting

void setup() {
  Serial.begin(115200);
  
  // Print column headers (Serial Plotter will ignore text after numbers start)
  Serial.println("Light_Sensor,Temperature_Simulation,Button_State");
  delay(1000);
}

void loop() {
  // Read actual sensor (if you have one connected)
  int lightValue = analogRead(1);  // GPIO 1
  int lightPercent = map(lightValue, 0, 4095, 0, 100);
  
  // Simulate temperature data
  static float temperature = 25.0;
  temperature += random(-10, 11) * 0.1;  // Random walk
  temperature = constrain(temperature, 15.0, 35.0);  // Keep realistic
  
  // Read button state (if connected)
  // For demo, we'll simulate button presses
  static int buttonCounter = 0;
  int buttonState = (buttonCounter % 100 < 10) ? 100 : 0;  // "Press" for 10% of time
  buttonCounter++;
  
  // Output for plotter
  Serial.print(lightPercent);
  Serial.print("\t");
  Serial.print(temperature);
  Serial.print("\t");
  Serial.println(buttonState);
  
  delay(100);
}
```

This example shows how to plot real sensor data alongside simulated signals. You can see patterns, detect anomalies, and understand how your sensors behave over time.

## Advanced Serial Monitor techniques

### Debugging with timestamps

```cpp
// Advanced Debugging with Timestamps

unsigned long startTime;

void setup() {
  Serial.begin(115200);
  startTime = millis();
  
  Serial.println("=== Advanced Debug Log ===");
  debugPrint("System initialization started");
}

void debugPrint(String message) {
  unsigned long currentTime = millis() - startTime;
  
  // Format: [HH:MM:SS.mmm] MESSAGE
  unsigned long seconds = currentTime / 1000;
  unsigned long minutes = seconds / 60;
  unsigned long hours = minutes / 60;
  
  Serial.print("[");
  if (hours < 10) Serial.print("0");
  Serial.print(hours % 24);
  Serial.print(":");
  if ((minutes % 60) < 10) Serial.print("0");
  Serial.print(minutes % 60);
  Serial.print(":");
  if ((seconds % 60) < 10) Serial.print("0");
  Serial.print(seconds % 60);
  Serial.print(".");
  
  unsigned long milliseconds = currentTime % 1000;
  if (milliseconds < 100) Serial.print("0");
  if (milliseconds < 10) Serial.print("0");
  Serial.print(milliseconds);
  
  Serial.print("] ");
  Serial.println(message);
}

void loop() {
  static int loopCount = 0;
  
  if (loopCount % 500 == 0) {  // Every 500 loops
    debugPrint("Periodic status check - system running normally");
  }
  
  if (loopCount == 1000) {
    debugPrint("Simulated sensor reading: 42.7°C");
  }
  
  if (loopCount == 2000) {
    debugPrint("Warning: Temperature threshold exceeded");
  }
  
  loopCount++;
  delay(10);
}
```

This creates professional-looking debug logs with timestamps, making it easier to understand the timing of events in your code.

### Memory and performance monitoring

```cpp
// System Performance Monitor

void setup() {
  Serial.begin(115200);
  Serial.println("=== System Performance Monitor ===");
  
  // Print system info
  Serial.print("Chip model: ");
  Serial.println(ESP.getChipModel());
  Serial.print("CPU frequency: ");
  Serial.print(ESP.getCpuFreqMHz());
  Serial.println(" MHz");
  Serial.print("Flash size: ");
  Serial.print(ESP.getFlashChipSize() / 1024 / 1024);
  Serial.println(" MB");
  Serial.println("---");
}

void loop() {
  static unsigned long lastCheck = 0;
  static int iterationCount = 0;
  
  unsigned long currentTime = millis();
  
  // Performance check every 5 seconds
  if (currentTime - lastCheck >= 5000) {
    Serial.println("=== Performance Report ===");
    
    // Memory usage
    Serial.print("Free heap: ");
    Serial.print(ESP.getFreeHeap());
    Serial.println(" bytes");
    
    // Loop performance
    Serial.print("Loop iterations in 5s: ");
    Serial.println(iterationCount);
    Serial.print("Average loop time: ");
    Serial.print(5000.0 / iterationCount, 2);
    Serial.println(" ms");
    
    // System uptime
    Serial.print("Uptime: ");
    Serial.print(currentTime / 1000);
    Serial.println(" seconds");
    
    Serial.println("---");
    
    lastCheck = currentTime;
    iterationCount = 0;
  }
  
  iterationCount++;
  
  // Simulate some work
  delay(10);
}
```

## Tips for effective serial debugging

**For Serial Monitor:**
- Use descriptive labels: `Serial.print("Temperature: ")` before the value
- Include units: `Serial.println("°C")` after temperature readings
- Add status indicators: Use ✓, ❌, ⚠️ symbols for visual feedback
- Group related output with separator lines: `Serial.println("---")`

**For Serial Plotter:**
- Keep data numeric only once plotting starts
- Use consistent update rates with `delay()` for smooth plots
- Scale different signals to similar ranges for better visualization
- Use meaningful value ranges (0-100% rather than raw ADC values)

**General debugging:**
- Start with high baud rates (115200) for faster data transfer
- Use `Serial.flush()` if you need to ensure data is sent immediately
- Add delays after `Serial.begin()` to let the connection stabilize
- Remember that printing lots of data can slow down your main program

## Troubleshooting common issues

**"Garbled text in Serial Monitor"**
- Check that baud rates match between code and monitor
- Make sure USB cable supports data (not just charging)
- Try a different USB port or cable

**"No data appearing"**
- Verify the correct COM port is selected
- Check that `Serial.begin()` is called in setup()
- Press the reset button on your tinyCore
- Try closing and reopening the Serial Monitor

**"Serial Plotter shows flat lines"**
- Make sure data is numeric (no text mixed in)
- Check that values are separated by tabs or spaces
- Verify the last value uses `Serial.println()`
- Try adjusting the time delay between readings

**"Can't send commands to tinyCore"**
- Ensure the ending is set to "Newline" in Serial Monitor
- Check that your code uses `Serial.available()` and `Serial.readString()`
- Verify that you're calling the read functions in the loop()

## What's next?

Now you have powerful tools for debugging and visualizing your projects. These skills are essential for:

**Debugging complex projects:**
- Tracking down intermittent bugs
- Understanding timing issues
- Monitoring system performance
- Validating sensor readings

**Data analysis:**
- Visualizing sensor patterns over time
- Comparing multiple data sources
- Detecting anomalies or trends
- Optimizing algorithm parameters

**Interactive development:**
- Testing functions with manual commands
- Adjusting parameters without reprogramming
- Creating simple user interfaces
- Remote debugging and control

The combination of Serial Monitor and Serial Plotter makes you a much more effective developer. You can see what your code is thinking, catch problems early, and create more robust projects.

These tools become even more powerful when combined with the sensors and communication protocols you've learned in previous tutorials. Imagine plotting IMU data in real-time, sending debug commands over ESP-NOW, or monitoring multiple sensors simultaneously.

!!! tip "Professional development tip"

    Get in the habit of adding debug prints early in your projects, even for code that seems simple. You'll thank yourself later when you need to track down an elusive bug or understand why a sensor isn't behaving as expected.

!!! warning "Having trouble?"

    Send us an email at [support@mr.industries](mailto:support@mr.industries) or join our [Discord](https://discord.gg/hvJZhwfQsF) for help!