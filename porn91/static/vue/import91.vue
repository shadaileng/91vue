<template>
    <div ref="import" class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
            <div class="modal-content container">
                <div class="row">
                    <a class="btn" @click="$emit('save', content)"><i class="fa fa-check-square-o"></i></a>
                    <a class="btn" @click="additem"><i class="fa fa-plus-square-o"></i></a>
                    <a class="btn" @click="content=''"><i class="fa fa-close"></i></a>
                </div>
                <div class="row">
                    <div ref="edit" class="col-md-6" style="background-color: rgba(251, 241, 227, 0.95);border-top: 1px solid black;border-right: 1px solid black;">
                        <div class="form-group">
                            <input class="mb-2 mt-2" type="text" name="key" placeholder="输入Key">
                            <input class="mb-2 mt-2" type="text" name="name" placeholder="输入名称">
                            <input class="mb-2 mt-2" type="text" name="src" placeholder="输入关联网页">
                            <input class="mb-2 mt-2" type="text" name="poster" placeholder="输入封面地址">
                            <input class="mb-2 mt-2" type="text" name="publish_date" placeholder="输入发布日期">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <textarea v-model="content" style="background-color: rgba(251, 241, 227, 0.95);resize: none;width: 100%; height: 100%;"></textarea>
                    </div>
                </div>
                <div class="row">
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
        additem() {
            let _obj = {}
            this.$refs.edit.querySelectorAll('input').forEach(el => {
                _obj[el.name] = el.value ? el.value : null
            })
            if (!_obj['key']) return
            _obj['path'] = '/root'
            let add_obj = []
            if (this.content) {
                add_obj = JSON.parse(this.content)
            }
            add_obj.push(_obj)
            this.content = JSON.stringify(add_obj, null, "\t")
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
