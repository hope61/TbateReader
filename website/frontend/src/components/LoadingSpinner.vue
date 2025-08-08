<template>
  <div class="loading-overlay" v-if="loading">
    <div class="loading-content">
      <div class="loading-logo">
        <picture>
          <source srcset="../assets/minicaera.webp" type="image/webp">
          <img src="../assets/minicaera.png" alt="Loading" width="60" height="60" />
        </picture>
      </div>
      <div class="loading-text">
        <h3>Mana's Embrace</h3>
        <p>Loading your stories...</p>
      </div>
      <div class="loading-bar">
        <div class="loading-progress"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    loading: {
      type: Boolean,
      default: true
    }
  }
}
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 25%, #2d2d4d 50%, #1a1a2e 75%, #0a0a0f 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease-out;
}

.loading-content {
  text-align: center;
  max-width: 300px;
}

.loading-logo {
  margin-bottom: 1.5rem;
  animation: pulse 2s infinite;
}

.loading-logo img {
  border-radius: 50%;
  filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.5));
}

.loading-text h3 {
  color: #ffffff;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.loading-text p {
  color: #c7c7d8;
  font-size: 1rem;
  margin-bottom: 2rem;
}

.loading-bar {
  width: 100%;
  height: 4px;
  background: rgba(139, 92, 246, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.loading-progress {
  height: 100%;
  background: linear-gradient(90deg, #8b5cf6, #a78bfa, #8b5cf6);
  background-size: 200% 100%;
  animation: loading-progress 1.5s infinite;
  border-radius: 2px;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes loading-progress {
  0% { 
    width: 0%;
    background-position: 200% 0;
  }
  50% {
    width: 70%;
  }
  100% { 
    width: 100%;
    background-position: -200% 0;
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
