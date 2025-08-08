<template>
  <div class="development-notice" v-if="showNotice">
    <div class="container">
      <div class="notice-content">
        <div class="notice-icon">
          <i class="fas fa-tools"></i>
        </div>
        <div class="notice-text">
          <strong>🚧 Under Development</strong>
          <span
            >This website is still in development. You may encounter bugs or
            missing features. Join our Discord to submit feature requests and
            suggest new novels!</span
          >
        </div>
        <button
          class="notice-close"
          @click="dismissNotice"
          aria-label="Close notice"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DevelopmentNotice",
  data() {
    return {
      showNotice: true,
    };
  },
  mounted() {
    // Check if user has dismissed the notice before
    const dismissed = localStorage.getItem("dev-notice-dismissed");
    if (dismissed) {
      this.showNotice = false;
    }
  },
  methods: {
    dismissNotice() {
      this.showNotice = false;
      localStorage.setItem("dev-notice-dismissed", "true");
    },
  },
};
</script>

<style scoped>
.development-notice {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  padding: 0.75rem 0;
  position: relative;
  z-index: 1001;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.notice-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  justify-content: space-between;
}

.notice-icon {
  font-size: 1.25rem;
  opacity: 0.9;
  flex-shrink: 0;
  /* Ensure icon is white, not purple */
  color: #ffffff !important;
}

.notice-icon i {
  color: #ffffff !important;
}

.notice-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.notice-text strong {
  font-size: 0.875rem;
  font-weight: 600;
}

.notice-text span {
  font-size: 0.8125rem;
  opacity: 0.9;
  line-height: 1.4;
}

.notice-close {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.5rem;
  border-radius: var(--radius);
  cursor: pointer;
  transition: var(--transition);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
}

.notice-close:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

@media (max-width: 768px) {
  .notice-content {
    gap: 0.75rem;
  }

  .notice-text span {
    font-size: 0.75rem;
  }

  .notice-close {
    width: 28px;
    height: 28px;
    padding: 0.375rem;
  }
}

@media (max-width: 480px) {
  .development-notice {
    padding: 0.5rem 0;
  }

  .notice-content {
    gap: 0.5rem;
  }

  .notice-text strong {
    font-size: 0.8125rem;
  }

  .notice-text span {
    font-size: 0.6875rem;
  }
}
</style>
