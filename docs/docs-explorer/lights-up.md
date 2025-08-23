---
title: Lights Up!
publish: true
date: 2025-01-27 12:00:00
update: 2025-01-27 12:00:00
description: Choose your lighting project
categories:
  - guide
hide:
  - toc
  - navigation
---

# Do you want to... 💡

*Choose the type of lighting project you want to build*

<style>
.project-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin: 2rem 0;
}

.project-card {
  background: #1a1f4d;
  border: 2px solid rgba(255,255,255,0.2);
  border-radius: 20px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  text-decoration: none;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: visible;
  min-height: 140px;
  height: auto;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  border-color: #00f0ff;
  border-width: 2px;
}

/* Top accent bars removed */

.project-card .icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  display: block;
  -webkit-text-stroke: 0.5px black;
  text-stroke: 0.5px black;
}

.project-card .title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: white;
}

.project-card .subtitle {
  font-size: 0.9rem;
  color: #e0e0e0;
  line-height: 1.4;
  opacity: 1;
  transform: translateY(0);
  transition: all 0.3s ease;
  margin-top: 0.5rem;
  padding: 0 0.5rem;
  text-align: center;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

/* Card colors */
/* Accent colors removed */

/* Inactive card styling */
.project-card.inactive {
  opacity: 0.4;
  filter: grayscale(0.8);
  cursor: not-allowed;
  pointer-events: none;
}

.project-card.inactive::after {
  content: 'Coming Soon';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0,0,0,0.8);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  z-index: 10;
}

.project-card.inactive:hover {
  transform: none;
  box-shadow: none;
  border-color: var(--md-default-fg-color--lightest);
}

@media (max-width: 768px) {
  .project-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<div class="project-grid">

<a href="../../core/blink-led" class="project-card card-basic">
  <span class="icon">💡</span>
  <div class="title">Turn lights on and off</div>
  <div class="subtitle">Basic LED control with GPIO</div>
</a>

<a href="#" class="project-card card-rgb inactive">
  <span class="icon">🌈</span>
  <div class="title">Use RGB LEDs</div>
  <div class="subtitle">Colorful lighting effects</div>
</a>

<a href="../../core/blink-led#part-2-pwm-control-dimming-and-brightening" class="project-card card-dimmer">
  <span class="icon">🔆</span>
  <div class="title">Adjust brightness of lights</div>
  <div class="subtitle">PWM dimming control</div>
</a>

<a href="../../advanced/ble" class="project-card card-phone">
  <span class="icon">📱</span>
  <div class="title">Control lights from my phone</div>
  <div class="subtitle">Wireless lighting control</div>
</a>

</div>

---

## 🚀 **Quick Start**

**New to tinyCore?** Start with [Setup](../../setup) to learn how to use the tinyCore.

**Want to see a complete project?** Try the [RGB Mood Light Tutorial](../../advanced/ble).

---

*Choose a lighting option above or [go back](index.md) to explore other project types!* 