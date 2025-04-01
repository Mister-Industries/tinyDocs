---
publish: 'true'
search:
  exclude: true
slug: flashing
title: Tag - flashing

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

