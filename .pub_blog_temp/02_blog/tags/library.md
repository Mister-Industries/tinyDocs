---
publish: 'true'
search:
  exclude: true
slug: library
title: Tag - library

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

