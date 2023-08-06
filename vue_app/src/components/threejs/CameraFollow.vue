<script setup>
import {AmbientLight, PointLight, AxesHelper, Scene, CameraHelper, OrthographicCamera, PerspectiveCamera, WebGLRenderer} from 'three';
import { PlaneGeometry, BoxGeometry, SphereGeometry, MeshBasicMaterial, MeshLambertMaterial, Mesh } from 'three';
import { Vector3 } from 'three';
import Stats from 'stats.js'
import * as dat from 'dat.gui'
// 引入扩展库OrbitControls.js
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// 引入扩展库GLTFLoader.js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// width和height用来设置js输出的Canvas画布尺寸(像素px)
const width = 600; //宽度
const height = 450; //高度
const canvasRef = ref(null)
const statsRef = ref(null)

/**
* 创建场景对象Scene
*/
const scene = new Scene();
const stats = new Stats()
/**
* 相机设置
*/

const k = width / height; //窗口宽高比
const s = 20; //三维场景显示范围控制系数，系数越大，显示的范围越大
const orthographicCamera = new OrthographicCamera(-s * k, s * k, s, -s, 1, 1000)
const perspectiveCamera = new PerspectiveCamera(45, height/ width, 1, 1000)
//创建相机对象
const cameraRef = ref(orthographicCamera)
cameraRef.value.position.set(-30, 40, 30); //设置相机位置
cameraRef.value.lookAt(scene.position); //设置相机方向(指向的场景对象)

const cameraHelper = new CameraHelper(cameraRef.value)
// scene.add(cameraHelper)

const axesHelper = new AxesHelper(20)
scene.add(axesHelper)

/**
* 光源设置
*/
//点光源
const point = new PointLight(0xffffff);
point.castShadow = true
point.position.set(40, 20, 30); //点光源位置
scene.add(point); //点光源添加到场景中
//环境光
const ambient = new AmbientLight(0x444444);
scene.add(ambient);

const planeGeometry = new PlaneGeometry(100, 20)
const planeBasicMaterial = new MeshLambertMaterial({color: '#cccccc'})
const plane = new Mesh(planeGeometry, planeBasicMaterial)
plane.receiveShadow = true
plane.rotateX(-Math.PI / 2)
scene.add(plane);


const cubeGeometry = new BoxGeometry(4, 4, 4)
const cubeBasicMaterial = new MeshLambertMaterial({color: '#cc0000', wireframe: false})
const cube = new Mesh(cubeGeometry, cubeBasicMaterial)
cube.castShadow = true
cube.position.set(2, 2, 2)
scene.add(cube);

const sphereGeometry = new SphereGeometry(2)
const sphereBasicMaterial = new MeshLambertMaterial({color: '#0000cc', wireframe: false})
const sphere = new Mesh(sphereGeometry, sphereBasicMaterial)
sphere.castShadow = true
sphere.position.set(12, 2, 2)
scene.add(sphere);

let renderer = null
let controls = null
onMounted(() => {
    stats.showPanel(0)
    statsRef.value.append(stats.dom)
    initGui()
    /**
    * 创建渲染器对象
    */
    renderer = new WebGLRenderer({canvas: canvasRef.value});
    // renderer.setPixelRatio(2)
    renderer.setSize(width, height, true);//设置渲染区域尺寸
    renderer.setClearColor(0xb9d3ff, 1); //设置背景颜色
    renderer.shadowMap.enabled = true
    controls = new OrbitControls(cameraRef.value, renderer.domElement);//创建控件对象
    controls.enableDamping = true
    // controls.addEventListener('change', render);//监听鼠标、键盘事件
    render()

});

const options = ref({
    camera: 'OrthographicCamera',
})
let angle = 0
const render = () => {
    controls.update()
    stats.update()
    angle += 1
    if (angle === 360) angle = 0
    const rad = Math.PI / 180 * angle
    const x = 10 * Math.cos(rad)
    const z = 10 * Math.sin(rad)
    const followPos = new Vector3(x, 5, z)
    sphere.position.copy(followPos)
    cameraRef.value.lookAt(followPos)
    //执行渲染操作   指定场景、相机作为参数
    renderer.render(scene, cameraRef.value);
    requestAnimationFrame(render);
}
const initGui = () => {
    if (document.querySelectorAll('.dg.main.a').length > 0) {
        return
    }
    const gui = new dat.GUI()
    gui.add(options.value, 'camera', ['OrthographicCamera', 'PerspectiveCamera']).onChange(el=>{
        if(el === 'PerspectiveCamera') {
            cameraRef.value = perspectiveCamera
        } else {
            cameraRef.value = orthographicCamera
        }
        cameraRef.value.position.set(-30, 40, 30); //设置相机位置
        cameraRef.value.lookAt(scene.position); //设置相机方向(指向的场景对象)
        var controls = new OrbitControls(cameraRef.value, renderer.domElement);//创建控件对象

    })
}

onUnmounted(()=>{
    document.querySelectorAll('.dg.main.a').forEach(el=>{
        el.parentElement.removeChild(el)
    })
})
</script>

<template>
    <div ref="statsRef"></div>
    <canvas ref="canvasRef"></canvas>
</template>
