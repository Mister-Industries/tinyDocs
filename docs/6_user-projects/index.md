---
title: User Projects
publish: true
date: 2025-01-27 12:00:00
update: 2025-01-27 12:00:00
description: Amazing projects built by the tinyCore community
categories:
  - projects
hide:
  - toc
  - navigation
---

# Community Projects 👥

*Discover amazing projects built by the tinyCore community*

<style>
.project-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
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

.project-card .image {
  width: 100%;
  height: 200px;
  background: var(--md-default-fg-color--lightest);
  border-radius: 8px;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: var(--md-default-fg-color--light);
  overflow: hidden;
}

.project-card .image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
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
  margin-bottom: 1rem;
}

.project-card .author {
  font-size: 0.8rem;
  color: var(--md-default-fg-color--light);
  font-style: italic;
}

.instructables-badge {
  background: #ff6b35;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
  display: inline-block;
  margin-top: 0.5rem;
}

/* Card colors - Red through Purple */
.card-cyberjacket { --card-color: #ff6b6b; }      /* Red */
.card-openheg { --card-color: #ff8e53; }           /* Orange */
.card-messagebox { --card-color: #ffb347; }        /* Light Orange */
.card-motiontracker { --card-color: #ffd700; }     /* Gold */
.card-rgbmood { --card-color: #32cd32; }           /* Lime Green */
.card-musical { --card-color: #00bfff; }           /* Deep Sky Blue */
.card-robotcar { --card-color: #9370db; }          /* Medium Purple */
.card-gamecontroller { --card-color: #8a2be2; }    /* Blue Violet */
.card-plantmonitor { --card-color: #9932cc; }      /* Dark Orchid */
.card-smarthome { --card-color: #ff69b4; }         /* Hot Pink */
.card-meshnetsensor { --card-color: #20b2aa; }     /* Light Sea Green */
.card-weatherstation { --card-color: #6a5acd; }    /* Slate Blue */

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
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .project-grid {
    grid-template-columns: 1fr;
  }
}
</style>

---

<div class="project-grid">

<a href="https://www.instructables.com/CyberJacket/" target="_blank" class="project-card card-cyberjacket">
  <div class="image">
    <img src="index/cyberjacket.jpg" alt="CyberJacket - Smart jacket with LED matrix display">
  </div>
  <div class="title">CyberJacket</div>
  <div class="subtitle">A smart RGB LED jacket with Bluetooth phone controls</div>
  <div class="author">by @GalahadGear</div>
  <div class="instructables-badge">Instructables</div>
</a>

<a href="https://www.instructables.com/Inspiring-Kids-to-Learn-About-Neuroscience-How-I-M/" target="_blank" class="project-card card-openheg">
  <div class="image">
    <img src="index/openheg.jpg" alt="OpenHEG - DIY Brain Scanner project">
  </div>
  <div class="title">OpenHEG</div>
  <div class="subtitle">DIY Hemoencephalography device for brain-computer interface</div>
  <div class="author">by @FacioErgoSum</div>
  <div class="instructables-badge">Instructables</div>
</a>

<a href="https://www.instructables.com/-How-to-Make-a-Long-Distance-Message-Box-/" target="_blank" class="project-card card-messagebox">
  <div class="image">
    <img src="index/longdistance.jpg" alt="Long Distance Message Box - Wireless messaging system">
  </div>
  <div class="title">Long Distance Message Box</div>
  <div class="subtitle">Wireless messaging system for long distance relationships</div>
  <div class="author">by @FacioErgoSum</div>
  <div class="instructables-badge">Instructables</div>
</a>

</div>

---

## 🎯 **Example Projects**

*Tutorial projects to get you started*

<div class="project-grid">

<a href="../1_get-started/motion-tracker" class="project-card card-motiontracker">
  <div class="image">📊</div>
  <div class="title">Motion Activity Tracker</div>
  <div class="subtitle">Collects data + Moves</div>
  <div class="author">Official Tutorial</div>
</a>

<a href="../advanced/ble" class="project-card card-rgbmood inactive">
  <div class="image">🌈</div>
  <div class="title">RGB Mood Light</div>
  <div class="subtitle">Lights up + Connects to phone</div>
  <div class="author">Official Tutorial</div>
</a>

<a href="../advanced/I2S" class="project-card card-musical inactive">
  <div class="image">🎵</div>
  <div class="title">Musical Touch Pad</div>
  <div class="subtitle">Makes Sound + Responds to input</div>
  <div class="author">Official Tutorial</div>
</a>

<a href="../basics/gpio" class="project-card card-robotcar inactive">
  <div class="image">🤖</div>
  <div class="title">Mini Robot Car</div>
  <div class="subtitle">Moves + Responds to input</div>
  <div class="author">Official Tutorial</div>
</a>

<a href="../basics/gpio" class="project-card card-gamecontroller inactive">
  <div class="image">🎮</div>
  <div class="title">Interactive Game Controller</div>
  <div class="subtitle">Responds to input + Connects to phone</div>
  <div class="author">Official Tutorial</div>
</a>

<a href="../advanced/ai" class="project-card card-plantmonitor inactive">
  <div class="image">🧠</div>
  <div class="title">Smart Plant Monitor</div>
  <div class="subtitle">Thinks + Collects data + Connects to internet</div>
  <div class="author">Official Tutorial</div>
</a>

<a href="../advanced/ble" class="project-card card-smarthome inactive">
  <div class="image">🏠</div>
  <div class="title">Smart Home Hub</div>
  <div class="subtitle">Connects to phone + Connects to internet + Lights up</div>
  <div class="author">Official Tutorial</div>
</a>

<a href="../advanced/esp-now" class="project-card card-meshnetsensor inactive">
  <div class="image">🔗</div>
  <div class="title">Mesh Network Sensor</div>
  <div class="subtitle">Connects to another tinyCore + Collects data</div>
  <div class="author">Official Tutorial</div>
</a>

<a href="../advanced/wifi" class="project-card card-weatherstation inactive">
  <div class="image">🌐</div>
  <div class="title">Weather Station</div>
  <div class="subtitle">Connects to internet + Collects data + Responds to input</div>
  <div class="author">Official Tutorial</div>
</a>

</div>

---

## 💡 **Share Your Project**

**Have you built something cool with tinyCore?** We'd love to feature it here!

**Submit your project:**

1. Share on [Instructables](https://www.instructables.com/) and tag it with #tinyCore

2. Post in our [Discord community](https://discord.gg/hvJZhwfQsF)

3. Email us at projects@tinycore.com

**What we're looking for:**

- Clear documentation and photos

- Open source code (and hardware when possible)

- Creative and innovative uses of tinyCore

- Projects that inspire others to build

---

*Ready to build something amazing? Check out our [Get Started](../get-started/) page!*
