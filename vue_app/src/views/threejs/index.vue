<script setup>
import menuLayout from '@/components/menuLayout.vue'
import firstScene from "@/components/threejs/firstScene.vue";
import materialLight from "@/components/threejs/materialLight.vue";
import materialLightAnimation from "@/components/threejs/materialLightAnimation.vue";
import ctrl from "@/components/threejs/ctrl.vue";
import Geometrys from "@/components/threejs/Geometrys.vue";
import GeometryProperty from "@/components/threejs/GeometryProperty.vue";
import SwitchCamera from "@/components/threejs/SwitchCamera.vue";
import CameraFollow from "@/components/threejs/CameraFollow.vue";
import Light from "@/components/threejs/Light.vue";
import Helper from "@/components/threejs/Helper.vue";
import Clock from "@/components/threejs/Clock.vue";
import GSAP from "@/components/threejs/GSAP.vue";
import BufferGeometry from "@/components/threejs/BufferGeometry.vue";
import Texture from "@/components/threejs/Texture.vue";
import ctrlcube from "@/components/threejs/ctrlcube.vue";
onMounted(() => {

});

const tabName = ref('Texture')
const currentTab = computed(()=>{
    return tabs[tabName.value].com
})
const tabs = reactive({
    firstScene: {
        name: '第一个场景',
        com: shallowRef(firstScene),
    },
    Helper: {
        name: '辅助工具',
        com: shallowRef(Helper),
    },
    materialLight: {
        name: '材质和光照',
        com: shallowRef(materialLight),
    },
    Texture: {
        name: '贴图',
        com: shallowRef(Texture),
    },
    Light: {
        name: '环境光',
        com: shallowRef(Light),
    },
    materialLightAnimation: {
        name: '动画',
        com: shallowRef(materialLightAnimation),
    },
    ctrl: {
        name: '控制和状态',
        com: shallowRef(ctrl),
    },
    SwitchCamera: {
        name: '切换摄像机',
        com: shallowRef(SwitchCamera),
    },
    CameraFollow: {
        name: '相机跟随',
        com: shallowRef(CameraFollow),
    },
    Clock: {
        name: '时钟',
        com: shallowRef(Clock),
    },
    GSAP: {
        name: 'GSAP',
        com: shallowRef(GSAP),
    },
    Geometrys: {
        name: '几何体',
        com: shallowRef(Geometrys),
    },
    GeometryProperty: {
        name: '几何体属性',
        com: shallowRef(GeometryProperty),
    },
    BufferGeometry: {
        name: '缓存几何体',
        com: shallowRef(BufferGeometry),
    },
    ctrlcube: {
        name: '控制几何体',
        com: shallowRef(ctrlcube),
    },
})


</script>
<template>
    <menuLayout>
        <template v-slot:section>
            <a class="list-group-item list-group-item-action" :class="{active: tabName === key}" @click="tabName = key" v-for="(tab, key) in tabs" :key="key" role="tab">{{tab.name}}</a>
        </template>
        <template v-slot:main>
            <component :is="currentTab"></component>
        </template>
    </menuLayout>
</template>
<style scoped>
</style>
