
import api from "@/api/api";
import {setProxy} from "@/api/api";

export default {
    install (app, options) {
        setProxy(options)
        app.config.globalProperties.$api = api;
    }
}