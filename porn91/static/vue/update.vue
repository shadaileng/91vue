<template>
    <div ref="update" class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
            <div class="modal-content container">
                <div class="row">
                    <div class="col bg-tf">
                        <span class="btn" @click="save"><i class="fa fa-floppy-o"></i></span>
                        <span class="btn" @click="refresh"><i class="fa fa-refresh"></i></span>
                    </div>
                </div>
                <div class="row">
                    <input type="text" class="form-control col-12" name="path" :value="item.path + '/' + item.name" disabled>
                    <input type="text" class="form-control col-8" name="key" v-model="item.key" disabled>
                    <select class="custom-select col-4" name="status" v-model="item.status">
                        <option value="-2">异常</option>
                        <option value="-1">暂停</option>
                        <option value="0">下载中</option>
                        <option value="1">下载完成</option>
                    </select>
                    <input type="text" class="form-control col-12" name="src" v-model="item.src" placeholder="输入下载地址">
                    <input type="text" class="form-control col-12" name="src_local" v-model="item.src_local" placeholder="输入播放地址">
                    <input type="text" class="form-control col-12" name="poster" v-model="item.poster" placeholder="输入封面下载地址">
                    <input type="text" class="form-control col-12" name="poster_local" v-model="item.poster_local" placeholder="输入封面本地地址">
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
                    path: 'path',
                    name: 'name',
                    key: 'key',
                    status: 0,
                    src: 'src',
                    src_local: 'src_local',
                    poster: 'poster',
                    poster_local: 'poster_local',
                }
            }
        },
    props: ['show', 'content'],
    emits: ['hide', 'save', 'refresh'],
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
        refresh() {
            this.$emit('refresh')
        },
        save() {
            this.$emit('save', this.item)

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
