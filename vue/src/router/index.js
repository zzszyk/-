// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import QuestionChoice from '../components/QuestionChoice.vue';
import WritePage from '../components/WritePage.vue';
import SearchPage from '../components/SearchPage.vue';
import DrawPage from '../components/DrawPage.vue';
import ReviewPage from '../components/ReviewPage.vue';
const routes = [ { path: '/', component: QuestionChoice },
	{ path: '/WritePage', component: WritePage },
	{ path: '/SearchPage', component: SearchPage },
    { path: '/DrawPage', component: DrawPage},
	{ path: '/ReviewPage', component: ReviewPage }, ];
const router = createRouter({ history: createWebHistory(), routes });
export default router;
