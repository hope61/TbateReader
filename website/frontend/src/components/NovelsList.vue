<template>
  <div class="container my-4">
    <h2 class="novels-title">Explore Novels</h2>
    <div class="row">
      <div
        class="col-12 col-sm-6 col-lg-4 mb-4"
        v-for="novel in novels"
        :key="novel.id"
      >
        <router-link :to="`/novels/${novel.id}`" class="text-decoration-none">
          <div class="card h-100 novel-card">
            <div class="card-img-container">
              <img
                v-if="novel.image_url"
                :src="novel.image_url"
                :alt="novel.title.replace(/_/g, ' ')"
                class="card-img-top"
                loading="lazy"
              />
              <div v-else class="card-img-placeholder">
                <i class="fas fa-book-open"></i>
                <span>No Cover Image</span>
              </div>
              <div class="card-overlay">
                <span class="read-more">
                  <i class="fas fa-arrow-right me-1"></i>Read Now
                </span>
              </div>
            </div>
            <div class="card-body text-center">
              <h5 class="card-title">{{ novel.title.replace(/_/g, " ") }}</h5>
              <div class="novel-meta">
                <span class="novel-type">
                  <i class="fas fa-book me-1"></i>Novel
                </span>
              </div>
            </div>
          </div>
        </router-link>
      </div>
    </div>
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      novels: [],
      loading: true,
      error: null,
    };
  },
  mounted() {
    this.fetchNovels();
  },
  methods: {
    async fetchNovels() {
      try {
        const response = await axios.get("/api/novels");
        this.novels = response.data;
      } catch (error) {
        this.error = "Failed to load novels. Please try again later.";
        console.error("Error fetching novels:", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.novels-title {
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  margin-bottom: 2rem;
  text-align: center;
  background: linear-gradient(
    135deg,
    var(--text-primary) 0%,
    var(--accent-light) 50%,
    var(--accent) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
  text-shadow: 0 0 20px var(--accent-glow);
}

.novel-card {
  transition: var(--transition-slow);
  border: 1px solid var(--border);
  position: relative;
  overflow: hidden;
  background: linear-gradient(
    135deg,
    var(--surface) 0%,
    var(--surface-elevated) 100%
  );
  backdrop-filter: blur(10px);
}

.novel-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(139, 92, 246, 0.1),
    transparent
  );
  transition: left 0.5s;
}

.novel-card:hover::before {
  left: 100%;
}

.novel-card:hover {
  border-color: var(--accent);
  transform: translateY(-8px);
  box-shadow: var(--shadow-purple), var(--shadow-xl);
}

.card-img-container {
  position: relative;
  overflow: hidden;
}

.card-img-top {
  height: 200px;
  object-fit: cover;
  width: 100%;
  transition: var(--transition-slow);
}

.novel-card:hover .card-img-top {
  transform: scale(1.05);
}

.card-img-placeholder {
  height: 200px;
  background: linear-gradient(
    135deg,
    var(--surface) 0%,
    var(--surface-hover) 100%
  );
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 0.875rem;
  text-align: center;
  border-bottom: 1px solid var(--border);
}

.card-img-placeholder i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: var(--accent);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: var(--transition);
}

.novel-card:hover .card-overlay {
  opacity: 1;
}

.read-more {
  color: white;
  font-weight: 600;
  font-size: 1rem;
  padding: 0.75rem 1.5rem;
  border: 2px solid white;
  border-radius: var(--radius);
  transition: var(--transition);
}

.novel-card:hover .read-more {
  background: white;
  color: var(--accent);
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
  transition: var(--transition);
  line-height: 1.3;
}

.novel-card:hover .card-title {
  color: var(--accent);
}

.novel-meta {
  margin-top: 0.5rem;
}

.novel-type {
  background: linear-gradient(
    135deg,
    rgba(139, 92, 246, 0.1) 0%,
    rgba(139, 92, 246, 0.2) 100%
  );
  color: var(--accent);
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius);
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid var(--border-accent);
  backdrop-filter: blur(5px);
}

.card-body {
  padding: 1.5rem;
}

/* Mobile-specific styles */
@media (max-width: 768px) {
  .novels-title {
    font-size: 1.75rem;
    margin-bottom: 1.5rem;
  }

  .novel-card {
    margin-bottom: 1rem;
  }

  .card-img-top,
  .card-img-placeholder {
    height: 160px;
  }

  .card-body {
    padding: 1rem;
  }

  .card-title {
    font-size: 1rem;
  }

  .read-more {
    font-size: 0.875rem;
    padding: 0.5rem 1rem;
  }
}

@media (max-width: 480px) {
  .novels-title {
    font-size: 1.5rem;
    margin-bottom: 1.25rem;
  }

  .card-img-top,
  .card-img-placeholder {
    height: 140px;
  }

  .card-body {
    padding: 0.75rem;
  }

  .card-title {
    font-size: 0.9375rem;
  }

  .novel-type {
    font-size: 0.6875rem;
    padding: 0.1875rem 0.5rem;
  }

  .read-more {
    font-size: 0.8125rem;
    padding: 0.375rem 0.75rem;
  }
}

/* Focus styles for accessibility */
.novel-card:focus-within {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .novel-card {
    border: 2px solid var(--text-primary);
  }

  .novel-card:hover {
    border-color: var(--accent);
  }
}
</style>
