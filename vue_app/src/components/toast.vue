<script setup>
import {Toast} from 'bootstrap'
const text = ref(''), title = ref('消息')
const toastDom = ref(null)
let toast = null
onMounted(() => {
    toast = new Toast(toastDom.value)
})
const show = (msg, titleVale)=>{
    text.value = msg
    titleVale !== undefined && (title.value = titleVale)
    toast.show()
}
defineExpose({
    show,
    title
})


</script>
<template>
    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 99911">
        <div id="liveToast" ref="toastDom" class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="1000">
            <div class="toast-header">
            <!-- <img src="..." class="rounded me-2" alt="..."> -->
            <strong class="me-auto">{{title}}</strong>
            <small>11 mins ago</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
            {{text}}
            </div>
        </div>
    </div>
</template>