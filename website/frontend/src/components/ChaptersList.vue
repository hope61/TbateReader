<template>
  <div class="container my-4">
    <!-- Novel Header -->
    <div class="novel-header">
      <div class="novel-info-container">
        <img
          v-if="novelImage"
          :src="novelImage"
          :alt="novelTitle.replace(/_/g, ' ')"
          class="novel-image"
          loading="lazy"
        />
        <div v-else class="novel-image-placeholder">No Cover Image</div>
        <div class="novel-details">
          <h2 class="novel-title">
            Chapters of {{ novelTitle.replace(/_/g, " ") }}
          </h2>
          <p class="novel-subtitle">{{ chapters.length }} chapters available</p>
        </div>
      </div>
    </div>

    <div class="back-button-container mb-4">
      <router-link to="/" class="btn btn-secondary text-decoration-none">
        <i class="fas fa-arrow-left me-2"></i>Back to Novels
      </router-link>
    </div>

    <div class="row g-3">
      <div
        class="col-12 col-sm-6 col-md-4 col-lg-3 mb-3"
        v-for="chapter in paginatedChapters"
        :key="chapter.id"
      >
        <router-link
          :to="`/novels/${novelId}/chapters/${chapter.number}`"
          class="text-decoration-none"
        >
          <div class="card h-100 chapter-card">
            <div class="card-body text-center d-flex flex-column">
              <div class="chapter-number">{{ chapter.number }}</div>
              <h5 class="card-title flex-grow-1">{{ chapter.title }}</h5>
              <div class="chapter-indicator mt-auto">
                <span class="read-indicator">
                  <i class="fas fa-book-open me-1"></i>Read Chapter
                </span>
              </div>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Mobile-friendly pagination -->
    <div class="pagination-container mt-4">
      <!-- Desktop pagination -->
      <div
        class="d-none d-md-flex justify-content-center align-items-center"
        role="navigation"
        aria-label="Chapter pagination"
      >
        <button
          class="btn btn-secondary me-2"
          :disabled="currentPage === 1"
          @click="goToPage(1)"
          aria-label="Go to first page"
        >
          <i class="fas fa-angle-double-left me-1"></i>First
        </button>
        <button
          class="btn btn-secondary me-2"
          :disabled="currentPage === 1"
          @click="goToPage(currentPage - 1)"
          aria-label="Previous page"
        >
          <i class="fas fa-angle-left me-1"></i>Previous
        </button>
        <span class="align-self-center mx-2" aria-live="polite">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <select
          v-model.number="currentPage"
          @change="goToPage(currentPage)"
          class="form-select mx-2"
          style="width: 100px"
          aria-label="Jump to page"
        >
          <option v-for="page in totalPages" :key="page" :value="page">
            {{ page }}
          </option>
        </select>
        <button
          class="btn btn-secondary ms-2"
          :disabled="currentPage === totalPages"
          @click="goToPage(currentPage + 1)"
          aria-label="Next page"
        >
          Next<i class="fas fa-angle-right ms-1"></i>
        </button>
        <button
          class="btn btn-secondary ms-2"
          :disabled="currentPage === totalPages"
          @click="goToPage(totalPages)"
          aria-label="Go to last page"
        >
          Last<i class="fas fa-angle-double-right ms-1"></i>
        </button>
      </div>

      <!-- Mobile pagination -->
      <div class="d-md-none">
        <div class="row justify-content-center mb-3">
          <div class="col-6">
            <button
              class="btn btn-secondary w-100"
              :disabled="currentPage === 1"
              @click="goToPage(currentPage - 1)"
              aria-label="Previous page"
            >
              <i class="fas fa-angle-left me-1"></i>Previous
            </button>
          </div>
          <div class="col-6">
            <button
              class="btn btn-secondary w-100"
              :disabled="currentPage === totalPages"
              @click="goToPage(currentPage + 1)"
              aria-label="Next page"
            >
              Next<i class="fas fa-angle-right ms-1"></i>
            </button>
          </div>
        </div>

        <div class="row justify-content-center mb-3">
          <div class="col-8">
            <select
              v-model.number="currentPage"
              @change="goToPage(currentPage)"
              class="form-select text-center"
              aria-label="Jump to page"
            >
              <option v-for="page in totalPages" :key="page" :value="page">
                Page {{ page }} of {{ totalPages }}
              </option>
            </select>
          </div>
        </div>

        <div class="row justify-content-center">
          <div class="col-6">
            <button
              class="btn btn-outline-secondary w-100"
              :disabled="currentPage === 1"
              @click="goToPage(1)"
              aria-label="Go to first page"
            >
              <i class="fas fa-angle-double-left me-1"></i>First
            </button>
          </div>
          <div class="col-6">
            <button
              class="btn btn-outline-secondary w-100"
              :disabled="currentPage === totalPages"
              @click="goToPage(totalPages)"
              aria-label="Go to last page"
            >
              Last<i class="fas fa-angle-double-right ms-1"></i>
            </button>
          </div>
        </div>
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
      chapters: [],
      novelTitle: "",
      novelImage: null,
      currentPage: 1,
      pageSize: 10,
      loading: true,
      error: null,
    };
  },
  computed: {
    novelId() {
      return this.$route.params.novelId;
    },
    totalPages() {
      return Math.ceil(this.chapters.length / this.pageSize);
    },
    paginatedChapters() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.chapters.slice(start, end);
    },
  },
  mounted() {
    this.fetchChapters();
  },
  methods: {
    async fetchChapters() {
      this.loading = true;
      try {
        const [chaptersResponse, novelResponse] = await Promise.all([
          axios.get(`/api/novels/${this.novelId}/chapters`),
          axios.get(`/api/novels/${this.novelId}`),
        ]);
        this.chapters = chaptersResponse.data;
        this.novelTitle = novelResponse.data.title;
        this.novelImage = novelResponse.data.image_url;
      } catch (error) {
        this.error = "Failed to load chapters. Please try again later.";
        console.error("Error fetching chapters:", error);
      } finally {
        this.loading = false;
      }
    },
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
  },
};
</script>

<style scoped>
.novel-header {
  background: linear-gradient(
    135deg,
    var(--surface) 0%,
    var(--surface-elevated) 50%,
    rgba(139, 92, 246, 0.1) 100%
  );
  border: 1px solid var(--border-accent);
  border-radius: var(--radius-3xl);
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow-purple-lg);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(20px);
}

.novel-header::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(139, 92, 246, 0.05),
    transparent
  );
  transition: left 0.5s;
}

.novel-header:hover::before {
  left: 100%;
}

.novel-info-container {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.novel-image {
  width: 120px;
  height: 160px;
  object-fit: cover;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  border: 3px solid var(--accent);
  flex-shrink: 0;
  transition: var(--transition-slow);
  filter: drop-shadow(0 0 10px var(--accent-glow));
}

.novel-image:hover {
  transform: scale(1.02);
  box-shadow: var(--shadow-purple-lg), var(--shadow-xl);
  filter: drop-shadow(0 0 20px var(--accent-glow));
}

.novel-image-placeholder {
  width: 120px;
  height: 160px;
  border: 3px solid var(--accent);
  border-radius: var(--radius-lg);
  background: linear-gradient(
    135deg,
    var(--surface) 0%,
    var(--surface-hover) 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 0.875rem;
  text-align: center;
  flex-shrink: 0;
}

.novel-details {
  flex: 1;
}

.novel-title {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
  font-weight: 700;
  background: linear-gradient(
    135deg,
    var(--text-primary) 0%,
    var(--accent-light) 50%,
    var(--accent) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 20px var(--accent-glow);
}

.novel-subtitle {
  font-size: 1.125rem;
  color: var(--accent);
  margin-bottom: 0;
  opacity: 0.9;
  font-weight: 500;
}

.back-button-container {
  text-align: center;
}

.chapter-card {
  transition: var(--transition-slow);
  border: 1px solid var(--border);
  position: relative;
  overflow: hidden;
  background: var(--surface);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chapter-card::before {
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

.chapter-card:hover::before {
  left: 100%;
}

.chapter-card:hover {
  border-color: var(--accent);
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
}

.chapter-number {
  background: linear-gradient(
    135deg,
    var(--accent) 0%,
    var(--accent-hover) 100%
  );
  color: white;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-weight: 700;
  font-size: 1.125rem;
  box-shadow: var(--shadow);
  transition: var(--transition);
  flex-shrink: 0;
}

.chapter-card:hover .chapter-number {
  transform: scale(1.1);
  box-shadow: var(--shadow-lg);
}

.chapter-indicator {
  margin-top: 1rem;
  flex-shrink: 0;
}

.read-indicator {
  background: rgba(139, 92, 246, 0.1);
  color: var(--accent);
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid rgba(139, 92, 246, 0.2);
  transition: var(--transition);
  display: inline-block;
}

.chapter-card:hover .read-indicator {
  background: rgba(139, 92, 246, 0.2);
  border-color: var(--accent);
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
  line-height: 1.3;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.chapter-card:hover .card-title {
  color: var(--accent);
}

.card-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.pagination-container {
  margin-top: 2rem;
}

/* Mobile-specific styles */
@media (max-width: 768px) {
  .novel-header {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .novel-info-container {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }

  .novel-image,
  .novel-image-placeholder {
    width: 140px;
    height: 180px;
  }

  .novel-title {
    font-size: 1.75rem;
  }

  .novel-subtitle {
    font-size: 1rem;
  }

  .chapter-card {
    margin-bottom: 0.75rem;
  }

  .card-body {
    padding: 1rem;
  }

  .card-title {
    font-size: 0.9375rem;
  }

  .chapter-number {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }

  .pagination-container {
    margin-top: 1.5rem;
  }

  .btn {
    font-size: 0.875rem;
    padding: 0.625rem 1rem;
  }

  .form-select {
    font-size: 0.875rem;
  }
}

@media (max-width: 480px) {
  .novel-header {
    padding: 1rem;
  }

  .novel-image,
  .novel-image-placeholder {
    width: 120px;
    height: 160px;
  }

  .novel-title {
    font-size: 1.5rem;
  }

  .novel-subtitle {
    font-size: 0.9375rem;
  }

  .chapter-number {
    width: 36px;
    height: 36px;
    font-size: 0.9375rem;
  }

  .read-indicator {
    font-size: 0.8125rem;
    padding: 0.375rem 0.75rem;
  }

  .card-body {
    padding: 0.75rem;
  }

  .card-title {
    font-size: 0.875rem;
  }
}

/* Extra small screens */
@media (max-width: 375px) {
  .row.g-3 {
    margin-left: -0.5rem;
    margin-right: -0.5rem;
  }

  .col-12 {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }

  .card-body {
    padding: 0.5rem;
  }

  .chapter-number {
    width: 32px;
    height: 32px;
    font-size: 0.875rem;
  }

  .read-indicator {
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
  }
}
</style>
