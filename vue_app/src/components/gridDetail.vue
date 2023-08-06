<script setup>
import { reactive } from "@vue/reactivity"

const props = defineProps({
    items: Array,
    select: Array,
})
const duration_filter = (duration) => {
    function prefix(num, n = 2, s = 0) {
        if (typeof (num) !== 'number') num = Number(num)
        if (isNaN(num)) num = ''
        return (Array(n).join(s) + num).slice(-n)
    }
    if (!duration) return "00:00"
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
const emit = defineEmits(['selectOne', 'play', 'getlist'])
const select = ref([])
// watch(select.value, (newVal, oldVal)=>{
//     console.log(`select: ${select.value}`)
// })
watch(props.select, (newVal, oldVal)=>{
    select.value.length = 0
    Object.assign(select.value, props.select)
})
</script>
<template>
    <div class="row text-start ps-3">
        <div class="col-12 mb-2 pointer row border-bottom"
            v-for="item, index in items" :key="item.id"
            @click.exact="$emit('selectOne', item.id, $event)"
            @click.ctrl.exact="$emit('selectOne', item.id, $event)"
            data-toggle="tooltip" data-placement="top" :title="item.name">
            <div class="position-relative overflow-hidden col-md-3 col-sm-12 d-none">
                <div class="scale"></div>
                <div :style="{'background-image': `url(${item.poster})`}" class="rounded img"></div>
                <small v-if="item.duration" class="layer">{{ duration_filter(item.duration) }}</small>
                <input class="select" type="checkbox" :value="item.id" v-model="select">
            </div>
            <div class="col-12 container">
                <div class="row justify-content-start">
                    <div class="col-12">
                        <input class="me-2" type="checkbox" :value="item.id" v-model="select">
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
</style>