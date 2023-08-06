<template>
    <div class="row pb-4 text-muted title-bg" >
        <div class="col-md-12 pb-2 pt-2 row">
            <div class="col-md-4 col-sm-12">
                <input @click.stop="selectAll" v-model="selected" type="checkbox">
                <span class="ml-3">已选中 {{selectItems.length}} / {{items.length}} </span>
            </div>
            <div class="col-md-8 row">
                <div class="col-md-8 d-none d-md-block text-center">
                    文件
                </div>
                <div class="col-md-4 d-none d-md-block text-center">
                    进度
                </div>
            </div>
        </div>
        <div v-for="item in items" :data-key="item.id" class="col-md-12 pt-2 pb-2 row fileitem" @click="selectOne(item.id, $event)" style="border-top: 1px solid cadetblue;">
            <div class="col-md-8" style="cursor: pointer;">
                <div v-if="item.content_type == 'd'">
                    <input @click.stop="selectOne(item.id, $event)" class="select" type="checkbox" :value="item.id" v-model="selectItems">
                    <i class="fa fa-folder-o ml-3 mr-3"></i>
                    <a href=""> {{item.name}}</a>
                </div>
                <div v-else data-toggle="tooltip" data-placement="top" :title="item.name">
                    <input @click.stop="selectOne(item.id, $event)" class="select" type="checkbox" :value="item.id" v-model="selectItems">
                    <i class="fa fa-file-o ml-3 mr-3"></i>
                    <a v-if="item.status !=1" class="disabled">{{item.name}}</a>
                    <a v-else @click.prevent.stop="this.$router.push({name: 'view', path: '/view', params: { path: ['root', item.uname, item.name], url: '/' + item.src_local, poster: '/' + item.poster_local, thumbnails: item.thumbnails ? '/' + item.thumbnails: '' }})" :href="'#/view/' + item.key">{{item.name}}</a>
                </div>
                <div class="row small">
                    <div class="col-5 col-lg-3 small"><span class="d-none d-sm-inline d-lg-inline">author: </span><a @click.prevent.stop="$emit('pageTo', item.uname)" href="#/"> {{item.uname}}</a></div>
                    <div class="col-7 col-lg-2 small"><span class="d-none d-sm-inline d-md-none">size: </span>{{ size_normalize(item.size) }}</div>
                    <div class="col-5 col-lg-3 small"><span class="d-none d-sm-inline d-lg-inline">publish: </span>{{item.publish_date}}</div>
                    <div class="col-7 col-lg-4 small"><span class="d-none d-sm-inline d-lg-inline">update: </span>{{item.updated_at}}</div>
                </div>
            </div>
            <div class="col-md-4 progress-zone">
                <div class="progress">
                    <div v-if="item.status === 1" class="progress-bar w-100" role="progressbar"
                        aria-valuenow="100" aria-valuemin="0"
                        aria-valuemax="100">100%</div>
                    <div v-else-if="item.status === 0 && item.status_data" class="progress-bar" :style="{width: item.status_data.scale + '%'}" role="progressbar"
                        aria-valuenow="0" aria-valuemin="0"
                        aria-valuemax="100">{{ (item.status_data.scale != undefined ? item.status_data.scale.toFixed(2) : 0) + '%' }}</div>
                    <div v-else class="progress-bar w-0" role="progressbar"
                        aria-valuenow="0" aria-valuemin="0"
                        aria-valuemax="100">0%</div>
                </div>
                <div v-if="item.status === 0 && item.status_data !== undefined" class="row pt-2 small info">
                    <div class="col-5 info-s">{{ size_normalize(item.status_data.total) }}</div>
                    <div class="col-5 info-v">{{ size_normalize(item.status_data.speed) + '/s' }}</div>
                    <div class="col-2 info-t">{{ item.status_data.threadNum != undefined ? item.status_data.threadNum : 0 }}</div>
                </div>
                <div v-else class="row pt-2 small info">
                    <div class="col-5 info-s">0</div>
                    <div class="col-5 info-v">0</div>
                    <div class="col-2 info-t">0</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            selected: false,
            selectItems: [],
        }
    },
    props: ['items'],
    emits: ['select', 'pageTo'],
    methods: {
        selectAll(){
            if (!this.items) return
            this.selectItems = []
            if (!this.selected) {
                this.items.forEach(el => {
                    this.selectItems.push(el.id)
                })
            }
        },
        selectOne(id, event) {
            if (event && event.target.tagName === "INPUT") {
                if (event.target.checked) {
                    this.selectItems.push(id)
                } else {
                    this.selectItems.splice(this.selectItems.indexOf(id), 1)
                }
                this.selectItems = this.selectItems
                return
            }
            this.selectItems = [id]
        },
        size_normalize(size) {
            if (size === undefined) return 0
            function foematNum(num) {
                return Math.round(num * 1000) / 1000
            }
            if (size == 0) return 0
            if (size < 1024) return foematNum(size) + "b"
            if (size < 1024 * 1024) return foematNum(size / 1024) + "K"
            if (size < 1024 * 1024 * 1024) return foematNum(size / 1024 / 1024) + "M"
            if (size < 1024 * 1024 * 1024 * 1024) return foematNum(size / 1024 / 1024 / 1024) + "M"
            return 0
        }
    },
    watch: {
        items: {
            handler(newVal, oldVal) {
                this.selectItems = []
                // log(newVal)
            },
            // deep: true,
        },
        selectItems: {
            handler(newVal, oldVal) {
                if (!this.items) return
                if (newVal.length === this.items.length) {
                    this.selected = true
                } else {
                    this.selected = false
                }
                // console.log('selectItems', newVal.length)
                this.$emit('select', newVal)
            },
            deep: true,
        }
    },
    computed: {
    }
}
</script>

<style>
.title-bg {
  background-color: rgba(255, 255, 255, 0.976);
}
</style>

<custom1>
  This could be e.g. documentation for the component.
</custom1>
