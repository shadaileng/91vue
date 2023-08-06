<script setup>
import {AmbientLight, PointLight, AxesHelper, Scene, CameraHelper, OrthographicCamera, WebGLRenderer} from 'three';
import { PlaneGeometry, BoxGeometry, SphereGeometry, MeshBasicMaterial, MeshLambertMaterial, Mesh } from 'three';
import { BufferGeometry, BufferAttribute } from 'three';
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

const vertices = [
    // front
    {pos: [-1, -1, 1], nor: [0, 0, 1], uv: [0, 0]},
    {pos: [ 1, -1, 1], nor: [0, 0, 1], uv: [1, 0]},
    {pos: [-1,  1, 1], nor: [0, 0, 1], uv: [0, 1]},
    {pos: [-1,  1, 1], nor: [0, 0, 1], uv: [0, 1]},
    {pos: [ 1, -1, 1], nor: [0, 0, 1], uv: [1, 0]},
    {pos: [ 1,  1, 1], nor: [0, 0, 1], uv: [1, 1]},
    // back
    {pos: [ 1, -1, -1], nor: [0, 0, -1], uv: [0, 0]},
    {pos: [-1, -1, -1], nor: [0, 0, -1], uv: [1, 0]},
    {pos: [ 1,  1, -1], nor: [0, 0, -1], uv: [0, 1]},
    {pos: [ 1,  1, -1], nor: [0, 0, -1], uv: [0, 1]},
    {pos: [-1, -1, -1], nor: [0, 0, -1], uv: [1, 0]},
    {pos: [-1,  1, -1], nor: [0, 0, -1], uv: [1, 1]},
    // left
    {pos: [-1, -1, -1], nor: [-1, 0, 0], uv: [0, 0]},
    {pos: [-1, -1,  1], nor: [-1, 0, 0], uv: [1, 0]},
    {pos: [-1,  1, -1], nor: [-1, 0, 0], uv: [0, 1]},
    {pos: [-1,  1, -1], nor: [-1, 0, 0], uv: [0, 1]},
    {pos: [-1, -1,  1], nor: [-1, 0, 0], uv: [1, 0]},
    {pos: [-1,  1,  1], nor: [-1, 0, 0], uv: [1, 1]},
    // right
    {pos: [ 1, -1,  1], nor: [ 1, 0, 0], uv: [0, 0]},
    {pos: [ 1, -1, -1], nor: [ 1, 0, 0], uv: [1, 0]},
    {pos: [ 1,  1,  1], nor: [ 1, 0, 0], uv: [0, 1]},
    {pos: [ 1,  1,  1], nor: [ 1, 0, 0], uv: [0, 1]},
    {pos: [ 1, -1, -1], nor: [ 1, 0, 0], uv: [1, 0]},
    {pos: [ 1,  1, -1], nor: [ 1, 0, 0], uv: [1, 1]},
    // top
    {pos: [-1,  1,  1], nor: [ 0, 1, 0], uv: [0, 0]},
    {pos: [ 1,  1,  1], nor: [ 0, 1, 0], uv: [1, 0]},
    {pos: [-1,  1, -1], nor: [ 0, 1, 0], uv: [0, 1]},
    {pos: [-1,  1, -1], nor: [ 0, 1, 0], uv: [0, 1]},
    {pos: [ 1,  1,  1], nor: [ 0, 1, 0], uv: [1, 0]},
    {pos: [ 1,  1, -1], nor: [ 0, 1, 0], uv: [1, 1]},
    // bottom
    {pos: [-1, -1, -1], nor: [ 0,-1, 0], uv: [0, 0]},
    {pos: [ 1, -1, -1], nor: [ 0,-1, 0], uv: [1, 0]},
    {pos: [-1, -1,  1], nor: [ 0,-1, 0], uv: [0, 1]},
    {pos: [-1, -1,  1], nor: [ 0,-1, 0], uv: [0, 1]},
    {pos: [ 1, -1, -1], nor: [ 0,-1, 0], uv: [1, 0]},
    {pos: [ 1, -1,  1], nor: [ 0,-1, 0], uv: [1, 1]},
]
const pos = [], nor = [], uv = []
for (let vertice of vertices) {
    pos.push(...vertice.pos)
    nor.push(...vertice.nor)
    uv.push(...vertice.uv)
}
const geometry = new BufferGeometry();
geometry.setAttribute("position", new BufferAttribute(new Float32Array(pos), 3))
geometry.setAttribute("normal", new BufferAttribute(new Float32Array(nor), 3))
geometry.setAttribute("uv", new BufferAttribute(new Float32Array(uv), 2))

const cubeBasicMaterial = new MeshLambertMaterial({color: '#cc0000', wireframe: false})
const cube = new Mesh(geometry, cubeBasicMaterial)
cube.castShadow = true
cube.position.set(2, 2, 2)
scene.add(cube);

const vertices1 = [
    // front
    {pos: [-1, -1, 1], nor: [0, 0, 1], uv: [0, 0]},
    {pos: [ 1, -1, 1], nor: [0, 0, 1], uv: [1, 0]},
    {pos: [-1,  1, 1], nor: [0, 0, 1], uv: [0, 1]},
    {pos: [ 1,  1, 1], nor: [0, 0, 1], uv: [1, 1]},
    // back
    {pos: [ 1, -1, -1], nor: [0, 0, -1], uv: [0, 0]},
    {pos: [-1, -1, -1], nor: [0, 0, -1], uv: [1, 0]},
    {pos: [ 1,  1, -1], nor: [0, 0, -1], uv: [0, 1]},
    {pos: [-1,  1, -1], nor: [0, 0, -1], uv: [1, 1]},
    // left
    {pos: [-1, -1, -1], nor: [-1, 0, 0], uv: [0, 0]},
    {pos: [-1, -1,  1], nor: [-1, 0, 0], uv: [1, 0]},
    {pos: [-1,  1, -1], nor: [-1, 0, 0], uv: [0, 1]},
    {pos: [-1,  1,  1], nor: [-1, 0, 0], uv: [1, 1]},
    // right
    {pos: [ 1, -1,  1], nor: [ 1, 0, 0], uv: [0, 0]},
    {pos: [ 1, -1, -1], nor: [ 1, 0, 0], uv: [1, 0]},
    {pos: [ 1,  1,  1], nor: [ 1, 0, 0], uv: [0, 1]},
    {pos: [ 1,  1, -1], nor: [ 1, 0, 0], uv: [1, 1]},
    // top
    {pos: [-1,  1,  1], nor: [ 0, 1, 0], uv: [0, 0]},
    {pos: [ 1,  1,  1], nor: [ 0, 1, 0], uv: [1, 0]},
    {pos: [-1,  1, -1], nor: [ 0, 1, 0], uv: [0, 1]},
    {pos: [ 1,  1, -1], nor: [ 0, 1, 0], uv: [1, 1]},
    // bottom
    {pos: [-1, -1, -1], nor: [ 0,-1, 0], uv: [0, 0]},
    {pos: [ 1, -1, -1], nor: [ 0,-1, 0], uv: [1, 0]},
    {pos: [-1, -1,  1], nor: [ 0,-1, 0], uv: [0, 1]},
    {pos: [ 1, -1,  1], nor: [ 0,-1, 0], uv: [1, 1]},
]
pos.length = 1
nor.length = 1
uv.length = 1
const position = new Float32Array(vertices1.length * 3)
const normals = new Float32Array(vertices1.length * 3)
const uvs = new Float32Array(vertices1.length * 2)
const index = {pos: 0, nor: 0, uv: 0}
for (let vertice of vertices1) {
    position.set(vertice.pos, index.pos)
    normals.set(vertice.nor, index.nor)
    uvs.set(vertice.uv, index.uv)
    index.pos += 3
    index.nor += 3
    index.uv += 2
}

const geometry_index = new BufferGeometry();
geometry_index.setAttribute("position", new BufferAttribute(new Float32Array(position), 3))
geometry_index.setAttribute("normal", new BufferAttribute(new Float32Array(normals), 3))
geometry_index.setAttribute("uv", new BufferAttribute(new Float32Array(uvs), 2))

geometry_index.setIndex([
     0,  1,  2,  2,  1,  3,
     4,  5,  6,  6,  5,  7,
     8,  9, 10, 10,  9, 11,
    12, 13, 14, 14, 13, 15,
    16, 17, 18, 18, 17, 19,
    20, 21, 22, 22, 21, 23,
])
const cube_index = new Mesh(geometry_index, cubeBasicMaterial)
cube_index.castShadow = true
cube_index.position.set(5, 2, 2)
scene.add(cube_index);

let renderer = null
let controls = null
onMounted(() => {
    stats.showPanel(0)
    statsRef.value.append(stats.dom)
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

const materials = [
    new MeshLambertMaterial({
        color: Math.random() * 0xffffff,
        flatShading: true,
    }),
    new MeshBasicMaterial({
        color: '#000000',
        wireframe: true,
    }),
]

const render = () => {
    controls.update()
    stats.update()
    const rotateSpeed = .01

    //执行渲染操作   指定场景、相机作为参数
    renderer.render(scene, camera);
    requestAnimationFrame(render);
}
</script>

<template>
    <div ref="statsRef"></div>
    <canvas ref="canvasRef"></canvas>
</template>
