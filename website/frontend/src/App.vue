<template>
  <div>
    <LoadingSpinner :loading="isLoading" />
    <div v-show="!isLoading">
      <DevelopmentNotice />
      <Navigation />
      <router-view></router-view>
      <Footer />
    </div>
  </div>
</template>

<script>
import Navigation from "./components/Navigation.vue";
import Footer from "./components/Footer.vue";
import DevelopmentNotice from "./components/DevelopmentNotice.vue";
import LoadingSpinner from "./components/LoadingSpinner.vue";

export default {
  components: {
    Navigation,
    Footer,
    DevelopmentNotice,
    LoadingSpinner,
  },
  data() {
    return {
      isLoading: true
    }
  },
  mounted() {
    document.body.classList.add("dark-mode");
    
    // Hide loading spinner after critical resources are loaded
    this.$nextTick(() => {
      // Wait for fonts and critical assets to load
      const hideLoading = () => {
        setTimeout(() => {
          this.isLoading = false;
        }, 300); // Small delay to ensure smooth transition
      };

      if (document.readyState === 'complete') {
        hideLoading();
      } else {
        window.addEventListener('load', hideLoading);
      }
    });
  },
};
</script>
