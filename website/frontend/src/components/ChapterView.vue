<template>
  <div class="container my-4">
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

    <!-- Simplified Navigation -->
    <div class="chapter-nav mb-4">
      <div class="nav-controls">
        <router-link
          :to="`/novels/${novelId}`"
          class="btn btn-outline-secondary"
        >
          <i class="fas fa-list me-2"></i>Chapter List
        </router-link>

        <div class="chapter-selector">
          <select
            id="chapterSelect"
            v-model="selectedChapter"
            @change="jumpToChapter"
            class="form-select"
            aria-label="Select chapter"
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

        <div class="nav-buttons">
          <button
            class="btn btn-primary"
            @click="goToChapter('prev')"
            :disabled="currentChapter === 0"
            aria-label="Previous chapter"
          >
            <i class="fas fa-angle-left"></i>
          </button>
          <button
            class="btn btn-primary"
            @click="goToChapter('next')"
            :disabled="currentChapter === chapters.length - 1"
            aria-label="Next chapter"
          >
            <i class="fas fa-angle-right"></i>
          </button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else class="reading-container">
      <div class="chapter-content">
        <div v-html="parsedContent"></div>
      </div>

      <!-- Bottom navigation -->
      <div class="reader-footer-nav">
        <div class="nav-footer">
          <button
            class="btn btn-primary"
            @click="goToChapter('prev')"
            :disabled="currentChapter === 0"
          >
            <i class="fas fa-angle-left me-2"></i>Previous
          </button>
          <a href="#top" class="btn btn-outline-secondary">
            <i class="fas fa-arrow-up"></i>
          </a>
          <button
            class="btn btn-primary"
            @click="goToChapter('next')"
            :disabled="currentChapter === chapters.length - 1"
          >
            Next<i class="fas fa-angle-right ms-2"></i>
          </button>
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
      selectedChapter: null,
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
        this.selectedChapter = parseInt(this.chapterNumber);
        // Scroll to top when loading new chapter
        window.scrollTo(0, 0);
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
    jumpToChapter() {
      if (this.selectedChapter) {
        this.$router.push(
          `/novels/${this.novelId}/chapters/${this.selectedChapter}`
        );
      }
    },
  },
};
</script>

<style scoped>
.chapter-header {
  background-color: var(--surface-elevated);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.novel-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.novel-image {
  width: 100px;
  height: 140px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.novel-details {
  flex: 1;
}

.novel-title {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.chapter-title {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.chapter-meta {
  display: flex;
  gap: 1rem;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

/* Navigation */
.chapter-nav {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
}

.nav-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.chapter-selector {
  flex: 1;
  max-width: 50%;
}

.nav-buttons {
  display: flex;
  gap: 0.5rem;
}

/* Reading container */
.reading-container {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  max-width: 800px;
  margin: 0 auto;
}

.chapter-content {
  padding: 2rem;
  line-height: 1.8;
  color: var(--text-primary);
}

.chapter-content p {
  margin-bottom: 1.5rem;
  text-indent: 1.5rem;
  line-height: 1.8;
  color: var(--text-primary);
}

.chapter-content p:first-of-type {
  font-weight: 500;
  text-indent: 0;
}

.chapter-content p:last-of-type {
  margin-bottom: 0;
}

/* Footer navigation */
.reader-footer-nav {
  border-top: 1px solid var(--border);
  background-color: var(--surface-elevated);
  padding: 1rem;
}

.nav-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .novel-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .novel-image {
    width: 120px;
    height: 160px;
    margin-bottom: 1rem;
  }

  .nav-controls {
    flex-direction: column;
    gap: 1rem;
  }

  .chapter-selector {
    width: 100%;
    max-width: 100%;
    order: 3;
  }

  .nav-buttons {
    width: 100%;
    justify-content: space-between;
    order: 2;
  }

  .chapter-nav .btn-outline-secondary {
    width: 100%;
    order: 1;
  }

  .chapter-content {
    padding: 1.5rem 1rem;
  }

  .nav-footer {
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .nav-footer .btn {
    flex: 1;
    text-align: center;
    padding: 0.5rem;
  }

  .nav-footer .btn-outline-secondary {
    flex: 0 0 auto;
    min-width: 50px;
  }
}

/* Small mobile screens */
@media (max-width: 480px) {
  .chapter-header {
    padding: 1rem;
  }

  .chapter-title {
    font-size: 1.3rem;
  }

  .chapter-content {
    padding: 1rem;
  }

  .chapter-content p {
    font-size: 1rem;
    line-height: 1.6;
    text-indent: 1rem;
  }
}
</style>
