<script setup>

</script>
<template>
    <svg class="sat-loader" view-box="0 0 100 100">
        <circle class="sat sat-back"></circle>
        <circle class="earth"></circle>
        <ellipse class="orbit"></ellipse>
        <circle class="sat sat-front"></circle>
    </svg>
</template>

<style scoped>
.sat-loader {
    width: 100px;
    height: 100px;
    --center: 50;
    --earth-r: 1.75em;
    --earth-fill: white;
    --earth-stroke: black;
    --earth-stroke-width: 4;
    --orbit-stroke: black;
    --orbit-stroke-width: 1;
    --sat-r: .6em;
    --sat-fill: black;
    --sat-max: 90;
    --sat-min: 10;
    --duration: 1s;
}
.earth {
    cx: var(--center);
    cy: var(--center);
    r: var(--earth-r);
    fill: var(--earth-fill);
    stroke: var(--earth-stroke);
    stroke-width: var(--earth-stroke-width);
}
.orbit {
    cx: var(--center);
    cy: var(--center);
    rx: 3em;
    ry: .3em;
    fill: none;
    stroke: var(--orbit-stroke);
    stroke-width: var(--orbit-stroke-width);
    transform-origin: center;
    transform: rotate(-45deg);
    stroke-dasharray: 220 55;
    stroke-dashoffset: 100;
}

.sat {
    r: var(--sat-r);
    fill: var(--sat-fill);
}
.sat-front {
    animation: sat-orbit var(--duration) ease-in-out infinite,
        orbit-front var(--duration) ease-in-out infinite;
}
.sat-back {
    animation: sat-orbit var(--duration) ease-in-out infinite;
}

@keyframes sat-orbit {
    0%, 100% {
        cx: var(--sat-max);
        cy: var(--sat-min);
    }
    50% {
        cx: var(--sat-min);
        cy: var(--sat-max);
    }
}
@keyframes orbit-front {
    0%, 49% {
        opacity: 0;
    }
    50% {
        opacity: 1;
    }
}
</style>