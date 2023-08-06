<script setup>
const props = defineProps({
    selector: String,
})
</script>
<template>
    <div class="top">
        <div @click="event=>{const el = event.target.getRootNode().querySelector(selector); el.scrollTo({left: 0, top: 0, behavior: 'smooth'})}"><i class="bi bi-arrow-up-square"></i></div>
        <div  @click="event=>{const el = event.target.getRootNode().querySelector(selector); el.scrollTo({left: 0, top: el.scrollHeight, behavior: 'smooth'})}"><i class="bi bi-arrow-down-square"></i></div>
    </div>
</template>

<style scoped>
.top{
    cursor: pointer;
    width: 60px;
    /* height: 40px; */
    border-radius: 10px;
    background: rgba(128, 128, 128, 0.92);
    color: blue;
    opacity: 0.5;
    line-height: 50px;
    text-align: center;
    font-size: 25px;
    position: absolute;
    bottom: 15%;
    right: 10%;
    /* display: none; */
}
</style>