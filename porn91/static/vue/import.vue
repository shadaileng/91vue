<template>
    <div>
        <div ref="import" class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
                <div class="modal-content board">
                    <textarea class="modal-content board" v-model="content" placeholder="import conten here"></textarea>
                    <div class="position-absolute" style="right: 0; cursor: pointer">
                        <a class="btn" @click="$emit('save', content)"><i class="fa fa-check-square-o"></i></a>
                        <a class="btn" @click="content=''"><i class="fa fa-close"></i></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
            return {
                content: ''
            }
        },
    props: ['show'],
    emits: ['hide', 'save'],
    mounted() {
        // this.modal('show')
        $(this.$refs.import).on('hide.bs.modal', ()=>{
            this.$emit('hide')
            this.content = ''
        })
    },
    methods: {
        modal(status) {
            // show || hide
            $(this.$refs.import).modal(status)
        },
        log(str) {
            console.log(JSON.stringify(str))
        },
    },
    watch: {
        show(newVal, oldVal) {
            if (newVal) {
                this.modal('show')
            } else {
                this.modal('hide')
            }
        },
    },
    computed: {
    }
}
</script>

<style>
.board {
  resize: none;
  height: 80vh;
}
</style>

<custom1>
  This could be e.g. documentation for the component.
</custom1>
