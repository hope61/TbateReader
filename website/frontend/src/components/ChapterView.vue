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

    <!-- Enhanced Quick Chapter Navigation -->
    <div class="quick-chapter-nav mb-4">
      <div class="row justify-content-center">
        <div class="col-12 col-lg-10">
          <div class="navigation-grid">
            <!-- Chapter Jump + Back Section -->
            <div class="chapter-jump-section">
              <router-link
                :to="`/novels/${novelId}?page=${returnPage}`"
                class="btn btn-outline-secondary back-btn mb-2"
              >
                <i class="fas fa-arrow-left me-2"></i>Back to Chapters
                <span class="page-info">(Page {{ returnPage }})</span>
              </router-link>

              <label for="chapterSelect" class="form-label mb-2">
                <i class="fas fa-search me-2"></i>Jump to Chapter:
              </label>
              <select
                id="chapterSelect"
                v-model="selectedChapter"
                @change="jumpToChapter"
                class="form-select chapter-select"
              >
                <option
                  v-for="chapter in chapters"
                  :key="chapter.id"
                  :value="chapter.number"
                >
                  {{ chapter.number }}: {{ chapter.title }}
                </option>
              </select>
            </div>

            <!-- Center Chapter Progress + Nav -->
            <div class="chapter-progress-section">
              <div class="nav-group">
                <button
                  class="btn btn-primary"
                  @click="goToFirst"
                  :disabled="currentChapter === 0"
                  aria-label="First chapter"
                >
                  <i class="fas fa-angle-double-left"></i>
                </button>
                <button
                  class="btn btn-primary"
                  @click="goToChapter('prev')"
                  :disabled="currentChapter === 0"
                  aria-label="Previous chapter"
                >
                  <i class="fas fa-angle-left"></i>
                </button>

                <span class="progress-pill"
                  >{{ currentChapter + 1 }} / {{ chapters.length }}</span
                >

                <button
                  class="btn btn-primary"
                  @click="goToChapter('next')"
                  :disabled="currentChapter === chapters.length - 1"
                  aria-label="Next chapter"
                >
                  <i class="fas fa-angle-right"></i>
                </button>
                <button
                  class="btn btn-primary"
                  @click="goToLast"
                  :disabled="currentChapter === chapters.length - 1"
                  aria-label="Last chapter"
                >
                  <i class="fas fa-angle-double-right"></i>
                </button>
              </div>

              <div class="progress-bar-container mt-3">
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{
                      width: `${((currentChapter + 1) / chapters.length) * 100}%`,
                    }"
                  ></div>
                </div>
              </div>
            </div>

            <!-- Reader Controls Section -->
            <div class="reader-controls-section">
              <div class="controls-row">
                <div class="control-group">
                  <span class="control-label">Text Size</span>
                  <div class="btn-group">
                    <button
                      class="btn btn-outline-secondary btn-sm"
                      @click="decreaseFont"
                      aria-label="Decrease font size"
                    >
                      A-
                    </button>
                    <button
                      class="btn btn-outline-secondary btn-sm"
                      @click="increaseFont"
                      aria-label="Increase font size"
                    >
                      A+
                    </button>
                  </div>
                </div>
                <div class="control-group">
                  <span class="control-label">Spacing</span>
                  <div class="btn-group">
                    <button
                      class="btn btn-outline-secondary btn-sm"
                      :class="{ active: settings.lineHeight === 'normal' }"
                      @click="setLineHeight('normal')"
                    >
                      Normal
                    </button>
                    <button
                      class="btn btn-outline-secondary btn-sm"
                      :class="{ active: settings.lineHeight === 'comfy' }"
                      @click="setLineHeight('comfy')"
                    >
                      Comfy
                    </button>
                  </div>
                </div>
              </div>
              <div class="controls-row">
                <div class="control-group">
                  <span class="control-label">Layout</span>
                  <div class="btn-group">
                    <button
                      class="btn btn-outline-secondary btn-sm"
                      :class="{ active: settings.width === 'narrow' }"
                      @click="setWidth('narrow')"
                    >
                      Narrow
                    </button>
                    <button
                      class="btn btn-outline-secondary btn-sm"
                      :class="{ active: settings.width === 'medium' }"
                      @click="setWidth('medium')"
                    >
                      Medium
                    </button>
                    <button
                      class="btn btn-outline-secondary btn-sm"
                      :class="{ active: settings.width === 'wide' }"
                      @click="setWidth('wide')"
                    >
                      Wide
                    </button>
                  </div>
                </div>
                <div class="control-group">
                  <span class="control-label">Theme</span>
                  <div class="btn-group">
                    <button
                      class="btn btn-outline-secondary btn-sm"
                      :class="{ active: settings.theme === 'auto' }"
                      @click="setTheme('auto')"
                    >
                      Auto
                    </button>
                    <button
                      class="btn btn-outline-secondary btn-sm"
                      :class="{ active: settings.theme === 'light' }"
                      @click="setTheme('light')"
                    >
                      Light
                    </button>
                    <button
                      class="btn btn-outline-secondary btn-sm"
                      :class="{ active: settings.theme === 'sepia' }"
                      @click="setTheme('sepia')"
                    >
                      Sepia
                    </button>
                    <button
                      class="btn btn-outline-secondary btn-sm"
                      :class="{ active: settings.theme === 'dark' }"
                      @click="setTheme('dark')"
                    >
                      Dark
                    </button>
                  </div>
                </div>
              </div>
            </div>
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
    <div v-else class="row justify-content-center">
      <div class="col-12" :class="readingWidthClass">
        <div class="reading-container" :class="themeClass">
          <div class="chapter-content" :style="contentStyle">
            <div v-html="parsedContent"></div>
          </div>

          <!-- Bottom navigation -->
          <div class="reader-footer-nav">
            <div
              class="d-flex justify-content-between align-items-center flex-wrap gap-2"
            >
              <button
                class="btn btn-primary"
                @click="goToChapter('prev')"
                :disabled="currentChapter === 0"
                aria-label="Previous chapter"
              >
                <i class="fas fa-angle-left me-2"></i>Previous
              </button>
              <a href="#top" class="btn btn-outline-secondary">
                <i class="fas fa-arrow-up me-2"></i>Top
              </a>
              <button
                class="btn btn-primary"
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
      returnPage: 1,
      selectedChapter: null,
      settings: {
        fontSize: 1.125,
        lineHeight: "comfy", // 'normal' | 'comfy'
        width: "medium", // 'narrow' | 'medium' | 'wide'
        theme: "auto", // 'auto' | 'light' | 'sepia' | 'dark'
      },
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
    returnPage() {
      const key = `novel_${this.novelId}_page`;
      return parseInt(localStorage.getItem(key)) || 1;
    },
    contentStyle() {
      const lh = this.settings.lineHeight === "comfy" ? 1.8 : 1.6;
      return {
        fontSize: `${this.settings.fontSize}rem`,
        lineHeight: lh,
      };
    },
    readingWidthClass() {
      return {
        "col-lg-7 col-xl-7": this.settings.width === "narrow",
        "col-lg-8 col-xl-8": this.settings.width === "medium",
        "col-lg-9 col-xl-9": this.settings.width === "wide",
      };
    },
    themeClass() {
      switch (this.settings.theme) {
        case "light":
          return "theme-light";
        case "sepia":
          return "theme-sepia";
        case "dark":
          return "theme-dark";
        default:
          return "theme-auto";
      }
    },
  },
  mounted() {
    this.fetchChapterData();
    this.loadReaderSettings();
  },
  watch: {
    chapterNumber() {
      this.fetchChapterData();
    },
    settings: {
      handler() {
        this.saveReaderSettings();
      },
      deep: true,
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
        this.selectedChapter = parseInt(this.chapterNumber);
      } catch (error) {
        this.error = "Failed to load chapter. Please try again later.";
        console.error("Error fetching chapter:", error);
      } finally {
        this.loading = false;
      }
    },
    goToFirst() {
      if (this.currentChapter > 0) {
        const first = this.chapters[0];
        this.$router.push(`/novels/${this.novelId}/chapters/${first.number}`);
      }
    },
    goToLast() {
      if (this.currentChapter < this.chapters.length - 1) {
        const last = this.chapters[this.chapters.length - 1];
        this.$router.push(`/novels/${this.novelId}/chapters/${last.number}`);
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
    jumpToChapter() {
      if (this.selectedChapter) {
        this.$router.push(
          `/novels/${this.novelId}/chapters/${this.selectedChapter}`
        );
      }
    },
    increaseFont() {
      this.settings.fontSize = Math.min(this.settings.fontSize + 0.0625, 1.5);
    },
    decreaseFont() {
      this.settings.fontSize = Math.max(this.settings.fontSize - 0.0625, 0.9);
    },
    setLineHeight(mode) {
      this.settings.lineHeight = mode;
    },
    setWidth(width) {
      this.settings.width = width;
    },
    setTheme(theme) {
      this.settings.theme = theme;
    },
    saveReaderSettings() {
      try {
        localStorage.setItem("reader_settings", JSON.stringify(this.settings));
      } catch (_) {}
    },
    loadReaderSettings() {
      try {
        const raw = localStorage.getItem("reader_settings");
        if (raw) {
          const parsed = JSON.parse(raw);
          this.settings = { ...this.settings, ...parsed };
        }
      } catch (_) {}
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

.quick-chapter-nav {
  background: var(--surface-elevated);
  border: 1px solid var(--border-accent);
  border-radius: var(--radius-xl);
  padding: 2rem;
  box-shadow: var(--shadow-md);
}

.navigation-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 2rem;
  align-items: center;
}

.chapter-jump-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.chapter-jump-section .form-label {
  color: var(--text-primary);
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.chapter-select {
  min-width: 200px;
  border-color: var(--border-accent);
  background-color: var(--surface);
  color: var(--text-primary);
  border-radius: var(--radius-lg);
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
}

.chapter-select:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 0.2rem rgba(139, 92, 246, 0.25);
}

.chapter-progress-section {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.nav-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.progress-pill {
  background: var(--surface);
  border: 1px solid var(--border-accent);
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius-lg);
  font-weight: 600;
  color: var(--text-primary);
}

.progress-bar-container {
  width: 260px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: var(--surface-hover);
  border-radius: var(--radius-full);
  overflow: hidden;
  border: 1px solid var(--border-accent);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(
    90deg,
    var(--accent) 0%,
    var(--accent-light) 100%
  );
  border-radius: var(--radius-full);
  transition: width 0.3s ease;
}

.back-btn {
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-lg);
  font-weight: 500;
  transition: all 0.2s ease;
}

.back-btn:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.page-info {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-left: 0.5rem;
}

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
@media (max-width: 992px) {
  .navigation-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
    text-align: center;
  }

  .chapter-jump-section {
    align-items: center;
  }

  .progress-bar-container {
    width: 200px;
  }
}

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

  .chapter-select {
    min-width: 180px;
  }

  .reading-container {
    padding: 1.5rem;
  }

  .chapter-content {
    padding: 2rem 1.5rem;
    font-size: 1rem;
    line-height: 1.7;
    text-indent: 1rem;
  }

  .chapter-content p {
    font-size: 1rem;
    line-height: 1.7;
    margin-bottom: 1.25rem;
    text-align: left;
    text-indent: 1rem;
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
  }

  .chapter-content p {
    font-size: 0.9375rem;
    line-height: 1.6;
    margin-bottom: 1rem;
    text-indent: 0.75rem;
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

.reader-controls-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.controls-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.control-label {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.btn-group .btn.active {
  background-color: var(--accent);
  color: #fff;
  border-color: var(--accent);
}

.reader-footer-nav {
  border-top: 1px solid var(--border-accent);
  background: var(--surface-elevated);
  padding: 1rem 1.25rem;
}

/* Theme modifiers for reading container */
.theme-auto {
  background: var(--surface);
  color: var(--text-primary);
}
.theme-light {
  background: #ffffff;
  color: #1f2937;
}
.theme-sepia {
  background: #f6f2e8;
  color: #3f3a33;
}
.theme-dark {
  background: #0f1115;
  color: #e5e7eb;
}

.theme-sepia .chapter-content p {
  color: #3f3a33;
}
.theme-dark .chapter-content p {
  color: #d1d5db;
}

/* Width helpers via grid cols are handled by readingWidthClass */
</style>
