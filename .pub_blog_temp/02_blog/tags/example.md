---
publish: 'true'
search:
  exclude: true
slug: example
title: Tag - example

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


## [I2S Audio Test](http://127.0.0.1:8000/blog/2024-11-24-12:00/)

<!--suppress LongLine -->
<div class="post-extra">
    <div class="col">
        <p class="post-date">2024-11-24 12:00:00</p>
    </div>
    <div class="col">
    
        <a href="http://127.0.0.1:8000/blog/tags/example/">#example</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/code/">#code</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/I2S/">#I2S</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/Audio/">#Audio</a>
    
    </div>
</div>

I had Claude write up an I2S Test for a speaker, specifically the MAX98357A. Here's the program it wrote:




<div class="post-link">

    <a href="http://127.0.0.1:8000/blog/2024-11-24-12:00/" title="I2S Audio Test">
        Read more
    </a>

</div>


## [SD Card Test](http://127.0.0.1:8000/blog/2024-11-23-12:05/)

<!--suppress LongLine -->
<div class="post-extra">
    <div class="col">
        <p class="post-date">2024-11-23 12:05:00</p>
    </div>
    <div class="col">
    
        <a href="http://127.0.0.1:8000/blog/tags/example/">#example</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/code/">#code</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/IMU/">#IMU</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/SD/">#SD</a>
    
    </div>
</div>

Finally got the SD Card working! Turns out the CS Pin is connected to GPIO1, not GPIO2, due to a pin mix-up in the library. Simple software fix, and it's like magic!

Also, I would recommend verifying that you don't have a corrupted Chinese-knockoff SD Card, as this will also cause you headaches and make things more difficult to solve.

For the SD test, we actually used the Arduino SD_Test Example, which worked out of the box (with our custom board library):



<div class="post-link">

    <a href="http://127.0.0.1:8000/blog/2024-11-23-12:05/" title="SD Card Test">
        Read more
    </a>

</div>


## [Custom Arduino Library](http://127.0.0.1:8000/blog/custom-arduino-library/)

<!--suppress LongLine -->
<div class="post-extra">
    <div class="col">
        <p class="post-date">2024-11-23 12:00:00</p>
    </div>
    <div class="col">
    
        <a href="http://127.0.0.1:8000/blog/tags/example/">#example</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/code/">#code</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/library/">#library</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/Arduino/">#Arduino</a>
    
    </div>
</div>

Our board needed a custom Arduino library, so I went through and made our own. First I started by copying the ***adafruit_feather_esp32s3_nopsram*** folder from:

*C:\Users\macge\AppData\Local\Arduino15\packages\esp32\hardware\esp32\3.1.0-RC2\variants*

I renamed this file to "***iota_core_esp32s3_nopsram***". (This is very important to remember, because this name definition must match exactly with the boards.txt file we will edit later.)

Within the folder there are four files:    

![image.png](image10.png)

We will want to edit both ***variant.cpp*** and ***pins_arduino.h***.

Let's start with ***pins_arduino.h***:

```cpp
#ifndef Pins_Arduino_h
#define Pins_Arduino_h

#include <stdint.h>
#include "soc/soc_caps.h"

#define USB_VID          0x239A
#define USB_PID          0x8113
#define USB_MANUFACTURER "Mister Industries"
#define USB_PRODUCT      "iotaCore ESP32-S3 No PSRAM"
#define USB_SERIAL       ""  // Empty string for MAC address

// User LED
#define LED_BUILTIN 33
#define BUILTIN_LED LED_BUILTIN  // Maps to the SIG LED Pin

#define I2C_POWER         6     // I2C power pin
#define PIN_I2C_POWER     6     // I2C power pin

static const uint8_t TX = 39;
static const uint8_t RX = 38;
#define TX1 TX
#define RX1 RX

static const uint8_t SDA = 3;
static const uint8_t SCL = 4;

static const uint8_t SS = 1;
static const uint8_t MOSI = 35;
static const uint8_t SCK = 36;
static const uint8_t MISO = 37;

static const uint8_t A0 = 18;
static const uint8_t A1 = 17;
static const uint8_t A2 = 16;
static const uint8_t A3 = 15;
static const uint8_t A4 = 14;
static const uint8_t A5 = 7;
static const uint8_t A6 = 3;
static const uint8_t A7 = 4;
static const uint8_t A8 = 5;
static const uint8_t A9 = 9;
static const uint8_t A10 = 10;
static const uint8_t A11 = 11;
static const uint8_t A12 = 12;
static const uint8_t A13 = 13;

static const uint8_t T3 = 3;
static const uint8_t T4 = 4;
static const uint8_t T5 = 5;
static const uint8_t T8 = 8;
static const uint8_t T9 = 9;
static const uint8_t T10 = 10;
static const uint8_t T11 = 11;
static const uint8_t T12 = 12;
static const uint8_t T13 = 13;
static const uint8_t T14 = 14;

#endif /* Pins_Arduino_h */
```

**The changes I made from the Adafruit library were:**

- Changing the manufacturer and product names
- Updating the built-in LED to Pin 33
- Removing the NEOPixel definitions
- Updated I2C Power pins to Pin 6 (instead of 7)
- Changed the SD Card CS pin to 1
- Updated A5 to Pin 7 (instead of 8)
- Updated A9 to Pin 9 (instead of 9)
- Removed T6 (since it's being used for I2C_PWR)

### Then we need to update variants.cpp

All I did for this was remove the NEOPixel definitions

```arduino
// This board has a power control pin, and we must set it to output and high
// in order to enable the NeoPixels.
pinMode(NEOPIXEL_POWER, OUTPUT);
digitalWrite(NEOPIXEL_POWER, HIGH);
```

### Next we will update boards.txt!

For this, we will copy the board entry for Adafruit's ESP32-S3 No PSRAM, and then modify with our device name we chose earlier:

```arduino
##############################################################
# iotaCore ESP32-S3 No PSRAM

iota_core_esp32s3_nopsram.name=iotaCore ESP32-S3 No PSRAM
iota_core_esp32s3_nopsram.vid.0=0x239A
iota_core_esp32s3_nopsram.pid.0=0x8113
iota_core_esp32s3_nopsram.vid.1=0x239A
iota_core_esp32s3_nopsram.pid.1=0x0113
iota_core_esp32s3_nopsram.vid.2=0x239A
iota_core_esp32s3_nopsram.pid.2=0x8114
iota_core_esp32s3_nopsram.upload_port.0.vid=0x239A
iota_core_esp32s3_nopsram.upload_port.0.pid=0x8113
iota_core_esp32s3_nopsram.upload_port.1.vid=0x239A
iota_core_esp32s3_nopsram.upload_port.1.pid=0x0113
iota_core_esp32s3_nopsram.upload_port.2.vid=0x239A
iota_core_esp32s3_nopsram.upload_port.2.pid=0x8114

iota_core_esp32s3_nopsram.bootloader.tool=esptool_py
iota_core_esp32s3_nopsram.bootloader.tool.default=esptool_py

iota_core_esp32s3_nopsram.upload.tool=esptool_py
iota_core_esp32s3_nopsram.upload.tool.default=esptool_py
iota_core_esp32s3_nopsram.upload.tool.network=esp_ota

iota_core_esp32s3_nopsram.upload.maximum_size=1310720
iota_core_esp32s3_nopsram.upload.maximum_data_size=327680
iota_core_esp32s3_nopsram.upload.flags=
iota_core_esp32s3_nopsram.upload.extra_flags=
iota_core_esp32s3_nopsram.upload.use_1200bps_touch=true
iota_core_esp32s3_nopsram.upload.wait_for_upload_port=true

iota_core_esp32s3_nopsram.serial.disableDTR=false
iota_core_esp32s3_nopsram.serial.disableRTS=false

iota_core_esp32s3_nopsram.build.tarch=xtensa
iota_core_esp32s3_nopsram.build.bootloader_addr=0x0
iota_core_esp32s3_nopsram.build.target=esp32s3
iota_core_esp32s3_nopsram.build.mcu=esp32s3
iota_core_esp32s3_nopsram.build.core=esp32
iota_core_esp32s3_nopsram.build.variant=iota_core_esp32s3_nopsram
iota_core_esp32s3_nopsram.build.board=IOTA_CORE_ESP32S3_NOPSRAM

iota_core_esp32s3_nopsram.build.usb_mode=0
iota_core_esp32s3_nopsram.build.cdc_on_boot=1
iota_core_esp32s3_nopsram.build.msc_on_boot=0
iota_core_esp32s3_nopsram.build.dfu_on_boot=0
iota_core_esp32s3_nopsram.build.f_cpu=240000000L
iota_core_esp32s3_nopsram.build.flash_size=8MB
iota_core_esp32s3_nopsram.build.flash_freq=80m
iota_core_esp32s3_nopsram.build.flash_mode=dio
iota_core_esp32s3_nopsram.build.boot=qio
iota_core_esp32s3_nopsram.build.partitions=default
iota_core_esp32s3_nopsram.build.defines=
iota_core_esp32s3_nopsram.build.loop_core=
iota_core_esp32s3_nopsram.build.event_core=
iota_core_esp32s3_nopsram.build.flash_type=qio
iota_core_esp32s3_nopsram.build.psram_type=qspi
iota_core_esp32s3_nopsram.build.memory_type={build.flash_type}_{build.psram_type}

iota_core_esp32s3_nopsram.menu.LoopCore.1=Core 1
iota_core_esp32s3_nopsram.menu.LoopCore.1.build.loop_core=-DARDUINO_RUNNING_CORE=1
iota_core_esp32s3_nopsram.menu.LoopCore.0=Core 0
iota_core_esp32s3_nopsram.menu.LoopCore.0.build.loop_core=-DARDUINO_RUNNING_CORE=0

iota_core_esp32s3_nopsram.menu.EventsCore.1=Core 1
iota_core_esp32s3_nopsram.menu.EventsCore.1.build.event_core=-DARDUINO_EVENT_RUNNING_CORE=1
iota_core_esp32s3_nopsram.menu.EventsCore.0=Core 0
iota_core_esp32s3_nopsram.menu.EventsCore.0.build.event_core=-DARDUINO_EVENT_RUNNING_CORE=0

iota_core_esp32s3_nopsram.menu.USBMode.default=Hardware CDC and JTAG
iota_core_esp32s3_nopsram.menu.USBMode.default.build.usb_mode=1
iota_core_esp32s3_nopsram.menu.USBMode.hwcdc=USB-OTG (TinyUSB)
iota_core_esp32s3_nopsram.menu.USBMode.hwcdc.build.usb_mode=0

iota_core_esp32s3_nopsram.menu.CDCOnBoot.cdc=Enabled
iota_core_esp32s3_nopsram.menu.CDCOnBoot.cdc.build.cdc_on_boot=1
iota_core_esp32s3_nopsram.menu.CDCOnBoot.default=Disabled
iota_core_esp32s3_nopsram.menu.CDCOnBoot.default.build.cdc_on_boot=0

iota_core_esp32s3_nopsram.menu.MSCOnBoot.default=Disabled
iota_core_esp32s3_nopsram.menu.MSCOnBoot.default.build.msc_on_boot=0
iota_core_esp32s3_nopsram.menu.MSCOnBoot.msc=Enabled (Requires USB-OTG Mode)
iota_core_esp32s3_nopsram.menu.MSCOnBoot.msc.build.msc_on_boot=1

iota_core_esp32s3_nopsram.menu.DFUOnBoot.default=Disabled
iota_core_esp32s3_nopsram.menu.DFUOnBoot.default.build.dfu_on_boot=0
iota_core_esp32s3_nopsram.menu.DFUOnBoot.dfu=Enabled (Requires USB-OTG Mode)
iota_core_esp32s3_nopsram.menu.DFUOnBoot.dfu.build.dfu_on_boot=1

iota_core_esp32s3_nopsram.menu.UploadMode.default=UART0 / Hardware CDC
iota_core_esp32s3_nopsram.menu.UploadMode.default.upload.use_1200bps_touch=false
iota_core_esp32s3_nopsram.menu.UploadMode.default.upload.wait_for_upload_port=false
iota_core_esp32s3_nopsram.menu.UploadMode.cdc=USB-OTG CDC (TinyUSB)
iota_core_esp32s3_nopsram.menu.UploadMode.cdc.upload.use_1200bps_touch=true
iota_core_esp32s3_nopsram.menu.UploadMode.cdc.upload.wait_for_upload_port=true

iota_core_esp32s3_nopsram.menu.PartitionScheme.tinyuf2=TinyUF2 8MB (2MB APP/3.7MB FATFS)
iota_core_esp32s3_nopsram.menu.PartitionScheme.tinyuf2.build.custom_bootloader=bootloader-tinyuf2
iota_core_esp32s3_nopsram.menu.PartitionScheme.tinyuf2.build.partitions=tinyuf2-partitions-8MB
iota_core_esp32s3_nopsram.menu.PartitionScheme.tinyuf2.upload.maximum_size=2097152
iota_core_esp32s3_nopsram.menu.PartitionScheme.tinyuf2.upload.extra_flags=0x410000 "{runtime.platform.path}/variants/{build.variant}/tinyuf2.bin"
iota_core_esp32s3_nopsram.menu.PartitionScheme.tinyuf2_noota=TinyUF2 8MB No OTA (4MB APP/3.7MB FATFS)
iota_core_esp32s3_nopsram.menu.PartitionScheme.tinyuf2_noota.build.custom_bootloader=bootloader-tinyuf2
iota_core_esp32s3_nopsram.menu.PartitionScheme.tinyuf2_noota.build.partitions=tinyuf2-partitions-8MB-noota
iota_core_esp32s3_nopsram.menu.PartitionScheme.tinyuf2_noota.upload.maximum_size=4194304
iota_core_esp32s3_nopsram.menu.PartitionScheme.tinyuf2_noota.upload.extra_flags=0x410000 "{runtime.platform.path}/variants/{build.variant}/tinyuf2.bin"
iota_core_esp32s3_nopsram.menu.PartitionScheme.default_8MB=Default (3MB APP/1.5MB SPIFFS)
iota_core_esp32s3_nopsram.menu.PartitionScheme.default_8MB.build.partitions=default_8MB
iota_core_esp32s3_nopsram.menu.PartitionScheme.default_8MB.upload.maximum_size=3342336

iota_core_esp32s3_nopsram.menu.CPUFreq.240=240MHz (WiFi)
iota_core_esp32s3_nopsram.menu.CPUFreq.240.build.f_cpu=240000000L
iota_core_esp32s3_nopsram.menu.CPUFreq.160=160MHz (WiFi)
iota_core_esp32s3_nopsram.menu.CPUFreq.160.build.f_cpu=160000000L
iota_core_esp32s3_nopsram.menu.CPUFreq.80=80MHz (WiFi)
iota_core_esp32s3_nopsram.menu.CPUFreq.80.build.f_cpu=80000000L
iota_core_esp32s3_nopsram.menu.CPUFreq.40=40MHz
iota_core_esp32s3_nopsram.menu.CPUFreq.40.build.f_cpu=40000000L
iota_core_esp32s3_nopsram.menu.CPUFreq.20=20MHz
iota_core_esp32s3_nopsram.menu.CPUFreq.20.build.f_cpu=20000000L
iota_core_esp32s3_nopsram.menu.CPUFreq.10=10MHz
iota_core_esp32s3_nopsram.menu.CPUFreq.10.build.f_cpu=10000000L

iota_core_esp32s3_nopsram.menu.FlashMode.qio=QIO 80MHz
iota_core_esp32s3_nopsram.menu.FlashMode.qio.build.flash_mode=dio
iota_core_esp32s3_nopsram.menu.FlashMode.qio.build.boot=qio
iota_core_esp32s3_nopsram.menu.FlashMode.qio.build.boot_freq=80m
iota_core_esp32s3_nopsram.menu.FlashMode.qio.build.flash_freq=80m
iota_core_esp32s3_nopsram.menu.FlashMode.qio120=QIO 120MHz
iota_core_esp32s3_nopsram.menu.FlashMode.qio120.build.flash_mode=dio
iota_core_esp32s3_nopsram.menu.FlashMode.qio120.build.boot=qio
iota_core_esp32s3_nopsram.menu.FlashMode.qio120.build.boot_freq=120m
iota_core_esp32s3_nopsram.menu.FlashMode.qio120.build.flash_freq=80m
iota_core_esp32s3_nopsram.menu.FlashMode.dio=DIO 80MHz
iota_core_esp32s3_nopsram.menu.FlashMode.dio.build.flash_mode=dio
iota_core_esp32s3_nopsram.menu.FlashMode.dio.build.boot=dio
iota_core_esp32s3_nopsram.menu.FlashMode.dio.build.boot_freq=80m
iota_core_esp32s3_nopsram.menu.FlashMode.dio.build.flash_freq=80m
iota_core_esp32s3_nopsram.menu.FlashMode.opi=OPI 80MHz
iota_core_esp32s3_nopsram.menu.FlashMode.opi.build.flash_mode=dout
iota_core_esp32s3_nopsram.menu.FlashMode.opi.build.boot=opi
iota_core_esp32s3_nopsram.menu.FlashMode.opi.build.boot_freq=80m
iota_core_esp32s3_nopsram.menu.FlashMode.opi.build.flash_freq=80m

iota_core_esp32s3_nopsram.menu.FlashSize.8M=8MB (64Mb)
iota_core_esp32s3_nopsram.menu.FlashSize.8M.build.flash_size=8MB

iota_core_esp32s3_nopsram.menu.UploadSpeed.921600=921600
iota_core_esp32s3_nopsram.menu.UploadSpeed.921600.upload.speed=921600
iota_core_esp32s3_nopsram.menu.UploadSpeed.115200=115200
iota_core_esp32s3_nopsram.menu.UploadSpeed.115200.upload.speed=115200
iota_core_esp32s3_nopsram.menu.UploadSpeed.256000.windows=256000
iota_core_esp32s3_nopsram.menu.UploadSpeed.256000.upload.speed=256000
iota_core_esp32s3_nopsram.menu.UploadSpeed.230400.windows.upload.speed=256000
iota_core_esp32s3_nopsram.menu.UploadSpeed.230400=230400
iota_core_esp32s3_nopsram.menu.UploadSpeed.230400.upload.speed=230400
iota_core_esp32s3_nopsram.menu.UploadSpeed.460800.linux=460800
iota_core_esp32s3_nopsram.menu.UploadSpeed.460800.macosx=460800
iota_core_esp32s3_nopsram.menu.UploadSpeed.460800.upload.speed=460800
iota_core_esp32s3_nopsram.menu.UploadSpeed.512000.windows=512000
iota_core_esp32s3_nopsram.menu.UploadSpeed.512000.upload.speed=512000

iota_core_esp32s3_nopsram.menu.DebugLevel.none=None
iota_core_esp32s3_nopsram.menu.DebugLevel.none.build.code_debug=0
iota_core_esp32s3_nopsram.menu.DebugLevel.error=Error
iota_core_esp32s3_nopsram.menu.DebugLevel.error.build.code_debug=1
iota_core_esp32s3_nopsram.menu.DebugLevel.warn=Warn
iota_core_esp32s3_nopsram.menu.DebugLevel.warn.build.code_debug=2
iota_core_esp32s3_nopsram.menu.DebugLevel.info=Info
iota_core_esp32s3_nopsram.menu.DebugLevel.info.build.code_debug=3
iota_core_esp32s3_nopsram.menu.DebugLevel.debug=Debug
iota_core_esp32s3_nopsram.menu.DebugLevel.debug.build.code_debug=4
iota_core_esp32s3_nopsram.menu.DebugLevel.verbose=Verbose
iota_core_esp32s3_nopsram.menu.DebugLevel.verbose.build.code_debug=5

iota_core_esp32s3_nopsram.menu.EraseFlash.none=Disabled
iota_core_esp32s3_nopsram.menu.EraseFlash.none.upload.erase_cmd=
iota_core_esp32s3_nopsram.menu.EraseFlash.all=Enabled
iota_core_esp32s3_nopsram.menu.EraseFlash.all.upload.erase_cmd=-e

iota_core_esp32s3_nopsram.menu.ZigbeeMode.default=Disabled
iota_core_esp32s3_nopsram.menu.ZigbeeMode.default.build.zigbee_mode=
iota_core_esp32s3_nopsram.menu.ZigbeeMode.default.build.zigbee_libs=
iota_core_esp32s3_nopsram.menu.ZigbeeMode.zczr=Zigbee ZCZR (coordinator/router)
iota_core_esp32s3_nopsram.menu.ZigbeeMode.zczr.build.zigbee_mode=-DZIGBEE_MODE_ZCZR
iota_core_esp32s3_nopsram.menu.ZigbeeMode.zczr.build.zigbee_libs=-lesp_zb_api_zczr -lesp_zb_cli_command -lzboss_stack.zczr -lzboss_port

```

I also re-arranged the ***UART0 / Hardware CDC*** and ***Hardware CDC and JTAG*** entries to defaults, so that we get rid of that pesky serial monitor issue when dealing with the default upload settings on Arduino. I don't know why Adafruit didn't fix this a long time ago...

Make sure to update the variant and board names:

```arduino
iota_core_esp32s3_nopsram.build.variant=iota_core_esp32s3_nopsram
iota_core_esp32s3_nopsram.build.board=IOTA_CORE_ESP32S3_NOPSRAM
```

And that's it! Now when you re-load Arduino, iotaCore will show up in the boards list in the IDE. Selecting the board and flashing the Blink example results in a working SIG light blinking!



<div class="post-link">

    &nbsp;

</div>


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


## [I2C Test](http://127.0.0.1:8000/blog/2024-11-6-12:05/)

<!--suppress LongLine -->
<div class="post-extra">
    <div class="col">
        <p class="post-date">2024-11-06 12:05:00</p>
    </div>
    <div class="col">
    
        <a href="http://127.0.0.1:8000/blog/tags/example/">#example</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/code/">#code</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/I2C/">#I2C</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/IMU/">#IMU</a>
    
    </div>
</div>

Date: November 6, 2024

Issues with I2C:

1. I2C PWR is run on a separate bus for low-power functionality, so you must enable I2C_PWR pin, which is GPIO 6! (Pin 10 on the ESP Module)
2. I2C default pins are 22 and 21, which do not work for our board. We are using pins 3/4 for SDA/SCL respectively.

This is what a working setup function looks like:

```cpp
void setup() {
  pinMode(6, OUTPUT); //Setup the I2C_PWR Pin
  digitalWrite(6, HIGH); //Turn on the I2C Devices
  Serial.begin(115200);
  Wire.begin(3, 4); //Initialize I2C on pins 3 (SDA) and 4 (SCL)
}
```

### LSM6DS3 (IMU) Test:

The IMU does not show up right away with the Adafruit example code because it is has the incorrect WHO_AM_I register value: ***0x69*** (nice) instead of the expected ***0x6A*** (not to be confused with the I2C Address, which is also ***0x6A**)*. To fix this, we have to change the Chip ID variable in the Adafruit_LSM6DS3TRC.h file: 

```arduino
#define LSM6DS3TRC_CHIP_ID 0x69 ///< LSM6DSL default device id from WHOAMI
```

(this is normally set to 0x6A)

**In the code, we also need to call "Wire.begin(3, 4)" before "lsm6ds3trc.begin_I2C()" and to set the I2C_PWR pin high:**

```cpp
  pinMode(6, OUTPUT);
  digitalWrite(6, HIGH);
  
  Serial.begin(115200);
  while (!Serial)
    delay(10);

  Serial.println("Starting I2C initialization...");
  Wire.begin(3, 4);
  delay(100);  // Give I2C time to stabilize
```

With this, I was able to get a nice Serial Plotter output in Arduino:

![image.png](image8.png)

![image.png](image9.png)

The final working Arduino code: *(note that this library file has already had its variables manually updated)*

```cpp
// Basic demo for accelerometer/gyro readings from Adafruit LSM6DS3TR-C

#include <Adafruit_LSM6DS3TRC.h>

// For SPI mode, we need a CS pin
#define LSM_CS 10
// For software-SPI mode we need SCK/MOSI/MISO pins
#define LSM_SCK 13
#define LSM_MISO 12
#define LSM_MOSI 11

Adafruit_LSM6DS3TRC lsm6ds3trc;

void setup(void) {
  pinMode(6, OUTPUT);
  digitalWrite(6, HIGH);
  
  Serial.begin(115200);
  while (!Serial)
    delay(10);

  Serial.println("Starting I2C initialization...");
  Wire.begin(3, 4);
  delay(100);  // Give I2C time to stabilize

  Serial.println("Scanning for I2C devices...");
  for (byte address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address < 16) {
        Serial.print("0");
      }
      Serial.println(address, HEX);
      
      // If this is our LSM6DS3TR-C address, try reading WHO_AM_I register
      if (address == 0x6A) {
        Wire.beginTransmission(0x6A);
        Wire.write(0x0F);  // WHO_AM_I register address
        Wire.endTransmission(false);
        Wire.requestFrom(0x6A, 1);
        if (Wire.available()) {
          byte whoAmI = Wire.read();
          Serial.print("WHO_AM_I register value: 0x");
          Serial.println(whoAmI, HEX);
          // Should be 0x6A for LSM6DS3TR-C
        }
      }
    }
  }

  Serial.println("Attempting to initialize LSM6DS3TR-C...");
  if (!lsm6ds3trc.begin_I2C()) {
    Serial.println("Failed to find LSM6DS3TR-C chip");
    Serial.println("Check your wiring!");
    while (1) {
      delay(10);
    }
  }

  Serial.println("LSM6DS3TR-C Found!");

  // lsm6ds3trc.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);
  Serial.print("Accelerometer range set to: ");
  switch (lsm6ds3trc.getAccelRange()) {
  case LSM6DS_ACCEL_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case LSM6DS_ACCEL_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case LSM6DS_ACCEL_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case LSM6DS_ACCEL_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }

  // lsm6ds3trc.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);
  Serial.print("Gyro range set to: ");
  switch (lsm6ds3trc.getGyroRange()) {
  case LSM6DS_GYRO_RANGE_125_DPS:
    Serial.println("125 degrees/s");
    break;
  case LSM6DS_GYRO_RANGE_250_DPS:
    Serial.println("250 degrees/s");
    break;
  case LSM6DS_GYRO_RANGE_500_DPS:
    Serial.println("500 degrees/s");
    break;
  case LSM6DS_GYRO_RANGE_1000_DPS:
    Serial.println("1000 degrees/s");
    break;
  case LSM6DS_GYRO_RANGE_2000_DPS:
    Serial.println("2000 degrees/s");
    break;
  case ISM330DHCX_GYRO_RANGE_4000_DPS:
    break; // unsupported range for the DS33
  }

  // lsm6ds3trc.setAccelDataRate(LSM6DS_RATE_12_5_HZ);
  Serial.print("Accelerometer data rate set to: ");
  switch (lsm6ds3trc.getAccelDataRate()) {
  case LSM6DS_RATE_SHUTDOWN:
    Serial.println("0 Hz");
    break;
  case LSM6DS_RATE_12_5_HZ:
    Serial.println("12.5 Hz");
    break;
  case LSM6DS_RATE_26_HZ:
    Serial.println("26 Hz");
    break;
  case LSM6DS_RATE_52_HZ:
    Serial.println("52 Hz");
    break;
  case LSM6DS_RATE_104_HZ:
    Serial.println("104 Hz");
    break;
  case LSM6DS_RATE_208_HZ:
    Serial.println("208 Hz");
    break;
  case LSM6DS_RATE_416_HZ:
    Serial.println("416 Hz");
    break;
  case LSM6DS_RATE_833_HZ:
    Serial.println("833 Hz");
    break;
  case LSM6DS_RATE_1_66K_HZ:
    Serial.println("1.66 KHz");
    break;
  case LSM6DS_RATE_3_33K_HZ:
    Serial.println("3.33 KHz");
    break;
  case LSM6DS_RATE_6_66K_HZ:
    Serial.println("6.66 KHz");
    break;
  }

  // lsm6ds3trc.setGyroDataRate(LSM6DS_RATE_12_5_HZ);
  Serial.print("Gyro data rate set to: ");
  switch (lsm6ds3trc.getGyroDataRate()) {
  case LSM6DS_RATE_SHUTDOWN:
    Serial.println("0 Hz");
    break;
  case LSM6DS_RATE_12_5_HZ:
    Serial.println("12.5 Hz");
    break;
  case LSM6DS_RATE_26_HZ:
    Serial.println("26 Hz");
    break;
  case LSM6DS_RATE_52_HZ:
    Serial.println("52 Hz");
    break;
  case LSM6DS_RATE_104_HZ:
    Serial.println("104 Hz");
    break;
  case LSM6DS_RATE_208_HZ:
    Serial.println("208 Hz");
    break;
  case LSM6DS_RATE_416_HZ:
    Serial.println("416 Hz");
    break;
  case LSM6DS_RATE_833_HZ:
    Serial.println("833 Hz");
    break;
  case LSM6DS_RATE_1_66K_HZ:
    Serial.println("1.66 KHz");
    break;
  case LSM6DS_RATE_3_33K_HZ:
    Serial.println("3.33 KHz");
    break;
  case LSM6DS_RATE_6_66K_HZ:
    Serial.println("6.66 KHz");
    break;
  }

  lsm6ds3trc.configInt1(false, false, true); // accelerometer DRDY on INT1
  lsm6ds3trc.configInt2(false, true, false); // gyro DRDY on INT2
}

void loop() {
  // Get a new normalized sensor event
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t temp;
  lsm6ds3trc.getEvent(&accel, &gyro, &temp);

//  Serial.print("\t\tTemperature ");
//  Serial.print(temp.temperature);
//  Serial.println(" deg C");

  /* Display the results (acceleration is measured in m/s^2) */
//  Serial.print("\t\tAccel X: ");
//  Serial.print(accel.acceleration.x);
//  Serial.print(" \tY: ");
//  Serial.print(accel.acceleration.y);
//  Serial.print(" \tZ: ");
//  Serial.print(accel.acceleration.z);
//  Serial.println(" m/s^2 ");

  /* Display the results (rotation is measured in rad/s) */
//  Serial.print("\t\tGyro X: ");
//  Serial.print(gyro.gyro.x);
//  Serial.print(" \tY: ");
//  Serial.print(gyro.gyro.y);
//  Serial.print(" \tZ: ");
//  Serial.print(gyro.gyro.z);
//  Serial.println(" radians/s ");
//  Serial.println();

  delay(100);

  // serial plotter friendly format

  Serial.print(temp.temperature);
  Serial.print(",");

  Serial.print(accel.acceleration.x);
  Serial.print(","); Serial.print(accel.acceleration.y);
  Serial.print(","); Serial.print(accel.acceleration.z);
  Serial.print(",");

  Serial.print(gyro.gyro.x);
  Serial.print(","); Serial.print(gyro.gyro.y);
  Serial.print(","); Serial.print(gyro.gyro.z);
  Serial.println();
  delayMicroseconds(10000);
}
```



<div class="post-link">

    &nbsp;

</div>


## [ESP-NOW Test](http://127.0.0.1:8000/blog/2024-11-06-12:00/)

<!--suppress LongLine -->
<div class="post-extra">
    <div class="col">
        <p class="post-date">2024-11-06 12:00:00</p>
    </div>
    <div class="col">
    
        <a href="http://127.0.0.1:8000/blog/tags/testing/">#testing</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/example/">#example</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/code/">#code</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/ESP-NOW/">#ESP-NOW</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/MAC/">#MAC</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/WiFi/">#WiFi</a>
    
    </div>
</div>

Had to find the MAC Addresses of the devices first, so I used this program:

```cpp
#include <WiFi.h>
#include <esp_wifi.h>

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Initialize WiFi properly
  WiFi.mode(WIFI_MODE_APSTA);  // Set to AP+STA mode
  delay(100);  // Give it some time to initialize
  
  // Print Station MAC
  Serial.print("Station MAC Address: ");
  Serial.println(WiFi.macAddress());
  
  // Print AP MAC
  Serial.print("AP MAC Address: ");
  Serial.println(WiFi.softAPmacAddress());
  
  // Additional info about relationship
  Serial.println("\nTypically, the AP MAC is the Station MAC with");
  Serial.println("the last byte incremented by 1");
}

void loop() {
  // Empty loop
}
```

Then you can use the ESPNOW Serial Example to test coms

I set it up to send IMU Data through via the Station device, to the AP device and graph it onto the serial plotter:

First, I used the ESP-NOW Serial Example as a basis for checking the ESP-NOW connection:

```
/*
    ESP-NOW Serial Example - Unicast transmission
    Lucas Saavedra Vaz - 2024
    Send data between two ESP32s using the ESP-NOW protocol in one-to-one (unicast) configuration.
    Note that different MAC addresses are used for different interfaces.
    The devices can be in different modes (AP or Station) and still communicate using ESP-NOW.
    The only requirement is that the devices are on the same Wi-Fi channel.
    Set the peer MAC address according to the device that will receive the data.

    Example setup:
    - Device 1: AP mode with MAC address F6:12:FA:42:B6:E8
                Peer MAC address set to the Station MAC address of Device 2 (F4:12:FA:40:64:4C)
    - Device 2: Station mode with MAC address F4:12:FA:40:64:4C
                Peer MAC address set to the AP MAC address of Device 1 (F6:12:FA:42:B6:E8)

    The device running this sketch will also receive and print data from any device that has its MAC address set as the peer MAC address.
    To properly visualize the data being sent, set the line ending in the Serial Monitor to "Both NL & CR".
*/

#include "ESP32_NOW_Serial.h"
#include "MacAddress.h"
#include "WiFi.h"

#include "esp_wifi.h"

// 0: AP mode, 1: Station mode
#define ESPNOW_WIFI_MODE_STATION 0

// Channel to be used by the ESP-NOW protocol
#define ESPNOW_WIFI_CHANNEL 1

#if ESPNOW_WIFI_MODE_STATION          // ESP-NOW using WiFi Station mode
#define ESPNOW_WIFI_MODE WIFI_STA     // WiFi Mode
#define ESPNOW_WIFI_IF   WIFI_IF_STA  // WiFi Interface
#else                                 // ESP-NOW using WiFi AP mode
#define ESPNOW_WIFI_MODE WIFI_AP      // WiFi Mode
#define ESPNOW_WIFI_IF   WIFI_IF_AP   // WiFi Interface
#endif

// Set the MAC address of the device that will receive the data
// For example: F4:12:FA:40:64:4C
const MacAddress peer_mac({0xF0, 0xF5, 0xBD, 0x50, 0xB0, 0x80});

ESP_NOW_Serial_Class NowSerial(peer_mac, ESPNOW_WIFI_CHANNEL, ESPNOW_WIFI_IF);

void setup() {
  Serial.begin(115200);

  Serial.print("WiFi Mode: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? "AP" : "Station");
  WiFi.mode(ESPNOW_WIFI_MODE);

  Serial.print("Channel: ");
  Serial.println(ESPNOW_WIFI_CHANNEL);
  WiFi.setChannel(ESPNOW_WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);

  while (!(WiFi.STA.started() || WiFi.AP.started())) {
    delay(100);
  }

  Serial.print("MAC Address: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? WiFi.softAPmacAddress() : WiFi.macAddress());

  // Start the ESP-NOW communication
  Serial.println("ESP-NOW communication starting...");
  NowSerial.begin(115200);
  Serial.println("You can now send data to the peer device using the Serial Monitor.\n");
}

void loop() {
  while (NowSerial.available()) {
    Serial.write(NowSerial.read());
  }

  while (Serial.available() && NowSerial.availableForWrite()) {
    if (NowSerial.write(Serial.read()) <= 0) {
      Serial.println("Failed to send data");
      break;
    }
  }

  delay(1);
}
```

```cpp
/*
    ESP-NOW Serial Example - Unicast transmission
    Lucas Saavedra Vaz - 2024
    Send data between two ESP32s using the ESP-NOW protocol in one-to-one (unicast) configuration.
    Note that different MAC addresses are used for different interfaces.
    The devices can be in different modes (AP or Station) and still communicate using ESP-NOW.
    The only requirement is that the devices are on the same Wi-Fi channel.
    Set the peer MAC address according to the device that will receive the data.

    Example setup:
    - Device 1: AP mode with MAC address F6:12:FA:42:B6:E8
                Peer MAC address set to the Station MAC address of Device 2 (F4:12:FA:40:64:4C)
    - Device 2: Station mode with MAC address F4:12:FA:40:64:4C
                Peer MAC address set to the AP MAC address of Device 1 (F6:12:FA:42:B6:E8)

    The device running this sketch will also receive and print data from any device that has its MAC address set as the peer MAC address.
    To properly visualize the data being sent, set the line ending in the Serial Monitor to "Both NL & CR".
*/

#include "ESP32_NOW_Serial.h"
#include "MacAddress.h"
#include "WiFi.h"

#include "esp_wifi.h"

// 0: AP mode, 1: Station mode
#define ESPNOW_WIFI_MODE_STATION 1

// Channel to be used by the ESP-NOW protocol
#define ESPNOW_WIFI_CHANNEL 1

#if ESPNOW_WIFI_MODE_STATION          // ESP-NOW using WiFi Station mode
#define ESPNOW_WIFI_MODE WIFI_STA     // WiFi Mode
#define ESPNOW_WIFI_IF   WIFI_IF_STA  // WiFi Interface
#else                                 // ESP-NOW using WiFi AP mode
#define ESPNOW_WIFI_MODE WIFI_AP      // WiFi Mode
#define ESPNOW_WIFI_IF   WIFI_IF_AP   // WiFi Interface
#endif

// Set the MAC address of the device that will receive the data
// For example: F4:12:FA:40:64:4C
const MacAddress peer_mac({0xF2, 0xF5, 0xBD, 0x50, 0xB0, 0x10});

ESP_NOW_Serial_Class NowSerial(peer_mac, ESPNOW_WIFI_CHANNEL, ESPNOW_WIFI_IF);

void setup() {
  Serial.begin(115200);

  Serial.print("WiFi Mode: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? "AP" : "Station");
  WiFi.mode(ESPNOW_WIFI_MODE);

  Serial.print("Channel: ");
  Serial.println(ESPNOW_WIFI_CHANNEL);
  WiFi.setChannel(ESPNOW_WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);

  while (!(WiFi.STA.started() || WiFi.AP.started())) {
    delay(100);
  }

  Serial.print("MAC Address: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? WiFi.softAPmacAddress() : WiFi.macAddress());

  // Start the ESP-NOW communication
  Serial.println("ESP-NOW communication starting...");
  NowSerial.begin(115200);
  Serial.println("You can now send data to the peer device using the Serial Monitor.\n");
}

void loop() {
  while (NowSerial.available()) {
    Serial.write(NowSerial.read());
  }

  while (Serial.available() && NowSerial.availableForWrite()) {
    if (NowSerial.write(Serial.read()) <= 0) {
      Serial.println("Failed to send data");
      break;
    }
  }

  delay(1);
}
```

This worked great, and I was able to send characters/messages through Serial Monitor between the devices!

Then for the station device, I used Claude to generate an interface which allowed the user to choose between a throughput test, streaming data the IMU, and stopping all actions, based on character commands sent from the AP device. This was the final output of working code:

```cpp
#include "ESP32_NOW_Serial.h"
#include "MacAddress.h"
#include "WiFi.h"
#include "esp_wifi.h"
#include <Adafruit_LSM6DS3TRC.h>

// ESP-NOW Configuration
#define ESPNOW_WIFI_MODE_STATION 1
#define ESPNOW_WIFI_CHANNEL 1

#if ESPNOW_WIFI_MODE_STATION
#define ESPNOW_WIFI_MODE WIFI_STA
#define ESPNOW_WIFI_IF   WIFI_IF_STA
#else
#define ESPNOW_WIFI_MODE WIFI_AP
#define ESPNOW_WIFI_IF   WIFI_IF_AP
#endif

// Set your receiver's MAC address here
const MacAddress peer_mac({0xF2, 0xF5, 0xBD, 0x50, 0xB0, 0x10});

ESP_NOW_Serial_Class NowSerial(peer_mac, ESPNOW_WIFI_CHANNEL, ESPNOW_WIFI_IF);
Adafruit_LSM6DS3TRC lsm6ds3trc;

// Buffer for formatting IMU data
char dataBuffer[100];

// Throughput test variables
unsigned long startTime;
unsigned long bytesTransmitted = 0;
unsigned long packetsTransmitted = 0;
bool isRunning = false;
bool inThroughputTest = false;
const unsigned long THROUGHPUT_TEST_DURATION = 5000; // 5 seconds test

void setup() {
  Serial.begin(115200);
  
  // Initialize IMU-related pins
  pinMode(6, OUTPUT);
  digitalWrite(6, HIGH);
  
  // Initialize I2C
  Wire.begin(3, 4);
  delay(100);

  // Initialize WiFi for ESP-NOW
  Serial.print("WiFi Mode: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? "AP" : "Station");
  WiFi.mode(ESPNOW_WIFI_MODE);

  Serial.print("Channel: ");
  Serial.println(ESPNOW_WIFI_CHANNEL);
  WiFi.setChannel(ESPNOW_WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);

  while (!(WiFi.STA.started() || WiFi.AP.started())) {
    delay(100);
  }

  Serial.print("MAC Address: ");
  Serial.println(ESPNOW_WIFI_MODE == WIFI_AP ? WiFi.softAPmacAddress() : WiFi.macAddress());

  // Initialize ESP-NOW
  Serial.println("ESP-NOW communication starting...");
  NowSerial.begin(115200);

  // Initialize LSM6DS3TR-C
  Serial.println("Initializing LSM6DS3TR-C...");
  if (!lsm6ds3trc.begin_I2C()) {
    Serial.println("Failed to find LSM6DS3TR-C chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("LSM6DS3TR-C Found!");

  // Configure IMU settings
  lsm6ds3trc.setAccelRange(LSM6DS_ACCEL_RANGE_2_G);
  lsm6ds3trc.setGyroRange(LSM6DS_GYRO_RANGE_250_DPS);
  lsm6ds3trc.setAccelDataRate(LSM6DS_RATE_104_HZ);
  lsm6ds3trc.setGyroDataRate(LSM6DS_RATE_104_HZ);

  lsm6ds3trc.configInt1(false, false, true);  // accelerometer DRDY on INT1
  lsm6ds3trc.configInt2(false, true, false);  // gyro DRDY on INT2

  Serial.println("Waiting for command from AP...");
  Serial.println("Commands:");
  Serial.println("'s' - Start IMU data transmission");
  Serial.println("'t' - Run throughput test");
  Serial.println("'x' - Stop current operation");
}

void performThroughputTest() {
  const char testData[] = "THROUGHPUT_TEST_PACKET";
  startTime = millis();
  bytesTransmitted = 0;
  packetsTransmitted = 0;
  
  Serial.println("Starting throughput test for 5 seconds...");
  
  while (millis() - startTime < THROUGHPUT_TEST_DURATION) {
    if (NowSerial.availableForWrite()) {
      // Send test packet
      for (size_t i = 0; i < strlen(testData); i++) {
        NowSerial.write(testData[i]);
      }
      NowSerial.write('\n');
      
      bytesTransmitted += strlen(testData) + 1;  // +1 for newline
      packetsTransmitted++;
    }
    
    // Check for stop command
    if (NowSerial.available()) {
      char cmd = NowSerial.read();
      if (cmd == 'x') {
        break;
      }
    }
  }
  
  // Calculate and display results
  unsigned long duration = millis() - startTime;
  float throughputKBps = (bytesTransmitted * 1000.0) / (duration * 1024.0);  // KB/s
  float packetsPerSecond = (packetsTransmitted * 1000.0) / duration;
  
  Serial.println("\nThroughput Test Results:");
  Serial.printf("Duration: %lu ms\n", duration);
  Serial.printf("Bytes transmitted: %lu\n", bytesTransmitted);
  Serial.printf("Packets transmitted: %lu\n", packetsTransmitted);
  Serial.printf("Throughput: %.2f KB/s\n", throughputKBps);
  Serial.printf("Packets per second: %.2f\n", packetsPerSecond);
  
  inThroughputTest = false;
}

void sendIMUData() {
  // Read IMU data
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t temp;
  lsm6ds3trc.getEvent(&accel, &gyro, &temp);

  // Format the data into a string
  snprintf(dataBuffer, sizeof(dataBuffer), "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f",
           temp.temperature,
           accel.acceleration.x,
           accel.acceleration.y,
           accel.acceleration.z,
           gyro.gyro.x,
           gyro.gyro.y,
           gyro.gyro.z);

  // Send the data over ESP-NOW
  if (NowSerial.availableForWrite()) {
    for (size_t i = 0; i < strlen(dataBuffer); i++) {
      NowSerial.write(dataBuffer[i]);
    }
    NowSerial.write('\n');
  }

  // Also print to Serial for debugging
  Serial.println(dataBuffer);
}

void loop() {
  // Check for incoming commands
  while (NowSerial.available()) {
    char cmd = NowSerial.read();
    
    switch (cmd) {
      case 's':
        if (!isRunning && !inThroughputTest) {
          Serial.println("Starting IMU data transmission...");
          isRunning = true;
        }
        break;
        
      case 't':
        if (!isRunning && !inThroughputTest) {
          inThroughputTest = true;
          performThroughputTest();
        }
        break;
        
      case 'x':
        if (isRunning || inThroughputTest) {
          Serial.println("Stopping current operation...");
          isRunning = false;
          inThroughputTest = false;
        }
        break;
    }
  }

  // Send IMU data if running
  if (isRunning) {
    sendIMUData();
    delay(100);  // Adjust this delay based on your needs
  }
}
```

After running the throughput test, I got around 57KB/s. This is about 0.46 Mbps!

The data also transferred cleanly, and I was able to view it through the serial plotter.

<aside>
Note: The AP device is still running the example ESP-NOW Serial program in this configuriation.
</aside>

### Update 11/23/24:

---

Since adding a custom board library, we no longer need to specify the I2C PWR pins, so these lines have been removed from the example:

```cpp
  // Initialize IMU-related pins
  ~~pinMode(6, OUTPUT);
	digitalWrite(6, HIGH);~~
```

Also, I2C pins have been written in the board specification, so we can remove those parameters from I2C.begin():

```cpp
  // Initialize I2C
  Wire.begin(~~3, 4~~);
  delay(100);

```



<div class="post-link">

    &nbsp;

</div>


## [Boot Up and Flash Test](http://127.0.0.1:8000/blog/boot-up-test/)

<!--suppress LongLine -->
<div class="post-extra">
    <div class="col">
        <p class="post-date">2024-10-28 12:00:00</p>
    </div>
    <div class="col">
    
        <a href="http://127.0.0.1:8000/blog/tags/example/">#example</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/programming/">#programming</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/flashing/">#flashing</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/boot/">#boot</a>
    
    </div>
</div>

Had some issues with Serial Monitor not working, and the device not being recognized, it was confusing to get down, but I solved those issues.

1. ERR light turns on during operation
    
    Apparently this is normal, ERR LED is connected to GPIO21, which is the Debug pin on the ESP32-S3. This means that it pulls low when it's in debug, and defaults high in regular mode (although this can be overridden in code [TESTED]).
    
    On our next revision, we should pull this pin active low, so that it turns on to signify bootloader mode. Speaking of bootloader mode... 
    
2. Board not recognized (not in Boot Mode)
    
    To get into Boot Mode, you have to hold down the BOOT button, press the RESET button momentarily (While still holding down BOOT), and then release the BOOT button.
    
    On Rev. 1 the ERR light will turn off if you did this successfully. 
    
    This may change the COM Port! Be sure to check in the IDE before flashing.
    
3. Serial Monitor not working
    
    There are a bunch of weird flash settings on Arduino that do not initialize correctly when you choose the board, and sometimes they reset when you open up the IDE after closing. 
    
    To fix this, make sure that these are your settings:
    
    ![[image1.png]]
    
    The big ones are 
    
    - Upload Mode: "UART0 / Hardware CDC"
    - USB Mode: "Hardware CDC and JTAG"
    - USB CDC On Boot: "Enabled"
    
    This should fix the errors with serial monitor.
    

Board works and boots using **Adafruit ESP32-S3 No PSRAM** Board.

Needs to have it's own Arduino Board file developed.



<div class="post-link">

    &nbsp;

</div>

