<template>
    <div>
        <div ref="export" class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl modal-dialog-centered" role="document">
                <textarea class="modal-content board" readonly v-model="content" ></textarea>
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
    props: ['content', 'show'],
    emits: ['hide'],
    mounted() {
        // this.modal('show')
        $(this.$refs.export).on('hide.bs.modal', ()=>{
            this.$emit('hide')
        })
    },
    methods: {
        modal(status) {
            // show || hide
            $(this.$refs.export).modal(status)
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
        },
        content(newVal, oldVal) {
            let el = this.$refs.export.querySelector('textarea')
            if (el.scrollTop + el.clientHeight > el.scrollHeight * .90) {
                el.scrollTo(0, el.scrollHeight)
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
