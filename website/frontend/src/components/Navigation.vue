<template>
  <nav class="navbar navbar-expand-lg">
    <div class="container">
      <router-link class="navbar-brand d-flex align-items-center" to="/">
        <img
          src="../assets/minicaera.png"
          class="logo me-2"
          width="40"
          height="40"
          alt="Mana's Embrace Logo"
        />
        <span class="brand-text">Mana's Embrace</span>
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
        @click="toggleMenu"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/" @click="closeMenu">
              <i class="fas fa-home me-1"></i>Home
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/contact" @click="closeMenu">
              <i class="fas fa-envelope me-1"></i>Contact
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "Navigation",
  watch: {
    // Close menu when route changes
    $route() {
      this.closeMenu();
    },
  },
  methods: {
    toggleMenu() {
      // This method can be used for additional functionality if needed
    },
    closeMenu() {
      // Close mobile menu when a link is clicked
      const navbarCollapse = document.getElementById("navbarNav");
      if (navbarCollapse) {
        // Remove the 'show' class directly
        navbarCollapse.classList.remove("show");

        // Also use Bootstrap's collapse method if available
        if (typeof bootstrap !== "undefined" && bootstrap.Collapse) {
          const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
            toggle: false,
          });
          bsCollapse.hide();
        }

        // Update the toggler button state
        const toggler = document.querySelector(".navbar-toggler");
        if (toggler) {
          toggler.setAttribute("aria-expanded", "false");
        }
      }
    },
  },
};
</script>

<style scoped>
.navbar {
  background: rgba(26, 26, 26, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
  padding: 0.75rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

/* Prevent collapsed container from reserving space when hidden - mobile only */
@media (max-width: 991.98px) {
  .collapse:not(.show) {
    display: none !important;
    height: 0 !important;
    overflow: hidden !important;
  }
}

/* Avoid extra margins creating a big dark bar */
.navbar-collapse {
  margin-top: 0;
}

.navbar-brand {
  color: var(--text-primary) !important;
  font-family: var(--font-sans);
  font-weight: 700;
  font-size: 1.25rem;
  text-decoration: none;
  transition: var(--transition);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-right: 0;
}

.navbar-brand:hover {
  color: var(--accent) !important;
  transform: translateY(-1px);
}

.brand-text {
  display: inline-block;
  background: linear-gradient(
    135deg,
    var(--text-primary) 0%,
    var(--accent-light) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo {
  transition: var(--transition);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.navbar-brand:hover .logo {
  transform: scale(1.05);
  filter: drop-shadow(0 4px 8px rgba(139, 92, 246, 0.3));
}

.navbar-nav {
  margin-left: auto !important;
  align-items: center;
}

.nav-link {
  color: var(--text-secondary) !important;
  font-family: var(--font-sans);
  font-weight: 500;
  font-size: 0.875rem;
  padding: 0.75rem 1rem !important;
  border-radius: var(--radius);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
  text-align: center;
  margin: 0 0.25rem;
}

.nav-link::before {
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
  transition: left 0.3s;
}

.nav-link:hover::before {
  left: 100%;
}

.nav-link:hover {
  color: var(--accent) !important;
  background: rgba(139, 92, 246, 0.1);
  transform: translateY(-1px);
}

.navbar-toggler {
  border: none;
  padding: 0.5rem;
  background: transparent;
  border-radius: var(--radius);
  transition: var(--transition);
  margin-left: auto;
}

.navbar-toggler:focus {
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.3);
  outline: none;
}

.navbar-toggler:hover {
  background: rgba(139, 92, 246, 0.1);
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba(139, 92, 246, 0.8)' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
  transition: var(--transition);
}

.navbar-toggler:hover .navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba(139, 92, 246, 1)' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}

.navbar-collapse {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  margin-top: 0.5rem;
  overflow: hidden;
  transition: var(--transition);
}

.nav-item {
  margin: 0.25rem 0;
}

.nav-item:first-child {
  margin-top: 0;
}

.nav-item:last-child {
  margin-bottom: 0;
}

/* Desktop styles */
@media (min-width: 992px) {
  .navbar-nav {
    flex-direction: row !important;
    margin-left: auto !important;
  }

  .nav-item {
    margin: 0 0.25rem;
  }

  .navbar-collapse {
    background: transparent;
    border: none;
    box-shadow: none;
    margin-top: 0;
  }
}

/* Mobile-specific styles */
@media (max-width: 991.98px) {
  .navbar {
    padding: 0.75rem 0;
  }

  .navbar-brand {
    font-size: 1.125rem;
    margin-right: 0;
  }

  .logo {
    width: 36px !important;
    height: 36px !important;
  }

  .navbar-collapse {
    background: rgba(26, 26, 26, 0.98);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-xl);
    margin-top: 0.5rem;
    padding: 0.5rem;
    border-radius: var(--radius-lg);
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    z-index: 1001;
  }

  .navbar-nav {
    text-align: center;
    padding: 0.5rem 0;
    margin: 0;
    flex-direction: column !important;
  }

  .nav-item {
    margin: 0.25rem 0;
    width: 100%;
  }

  .nav-link {
    padding: 0.875rem 1.25rem !important;
    border-radius: var(--radius);
    margin: 0.125rem 0;
    font-size: 1rem;
    font-weight: 500;
    width: 100%;
    display: block;
  }

  .nav-link:hover {
    background: rgba(139, 92, 246, 0.15);
    color: var(--accent) !important;
    transform: translateX(4px);
  }

  .brand-text {
    font-size: 1rem;
  }
}

@media (max-width: 576px) {
  .navbar {
    padding: 0.5rem 0;
  }

  .navbar-brand {
    font-size: 1rem;
  }

  .logo {
    width: 32px !important;
    height: 32px !important;
  }

  .brand-text {
    font-size: 0.875rem;
  }

  .navbar-collapse {
    margin-top: 0.25rem;
    padding: 0.25rem;
  }

  .nav-link {
    padding: 0.75rem 1rem !important;
    font-size: 0.9375rem;
  }
}

/* Let Bootstrap handle the collapse animation */
.navbar-collapse {
  transition: height 0.35s ease;
}

/* Focus styles for accessibility */
.navbar-toggler:focus,
.nav-link:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .navbar {
    background: rgba(0, 0, 0, 0.95);
    border-bottom: 2px solid var(--text-primary);
  }

  .nav-link {
    color: var(--text-primary) !important;
  }

  .nav-link:hover {
    color: var(--accent) !important;
    background: rgba(139, 92, 246, 0.2);
  }
}
</style>
