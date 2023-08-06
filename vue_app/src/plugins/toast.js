import toast from '@/components/toast.vue'
export default {
    install (app, options) {
        const Toast = createApp(toast)
        const root = document.createElement('div');
        document.body.appendChild(root);
        const vm =Toast.mount(root)
        app.config.globalProperties.$toast = vm.show
    }
}