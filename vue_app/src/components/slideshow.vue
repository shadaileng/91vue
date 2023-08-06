<script setup>
const props = defineProps({
    items: Array,
})
const scrollTo = (index)=>{
    setTimeout(()=>{
    current.value = index
        const width_total = img_nav.value.offsetWidth
        const left = img_nav.value.querySelectorAll('li')[current.value].offsetLeft
        let scrollTop = left - width_total / 2
        img_nav.value.scrollTo({
            left: scrollTop,
            behavior: 'smooth',
        })
    }, 500)
}
const prev = () => {
    if (current.value <= 0) return
    emit('select', props.items[--current.value])
}
const next = () => {
    if (current.value >= props.items.length - 1) return
    emit('select', props.items[++current.value])
}
const emit = defineEmits()
const img_nav = ref(null), current = ref(0)

const btnHide = ()=>{
    img_nav.value.querySelectorAll('button').forEach(el=>{
        el.style.display = 'none'
    })
}
const btnShow = ()=>{
    img_nav.value.querySelectorAll('button').forEach(el=>{
        el.style.display = 'block'
    })
}

defineExpose({
    scrollTo,
    btnHide,
    btnShow
})
</script>
<template>
    <ul class="list-group list-group-horizontal overflow-scroll" style="overflow-x: auto;" ref="img_nav">
        <button class="carousel-control-prev button_height" type="button" @click="prev();scrollTo(current);" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next button_height" type="button" @click="next();scrollTo(current);" data-bs-target="#carouselExampleControls" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
        </button>
        <li class="list-group-item" v-for="item, index in items" :key="item.id" :class="{active: current === index}">
            <slot :item="item" :index="index"/>
        </li>
    </ul>
</template>
<style scoped>
.button_height {
    position: absolute;
    height: 10%;
    top: 45%;
}
</style>
