# How to Detect Motion (IMU)

Want to make your tinyCore react to movement? Let's learn to use the built-in motion sensor! The tinyCore has a super cool IMU (Inertial Measurement Unit) that can detect when you move, shake, or rotate it in any direction.

!!! warning "Are you skipping ahead?"

    Make sure you have already setup your Arduino IDE using the [previous tutorial](../get-started/arduino-ide.md)!

## What the heck is an IMU?

An IMU stands for "Inertial Measurement Unit" - basically it's a motion tracker! Think of it like the sensor in your smartphone that knows when you flip it to rotate the screen, or the one in your fitness tracker that counts your steps.

The tinyCore's IMU has **6 "Degrees of Freedom"** (6DOF), meaning it measures 6 different things:

**Accelerometer (3 axes):**
- **X-axis** - Forward/backward movement  
- **Y-axis** - Left/right movement
- **Z-axis** - Up/down movement (gravity!)

**Gyroscope (3 axes):**
- **X-axis** - Rolling motion (like a barrel roll)
- **Y-axis** - Pitching motion (like nodding yes)  
- **Z-axis** - Yawing motion (like shaking your head no)

![6DOF Motion Diagram](images/6dof-motion.png)

If you're into aerospace, you might know these as **pitch, yaw, and roll**!

## What you'll need

- Your tinyCore ESP32-S3 (the IMU is built right in!)
- USB-C cable
- About 15 minutes

## Step 1: Install the IMU library

The tinyCore uses the LSM6DSOX IMU chip, and Adafruit made an awesome library for it.

1. Open Arduino IDE
2. Go to **Tools → Manage Libraries**
3. Search for `Adafruit LSM6DS`
4. Install **Adafruit LSM6DS** by Adafruit

![IMU Library Installation](images/imu-library.png)

!!! tip "For legacy boards"

    If you have an older tinyCore (labeled "iotaCore" on the back), you'll need our special library instead. Check the [setup documentation](../get-started/imu.md) for legacy instructions.

## Step 2: The code

Here's the code that reads all 6 motion sensors and displays the data in a way that's perfect for Arduino's Serial Plotter:

```cpp
#include <Adafruit_LSM6DSOX.h>

Adafruit_LSM6DSOX lsm6dsox;
unsigned long lastSampleTime = 0;
const unsigned long SAMPLE_INTERVAL = 25; // Sample every 25ms (40 times per second)

void setup() {
  Serial.begin(115200);
  
  // Initialize IMU power pin
  pinMode(6, OUTPUT);
  digitalWrite(6, HIGH);  // Turn on the IMU
  
  // Initialize I2C communication
  Wire.begin(3, 4);  // SDA=3, SCL=4 on tinyCore
  delay(100);

  // Scan for the IMU on the I2C bus
  Serial.println("Scanning for I2C devices...");
  for (byte address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
      
      // Check if this is our IMU
      if (address == 0x6A || address == 0x6B) {
        Wire.beginTransmission(address);
        Wire.write(0x0F);  // WHO_AM_I register
        Wire.endTransmission(false);
        Wire.requestFrom(address, 1);
        if (Wire.available()) {
          byte whoAmI = Wire.read();
          Serial.print("WHO_AM_I register value: 0x");
          Serial.println(whoAmI, HEX);
          // Should be 0x6C for LSM6DSOX
        }
      }
    }
  }

  // Initialize the IMU
  Serial.println("Attempting to initialize LSM6DSOX...");
  if (!lsm6dsox.begin_I2C()) {
    Serial.println("Failed to find LSM6DSOX chip");
    Serial.println("Check your wiring!");
    while (1) {
      delay(10);
    }
  }

  Serial.println("LSM6DSOX Found! 🎉");

  // Configure IMU settings
  lsm6dsox.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);    // ±2g sensitivity
  lsm6dsox.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);  // ±250 degrees/second
  lsm6dsox.setAccelDataRate(LSM6DS_RATE_104_HZ);     // 104 samples/second
  lsm6dsox.setGyroDataRate(LSM6DS_RATE_104_HZ);      // 104 samples/second
  
  // Print column headers for Serial Plotter
  Serial.println("AccelX,AccelY,AccelZ,GyroX,GyroY,GyroZ,Temp");
}

void sampleIMUData() {
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t temp;
  
  // Get fresh data from the IMU
  lsm6dsox.getEvent(&accel, &gyro, &temp);
  
  // Print data in Serial Plotter format (comma-separated)
  Serial.print(accel.acceleration.x);  Serial.print(",");
  Serial.print(accel.acceleration.y);  Serial.print(",");
  Serial.print(accel.acceleration.z);  Serial.print(",");
  Serial.print(gyro.gyro.x);           Serial.print(",");
  Serial.print(gyro.gyro.y);           Serial.print(",");
  Serial.print(gyro.gyro.z);           Serial.print(",");
  Serial.println(temp.temperature);
}

void loop() {
  unsigned long currentTime = millis();
  
  // Sample data at our specified interval (25ms = 40Hz)
  if (currentTime - lastSampleTime >= SAMPLE_INTERVAL) {
    sampleIMUData();
    lastSampleTime = currentTime;
  }
}
```

## Step 3: Upload and test

1. Connect your tinyCore via USB-C
2. Select your board: `tinyCore ESP32-S3 No PSRAM`
3. Upload the code
4. Open **Serial Monitor** (115200 baud) to see the data scrolling

You should see numbers streaming like:
```
0.15,-0.23,9.81,0.01,-0.02,0.00,25.4
```

## Step 4: Visualize with Serial Plotter

Here's where it gets really cool! Arduino has a built-in tool to graph the data in real-time.

1. Close the Serial Monitor
2. Go to **Tools → Serial Plotter** 
3. Set the baud rate to **115200** (bottom right)
4. Watch the magic happen!

You should see 7 colored lines dancing around. Each line represents one sensor:

- **Red, Orange, Yellow** = Accelerometer X, Y, Z
- **Green, Blue, Purple** = Gyroscope X, Y, Z  
- **Pink** = Temperature

![Serial Plotter Screenshot](images/serial-plotter-imu.png)

## Step 5: Fun experiments!

Now for the fun part - let's see what different movements look like!

### Experiment 1: Gravity Detection
Place your tinyCore flat on a table. You should see:
- **AccelZ (yellow line)** hovering around **9.81** - that's gravity!
- Other lines should be close to zero

### Experiment 2: Shake Test  
Shake the device and watch all the accelerometer lines go crazy! The more you shake, the bigger the spikes.

### Experiment 3: Rotation Detection
Hold the device and slowly rotate it like a steering wheel. Watch the **GyroZ (purple line)** spike when you turn it.

### Experiment 4: Drawing in the Air
Try drawing circles, figure-8s, or writing letters in the air. See if you can recognize the patterns in the gyroscope data!

??? question "Brain Teaser: Can you guess what movement made this pattern? 🤔"

    If you see regular sine waves in the gyroscope data with about 13 peaks per second, and we're sampling 40 times per second... that's someone spinning the device at exactly 3 Hz (3 rotations per second)!

## Understanding the data

**Accelerometer values** (m/s²):
- **Positive X** = Moving forward/right
- **Positive Y** = Moving up/left  
- **Positive Z** = Moving up (fighting gravity)
- **~9.81** on any axis = That axis is pointing down (gravity)

**Gyroscope values** (degrees/second):
- **Positive values** = Rotating in one direction
- **Negative values** = Rotating the opposite direction
- **Zero** = Not rotating

**Temperature** (°C):
- Just the temperature of the IMU chip itself
- Useful for temperature compensation in precision applications

## Common issues

**"Failed to find LSM6DSOX chip"**
- Make sure you selected the right board type
- Try pressing the reset button and uploading again
- Check that your tinyCore is genuine (older versions might use different chips)

**Noisy/jumpy data**
- This is normal! Real sensors have noise
- You can smooth the data with software filters (see our [advanced IMU guide](../reference/imu.md))
- Make sure the device isn't vibrating from external sources

**Serial Plotter shows nothing**
- Check the baud rate is set to 115200
- Make sure Serial Monitor is closed first
- Try restarting the Arduino IDE

## Code walkthrough

Let's break down what the code does:

**Power and Communication Setup:**
```cpp
pinMode(6, OUTPUT);     // Pin 6 controls IMU power
digitalWrite(6, HIGH);  // Turn on the IMU
Wire.begin(3, 4);       // Start I2C on pins 3(SDA), 4(SCL)
```

**IMU Configuration:**
```cpp
lsm6dsox.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);  // ±2g range (good for most motion)
lsm6dsox.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS); // ±250°/sec (good for hand motion)
```

**Data Reading:**
```cpp
lsm6dsox.getEvent(&accel, &gyro, &temp);  // Get fresh readings
accel.acceleration.x  // X-axis acceleration in m/s²
gyro.gyro.x          // X-axis rotation in degrees/second
```

## What's next?

Now that you can detect motion, you can build amazing projects:

- **Gesture recognition** - Detect specific movements like waves or taps
- **Step counter** - Count steps like a fitness tracker  
- **Motion alarm** - Detect when something moves
- **Game controller** - Use motion to control games
- **Data logger** - Record motion for analysis
- **Wireless motion sharing** - Send motion data to another device with [ESP-NOW](link-tinycores.md)

Want to dive deeper? Check out our [IMU reference guide](../reference/imu.md) to learn about filtering, calibration, and advanced features like tap detection and gesture recognition.

!!! tip "Pro tip"

    The IMU also has built-in features like tap detection, step counting, and even basic gesture recognition! These are covered in the advanced tutorials.

!!! warning "Having trouble?"

    Send us an email at [support@mr.industries](mailto:support@mr.industries) or join our [Discord](https://discord.gg/hvJZhwfQsF) for help!