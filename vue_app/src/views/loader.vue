<script setup>
import loaderMobius from '@/components/loaderMobius.vue'
import loaderRotateCube from '@/components/loaderRotateCube.vue'
import loaderSatorbit from '@/components/loaderSatorbit.vue'
import loaderCubes from '@/components/loaderCubes.vue'
import switched from '@/components/switch.vue'

</script>
<template>
    <div class="loader" style="height: 70%;">
        <loaderCubes></loaderCubes>
        <loaderRotateCube style="--width: 200px;"></loaderRotateCube>
        <loaderMobius style="--duration: 2s;--width: 300px;"></loaderMobius>
        <loaderSatorbit style="--duration: 1s"></loaderSatorbit>
        <switched style="--width: 60px" :mode="false"></switched>
    </div>
</template>

<style scoped>
.loader {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
