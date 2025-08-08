<template>
  <div class="container my-5">
    <div class="contact-content">
      <h1 class="contact-title">Contact Us</h1>
      <p class="contact-lead">Have questions or feedback? Reach out to us!</p>

      <div class="contact-info">
        <div class="contact-item">
          <p class="contact-label">Join our community on Discord:</p>
          <a
            href="https://discord.gg/vYJQwqAaWE"
            class="btn btn-primary discord-btn"
          >
            <i class="fab fa-discord me-1"></i> Join Discord
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Contact",
};
</script>

<style scoped>
.contact-content {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.contact-title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: var(--text-primary);
  text-align: center;
}

.contact-lead {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  color: var(--text-secondary);
  text-align: center;
}

.contact-subtitle {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
  text-align: center;
}

.contact-info {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 2rem;
  box-shadow: var(--shadow-lg);
  text-align: center;
}

.contact-item {
  margin-bottom: 1.5rem;
}

.contact-item:last-child {
  margin-bottom: 0;
}

.contact-label {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
  font-weight: 500;
}

.contact-link {
  color: var(--accent);
  font-size: 1.1rem;
  text-decoration: none;
  transition: var(--transition);
}

.contact-link:hover {
  color: var(--accent-hover);
  text-decoration: underline;
}

.discord-btn {
  font-size: 1.1rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: var(--transition);
}

.discord-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

/* Mobile-specific styles */
@media (max-width: 576px) {
  .contact-title {
    font-size: 2rem;
  }

  .contact-lead {
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
  }

  .contact-info {
    padding: 1.5rem;
    margin: 0 0.5rem;
  }

  .contact-item {
    margin-bottom: 1.25rem;
  }

  .contact-label {
    font-size: 1rem;
  }

  .contact-link {
    font-size: 1rem;
  }

  .discord-btn {
    font-size: 1rem;
    padding: 0.75rem 1.25rem;
    width: 100%;
  }
}

@media (min-width: 577px) and (max-width: 767px) {
  .contact-title {
    font-size: 2.2rem;
  }

  .contact-info {
    padding: 1.75rem;
  }
}
</style>
