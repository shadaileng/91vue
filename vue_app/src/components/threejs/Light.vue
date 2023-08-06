<script setup>
import {AmbientLight, PointLight, AxesHelper, Scene, CameraHelper, OrthographicCamera, WebGLRenderer} from 'three';
import { PlaneGeometry, BoxGeometry, SphereGeometry, MeshBasicMaterial, MeshLambertMaterial, Mesh } from 'three';
import { Color } from 'three';
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
//创建相机对象
const camera = new OrthographicCamera(-s * k, s * k, s, -s, 1, 1000);
camera.position.set(-30, 40, 30); //设置相机位置
camera.lookAt(scene.position); //设置相机方向(指向的场景对象)

const cameraHelper = new CameraHelper(camera)
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
    controls = new OrbitControls(camera, renderer.domElement);//创建控件对象
    controls.enableDamping = true
    // controls.addEventListener('change', render);//监听鼠标、键盘事件
    render()
});

const options = ref({
    rotateSpeed: .02,
    runSpeed: 1,
    ambient: '#0c0c0c',
})
ambient.color = new Color(options.value.ambient)
let angle = 0
const render = () => {
    controls.update()
    stats.update()
    const rotateSpeed = options.value.rotateSpeed
    cube.rotation.x += rotateSpeed
    cube.rotation.y += rotateSpeed
    cube.rotation.z += rotateSpeed
    angle += options.value.runSpeed
    if (angle === 360) angle = 0
    const rad = Math.PI / 180 * angle
    sphere.position.x = 20 + 10 * Math.cos(rad)
    sphere.position.y = 2 + 10 * Math.abs(Math.sin(rad))
    //执行渲染操作   指定场景、相机作为参数
    renderer.render(scene, camera);
    requestAnimationFrame(render);
}
const initGui = () => {
    if (document.querySelectorAll('.dg.main.a').length > 0) {
        return
    }
    const gui = new dat.GUI()
    gui.add(options.value, "rotateSpeed", 0, 1)
    gui.add(options.value, "runSpeed", 0, 10)
    gui.addColor(options.value, 'ambient').onChange(el=>{
    ambient.color = new Color(el)
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
