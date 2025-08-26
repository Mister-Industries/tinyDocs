---
title: Makes Sound!
publish: true
date: 2025-01-27 12:00:00
update: 2025-01-27 12:00:00
description: Choose your audio project
categories:
  - guide
hide:
  - toc
  - navigation
---

# Do you want to... 🎵

*Choose the type of audio project you want to build*

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

<a href="#" class="project-card card-record inactive">
  <span class="icon">🎤</span>
  <div class="title">Record audio</div>
  <div class="subtitle">Capture sound with microphone</div>
</a>

<a href="#" class="project-card card-playback inactive">
  <span class="icon">🔊</span>
  <div class="title">Playback audio</div>
  <div class="subtitle">Play sounds and music</div>
</a>

<a href="#" class="project-card card-sample inactive">
  <span class="icon">🎛️</span>
  <div class="title">Sample audio</div>
  <div class="subtitle">Real-time audio processing</div>
</a>

<a href="../../2_tiny-core/basics/save-data-to-sdcard" class="project-card card-save">
  <span class="icon">💾</span>
  <div class="title">Save audio</div>
  <div class="subtitle">Store audio files on SD card</div>
</a>

<a href="#" class="project-card card-music inactive">
  <span class="icon">🎼</span>
  <div class="title">Play music</div>
  <div class="subtitle">Generate tones and melodies</div>
</a>

<a href="#" class="project-card card-midi inactive">
  <span class="icon">🎹</span>
  <div class="title">Be an instrument (MIDI)</div>
  <div class="subtitle">Create musical controllers</div>
</a>

</div>

---

## 🚀 **Quick Start**

**New to tinyCore?** Start with [SD Card Basics](../../2_tiny-core/basics/save-data-to-sdcard) to learn how to store data.

**Want to see a complete project?** Try the [Musical Touch Pad Tutorial](../../2_tiny-core/advanced/midi-instrument).

---

*Choose an audio option above or [go back](index.md) to explore other project types!* 