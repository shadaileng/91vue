<script setup>
import * as THREE from 'three';
// 引入扩展库OrbitControls.js
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// 引入扩展库GLTFLoader.js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// width和height用来设置Three.js输出的Canvas画布尺寸(像素px)
const width = 800; //宽度
const height = 500; //高度
/**
 * 透视投影相机设置
 */
// // 30:视场角度, width / height:Canvas画布宽高比, 1:近裁截面, 3000：远裁截面
// const camera = new THREE.PerspectiveCamera(30, width / height, 1, 3000);
// camera.position.set(292, 223, 185); //相机在Three.js三维坐标系中的位置
// camera.lookAt(0, 0, 0); //相机观察目标指向Three.js坐标系原点

/**
* 创建场景对象Scene
*/
const scene = new THREE.Scene();

/**
* 相机设置
*/
// const width = window.innerWidth; //窗口宽度
// const height = window.innerHeight; //窗口高度
const k = width / height; //窗口宽高比
const s = 200; //三维场景显示范围控制系数，系数越大，显示的范围越大
//创建相机对象
const camera = new THREE.OrthographicCamera(-s * k, s * k, s, -s, 1, 1000);
camera.position.set(200, 300, 200); //设置相机位置
camera.lookAt(scene.position); //设置相机方向(指向的场景对象)
/**
* 创建渲染器对象
*/
const renderer = new THREE.WebGLRenderer();
renderer.setSize(width, height);//设置渲染区域尺寸
renderer.setClearColor(0xb9d3ff, 1); //设置背景颜色

/**
* 光源设置
*/
//点光源
const point = new THREE.PointLight(0xffffff);
point.position.set(400, 200, 300); //点光源位置
scene.add(point); //点光源添加到场景中
//环境光
const ambient = new THREE.AmbientLight(0x444444);
scene.add(ambient);


/**
* 创建网格模型
*/
// const geometry = new THREE.SphereGeometry(60, 40, 40); //创建一个球体几何对象
const geometry = new THREE.BoxGeometry(100, 200, 100); //创建一个立方体几何对象Geometry
const material = new THREE.MeshLambertMaterial({
color: 0x0000ff
}); //材质对象Material
const mesh = new THREE.Mesh(geometry, material); //网格模型对象Mesh
scene.add(mesh); //网格模型添加到场景中

const container = ref(null)
onMounted(() => {
    container.value.appendChild(renderer.domElement)
    render()
});

const render = () => {
    //执行渲染操作   指定场景、相机作为参数
    mesh.rotateY(.01)
    renderer.render(scene, camera);
    requestAnimationFrame(render);
}

</script>

<template>
    <div class="row" ref="container" style="height: 70%;">

    </div>
</template>
