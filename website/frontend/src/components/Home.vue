<template>
  <div>
    <div class="hero">
      <h1>Mana's Embrace</h1>
      <div class="hero-subtitle">
        <span class="subtitle-text">Where stories come alive</span>
      </div>
    </div>

    <!-- Featured Section -->
    <div class="featured-section">
      <div class="container">
        <div class="featured-content">
          <div class="featured-text">
            <h2>Discover Epic Tales</h2>
            <p>
              Immerse yourself in captivating stories with our carefully curated
              collection of novels. From fantasy adventures to epic journeys,
              find your next favorite read.
            </p>
            <div class="featured-stats">
              <div class="stat">
                <span class="stat-number">4</span>
                <span class="stat-label">Novel Available</span>
              </div>
              <div class="stat">
                <span class="stat-number">4000+</span>
                <span class="stat-label">Chapters</span>
              </div>
            </div>
          </div>
          <div class="featured-visual">
            <div class="floating-elements">
              <div class="floating-element">📚</div>
              <div class="floating-element">✨</div>
              <div class="floating-element">🌟</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Audio Book Notice -->
    <div class="audio-notice">
      <div class="container">
        <div class="notice-content">
          <div class="notice-icon">
            <i class="fas fa-headphones"></i>
          </div>
          <div class="notice-text">
            <h3>🎧 Audiobooks Wanted!</h3>
            <p>
              We're actively searching for audiobooks for our available novels! 
              If you have access to official or high-quality audiobooks for any of these series, 
              please join our <strong>Discord server</strong> and message us about it.
            </p>
            <div class="novels-wanted">
              <div class="wanted-novel">
                <span class="novel-icon">📚</span>
                <strong>TBATE</strong> (The Beginning After The End)
              </div>
              <div class="wanted-novel">
                <span class="novel-icon">🌙</span>
                <strong>Shadow Slave</strong>
              </div>
              <div class="wanted-novel">
                <span class="novel-icon">🔮</span>
                <strong>Lord Of The Mysteries</strong>
              </div>
              <div class="wanted-novel">
                <span class="novel-icon">⚙️</span>
                <strong>86 - Eighty Six</strong>
              </div>
            </div>
            <div class="notice-highlight">
              <span class="highlight-icon">🤖</span>
              <span class="highlight-text">
                <strong>Currently Available:</strong> AI-generated TBATE Volume 12
                audiobook (unreleased chapters)
              </span>
            </div>
            <div class="discord-cta">
              <a
                href="https://discord.gg/vYJQwqAaWE"
                class="btn btn-primary discord-btn"
              >
                <i class="fab fa-discord"></i>
                Join Our Discord
              </a>
              <span class="discord-note"
                >Message us about any audiobooks!</span
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <NovelsList />
    <Roadmap />
  </div>
</template>

<script>
import NovelsList from "./NovelsList.vue";
import Roadmap from "./Roadmap.vue";

export default {
  components: {
    NovelsList,
    Roadmap,
  },
};
</script>
