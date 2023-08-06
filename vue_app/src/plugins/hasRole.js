import { user } from "@/store/user";
import { storeToRefs } from "pinia";

export default {
    install (app, options) {
        const userStore = user();
        const { token, roles } = storeToRefs(userStore);
        app.directive('hasRole', {
            mounted(el, binding) {
                el.parentNode_ = el.parentNode
                if (!token.value || !roles.value.includes(binding.value)) {
                    el.parentNode.removeChild(el)
                }
            },
            updated(el, binding) {
                if (token.value && roles.value.includes(binding.value)) {
                    !el.parentNode_.contains(el) && el.parentNode_.appendChild(el)
                } else {
                    el.parentNode_.contains(el) && el.parentNode.removeChild(el)
                }
            },
        })
    }
}