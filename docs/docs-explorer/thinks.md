---
title: Thinks!
publish: true
date: 2025-01-27 12:00:00
update: 2025-01-27 12:00:00
description: Choose your AI/ML project
categories:
  - guide
hide:
  - toc
  - navigation
---

# Do you want to... 🧠

*Choose the type of AI/ML project you want to build*

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
.card-chatgpt { --card-color: #ff6b6b; }     /* Red */
.card-gemini { --card-color: #ff8e53; }       /* Orange */
.card-tinyml { --card-color: #ffb347; }       /* Light Orange */
.card-google { --card-color: #ffd700; }       /* Gold */
.card-alexa { --card-color: #32cd32; }        /* Lime Green */
.card-vision { --card-color: #00bfff; }       /* Deep Sky Blue */
.card-voice { --card-color: #9370db; }        /* Medium Purple */
.card-line { --card-color: #8a2be2; }         /* Blue Violet */

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

<a href="#" class="project-card card-chatgpt inactive">
  <span class="icon">🤖</span>
  <div class="title">Run ChatGPT models</div>
  <div class="subtitle">Large language models</div>
</a>

<a href="#" class="project-card card-gemini inactive">
  <span class="icon">🧠</span>
  <div class="title">Run Gemini models</div>
  <div class="subtitle">Google's AI models</div>
</a>

<a href="#" class="project-card card-tinyml inactive">
  <span class="icon">📱</span>
  <div class="title">Run tinyML models</div>
  <div class="subtitle">Edge AI and machine learning</div>
</a>

<a href="#" class="project-card card-google inactive">
  <span class="icon">🏠</span>
  <div class="title">Use Google Home</div>
  <div class="subtitle">Smart home integration</div>
</a>

<a href="#" class="project-card card-alexa inactive">
  <span class="icon">📢</span>
  <div class="title">Use Alexa</div>
  <div class="subtitle">Amazon voice assistant</div>
</a>

<a href="#" class="project-card card-vision inactive">
  <span class="icon">👁️</span>
  <div class="title">Computer vision</div>
  <div class="subtitle">Image recognition and processing</div>
</a>

<a href="#" class="project-card card-voice inactive">
  <span class="icon">🎤</span>
  <div class="title">Voice commands</div>
  <div class="subtitle">Speech recognition</div>
</a>

<a href="#" class="project-card card-line inactive">
  <span class="icon">🛤️</span>
  <div class="title">Line following</div>
  <div class="subtitle">Robot navigation</div>
</a>

</div>

---

*Choose an AI/ML option above or [go back](index.md) to explore other project types!* 