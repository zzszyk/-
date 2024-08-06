import { createApp } from 'vue'
import App from '../App.vue'
import router from './router';
//导包
import DevUI from 'vue-devui';
import 'vue-devui/style.css';
import '@devui-design/icons/icomoon/devui-icon.css';
import { ThemeServiceInit, infinityTheme } from 'devui-theme';

import './font/font.css'

//import mitt from "mitt"

import mitt from "mitt";

const emitter = mitt()

export default emitter

ThemeServiceInit({ infinityTheme }, 'infinityTheme');

const app = createApp(App);

//app.config.globalProperties.$bus = new mitt();

app.use(router).use(DevUI).mount('#app')
