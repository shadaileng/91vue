<template>
    <div class="row">
        <nav class="col-md-8" aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <a @click="$emit('pageToAll')" href="#/">{{path['all']}}</a>
                </li>
                <li v-if="path['uname']" class="breadcrumb-item">
                    <a @click="$emit('pageToAuthorAll')" href="#/">{{path['uname']}}</a>
                </li>
                <li class="breadcrumb-item" aria-current="page">
                    <div class="dropdown d-inline-block">
                        <span class="dropdown-toggle pointer" id="uname_status" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">{{status[path['status'] || '']}}</span>
                        <div class="dropdown-menu" aria-labelledby="uname_status">
                            <a v-for="key in Object.keys(status)" class="dropdown-item" href="#/" @click="$emit('pageToStatus', key)">{{ status[key] }}</a>
                        </div>    
                    </div>
                </li>
                <div class="custom-control custom-switch position-absolute pl-5 mr-3" style="right: 0px;">
                    <span style="left: -16px; position: absolute;">list</span>
                    <input type="checkbox" class="custom-control-input pl-5" id="mode" :checked="mode !== 'list'" @click="switchMode">
                    <label class="custom-control-label" for="mode">grid</label>
                </div>
            </ol>
        </nav>
    </div>
</template>

<script>
export default {
    data() {
        return {
            modeCur: 'list',
            status: {
                '': '全部',
                '1': '完成',
                '0': '下载中',
                '-1': '暂停',
                '-2': '异常',
            }
        }
    },
    props: ['mode', 'path'],
    emits: ['switchMode', 'pageToAll', 'pageToAuthorAll', 'pageToStatus'],
    methods: {
        switchMode(event) {
            let checked = event.currentTarget.checked
            if (checked) {
                this.modeCur = 'grid'
            } else {
                this.modeCur = 'list'
            }
            this.$emit('switchMode', this.modeCur)
        }
    },
    mounted() {
        this.modeCur = this.mode
    },
    watch: {
    },
    computed: {
    }
}
</script>

<style>
.pointer {
    cursor: pointer
}
</style>

<custom1>
  This could be e.g. documentation for the component.
</custom1>
