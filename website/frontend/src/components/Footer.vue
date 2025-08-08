<template>
  <footer>
    <div class="container">
      <p class="copyright">&copy; 2025 Mana's Embrace. All rights reserved.</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
};
</script>

<style scoped>
footer {
  background: var(--surface);
  border-top: 1px solid var(--border);
  color: var(--text-secondary);
  padding: 2rem 0;
  text-align: center;
  margin-top: 4rem;
  position: relative;
  overflow: hidden;
}

footer::before {
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

footer:hover::before {
  left: 100%;
}

.copyright {
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
  color: var(--text-muted);
  font-weight: 500;
}

/* Mobile-specific styles */
@media (max-width: 768px) {
  footer {
    padding: 1.5rem 0;
    margin-top: 3rem;
  }

  .copyright {
    margin-bottom: 1rem;
    font-size: 0.8125rem;
  }

  .container {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
  }
}

@media (max-width: 480px) {
  footer {
    padding: 1.25rem 0;
  }

  .copyright {
    margin-bottom: 0.875rem;
    font-size: 0.75rem;
  }

  .container {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  footer {
    border-top: 2px solid var(--text-primary);
  }

  .copyright {
    color: var(--text-primary);
  }
}
</style>
