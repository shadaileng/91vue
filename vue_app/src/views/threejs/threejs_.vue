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

const helper = new THREE.CameraHelper(camera)
scene.add(helper)
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
// scene.add(mesh); //网格模型添加到场景中

const loadData = () => {
    const loader = new THREE.FileLoader()
    loader.load('static/100000_full.json', (data) => {
        const jsondata = JSON.parse(JSON.parse(JSON.stringify(data)))
        generateGeometry(jsondata)
    })
}

const generateGeometry = (jsondata) => {
    // 初始化一个地图对象
    const map = new THREE.Object3D()
    // 墨卡托投影转换
    /*
    const projection = d3
        .geoMercator()
        .center([104.0, 37.5])
        .scale(80)
        .translate([0, 0])

    */
    jsondata.features.forEach((elem) => {
        // 定一个省份3D对象
        const provinces = genProvinces(elem)
        map.add(provinces)
        map.rotateY(-45)
        map.position.set(0, 80, 0)
        map.scale.set(6, 6, 6)
    })
    console.log(map)
    scene.add(map)
}


const genProvinces = (elem) => {
    const province = new THREE.Object3D()

    const coordinates = elem.geometry.coordinates
    // 循环坐标数组
    coordinates.forEach((multiPolygon) => {
        if (elem.geometry.type === 'MultiPolygon') {
            multiPolygon.forEach((polygon) => {
                const { mesh, line } = generateShape(polygon)
                province.add(mesh)
                province.add(line)
            })
        } else {
            const { mesh, line } = generateShape(multiPolygon)
            province.add(mesh)
            province.add(line)
        }
    })

    return province
}

const generateShape = (polygon) => {
    const shape = new THREE.Shape()
    const points = [];
    for (let i = 0; i < polygon.length; i++) {
        // const [x, y] = projection(polygon[i])
        const [x, y] = polygon[i]
        const pos = new THREE.Vector2(x, y)
            .sub(new THREE.Vector2(104.0, 37.5))
        //     .center([104.0, 37.5])
        if (i === 0) {
            shape.moveTo(pos.x, pos.y)
        }
        shape.lineTo(pos.x, pos.y)
        points.push(new THREE.Vector3(pos.x, pos.y, 4.01))
    }
    const lineGeometry = new THREE.BufferGeometry().setFromPoints( points );

    const extrudeSettings = {
        depth: 10,
        bevelEnabled: false,
    }

    const geometry = new THREE.ExtrudeGeometry(
        shape,
        extrudeSettings
    )
    const material = new THREE.MeshBasicMaterial({
        color: '#2defff',
        transparent: true,
        opacity: 0.6,
    })
    const material1 = new THREE.MeshBasicMaterial({
        color: '#3480C4',
        transparent: true,
        opacity: 0.5,
    })
    const lineMaterial = new THREE.LineBasicMaterial({
        color: 'white',
    })

    const mesh = new THREE.Mesh(geometry, [material, material1])
    const line = new THREE.Line(lineGeometry, lineMaterial)
    mesh.rotateY(180 / Math.PI * 175)
    line.rotateY(180 / Math.PI * 175)
    return {mesh, line}
}

const container = ref(null)
onMounted(() => {
    loadData()
    container.value.appendChild(renderer.domElement)
    render()
    var controls = new OrbitControls(camera, renderer.domElement);//创建控件对象
    // controls.addEventListener('change', render);//监听鼠标、键盘事件
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
