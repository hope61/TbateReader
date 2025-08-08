<template>
  <div class="container my-5">
    <div class="roadmap-header">
      <h1>Feature Roadmap</h1>
      <p class="lead">
        See what's coming next and track our development progress
      </p>
    </div>

    <div class="roadmap-grid">
      <!-- Coming Soon -->
      <div class="roadmap-section">
        <h2 class="section-title coming-soon">
          <i class="fas fa-rocket"></i>
          Coming Soon
        </h2>
        <div class="feature-cards">
          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-headphones"></i>
            </div>
            <div class="feature-content">
              <h3>Audio Book Reader</h3>
              <p>
                Listen to chapters with high-quality text-to-speech narration.
                Perfect for hands-free reading during commutes or workouts.
              </p>
              <div class="feature-tags">
                <span class="tag">Audio</span>
                <span class="tag">Accessibility</span>
              </div>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-robot"></i>
            </div>
            <div class="feature-content">
              <h3>AI-Generated Audio Chapters</h3>
              <p>
                For novels with incomplete releases, AI will generate audio
                narration for unreleased chapters using text-to-speech
                technology.
              </p>
              <div class="feature-tags">
                <span class="tag">AI</span>
                <span class="tag">Audio</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- In Progress -->
      <div class="roadmap-section">
        <h2 class="section-title in-progress">
          <i class="fas fa-cogs"></i>
          In Progress
        </h2>
        <div class="feature-cards">
          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-heading"></i>
            </div>
            <div class="feature-content">
              <h3>Chapter Titles</h3>
              <p>
                Adding descriptive titles to each chapter to make navigation
                easier and provide better context for readers.
              </p>
              <div class="feature-tags">
                <span class="tag">Navigation</span>
                <span class="tag">UX</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Planned -->
      <div class="roadmap-section">
        <h2 class="section-title planned">
          <i class="fas fa-lightbulb"></i>
          Planned Features
        </h2>
        <div class="feature-cards">
          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-bookmark"></i>
            </div>
            <div class="feature-content">
              <h3>Reading Progress</h3>
              <p>
                Track your reading progress, bookmark favorite chapters, and
                resume where you left off across devices.
              </p>
              <div class="feature-tags">
                <span class="tag">Progress</span>
                <span class="tag">Sync</span>
              </div>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="fas fa-users"></i>
            </div>
            <div class="feature-content">
              <h3>Community Features</h3>
              <p>
                Discuss chapters, share theories, and connect with other readers
                through comments and forums.
              </p>
              <div class="feature-tags">
                <span class="tag">Social</span>
                <span class="tag">Community</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="roadmap-footer">
      <div class="cta-section">
        <h3>Have a Feature Request or Novel Suggestion?</h3>
        <p>
          Join our Discord community to submit feature requests and suggest new
          novels!
        </p>
        <a href="https://discord.gg/vYJQwqAaWE" class="btn btn-primary">
          <i class="fab fa-discord me-2"></i>Join Discord
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Roadmap",
};
</script>

<style scoped>
.roadmap-header {
  text-align: center;
  margin-bottom: 3rem;
}

.roadmap-header h1 {
  background: linear-gradient(
    135deg,
    var(--text-primary) 0%,
    var(--accent-light) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
}

.roadmap-header .lead {
  color: var(--text-secondary);
  font-size: 1.125rem;
  max-width: 600px;
  margin: 0 auto;
}

.roadmap-grid {
  display: grid;
  gap: 3rem;
  margin-bottom: 4rem;
}

.roadmap-section {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 2rem;
  box-shadow: var(--shadow-lg);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 2rem;
  font-size: 1.5rem;
  font-weight: 600;
  /* Neutralize global h2 gradient */
  background: none !important;
  -webkit-background-clip: initial !important;
  background-clip: initial !important;
  -webkit-text-fill-color: currentColor !important;
}

/* Ensure the icon inherits the intended color */
.section-title i {
  font-size: 1.25rem;
  color: currentColor !important;
}

.section-title.coming-soon {
  color: #f59e0b !important;
}

.section-title.in-progress {
  color: #3b82f6 !important;
}

.section-title.planned {
  color: var(--accent) !important;
}

.feature-cards {
  display: grid;
  gap: 1.5rem;
}

.feature-card {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  background: var(--surface-hover);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  transition: var(--transition-slow);
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  border-color: var(--accent);
}

.feature-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(
    135deg,
    var(--accent) 0%,
    var(--accent-hover) 100%
  );
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  flex-shrink: 0;
}

.feature-content {
  flex: 1;
}

.feature-content h3 {
  margin-bottom: 0.75rem;
  color: var(--text-primary);
  font-size: 1.25rem;
}

.feature-content p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1rem;
}

.feature-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  background: rgba(139, 92, 246, 0.1);
  color: var(--accent);
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius);
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.roadmap-footer {
  text-align: center;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 3rem 2rem;
  box-shadow: var(--shadow-lg);
}

.cta-section h3 {
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.cta-section p {
  color: var(--text-secondary);
  margin-bottom: 2rem;
  font-size: 1.125rem;
}

@media (max-width: 768px) {
  .roadmap-section {
    padding: 1.5rem;
  }

  .feature-card {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .feature-icon {
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
    margin: 0 auto;
  }

  .roadmap-footer {
    padding: 2rem 1.5rem;
  }
}

@media (max-width: 480px) {
  .roadmap-header {
    margin-bottom: 2rem;
  }

  .roadmap-section {
    padding: 1rem;
  }

  .feature-card {
    padding: 1rem;
  }

  .feature-content h3 {
    font-size: 1.125rem;
  }

  .roadmap-footer {
    padding: 1.5rem 1rem;
  }
}
</style>
