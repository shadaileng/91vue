<template>
    <div ref="update" class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
            <div class="modal-content container">
                <div class="row">
                    <div class="col bg-tf">
                        <span class="btn" @click="save"><i class="fa fa-terminal"></i></span>
                    </div>
                </div>
                <div class="row">
                    <input type="text" class="col-3" :value="item.command" disabled>
                    <input type="text" class="col" v-for="(value, name) in item.params" :placeholder="name" :value="value" @input="item.params[name] = $event.target.value">
                </div>
                <div class="row bg-tf">
                    <hr>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
            return {
                item: {
                    command: 'loadrflist',
                    params: {
                        range: '1:2'
                    },
                }
            }
        },
    props: ['show', 'content'],
    emits: ['send', 'hide'],
    mounted() {
        // this.modal('show')
        $(this.$refs.update).on('hide.bs.modal', ()=>{
            this.$emit('hide')
            this.item = ''
        })
    },
    methods: {
        modal(status) {
            // show || hide
            $(this.$refs.update).modal(status)
        },
        save() {
            this.$emit('send', this.item)

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
        content: {
            handler(newVal, oldVal) {
                this.item = newVal
                // log(newVal, 'sub')
            },
            deep: true,
        },
    },
    computed: {
    }
}
</script>

<style>
.bg-tf {
    background-color: rgba(251, 241, 227, 0.95);
}
</style>

<custom1>
  This could be e.g. documentation for the component.
</custom1>
