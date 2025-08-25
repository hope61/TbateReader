import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  build: {
    // Optimize chunks
    rollupOptions: {
      output: {
        manualChunks: (id) => {
          if (id.includes("node_modules")) {
            if (id.includes("vue")) return "vue-vendor";
            if (id.includes("bootstrap")) return "bootstrap";
            if (id.includes("axios")) return "axios";
            return "vendor";
          }
          if (id.includes("/components/Home")) return "home";
          if (id.includes("/components/")) return "components";
        },
      },
    },
    // Disable source maps for production
    sourcemap: false,
    // Inline small assets
    assetsInlineLimit: 2048,
    // Enable CSS code splitting
    cssCodeSplit: true,
    // Minify options
    minify: "terser",
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
        pure_funcs: ["console.log", "console.info", "console.debug"],
      },
    },
    // Target modern browsers for smaller bundles
    target: "es2020",
  },
  // Optimize dependencies
  optimizeDeps: {
    include: ["vue", "vue-router", "axios", "bootstrap"],
  },
});
