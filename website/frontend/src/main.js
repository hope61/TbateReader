import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";

// Defer non-critical CSS loading
const loadCSS = (href) => {
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = href;
  document.head.appendChild(link);
};

// Load Bootstrap CSS asynchronously
const loadBootstrap = () => {
  import("bootstrap/dist/css/bootstrap.min.css");
  import("bootstrap/dist/js/bootstrap.bundle.min.js");
};

// Load main CSS asynchronously after critical CSS
const loadMainCSS = () => {
  import("./main.css");
};

// Load non-critical resources after DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    loadBootstrap();
    loadMainCSS();
  });
} else {
  loadBootstrap();
  loadMainCSS();
}

// Add Font Awesome CDN with performance optimizations
const fontAwesomeLink = document.createElement("link");
fontAwesomeLink.rel = "stylesheet";
fontAwesomeLink.href =
  "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css";
fontAwesomeLink.media = "print";
fontAwesomeLink.onload = function() { this.media = "all"; };
document.head.appendChild(fontAwesomeLink);

// Add DNS prefetch for external resources
const dnsPrefetch = document.createElement("link");
dnsPrefetch.rel = "dns-prefetch";
dnsPrefetch.href = "//cdnjs.cloudflare.com";
document.head.appendChild(dnsPrefetch);

// Do NOT force a baseURL; use relative URLs so phone hits same host as frontend
// If you deploy behind a different domain, set VITE_API_BASE_URL explicitly
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || "";

// Add API key to all requests if available
axios.interceptors.request.use(
  (config) => {
    const apiKey = import.meta.env.VITE_API_KEY;
    if (apiKey) {
      config.headers["X-API-Key"] = apiKey;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for error handling
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          console.error("Authentication failed. Please check your API key.");
          break;
        case 429:
          console.error("Rate limit exceeded. Please try again later.");
          break;
        case 413:
          console.error("Request too large.");
          break;
        default:
          console.error(
            `Request failed: ${error.response.status} ${error.response.statusText}`
          );
      }
    } else if (error.request) {
      console.error("Network error. Please check your connection.");
    } else {
      console.error("Request configuration error:", error.message);
    }
    return Promise.reject(error);
  }
);

createApp(App).use(router).mount("#app");
