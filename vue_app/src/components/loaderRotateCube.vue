<script setup>

</script>
<template>
    <div class="rotate-cube"></div>
</template>

<style scoped>
.rotate-cube {
    --duration: .5s;
    --width: 48px;
    width: var(--width);
    height: var(--width);
    position: relative;
    margin: 20px;
}
.rotate-cube:before {
    content: '';
    width: var(--width);
    height: calc(var(--width) * .2);
    background: #f0808050;
    position: absolute;
    top: calc(var(--width) * .8);
    left: 0;
    border-radius: 50%;
    animation: shadow01 var(--duration) linear infinite;
}
.rotate-cube:after {
    content: '';
    width: 60%;
    height: 60%;
    background: #f08080;
    position: absolute;
    top: 0;
    left: 20%;
    border-radius: 4px;
    animation: jump01 var(--duration) linear infinite;
}
@keyframes jump01 {
    15% {
        border-bottom-right-radius: calc(var(--width) * .2);
    }
    25% {
        transform: translateY(calc(var(--width) / 6)) rotate(22.5deg);
    }
    50% {
        transform: translateY(calc(var(--width) / 3)) rotate(45deg);
        border-bottom-right-radius: calc(var(--width) * .4);
    }
    75% {
        transform: translateY(calc(var(--width) / 6)) rotate(67.5deg);
    }
    100% {
        transform: translateY(calc(var(--width) * 0)) rotate(90deg);
    }
}

@keyframes shadow01 {
    0%,100% {
        transform: scale(.6, 1);
    }
    50% {
        transform: scale(1, 1);
    }
}
</style>
