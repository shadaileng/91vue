<template>
    <div>
        <button class="btn btn-sm d-none" @click="modal('show');$emit('share')">分享</button>
        <div ref="share" class="modal fade bd-example-modal-lg " tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
                <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
                    <slot></slot>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
            return {
            }
        },
    props: ['show'],
    emits: ['hide'],
    mounted() {
        // this.modal('show')
        $(this.$refs.share).on('hide.bs.modal', ()=>{
            this.$emit('hide')
        })
    },
    methods: {
        modal(status) {
            // show || hide
            $(this.$refs.share).modal(status)
        },
        log(str) {
            console.log(JSON.stringify(str))
        },
    },
    watch: {
        show(newVal, oldVal) {
            if (newVal) {
                this.modal('show')
            }
        }
    },
    computed: {
    }
}
</script>

<style>
.img-board {
  width: 80vh;
  height: 80vh;
}
</style>

<custom1>
  This could be e.g. documentation for the component.
</custom1>
