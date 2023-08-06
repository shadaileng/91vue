import { createApp } from 'vue'


// 导入自己的scss文件
import './assets/my.scss'

// 导入所有bootstrapjs
import * as bootstrap from 'bootstrap'

import { createPinia } from "pinia";
import piniaPluginPersist from "pinia-plugin-persist";

import './style.css'
import App from './App.vue'
import router from "./router";
import loadPicPlugin from '@/plugins/loadPicPlugin'
import loadPicBack from '@/plugins/loadPicBack'
import hasRole from '@/plugins/hasRole'
import loader from '@/plugins/loader'
import toast from '@/plugins/toast'
import api from '@/plugins/api'

import "./api/mock.js";

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersist);
app.use(pinia);
// app.use(loadPicPlugin)
app.use(loadPicBack)
app.use(hasRole)
app.use(loader)
app.use(toast)
app.use(router);
app.use(api, {loading: app.config.globalProperties.$loading});
app.mount("#app");