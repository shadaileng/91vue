<template>
    <div class="row pb-4 video-grid text-muted">
        <div class="col-md-12 pb-2 pt-2 title-bg">
            <input @click.stop="selectAll" v-model="selected" type="checkbox">
            <span class="ml-3">已选中 {{selectItems.length}} / {{items.length}}</span>
        </div>
        <div v-for="item in items" :data-key="item.id" class="col-md-3 col-sm-6 col-12 fileitem mb-2 pointer"
            data-toggle="tooltip" data-placement="top" :title="item.name" @click="selectOne(item.id, $event)">
            <div :class="{'video-elem': true, 'video-elem-0': item.status==0, 'video-elem--1': item.status==-1 || item.status==-2}">
                <div class="display d-block">
                    <div class="scale"></div>
                    <div v-if="item.content_type == 'd'" class="img" style="background-image: url('/static/app/folder.png')"></div>
                    <div v-else class="img" style="background-size: cover" :style="{'background-image': 'url(/' + item.poster_local + ')'}"></div>
                    <small v-if="item.duration" class="layer">{{ duration_filter(item.duration) }}</small>
                    <input class="select" type="checkbox" @click.stop="selectOne(item.id, $event)" :value="item.id" v-model="selectItems">
                </div>
                <a class="title text-sub-title mt-2 ml-3 mr-3 disabled" v-if="item.status != 1"> {{ item.name }} </a>
                <a class="title text-sub-title mt-2 ml-3 mr-3" v-else @click.prevent.stop="this.$router.push({name: 'view', path: '/view', params: { path: ['root', item.uname, item.name], url: '/' + item.src_local, poster: '/' + item.poster_local, thumbnails: item.thumbnails ? '/' + item.thumbnails: '' }})" :href="'#/view/' + item.key"> {{ item.name }} </a>
                <a class="text-sub-title mt-2 ml-3 mr-3" @click.prevent.stop="$emit('pageTo', item.uname)" :href="'#/' + item.uname"><small>{{ item.uname }}</small></a>
                <small v-if="item.publish_date" class="d-md-none d-lg-block text-sub-title float-right mr-3">{{item.publish_date}}</small>
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
            log(this.selectItems)
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
        loadPoster() {
            this.items.forEach(item => {
                let img = new Image()
                img.onload = function () {
                    console.log('successed load ' + item.poster_local)
                }
                img.onerror = function () {
                    item.poster_local = 'static/app/404.png'
                }
                if (!item.poster_local) item.poster_local = 'static/app/404.png'
                img.src = '/' + item.poster_local
            })
        },
        duration_filter(duration) {
            if (prefix === undefined) return ''
            duration = Number(duration)
            let date = new Date(duration * 1000)
            if (duration < 60) return '00:' + prefix(date.getMilliseconds())
            if (duration < 60 * 60) return prefix(date.getMinutes()) + ':' + prefix(date.getMilliseconds())
            return ~~(duration / 3600) + ":" + prefix(date.getMinutes()) + ':' + prefix(date.getMilliseconds())
        }
    },
    mounted() {
        this.loadPoster()
    },
    watch: {
        items: {
            handler(newVal, oldVal) {
                this.selectItems = []
                this.loadPoster()
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
.pointer {
    cursor: pointer;
}
.video-elem {
    background-color: #f8f9fa;
}
.video-elem .display {
    position: relative;
    overflow: hidden;
    background-color: #ced4da;
    color: #fff;
}

.video-elem .display .scale {
    margin-top: 60%;
}
.video-elem .display .img {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: 50%;
    border-radius: 5px;
}
.video-elem .title {
    display: block;
    height: 2.4rem;
    line-height: 1.2rem;
    overflow: hidden;
    font-size: .9rem;
}
.video-elem .display .layer {
    padding: 0 .7rem;
    border: none;
    position: absolute;
    bottom: .25rem;
    font-size: .875rem;
    right: .5rem;
    background-color: rgba(0,0,0,.3);
    color: #f2f2f2;
}

.video-elem--1 {
    box-shadow:2px 2px 8px rgb(245, 85, 85), -2px 2px 8px rgb(245, 85, 85);
    border-radius: 5px; 
    border-right: 1px solid rgb(245, 85, 85);
}

.video-elem-0 {
    box-shadow:2px 2px 8px rgb(47, 206, 47), -2px 2px 8px rgb(47, 206, 47);
    border-radius: 5px; 
    border-right: 1px solid rgb(47, 206, 47);
}

.video-elem input {
    position: absolute;
    top: .25rem;
    right: .25rem;
}

</style>

<custom1>
  This could be e.g. documentation for the component.
</custom1>
