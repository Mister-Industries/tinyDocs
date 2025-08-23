---
title: Responds to Input!
publish: true
date: 2025-01-27 12:00:00
update: 2025-01-27 12:00:00
description: Choose your input project
categories:
  - guide
hide:
  - toc
  - navigation
---

# Do you want to... 🎮

*Choose the type of input project you want to build*

<style>
.project-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin: 2rem 0;
}

.project-card {
  background: var(--md-default-bg-color);
  border: 2px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
  display: block;
  position: relative;
  overflow: hidden;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  border-color: var(--md-primary-fg-color);
}

.project-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--card-color, #666);
}

.project-card .icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.project-card .title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--md-default-fg-color);
}

.project-card .subtitle {
  font-size: 0.9rem;
  color: var(--md-default-fg-color--light);
  line-height: 1.4;
}

/* Card colors */
.card-keyboard { --card-color: #ff6b6b; }     /* Red */
.card-mouse { --card-color: #ff8e53; }         /* Orange */
.card-game { --card-color: #ffb347; }          /* Light Orange */
.card-buttons { --card-color: #ffd700; }       /* Gold */
.card-wireless { --card-color: #32cd32; }      /* Lime Green */

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

<a href="#" class="project-card card-keyboard inactive">
  <span class="icon">⌨️🖱️</span>
  <div class="title">Keyboard/Mouse</div>
  <div class="subtitle">USB HID device</div>
</a>

<a href="#" class="project-card card-mouse inactive">
  <span class="icon">🎮</span>
  <div class="title">Game Controller</div>
  <div class="subtitle">Custom gamepad</div>
</a>

<a href="#" class="project-card card-buttons inactive">
  <span class="icon">🔘</span>
  <div class="title">Physical buttons</div>
  <div class="subtitle">Switches and tactile inputs</div>
</a>

<a href="../../advanced/ble" class="project-card card-wireless">
  <span class="icon">📱</span>
  <div class="title">Wireless controller</div>
  <div class="subtitle">Bluetooth input device</div>
</a>

</div>

---

## 🚀 **Quick Start**

**New to tinyCore?** Start with [GPIO Basics](../../basics/gpio) to learn how to read buttons.

**Want to create USB devices?** Check out [HID Basics](../../advanced/hid) for keyboard/mouse functionality.

**Want to see a complete project?** Try the [Interactive Game Controller Tutorial](../../advanced/ble).

---

*Choose an input option above or [go back](index.md) to explore other project types!* 