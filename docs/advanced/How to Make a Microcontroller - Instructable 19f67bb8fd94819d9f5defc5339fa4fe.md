# How to Make a Microcontroller - Instructable

Created: February 18, 2025 10:25 PM

Background:

Ever since I was a small child, I've wanted to develop the skills necessary to design my own circuit boards. I didn't really know how they worked or what was going on, but I knew they were cool. 7 years later, as a senior in electrical engineering, I finally have those tools and I'd like to share some of them with you. 

If you've ever wanted to make your own Arduino, done lots of solderless breadboarding, and want to create something more professional, maybe even your own product, this tutorial is for you. 

What is a microcontroller? 

First we should actually go over what a microcontroller is. Most people know about circuit boards but they don't understand how they work. Microcontrollers are the brains of these boards. They are the tiny logic modules that contain useful built in functions, like analog voltage measurements (inputs and outputs) and serial communication, not to be confused with cereal communication, when you cry into your froot loops, although if you get into Engineering this may be a more common occurrence than you'd like.

Serial communication is how two different circuits talk to each other. There are tons of different protocols, wiring configurations, etc, but essentially it's the external language your microcontroller can use to communicate with other chips. This could be I2C (usually pronounced Eye-squared-see) SPI (pronounced “Spy”) UART or CAN. 

You can learn all about serial communication in this Instructable.

Overall, these microchips are extremely useful, however they are usually small, hard to use with a breadboard, and require what we call a “breakout” board. If we connect a chip, some useful peripherals, and breakout pins onto one PCB, we call this a “microcontroller”. Everything you need to control and take basic digital/analog measurements on one board