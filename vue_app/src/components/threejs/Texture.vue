<script setup>
import { AxesHelper, Scene, CameraHelper, OrthographicCamera, WebGLRenderer} from 'three';
import { AmbientLight, PointLight, DirectionalLight} from 'three';
import { Mesh, PlaneGeometry, BoxGeometry, SphereGeometry} from 'three';
import { MeshBasicMaterial, MeshLambertMaterial, MeshStandardMaterial } from 'three';
import { TextureLoader, RepeatWrapping, MirroredRepeatWrapping, NearestFilter, DoubleSide } from 'three';
import { BufferAttribute } from 'three';
// 引入扩展库OrbitControls.js BufferAttribute
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// 引入扩展库GLTFLoader.js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// width和height用来设置js输出的Canvas画布尺寸(像素px)
const width = 600; //宽度
const height = 450; //高度
const canvasRef = ref(null)

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
// scene.add(cameraHelper)

const axesHelper = new AxesHelper(20)
scene.add(axesHelper)

/**
* 光源设置
*/
//环境光
const ambient = new AmbientLight(0x444444, .5);
scene.add(ambient);
//点光源
const point = new PointLight(0xffffff);
point.castShadow = true
point.position.set(40, 20, 30); //点光源位置
scene.add(point); //点光源添加到场景中
// 平行光
const directionalLight = new DirectionalLight(0xffffff, .5);
directionalLight.castShadow = true
directionalLight.position.set(-1, 1, 0); //点光源位置
scene.add(directionalLight); //点光源添加到场景中

const textureloader = new TextureLoader()
const texture = textureloader.load('http://cdn-hw-static.shanhutech.cn/bizhi/staticwp/202212/e9b453e17ec604f36f873e59e04b101a--2378904596.jpg')
// 偏移量: 二维向量,范围是[0, 1]
// texture.offset.x = 0.5
// texture.offset.y = 0.5
// texture.offset.set(0.5, 0.5)
// 旋转中心: 二维向量,范围是[0, 1]
texture.center.set(0.5, 0.5)
// 旋转角度: 标量,单位是弧度
texture.rotation = Math.PI / 4

// 设置重复
texture.repeat.set(3, 3)
texture.wrapS = MirroredRepeatWrapping
texture.wrapT = RepeatWrapping

// 设置贴图采样方法
texture.magFilter = NearestFilter
texture.minFilter = NearestFilter

// https://www.poliigon.com/


const text2png = (text, fill=true) => {
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')

    ctx.font="55px Arial"
    const width = ctx.measureText(text).width

    ctx.strokeStyle="blue";
    ctx.moveTo(5,100);
    ctx.lineTo(width + 15,100);
    ctx.stroke();
    ctx.beginPath()
    ctx.textBaseline="bottom";
    if (fill) {
        ctx.fillStyle="#ffffff";
        ctx.fillText(text,10,100)
    } else {
        ctx.strokeStyle="#444444";
        ctx.strokeText(text,10,100)
    }
    return canvas.toDataURL('image/png')
}


const alphaTexture = textureloader.load(text2png('Shadaileng'))
const aoTexture = textureloader.load(text2png('Shadaileng', false))

// side: 默认正面: FrontSide
// roughness: 粗糙度
const planeGeometry = new PlaneGeometry(100, 20)
const planeBasicMaterial = new MeshStandardMaterial({
    color: '#cccccc',
    side: DoubleSide,
    roughness: 1,
    roughnessMap : alphaTexture,
    metalness: 1,
    metalnessMap: alphaTexture,
})
const plane = new Mesh(planeGeometry, planeBasicMaterial)
plane.receiveShadow = true
plane.rotateX(-Math.PI / 2)
scene.add(plane);


const cubeGeometry = new BoxGeometry(4, 4, 4)
let cube = new Mesh(cubeGeometry, new MeshLambertMaterial({
    color: '#cccccc',
    wireframe: false,
    map: texture,
}))
cube.castShadow = true
cube.position.set(2, 2, 2)
scene.add(cube);

// alphaMap: 灰度纹理，用于控制整个表面的不透明度,需要设置transparent
cube = new Mesh(cubeGeometry, new MeshLambertMaterial({
    color: '#cccccc',
    wireframe: false,
    map: texture,
    alphaMap: alphaTexture,
    transparent: true,
}))
cube.castShadow = true
cube.position.set(8, 2, 2)
scene.add(cube);


// aoMap: 纹理的红色通道用作环境遮挡贴图。默认值为null。aoMap需要第二组UV
const cubeGeometry_ = new BoxGeometry(4, 4, 4)
cubeGeometry_.setAttribute('uv2', new BufferAttribute(cubeGeometry_.attributes.array, 2))
cube = new Mesh(cubeGeometry, new MeshLambertMaterial({
    color: '#cccccc',
    wireframe: false,
    map: alphaTexture,
    aoMap: aoTexture,
    aoMapIntensity: .5,
    transparent: true,
}))
cube.castShadow = true
cube.position.set(14, 2, 2)
scene.add(cube);

// 位移贴图
cube = new Mesh(new PlaneGeometry(4, 4, 200, 200), new MeshStandardMaterial({
    color: '#cccccc',
    wireframe: false,
    map: alphaTexture,
    displacementMap: aoTexture,
    displacementScale: .5,
    transparent: true,
}))
cube.castShadow = true
cube.position.set(20, 2, 2)
scene.add(cube);

// 金属贴图
cube = new Mesh(new PlaneGeometry(4, 4, 200, 200), new MeshStandardMaterial({
    color: '#cccccc',
    wireframe: false,
    metalness: 1,
    metalnessMap: alphaTexture,
    transparent: true,
}))
cube.castShadow = true
cube.position.set(26, 2, 2)
scene.add(cube);


// opacity: 透明度,需要设置transparent
const sphereGeometry = new SphereGeometry(2)
const sphere = new Mesh(sphereGeometry, new MeshLambertMaterial({
    color: '#cccccc',
    wireframe: false,
    map: texture,
    transparent: true,
    opacity: .5,
}))
sphere.castShadow = true
sphere.position.set(-6, 2, 2)
scene.add(sphere);

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
    renderer.shadowMap.enabled = true
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
