import { createRouter, createWebHistory } from "vue-router";
import Home from "../components/Home.vue";
import Contact from "../components/Contact.vue";
import ChaptersList from "../components/ChaptersList.vue";
import ChapterView from "../components/ChapterView.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/contact", component: Contact },
  { path: "/novels/:novelId", component: ChaptersList },
  { path: "/novels/:novelId/chapters/:chapterNumber", component: ChapterView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
