<script setup>
import {Offcanvas} from 'bootstrap'
const offcanvasDom = ref(null)
const emit = defineEmits(['hiden'])
let offcanvas = null
onMounted(() => {
    offcanvas = new Offcanvas(offcanvasDom.value)
    offcanvasDom.value.addEventListener('hidden.bs.offcanvas', function (event) {
        emit('hiden')
    })
})
const show = ()=>{
    // console.log(offcanvas)
    offcanvas.show()
}
const hide = ()=>{
    // console.log(offcanvas)
    offcanvas.hide()
}
defineExpose({
    show,
    hide,
})
</script>

<template>
    <div ref="offcanvasDom" class="offcanvas offcanvas-end" tabindex="-1" aria-labelledby="offcanvasExampleLabel">
        <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasExampleLabel"><slot name="title"></slot></h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
            <slot name="body"></slot>
        </div>
    </div>
</template>
