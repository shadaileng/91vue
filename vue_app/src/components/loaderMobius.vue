<script setup>

</script>
<template>
    <div class="mobius inline-block">
        <div class="lt"><div></div></div>
        <div class="lb"><div></div></div>
        <div class="rt"><div></div></div>
        <div class="rb"><div></div></div>
    </div>
</template>

<style scoped>
.mobius {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    --duration: 1s;
    --width: 300px;
    --height: calc(var(--width) / 2);
}
.mobius::before,
.mobius::after {
    content: "";
    width: calc(var(--width) / 2);
    height: var(--height);
    border-radius: 50%;
    border: calc(var(--height) / 10) solid #57606f;
    box-sizing: border-box;
    position: relative;
    z-index: 1;
}
.mobius::after {
    left: calc(var(--height) / -10);
}
.mobius div {
    width: calc(var(--width) / 2);
    height: var(--height);
    position: absolute;
    left: 0;
    clip-path: polygon(0 0, 100% 0, 100% 50%, 0 50%);
    z-index: 2;
}
.mobius div div {
    width: calc(var(--width) / 2);
    height: var(--height);
    box-sizing: border-box;
    border-style: solid;
    border-width: calc(var(--height) / 10);
    border-color: #f08080 #f08080 transparent transparent;
    border-radius: 50%;
    transform: rotate(135deg);
    animation: roll var(--duration) linear infinite;
}

.lb {
    transform: scale(-1, -1)
}
.rt {
    transform: translateX(calc(100% - var(--height) / 10)) scale(-1, 1)
}
.rb {
    transform: translateX(calc(100% - var(--height) / 10)) scale(1, -1)
}

.mobius .rb div {
    animation-delay: calc(var(--duration) / 4);
}
.mobius .rt div {
    animation-delay: calc(var(--duration) / 4 * 2);
}
.mobius .lb div {
    animation-delay: calc(var(--duration) / 4 * 3);
}

@keyframes roll {
    50%, 100% {
        transform: rotate(495deg);
    }
}
</style>
