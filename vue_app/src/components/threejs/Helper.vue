<script setup>
import {AmbientLight, PointLight, Scene, OrthographicCamera, WebGLRenderer} from 'three';
import { PlaneGeometry, BoxGeometry, SphereGeometry, MeshBasicMaterial, MeshLambertMaterial, Mesh } from 'three';
import { Vector3, ArrowHelper, AxesHelper, CameraHelper } from 'three';
// 引入扩展库OrbitControls.js
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// 引入扩展库GLTFLoader.js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const canvasRef = ref(null)

// width和height用来设置js输出的Canvas画布尺寸(像素px)
const width = 600; //宽度
const height = 450; //高度

/**
* 创建场景对象Scene
*/
const scene = new Scene();

/**
* 相机设置
*/
const k = width / height; //窗口宽高比
const s = 20; //三维场景显示范围控制系数，系数越大，显示的范围越大
//创建相机对象
const camera = new OrthographicCamera(-s * k, s * k, s, -s, 1, 1000);
camera.position.set(-30, 40, 30); //设置相机位置
camera.lookAt(scene.position); //设置相机方向(指向的场景对象)

const cameraHelper = new CameraHelper(camera)
scene.add(cameraHelper)

const arrowHelper = new ArrowHelper( new Vector3(1, 2, 0).normalize(), new Vector3(0, 0, 0), 1, 0xffff00 );
scene.add( arrowHelper )

const axesHelper = new AxesHelper(20)
scene.add(axesHelper)


const planeGeometry = new PlaneGeometry(100, 20)
const planeBasicMaterial = new MeshBasicMaterial({color: '#cccccc'})
const plane = new Mesh(planeGeometry, planeBasicMaterial)
plane.rotateX(-Math.PI / 2)
// plane.rotation.x = -Math.PI / 2
scene.add(plane);

let renderer = null
let controls = null
onMounted(() => {
    /**
    * 创建渲染器对象
    */
    renderer = new WebGLRenderer({canvas: canvasRef.value});
    // renderer.setPixelRatio(2)
    renderer.setSize(width, height, true);//设置渲染区域尺寸
    renderer.setClearColor(0xb9d3ff, 1); //设置背景颜色
    controls = new OrbitControls(camera, renderer.domElement);//创建控件对象
    controls.enableDamping = true
    // controls.addEventListener('change', render);//监听鼠标、键盘事件
    render()
});


const render = () => {
    controls.update()
    //执行渲染操作   指定场景、相机作为参数
    renderer.render(scene, camera);
    requestAnimationFrame(render);
}

</script>

<template>
    <canvas ref="canvasRef"></canvas>
</template>
