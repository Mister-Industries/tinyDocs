---
title: "Devlog #2: Boards Arrive & First Fulfillment!"
slug: devlog-2
publish: true
date: 2025-02-23
authors: 
  - macgeoffrey
description: "Devlog #2"
categories:
  - Devlog
tags:
  - orders
  - fulfillment
  - PCB
  - design
  - marketing
  - expansions
  - Devlog
hide:
  - toc
  - navigation
---

**A lot has happened in the last month! As an overview we've:**

- Ordered, received, and tested our Rev. 2 boards
- Changed our name from **iotaCore** to **tinyCore**!
- Started flyering/marketing around CU campus
- Partnered with a wearable technologies course at CU to get hands-on beta-testing & feedback
- Published [our website](http://mr.industries) and setup online payments
- **Fulfilled our first orders!!**

<!-- more -->

**tinyCore Updates:**

Revision 2 arrived in the mail with a slight delay from the Lunar New Year on Feb 18th!

We immediately unboxed them for initial inspection, and they look ***sharp***. 

![IMG_20250218_172607_695.jpg](devlog-2/IMG_20250218_172607_695.jpg)

![IMG_20250218_172557_319 copy.jpg](devlog-2/IMG_20250218_172557_319_copy.jpg)

So far we've tested over half of the boards, and no issues have been found. Here's our basic testing procedure:

**Testing Procedure:**

- Connect to PC via USB (Should be recognized as generic ESP32 device, and will be connecting & disconnecting). PWR LED should be on, Charging should be flashing.
- Hold down BOOT, RST, BOOT sequence. Device will stop disconnecting.
- Flash Blink Example (SIG LED should begin blinking)
- 3V3 and PWR pins are >2.9V
- Plug in LiPo, CHG goes solid.
- Battery pins are >4.00V
- Analog and Digital Pins should all be floating around the same value 10-50mV.
- Confirm device still runs on Battery Power once USB is removed.

After this is complete, orders were placed in plastic boxes, with enclosure, USB-C cables, 8pin and 9pin headers, nuts/bolts, and a BOM:

![IMG_2425.JPG](devlog-2/IMG_2425.jpg)

![image.png](devlog-2/image11.png)

![IMG_2418.JPG](devlog-2/IMG_2418.jpg)

Then we put labels on the boxes and wrapped them for delivery!

![IMG_20250219_002816_322.jpg](devlog-2/43e9603a-8b88-451d-8ab5-45c5be8ce2d4.png)

Kits were fulfilled the next day! (Note: still need to get some photos of the happy customers!)

**Enclosure Updates:**

We've done a bunch of testing and revision to the board enclosures in prep for Revision 2 and our first fulfillment. From our last enclosure we have:

- Improve the overall tolerances and fit
- Added snap tabs to prevent unintentional opening
- Added M3 Heat-inset Nuts and Machine Bolts
- Tried out a wide variety of new colors and configurations
- Added the new multi-color tinyCore logo!
- Slightly increased the wall thickness

You can see how these revisions turned out:

![tinyCore-store-1.jpg](devlog-2/tinyCore-store-1.jpg)

![tinyCore-store-2.jpg](devlog-2/tinyCore-store-2.jpg)

![tinyCore-store-6.jpg](devlog-2/tinyCore-store-6.jpg)

![IMG_2439.JPG](devlog-2/5da02b4b-26ff-4d94-8f46-34d1b2ad6d27.png)

So far we have colors in Red, Yellow, Green, Blue, Purple, Black, Grey, and White!

![image.png](devlog-2/79004a16-4446-4bd2-ac19-3e32ae247351.png)

And, the enclosures still fit with our Expansion module prototypes:

![WatchImage-2.jpg](devlog-2/c3f84132-d6b2-44f6-b5e2-2793f9ab2bba.png)

**For a future enclosure revision, I'd still like to:**

- Add SD Card accessibility
- Finish adding Buttons (TPU)
- Add TPU "Rubber" feet
- Experiment with using clear filament for light-pipes.

**Outside of these updates...**

We've got our flyers which we have been sharing around campus:

![image.png](devlog-2/image12.png)

And, we've already had people commenting that they've seen the posters, plus we've had quite a lot of QR Code scans so far!

We've also been rapidly working on our other expansion board prototypes, and we now have working versions of the tinySniff, tinyDisplay, tinyVoice, tinyGlow, and tinyProto, in various development stages:

<div class="grid cards" markdown>

- ![tinySniff.png](devlog-2/tinySniff.png)

- ![tinyProto.png](devlog-2/tinyProto.png)

- ![tinyDisplay.png](devlog-2/tinyDisplay.png)

- ![tinyGlow.png](devlog-2/tinyGlow.png)

- ![tinyVoice.png](devlog-2/tinyVoice.png)

</div>

That's about it for this monthly update, but as a teaser for what's to come, we're excited to announce we're officially started on the 

**Road to Kickstarter**.