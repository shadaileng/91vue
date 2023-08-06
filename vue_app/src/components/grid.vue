<script setup>
import { reactive } from "@vue/reactivity"
const VUE_91_API = config.apis.porn91

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
    duration = Number(duration)
    let date = new Date(duration * 1000)
    if (duration < 60) return '00:' + prefix(date.getSeconds())
    if (duration < 60 * 60) return prefix(date.getMinutes()) + ':' + prefix(date.getSeconds())
    return ~~(duration / 3600) + ":" + prefix(date.getMinutes()) + ':' + prefix(date.getSeconds())
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
        <div class="col-xs-12 col-sm-6 col-md-3 mb-2 me-2 pointer row"
            v-for="item, index in items" :key="item.id"
            @click.exact="$emit('selectOne', item.id, $event)"
            @click.ctrl.exact="$emit('selectOne', item.id, $event)"
            data-toggle="tooltip" data-placement="top" :title="item.name">
            <div class="position-relative overflow-hidden col-12">
                <div class="scale"></div>
                <!-- <div :style="{'background-image': `url(${item.poster})`}" class="rounded img"></div> -->
                <div v-loadback="{val1: item.poster, val2: `${VUE_91_API}/${item.poster_local}`}" class="rounded img"></div>
                <small v-if="item.duration" class="layer">{{ duration_filter(item.duration) }}</small>
                <input class="select" type="checkbox" :value="item.id" v-model="select">
            </div>
            <div class="col-md-12">
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
    display: block;
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