import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import 'jquery/dist/jquery.min.js'
import "../src/assets/form.css";

const app = createApp(App)

app.use(router)

app.mount('#app')