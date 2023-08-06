<script setup>
import pagination from '@/components/pagination.vue'
import config from "@/config"
const VUE_91_API = config.apis.porn91

const props = defineProps({
    items: Array,
    select: Array,
    view: String,
    editable: Boolean,
    page: Object,
})
const duration_filter = (duration) => {
    function prefix(num, n = 2, s = 0) {
        if (typeof (num) !== 'number') num = Number(num)
        if (isNaN(num)) num = ''
        return (Array(n).join(s) + num).slice(-n)
    }
    duration = Number(duration)
    let date = new Date(duration * 1000)
    if (duration < 60) return '00:' + prefix(date.getSeconds())
    if (duration < 60 * 60) return prefix(date.getMinutes()) + ':' + prefix(date.getSeconds())
    return ~~(duration / 3600) + ":" + prefix(date.getMinutes()) + ':' + prefix(date.getSeconds())
}

const size_normalize = (size) => {
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

const emit = defineEmits(['selectOne', 'selectAll', 'play', 'getlist', 'view'])
const selected = ref(props.select.length === props.items.length && props.items.length !== 0)
const select = ref([])

watch(props.select, (newVal, oldVal)=>{
    select.value.length = 0
    Object.assign(select.value, props.select)
    selected.value = props.select.length === props.items.length && props.items.length !== 0
})



const listMap = {
    'grid': "col-xs-12 col-sm-6 col-md-3 mb-2 me-2 pointer row",
    'detail': "col-12 mb-2 pointer row border-bottom",
}
// watch(props.view, (newVal, oldVal)=>{
//     listMap[props.view]
// })
</script>
<template>
    <nav class="row pt-3 ps-3" aria-label="breadcrumb">
        <ol class="breadcrumb col-md-6 col-sm-12 small">
            <slot name="navigate"></slot>
        </ol>
        <div class="col-md-6 col-sm-12 d-flex justify-content-end pointer">
            <ul class="nav nav-tabs">
                <li class="nav-item" v-if="editable" @click.stop="editable && emit('selectAll')">
                    <a class="nav-link_">
                        <span class="pe-2">{{ select.length }} / {{ items.length }}</span>
                        <input type="checkbox" class="mt-1" v-model="selected">
                    </a>
                </li>
                <li class="nav-item" v-for="item,index in ['grid', 'detail']" :key="index">
                    <a class="nav-link" aria-current="page" :class="{active: item === view }" @click="emit('view', item)">{{item}}</a>
                </li>
            </ul>
        </div>
    </nav>
    <div class="row text-start ps-3">
        <div :class="listMap[view]"
            v-for="item, index in items" :key="item.id"
            @click.exact="editable && $emit('selectOne', item.id, $event)"
            @click.ctrl.exact="editable && $emit('selectOne', item.id, $event)"
            data-toggle="tooltip" data-placement="top" :title="item.name">
            <div class="position-relative overflow-hidden col-12"
                v-if="view === 'grid'">
                <div class="scale"></div>
                <!-- <div :style="{'background-image': `url(${item.poster})`}" class="rounded img"></div> -->
                <div v-loadback="{val1: item.poster, val2: item.poster_local !== null && `${(VUE_91_API + '/' + item.poster_local)}`}" class="rounded img"></div>
                <small v-if="item.duration" class="layer">{{ duration_filter(item.duration) }}</small>
                <input v-if="editable" class="select" type="checkbox" :value="item.id" v-model="select">
            </div>
            <div class="col-md-12" v-if="view === 'grid'">
                <div class="row">
                    <a class="title text-sub-title mt-2 disabled"
                        @click.prevent.stop="item.status === 1 && $emit('play', item, index)"> {{ item.name }} </a>
                </div>
                <div class="row">
                    <div class="small d-flex justify-content-between">
                        <a class="text-sub-title" @click.prevent.stop="$emit('getlist', {uname: item.uname, index: 1})"><small>{{ item.uname }}</small></a>
                        <small v-if="item.publish_date" class="d-md-none d-lg-block text-sub-title">{{item.publish_date}}</small>
                    </div>
                </div>
            </div>
            <div class="col-md-12 container" v-if="view === 'detail'">
                <div class="row justify-content-start">
                    <div class="col-12">
                        <input v-if="editable" class="me-2" type="checkbox" :value="item.id" v-model="select">
                        <a class="title text-sub-title mt-2 disabled"  @click.prevent.stop="item.status === 1 && $emit('play', item, index)"> {{ item.name }} </a>
                    </div>
                </div>
                <div class="row small">
                    <div class="col-5 col-lg-3 small"><span class="d-none d-sm-inline d-lg-inline">author: </span><a @click.prevent.stop="$emit('getlist', {uname: item.uname, index: 1})"> {{item.uname}}</a></div>
                    <div class="col-7 col-lg-3 small"><span class="d-none d-sm-inline d-lg-inline">size: </span>{{ size_normalize(item.size) }} / {{ duration_filter(item.duration) }}</div>
                    <div class="col-5 col-lg-2 small"><span class="d-none d-sm-inline d-lg-inline">publish: </span>{{item.publish_date}}</div>
                    <div class="col-7 col-lg-4 small"><span class="d-none d-sm-inline d-lg-inline">update: </span>{{item.updated_at}}</div>
                </div>
            </div>
        </div>
    </div>
    <div class="row" v-if="items.length > 0">
        <div class="col-12">
            <pagination @pageto="index => $emit('getlist', {index})"
                :total_count="page.total"
                :total_page="page.pages"
                :pageno="page.index"
                :count="page.size"></pagination>
        </div>
    </div>
    <span v-if="false"/>
</template>

<style scoped>
.pointer {
    cursor: pointer;
}
.scale {
    margin-top: 60%;
}
.img {
    height: 100%;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: 50%;
}
.title {
    /* display: block; */
    height: 2.4rem;
    line-height: 1.2rem;
    overflow: hidden;
    font-size: .9rem;
}
.layer {
    padding: 0 0.7rem;
    border: none;
    position: absolute;
    bottom: 0.25rem;
    font-size: .875rem;
    right: 0.5rem;
    background-color: rgba(0,0,0,.3);
    color: #f2f2f2;
}
.select {
    position: absolute;
    top: 0.25rem;
    right: 0.25rem;
}

.nav-link_ {
    line-height: 2.5rem;
    color: #6c757d;
    background-color: transparent;
    border-color: transparent;
    margin-bottom: -1px;
    background: 0 0;
    border: 1px solid transparent;
    border-top-left-radius: 0.25rem;
    border-top-right-radius: 0.25rem;
    padding: 0.5rem 1rem;
    text-decoration: none;
    transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out;
}
</style>