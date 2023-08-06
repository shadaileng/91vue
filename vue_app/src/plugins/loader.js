import loading from '@/components/loading.vue'
export default {
    install (app, options) {
        const Loading = createApp(loading)
        const root = document.createElement('div');
        document.body.appendChild(root);
        const vm = Loading.mount(root)
        app.config.globalProperties.$loading = vm.loading
    }
}