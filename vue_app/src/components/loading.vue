<script setup>
import loaderMobius from '@/components/loaderMobius.vue'
import {Modal} from 'bootstrap'
const modalDom = ref(null)
let modal = null
const props = defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
})
onMounted(() => {
    modal = new Modal(modalDom.value, {
        keyboard: false,
        backdrop: 'static'
    })
})
const loading = (status=true) => {
    if (!modal) returns
    if (status) {
        if (modal._isShown) return
        modal.show()
    } else {
        setTimeout(()=>{
            modal.hide()
        }, 1000)
    }
}
defineExpose({
    loading
})

</script>
<template>
    <div ref="modalDom" class="modal fade" style="z-index: 99999999" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered">
            <div class="text-center" style="margin: 0 auto;">
                <!-- <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div> -->
                <loaderMobius></loaderMobius>
            </div>
        </div>
    </div>
</template>