# Building a Motion Tracker [DRAFT]


Nice job getting this far! Hopefully you've gotten all of the software installed, programmed the board, tested the IMU, and enjoyed your gummy bears. 

It's time for your first challenge! Using what you've learned so far, we're going to develop your first smart device, featuring everything special about the tinyCore. And we'll be learning something new, how to use the SD Card!

!!! note
    
    If you want to learn about the SD Card in depth, check out the [SD Card Tutorial](../basics/sdcard.md) in the Advanced section.


We're going to create a motion tracker/data-logger. This is a device that will measure motion (IMU) and record it (SD Card), then wirelessly send it's data to a computer, which can be graphed out.

This type of device is extremely useful in all sorts of scenarios. I've seen students use this to create a fitness rep counter, musical gloves, a FitBit for cows, a DIY step-counter, door entry alerts, and Physics I acceleration/velocity lab experiments. 

Before we show you the code, let's talk about architecture, how does this system actually work? What would it take to build this system with an industry standard like the Adafruit Feather?

``` mermaid
flowchart TD
    BATT[LiPo Battery - External] 
    COMP[Computer/Host - External]
    ROUTER[WiFi Router - External] 
    SDCARD[Micro SD Card]
    
    subgraph TINYCORE[tinyCore Integrated Board]
        USB[USB-C Port]
        CC[Charge Controller]
        POWER[3.3V Power Rail]
        ESP[ESP32S3 Main Processor]
        IMU[LSM6DSOX IMU Integrated]
        SDSLOT[SD Card Slot]
        WIFI[WiFi Module]
        BLE[Bluetooth LE]
        
        USB --> CC
        CC --> POWER
        POWER --> ESP
        ESP --> IMU
        ESP --> SDSLOT
        ESP --> WIFI
        ESP --> BLE
    end
    
    BATT --> CC
    USB --> COMP
    WIFI --> ROUTER
    ROUTER --> COMP
    BLE --> COMP
    SDCARD --> SDSLOT
```

This is where the beauty of the tinyCore's integration comes in. Normally, you would need to purchase breakouts of an:
- ESP32-S3
- LiPo Battery Power Management
- Micro SD-Card
- LSM6DSOX IMU

Then you would spend a few hours wiring everything together, hopefully making no mistakes, and voila! (Oh wait, you still need code!)

Instead, the tinyCore has everything you need, all in one place. 

Now that we've gone over the hardware architecture, let's talk about the software architecture. It will look something like this:

``` mermaid
flowchart LR
    %% Data Collection
    START([Device Powers On]) --> INIT[Initialize Sensors]
    INIT --> CALIB[Calibrate IMU]
    CALIB --> LOOP{Main Loop}
    
    %% Sensor Reading
    LOOP --> READ[Read IMU Data<br/>Accelerometer XYZ<br/>Gyroscope XYZ]
    READ --> PROC[Process Data<br/>Apply Filters<br/>Calculate Motion Metrics]
    
    %% Data Storage Decision
    PROC --> STORE{Storage Mode?}
    STORE -->|Local Logging| SD_WRITE[Write to SD Card<br/>Timestamp + Data]
    STORE -->|Real-time Stream| WIRELESS[Send via WiFi/BLE]
    STORE -->|Both| SD_WRITE
    STORE -->|Both| WIRELESS
    
    %% Continue Loop
    SD_WRITE --> DELAY[Delay/Sleep]
    WIRELESS --> DELAY
    DELAY --> LOOP
    
    %% External Data Access
    SD_WRITE -.-> USB_READ[USB Data Download]
    WIRELESS -.-> ANALYSIS[Real-time Analysis<br/>on Computer]
    
    %% Styling
    classDef start fill:#4caf50,stroke:#2e7d32,stroke-width:2px
    classDef process fill:#2196f3,stroke:#1565c0,stroke-width:2px
    classDef decision fill:#ff9800,stroke:#ef6c00,stroke-width:2px
    classDef output fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px
    
    class START,INIT,CALIB start
    class READ,PROC,DELAY process
    class LOOP,STORE decision
    class SD_WRITE,WIRELESS,USB_READ,ANALYSIS output
```

The datalogger has three main processes:
1. Setup or Initialization
2. Measure/Record Data
3. Transfer Data

We'll be using UDP to dump the packets to an IP address, so it's easy for us to write a python program that can graph out the information in a useful way.

We'll also be measuring data, but before we send it, we need to process it. This will look like a Kalman filter, and oversampling for noise removal.

So here's the code:

And here's the python program as well:

Once we flash it, we should see this on our python UI!

Try shaking the board around, and watch it rotate in real-time!

Nice job. You've completed your very first project with tinyCore, and we hope it only took about 30 minutes!