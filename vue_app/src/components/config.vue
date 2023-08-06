
<script setup>
import { reactive } from "@vue/reactivity";
// import { defineProps, defineEmits } from "vue";
const props = defineProps({
    items: Array
})
const emit = defineEmits()
const items = reactive([]), remove = reactive([])

onMounted(()=>{
    init()
})
const init = () => {
    items.length = 0
    Object.assign(items, JSON.parse(JSON.stringify(props.items)))
}
const add = () => {
    items.push({
        name: '',
        url: '',
        enable: false,
    })
}
const refresh = () => {
    remove.length = 0
    init()
}
const save = () => {
    const remove_ = Object.assign([], JSON.parse(JSON.stringify(remove)))
    emit('save', items, remove_)
    remove.length = 0
}
const del = (item) => {
    if (item['id']) {
        remove.push(item['id'])
    }
    items.splice(items.indexOf(item), 1)
}
const focus = (event) => {
    let el = event.target
    el.contentEditable = true
    el.focus()
    el.style.height = ''
}
const change = (item, key, event) => {
    let el = event.target
    item[key] = el.innerText
    el.contentEditable = false
    el.style.height = '2.5rem'
}

watch(props.items, (newVal, oldVal)=>{
    init()
})

</script>

<template>
    <div class="container">
        <div class="row">
            <div class="col" style="background-color: rgba(251, 241, 227, 0.95);">
                <span class="btn" @click="add"><i class="bi-plus-square"></i></span>
                <span class="btn"  @click="save"><i class="bi bi-sd-card"></i></span>
                <span class="btn"  @click="refresh"><i class="bi bi-recycle"></i></span>
            </div>
        </div>
        <div class="row line">
            <div class="col-2">Key</div>
            <div class="col-8">Value</div>
            <div class="col-1 text-center">En</div>
            <div class="col-1 text-center">del</div>
        </div>
        <div class="row line" v-for="(item, key) in items" :key="key">
            <div class="col-md-2 col-sm-12 overflow-hidden text-break" @dblclick="focus($event)" @blur="change(item, 'key', $event)">{{ item.key }}</div>
            <div class="col-md-8 col-sm-12 overflow-hidden text-break" style="height: 2.5rem" @dblclick="focus($event)" @blur="change(item, 'value', $event)">{{ item.value }}</div>
            <div class="col-md-1 col-sm-12 text-center opt" @click="item.enable = !item.enable"><input type="checkbox" v-model="item.enable"></div>
            <div class="col-md-1 col-sm-12 text-center opt"><i class="fa fa-trash-o" @click="del(item)"></i></div>
        </div>
    </div>
</template>

<style scoped>
.opt {
  cursor: pointer;
}
.br {
    border-right: 1px solid #cccccc
}
.line {
    border-top: 1px solid #cccccc;
    line-height: 2.5rem;
}
</style>
