<template>
  <div>
    <DevelopmentNotice />
    <Navigation />
    <router-view></router-view>
    <Footer />
  </div>
</template>

<script>
import Navigation from "./components/Navigation.vue";
import Footer from "./components/Footer.vue";
import DevelopmentNotice from "./components/DevelopmentNotice.vue";

export default {
  components: {
    Navigation,
    Footer,
    DevelopmentNotice,
  },
  mounted() {
    document.body.classList.add("dark-mode");
  },
};
</script>
