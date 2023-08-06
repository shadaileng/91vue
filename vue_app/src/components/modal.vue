<script setup>
import {Modal} from 'bootstrap'
const modalDom = ref(null)
const emit = defineEmits(['hiden', 'submit'])
let modal = null

const props = defineProps({
    submitShow: Boolean,
})
onMounted(() => {
    modal = new Modal(modalDom.value)
    modalDom.value.addEventListener('hidden.bs.modal', function (event) {
        emit('hiden')
    })
})
const show = async ()=>{
    // console.log(modal)
    modal.show()
}
const hide = async ()=>{
    // console.log(modal)
    modal.hide()
}
defineExpose({
    show,
    hide,
})
</script>

<template>
    <!-- Modal -->
    <div ref="modalDom" class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl modal-dialog-centered">
             <div class="modal-content">
                <!-- <div class="modal-header">
                    <h5 class="modal-title" id="staticBackdropLabel">Modal title</h5>
                </div> -->
                <div class="modal-body p-0">
                    <slot></slot>
                    <button type="button" class="btn-close btn-close-white btn-close-local" data-bs-dismiss="modal" aria-label="Close"></button>
                    <button type="button" v-if="submitShow" class="btn btn-submit" @click="emit('submit')"></button>
                </div>
             </div>
        </div>
    </div>
</template>
<style scoped>
.btn-close-local {
    position: absolute;
    top: 10px;
    right: 10px;
    box-shadow: inset 0 0 20px #fff;
    z-index: 99999;
}

.btn-submit {
    box-sizing: content-box;
    width: 1em;
    height: 1em;
    padding: .25em .25em;
    color: #000;
    background: transparent url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23000'%3e%3cpath d='M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z'/%3e%3c/svg%3e") center/1em auto no-repeat;
    border: 0;
    border-radius: .25rem;
    opacity: .5;
    filter: invert(1) grayscale(100%) brightness(200%);
    position: absolute;
    top: 10px;
    right: 40px;
    box-shadow: inset 0 0 20px #fff;
}
.btn-submit:hover {
    color: #000;
    text-decoration: none;
    opacity: .75;
}
</style>
