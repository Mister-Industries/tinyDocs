---
title: Project Explorer
publish: true
date: 2025-01-27 12:00:00
update: 2025-01-27 12:00:00
description: Interactive guide to find the right tinyCore documentation for your project
categories:
  - guide
hide:
  - toc
  - navigation
---

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 2rem;">
  <a href="../../1_get-started/" class="project-card" style="
    width: 1026px;
    height: 296px;
    padding: 2rem;
    margin: 0;
    text-decoration: none;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: #1a1f4d;
    border: 2px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    color: white;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  " onmouseover="this.style.transform='translateY(-4px)'; this.style.borderColor='#00f0ff'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.15)'; this.querySelector('.rocket-icon').style.filter='drop-shadow(0 0 20px rgba(255, 255, 255, 0.6))'" 
     onmouseout="this.style.transform='translateY(0)'; this.style.borderColor='rgba(255,255,255,0.2)'; this.style.boxShadow='none'; this.querySelector('.rocket-icon').style.filter='none'">
    <span class="rocket-icon" style="font-size: 3.5rem; margin-bottom: 0.75rem; color: white; -webkit-text-stroke: 0.5px black; text-stroke: 0.5px black; transition: all 0.3s ease;"><i class="fas fa-rocket"></i></span>
    <div style="font-size: 1.4rem; font-weight: 600; margin-bottom: 0.5rem; color: white; width: 60%; text-align: center;">New to tinyCore?</div>
    <div style="font-size: 1rem; color: #e0e0e0; text-align: center; width: 60%;">Start here</div>
  </a>
</div>

<div style="text-align: center; margin: 0.2rem 0 0 0;">
  <h1 style="color: white;">I want to build something that...</h1>
</div>

<style>
.project-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
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
  width: 350px;
  height: auto;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  border-color: #00f0ff;
  border-width: 2px;
}

/* Individual glow colors for each icon */
.project-card:hover .icon-red {
  filter: drop-shadow(0 0 20px rgba(231, 76, 60, 0.6));
}

.project-card:hover .icon-orange {
  filter: drop-shadow(0 0 20px rgba(243, 156, 18, 0.6));
}

.project-card:hover .icon-yellow {
  filter: drop-shadow(0 0 20px rgba(241, 196, 15, 0.6));
}

.project-card:hover .icon-green {
  filter: drop-shadow(0 0 20px rgba(39, 174, 96, 0.6));
}

.project-card:hover .icon-blue {
  filter: drop-shadow(0 0 20px rgba(52, 152, 219, 0.6));
}

.project-card:hover .icon-indigo {
  filter: drop-shadow(0 0 20px rgba(64, 0, 255, 0.6));
}

.project-card:hover .icon-violet {
  filter: drop-shadow(0 0 20px rgba(168, 85, 247, 0.6));
}

.project-card:hover .icon-pink {
  filter: drop-shadow(0 0 20px rgba(233, 30, 99, 0.6));
}

.project-card:hover .icon-cyan {
  filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.6));
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

.project-card:hover .subtitle {
  opacity: 1;
  transform: translateY(0);
  max-height: none;
}

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
  border-color: rgba(255,255,255,0.2);
}

/* Rainbow icon colors */
.icon-red { color: #e74c3c; }
.icon-orange { color: #f39c12; }
.icon-yellow { color: #f1c40f; }
.icon-green { color: #27ae60; }
.icon-blue { color: #3498db; }
.icon-indigo { color: #4000ff; }
.icon-violet { color: #a855f7; }
.icon-pink { color: #e91e63; }
.icon-cyan { color: #00ffff; }

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

<div class="project-grid">

<a href="lights-up" class="project-card">
  <span class="icon icon-red"><i class="fas fa-lightbulb"></i></span>
  <div class="title">Lights up!</div>
  <div class="subtitle">I want beautiful lighting effects</div>
</a>

<a href="makes-sound" class="project-card">
  <span class="icon icon-orange"><i class="fas fa-music"></i></span>
  <div class="title">Makes Sound!</div>
  <div class="subtitle">I want to create audio and music</div>
</a>

<a href="moves" class="project-card">
  <span class="icon icon-yellow"><i class="fas fa-robot"></i></span>
  <div class="title">Moves!</div>
  <div class="subtitle">I want to sense movement and control motors</div>
</a>

<a href="collects-data" class="project-card">
  <span class="icon icon-green"><i class="fas fa-chart-line"></i></span>
  <div class="title">Collects data!</div>
  <div class="subtitle">I want to measure and record information</div>
</a>

<a href="responds-to-input" class="project-card">
  <span class="icon icon-blue"><i class="fas fa-gamepad"></i></span>
  <div class="title">Responds to input!</div>
  <div class="subtitle">I want interactive controls</div>
</a>

<a href="thinks" class="project-card">
  <span class="icon icon-indigo"><i class="fas fa-brain"></i></span>
  <div class="title">Thinks!</div>
  <div class="subtitle">I want AI and machine learning</div>
</a>

<a href="../../2_tiny-core/advanced/dabble-app" class="project-card">
  <span class="icon icon-violet"><i class="fas fa-mobile-alt"></i></span>
  <div class="title">Connects to my phone!</div>
  <div class="subtitle">I want wireless communication</div>
</a>

<a href="../../2_tiny-core/basics/link-tiny-cores" class="project-card">
  <span class="icon icon-pink"><i class="fas fa-link"></i></span>
  <div class="title">Connects to another tinyCore!</div>
  <div class="subtitle">I want device-to-device communication</div>
</a>

<a href="../../2_tiny-core/basics/wifi" class="project-card">
  <span class="icon icon-cyan"><i class="fas fa-wifi"></i></span>
  <div class="title">Connects to the internet!</div>
  <div class="subtitle">I want web connectivity</div>
</a>

</div>

---

## 🛠️ **Getting Started & Learning Paths**

<div class="project-grid">

<a href="../../1_get-started/" class="project-card">
  <span class="icon icon-red"><i class="fas fa-tools"></i></span>
  <div class="title">Setup Guide</div>
  <div class="subtitle">I need to set up my tinyCore first</div>
</a>

<a href="../../2_tiny-core/basics" class="project-card">
  <span class="icon icon-orange"><i class="fas fa-book"></i></span>
  <div class="title">Learn Basics</div>
  <div class="subtitle">I want to understand the fundamentals</div>
</a>

<a href="../../2_tiny-core/advanced" class="project-card">
  <span class="icon icon-yellow"><i class="fas fa-bolt"></i></span>
  <div class="title">Advanced Features</div>
  <div class="subtitle">I want to explore advanced capabilities</div>
</a>

</div>

---

## 🎯 **Example Project Tutorials**

<div class="project-grid">

<a href="../../1_get-started/motion-tracker" class="project-card">
  <span class="icon icon-green"><i class="fas fa-chart-line"></i></span>
  <div class="title">Motion Activity Tracker</div>
  <div class="subtitle">Collects data + Moves</div>
</a>

<a href="../../2_tiny-core/advanced/bluetooth" class="project-card inactive">
  <span class="icon icon-blue"><i class="fas fa-lightbulb"></i></span>
  <div class="title">RGB Mood Light</div>
  <div class="subtitle">Lights up + Connects to phone</div>
</a>

<a href="../../2_tiny-core/advanced/midi-instrument" class="project-card inactive">
  <span class="icon icon-indigo"><i class="fas fa-music"></i></span>
  <div class="title">Musical Touch Pad</div>
  <div class="subtitle">Makes Sound + Responds to input</div>
</a>

<a href="../../2_tiny-core/basics/button-press" class="project-card inactive">
  <span class="icon icon-violet"><i class="fas fa-robot"></i></span>
  <div class="title">Mini Robot Car</div>
  <div class="subtitle">Moves + Responds to input</div>
</a>

<a href="../../2_tiny-core/basics/button-press" class="project-card inactive">
  <span class="icon icon-pink"><i class="fas fa-gamepad"></i></span>
  <div class="title">Interactive Game Controller</div>
  <div class="subtitle">Responds to input + Connects to phone</div>
</a>

<a href="../../2_tiny-core/advanced/tinyML" class="project-card inactive">
  <span class="icon icon-cyan"><i class="fas fa-brain"></i></span>
  <div class="title">Smart Plant Monitor</div>
  <div class="subtitle">Thinks + Collects data + Connects to internet</div>
</a>

<a href="../../2_tiny-core/advanced/bluetooth" class="project-card inactive">
  <span class="icon icon-red"><i class="fas fa-home"></i></span>
  <div class="title">Smart Home Hub</div>
  <div class="subtitle">Connects to phone + Connects to internet + Lights up</div>
</a>

<a href="../../2_tiny-core/basics/esp-now" class="project-card inactive">
  <span class="icon icon-orange"><i class="fas fa-network-wired"></i></span>
  <div class="title">Mesh Network Sensor</div>
  <div class="subtitle">Connects to another tinyCore + Collects data</div>
</a>

<a href="../../2_tiny-core/basics/wifi" class="project-card inactive">
  <span class="icon icon-yellow"><i class="fas fa-cloud-sun"></i></span>
  <div class="title">Weather Station</div>
  <div class="subtitle">Connects to internet + Collects data + Responds to input</div>
</a>

</div>



---

## 💡 **Still not sure?**

**Take our quick quiz!** (Coming soon)

**Need help?** Join our [Discord community](https://discord.gg/hvJZhwfQsF) for personalized guidance!

---