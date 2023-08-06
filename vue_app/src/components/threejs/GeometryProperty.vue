<script setup>
import {AmbientLight, PointLight, AxesHelper, Scene, CameraHelper, OrthographicCamera, WebGLRenderer} from 'three';
import { PlaneGeometry, BoxGeometry, SphereGeometry, MeshBasicMaterial, MeshLambertMaterial, Mesh } from 'three';
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
    scale: {
        x: 0,
        y: 0,
        z: 0,
        scale: function() {
            const {x, y, z} = this
            cube.scale.x += x
            cube.scale.y += y
            cube.scale.z += z
        },
    },
    translate: {
        x: 0,
        y: 0,
        z: 0,
        translate: function(){
            const {x, y, z} = this
            cube.translateX(x)
            cube.translateY(y)
            cube.translateZ(z)
        },
    },
    rotate: {
        x: 0,
        y: 0,
        z: 0,
        rotate: function(){
            const {x, y, z} = this
            cube.rotateX(x)
            cube.rotateY(y)
            cube.rotateZ(z)
        },
    },
    color: '#cc0000',
})
const render = () => {
    controls.update()
    stats.update()
    //执行渲染操作   指定场景、相机作为参数
    renderer.render(scene, camera);
    requestAnimationFrame(render);
}
const initGui = () => {
    if (document.querySelectorAll('.dg.main.a').length > 0) {
        return
    }
    const gui = new dat.GUI()
    const scaletion = gui.addFolder('scaletion')
    scaletion.add(cube.scale, "x", 1, 10).listen().onChange(val=>{
        console.log(`x轴缩放值: ${val}`)
    }).onFinishChange(val=>{
        console.log(`x轴最终缩放值:${val}`)
    })
    scaletion.add(cube.scale, "y", 1, 10).listen().onChange(val=>{
        console.log(`y轴缩放值: ${val}`)
    }).onFinishChange(val=>{
        console.log(`y轴最终缩放值:${val}`)
    })
    scaletion.add(cube.scale, "z", 1, 10).listen()
    const position = gui.addFolder('position')
    position.add(cube.position, "x", -10, 10).listen()
    position.add(cube.position, "y", -10, 10).listen()
    position.add(cube.position, "z", -10, 10).listen()
    const rotation = gui.addFolder('rotation')
    rotation.add(cube.rotation, "x", 0, Math.PI, .01).listen()
    rotation.add(cube.rotation, "y", 0, Math.PI, .01).listen()
    rotation.add(cube.rotation, "z", 0, Math.PI, .01).listen()
    const scale = gui.addFolder('scale')
    scale.add(options.value.scale, "x", -3, 3)
    scale.add(options.value.scale, "y", -3, 3)
    scale.add(options.value.scale, "z", -3, 3)
    scale.add(options.value.scale, "scale")
    const translate = gui.addFolder('translate')
    translate.add(options.value.translate, "x", -10, 10)
    translate.add(options.value.translate, "y", -10, 10)
    translate.add(options.value.translate, "z", -10, 10)
    translate.add(options.value.translate, "translate")
    const rotate = gui.addFolder('rotate')
    rotate.add(options.value.rotate, "x", -3, 3)
    rotate.add(options.value.rotate, "y", -3, 3)
    rotate.add(options.value.rotate, "z", -3, 3)
    rotate.add(options.value.rotate, "rotate")
    gui.addColor(options.value, 'color').onChange(val=>{
        cube.material.color.set(val)
    }).onFinishChange(val=>{
        console.log(`最终颜色值:${val}`)
    }).name("设置颜色")
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
