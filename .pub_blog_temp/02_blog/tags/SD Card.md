---
publish: 'true'
search:
  exclude: true
slug: sd-card
title: Tag - SD Card

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


## [SD Card Test](http://127.0.0.1:8000/blog/2024-11-23-12:05/)

<!--suppress LongLine -->
<div class="post-extra">
    <div class="col">
        <p class="post-date">2024-11-23 12:05:00</p>
    </div>
    <div class="col">
    
        <a href="http://127.0.0.1:8000/blog/tags/testing/">#testing</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/example/">#example</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/code/">#code</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/SD Card/">#SD Card</a>
    
        <a href="http://127.0.0.1:8000/blog/tags/IMU/">#IMU</a>
    
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

