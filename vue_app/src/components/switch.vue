<script setup>
const mode = ref(false)
</script>
<template>
    <div class="checkbox" @click="mode = !mode">
        <input type="checkbox" v-model="mode"/>
        <label class="a"></label>
    </div>
</template>

<style scoped>
.checkbox {
    --width: 60px;
    --left: -100%;
    --right: -20%;
    --duration: .5s;
    position: relative;
    width: var(--width);
    height: calc(var(--width) / 2);
}
.checkbox::before {
    content: '';
    position: absolute;
    top: 0;
    height: 100%;
    width: calc(var(--width) / 2);
    background: #243548;
    border-radius: 50%;
    box-shadow: calc(var(--width) * .4) 0px 0px #243548;
    transform: translate(var(--left));
}
.checkbox label{
    position: absolute;
    z-index: 2;
    width: 50%;
    height: 100%;
    background: #eebb00;
    border-radius: 50%;
    transform: translate(var(--left)) scale(1.1);
    box-shadow: 0px 0px 15px 0px #eebb00;
    transition: transform .4s ease-in-out;
    cursor: pointer;
}
.checkbox input {
    position: absolute;
    z-index: 0;
    opacity: 0;
    visibility: hidden;
}
.checkbox input:checked + label{
    transform: translate(var(--right)) scale(1.1);
    animation: checked var(--duration) linear;
    background: #00ff00;
}
.checkbox input:not(checked) + label{
    /* transform: translate(90%) scale(1.1); */
    animation: unchecked var(--duration) linear;
    background: #ff3300;
}
@keyframes checked {
    10%, 90% {
        background: #ccff00;
    }
    0% {
        transform: translate(var(--left)) scale(1.1);
    }
    50% {
        transform: translate(-50%) scale(.6);
    }
    100% {
        transform: translate(var(--right)) scale(1.1);
    }
}
@keyframes unchecked {
    10%, 90% {
        background: #ccff00;
    }
    0% {
        transform: translate(var(--right)) scale(1.1);
    }
    50% {
        transform: translate(-50%) scale(.6);
        background: #ccff00;
    }
    100% {
        transform: translate(var(--left)) scale(1.1);
    }
}
</style>