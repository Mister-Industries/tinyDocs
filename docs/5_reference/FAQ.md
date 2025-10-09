# Frequently Asked Questions

## How do I use 5V? 

We do not recommend using 5V with this board.

The ESP32-S3 is a 3.3V native chip, so there is no 5V supply on the board and the GPIO is rated for 3.3V. However, the USB-C input is rated for up to 6V. We are revising the board to include a breakout pin for this VBUS, which will support 5V (input only). Until then, this pin is currently available as a testpoint next to the Battery Plug.

## What size battery can I use?

As long as the battery has the correct polarity (check the board for +/- labeling), you can connect any capacity (mAh) of 3.7v LiPo/Li-ion batteries. These batteries charge up to 4.2V, which is supported by our Battery Management IC.

## Can I add more than two QWIIC devices?

Yes, you can daisy chain many more I2C devices, as long as they have a pass-through on the board. You can also get QWIIC splitters, such as [this one](https://www.digikey.com/en/products/detail/sparkfun-electronics/18012/13998109) from Sparkfun, to add more devices.

## Do you support MicroPython, PlatformIO, and ESP-IDF?

In theory, the ESP32-S3 is compatible with all of these systems, however we have not completed development on the custom library packages for these platforms. Our recommendation is to use the libraries for Adafruit's ESP32-S3 Feather as a starting point, since it has a similar pinout architecture as our board (minus the IMU and SD Card). We appreciate development contributions from the community, so please let us know what you find!

## What if I run out of digital/analog GPIO?

Although we have intentionally labeled the board to default to 6 Analog and 6 Digital input/outputs, ALL of the pins on the ESP32-S3 can be repurposed as analog OR digital pins. However, this functionality is confusing to beginners, and it comes with some caveats. The first is that there are two ADC channels on the board, one of which is dedicated to the Analog pins, and the other which is dedicated to the Digital pins AND Wi-Fi. If you are using Wi-Fi, the digital pins will be very noisy in analog sampling mode. This similarly applies to the Serial pins. Most of these pins are in use by either the I2C bus, or the SD Card, so you may have some loss in functionality if you try to overwrite their default uses. But if you aren't using the SD Card, feel free to use the SCK, MOSI, MISO pins!

## How big can the SD Card be?

The standard formatting for the SD Card is FAT32, which implies a limit in size at 32GB, this is confirmed by the SD Card Library, however we have been able to successfully use 128GB SD Cards (although we have not tried to fill the entire SD Card with information, so this may still cap at 32GB).

I'd recommend sticking to a 32GB Card, with 4GB as the maximum individual file size. Your mileage may vary!