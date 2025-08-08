<template>
  <div class="container my-5">
    <!-- Chapter Header with Novel Info -->
    <div class="chapter-header">
      <div class="novel-info">
        <img
          v-if="novelImage"
          :src="novelImage"
          :alt="novelTitle.replace(/_/g, ' ')"
          class="novel-image"
          loading="lazy"
        />
        <div v-else class="novel-image-placeholder">No Cover Image</div>
        <div class="novel-details">
          <h2 class="novel-title">{{ novelTitle.replace(/_/g, " ") }}</h2>
          <h1 class="chapter-title">{{ chapterTitle }}</h1>
          <div class="chapter-meta">
            <span class="chapter-number">Chapter {{ chapterNumber }}</span>
            <span class="chapter-progress"
              >{{ currentChapter + 1 }} of {{ chapters.length }}</span
            >
          </div>
        </div>
      </div>
    </div>

    <!-- Desktop navigation -->
    <div class="d-none d-md-flex justify-content-between mb-4">
      <router-link
        :to="`/novels/${novelId}`"
        class="btn btn-secondary text-decoration-none"
      >
        <i class="fas fa-arrow-left me-2"></i>Back to Chapters
      </router-link>
      <div>
        <button
          class="btn btn-secondary text-decoration-none me-2"
          @click="goToChapter('prev')"
          :disabled="currentChapter === 0"
          aria-label="Previous chapter"
        >
          <i class="fas fa-angle-left me-2"></i>Previous
        </button>
        <button
          class="btn btn-secondary text-decoration-none"
          @click="goToChapter('next')"
          :disabled="currentChapter === chapters.length - 1"
          aria-label="Next chapter"
        >
          Next<i class="fas fa-angle-right ms-2"></i>
        </button>
      </div>
    </div>

    <!-- Mobile navigation -->
    <div class="d-md-none mb-4">
      <div class="row mb-3">
        <div class="col-12">
          <router-link
            :to="`/novels/${novelId}`"
            class="btn btn-secondary text-decoration-none w-100"
          >
            <i class="fas fa-arrow-left me-2"></i>Back to Chapters
          </router-link>
        </div>
      </div>
      <div class="row">
        <div class="col-6">
          <button
            class="btn btn-secondary text-decoration-none w-100"
            @click="goToChapter('prev')"
            :disabled="currentChapter === 0"
            aria-label="Previous chapter"
          >
            <i class="fas fa-angle-left me-2"></i>Previous
          </button>
        </div>
        <div class="col-6">
          <button
            class="btn btn-secondary text-decoration-none w-100"
            @click="goToChapter('next')"
            :disabled="currentChapter === chapters.length - 1"
            aria-label="Next chapter"
          >
            Next<i class="fas fa-angle-right ms-2"></i>
          </button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else class="row justify-content-center">
      <div class="col-12 col-lg-8">
        <div class="reading-container">
          <div class="chapter-content">
            <div v-html="parsedContent"></div>
          </div>

          <!-- Desktop footer navigation -->
          <div class="d-none d-md-flex justify-content-between mt-5">
            <button
              class="btn btn-secondary text-decoration-none"
              @click="goToChapter('prev')"
              :disabled="currentChapter === 0"
              aria-label="Previous chapter"
            >
              <i class="fas fa-angle-left me-2"></i>Previous
            </button>
            <button
              class="btn btn-secondary text-decoration-none"
              @click="goToChapter('next')"
              :disabled="currentChapter === chapters.length - 1"
              aria-label="Next chapter"
            >
              Next<i class="fas fa-angle-right ms-2"></i>
            </button>
          </div>

          <!-- Mobile footer navigation -->
          <div class="d-md-none mt-4">
            <div class="row">
              <div class="col-6">
                <button
                  class="btn btn-secondary text-decoration-none w-100"
                  @click="goToChapter('prev')"
                  :disabled="currentChapter === 0"
                  aria-label="Previous chapter"
                >
                  <i class="fas fa-angle-left me-2"></i>Previous
                </button>
              </div>
              <div class="col-6">
                <button
                  class="btn btn-secondary text-decoration-none w-100"
                  @click="goToChapter('next')"
                  :disabled="currentChapter === chapters.length - 1"
                  aria-label="Next chapter"
                >
                  Next<i class="fas fa-angle-right ms-2"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      chapterTitle: "",
      chapterContent: "",
      chapters: [],
      currentChapter: 0,
      novelTitle: "",
      novelImage: null,
      loading: true,
      error: null,
    };
  },
  computed: {
    novelId() {
      return this.$route.params.novelId;
    },
    chapterNumber() {
      return this.$route.params.chapterNumber;
    },
    parsedContent() {
      return this.chapterContent
        .split("\n\n")
        .map((paragraph) => `<p>${paragraph.split("\n").join("<br>")}</p>`)
        .join("");
    },
  },
  mounted() {
    this.fetchChapterData();
  },
  watch: {
    chapterNumber() {
      this.fetchChapterData();
    },
  },
  methods: {
    async fetchChapterData() {
      try {
        const [chapterResponse, chaptersResponse, novelResponse] =
          await Promise.all([
            axios.get(
              `/api/novels/${this.novelId}/chapters/${this.chapterNumber}`
            ),
            axios.get(`/api/novels/${this.novelId}/chapters`),
            axios.get(`/api/novels/${this.novelId}`),
          ]);
        this.chapterTitle = chapterResponse.data.title;
        this.chapterContent = chapterResponse.data.content;
        this.chapters = chaptersResponse.data;
        this.novelTitle = novelResponse.data.title;
        this.novelImage = novelResponse.data.image_url;
        this.currentChapter = this.chapters.findIndex(
          (ch) => ch.number == this.chapterNumber
        );
      } catch (error) {
        this.error = "Failed to load chapter. Please try again later.";
        console.error("Error fetching chapter:", error);
      } finally {
        this.loading = false;
      }
    },
    goToChapter(direction) {
      if (
        direction === "next" &&
        this.currentChapter < this.chapters.length - 1
      ) {
        const nextChapter = this.chapters[this.currentChapter + 1];
        this.$router.push(
          `/novels/${this.novelId}/chapters/${nextChapter.number}`
        );
      } else if (direction === "prev" && this.currentChapter > 0) {
        const prevChapter = this.chapters[this.currentChapter - 1];
        this.$router.push(
          `/novels/${this.novelId}/chapters/${prevChapter.number}`
        );
      }
    },
  },
};
</script>

<style scoped>
.chapter-header {
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

.chapter-header::before {
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

.chapter-header:hover::before {
  left: 100%;
}

.novel-info {
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
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: var(--accent);
  font-weight: 600;
}

.chapter-title {
  font-size: 2.25rem;
  margin-bottom: 1rem;
  color: var(--text-primary);
  line-height: 1.2;
  background: linear-gradient(
    135deg,
    var(--text-primary) 0%,
    var(--accent-light) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.chapter-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.chapter-number {
  background: linear-gradient(
    135deg,
    var(--accent) 0%,
    var(--accent-hover) 100%
  );
  color: white;
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-weight: 600;
  box-shadow: var(--shadow);
}

.chapter-progress {
  color: var(--text-secondary);
  opacity: 0.8;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Enhanced Reading Experience */
.reading-container {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  max-width: 800px;
  margin: 0 auto;
}

.chapter-content {
  padding: 3rem 2rem;
  line-height: 1.8;
  font-size: 1.125rem;
  color: var(--text-secondary);
  text-align: justify;
  text-indent: 1.5rem;
  letter-spacing: 0.01em;
  word-spacing: 0.05em;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  overflow: hidden;
}

.chapter-content p {
  margin-bottom: 1.5rem;
  text-indent: 1.5rem;
  line-height: 1.8;
  font-size: 1.125rem;
  color: var(--text-secondary);
  text-align: justify;
  letter-spacing: 0.01em;
  word-spacing: 0.05em;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  overflow: hidden;
}

.chapter-content p:first-of-type {
  font-size: 1.25rem;
  font-weight: 500;
  color: var(--text-primary);
  text-indent: 0;
  text-align: left;
  margin-bottom: 2rem;
}

.chapter-content p:last-of-type {
  margin-bottom: 0;
}

/* Reading mode enhancements */
@media (prefers-color-scheme: dark) {
  .chapter-content {
    background: var(--surface);
  }
}

/* Mobile-specific styles */
@media (max-width: 768px) {
  .chapter-header {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .novel-info {
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
    font-size: 1.125rem;
  }

  .chapter-title {
    font-size: 1.75rem;
    margin-bottom: 0.75rem;
  }

  .chapter-meta {
    justify-content: center;
    flex-wrap: wrap;
  }

  .chapter-content {
    padding: 2rem 1.5rem;
    font-size: 1rem;
    line-height: 1.7;
    text-indent: 1rem;
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
    overflow: hidden;
  }

  .chapter-content p {
    font-size: 1rem;
    line-height: 1.7;
    margin-bottom: 1.25rem;
    text-align: left;
    text-indent: 1rem;
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
    overflow: hidden;
  }

  .chapter-content p:first-of-type {
    font-size: 1.125rem;
    margin-bottom: 1.5rem;
  }

  .btn {
    font-size: 0.875rem;
    padding: 0.625rem 1rem;
  }
}

@media (max-width: 480px) {
  .chapter-header {
    padding: 1rem;
  }

  .novel-image,
  .novel-image-placeholder {
    width: 120px;
    height: 160px;
  }

  .chapter-title {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  .chapter-content {
    padding: 1.5rem 1rem;
    font-size: 0.9375rem;
    line-height: 1.6;
    text-indent: 0.75rem;
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
    overflow: hidden;
  }

  .chapter-content p {
    font-size: 0.9375rem;
    line-height: 1.6;
    margin-bottom: 1rem;
    text-indent: 0.75rem;
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
    overflow: hidden;
  }

  .chapter-content p:first-of-type {
    font-size: 1rem;
    margin-bottom: 1.25rem;
  }

  .btn {
    font-size: 0.8125rem;
    padding: 0.5rem 0.75rem;
  }
}

/* Focus styles for better accessibility */
.btn:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .chapter-content p {
    color: var(--text-primary);
  }

  .chapter-meta {
    gap: 1.5rem;
  }
}

/* Reading mode optimizations */
@media (prefers-reduced-motion: reduce) {
  .chapter-content {
    animation: none;
  }
}
</style>
