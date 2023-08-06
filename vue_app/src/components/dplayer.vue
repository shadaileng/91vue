<script setup>
import DPlayer from 'dplayer';
import config from "@/config"
const VUE_91_API = config.apis.porn91

const text2png = (text) => {
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')

    ctx.font="55px Arial"
    const width = ctx.measureText(text).width

    ctx.strokeStyle="blue";
    ctx.moveTo(5,100);
    ctx.lineTo(width + 15,100);
    ctx.stroke();

    ctx.fillStyle="#4c4aac88";
    // ctx.fillRect(0, 0, 400, 150)
    ctx.beginPath()
    ctx.ellipse(width / 2 + 10,70,width / 2 + 10, 60, -Math.PI / 25,0,Math.PI*2);
    ctx.fill()

    ctx.beginPath()
    ctx.fillStyle="#ffff88";
    ctx.textBaseline="bottom";
    ctx.fillText(text,10,100)
    return canvas.toDataURL('image/png')
}

const playerDom = ref(null), dp = ref(null)
const play = async (item) => {
    if (!item) return
    const {src_local, poster_local, name} = item
    const src = `${VUE_91_API}/${src_local}`
    const poster = `${VUE_91_API}/${poster_local}`

    dp.value = new DPlayer({
        container: playerDom.value,
        lang: 'zh-cn',
        theme: '#FADFA3',
        preload: 'auto',
        screenshot: true,
        logo: text2png('Shadaileng'),
        video: {
            url: src,
            pic: poster,
            thumbnails: `${src.split('.')[0]}.png`,
        },
        // subtitle: {
        //     url: 'webvtt.vtt',
        // },
        // danmaku: {
        //     id: 'demo',
        //     api: 'https://api.prprpr.me/dplayer/',
        // },

    });
    const videoTitle = document.createElement('marquee')
    videoTitle.classList.add('title')
    videoTitle.style.cssText = `
        color: rgb(255, 255, 255);
        position: absolute;
        top: 20px;
        left: 80px;
        background: #1b6068aa;
        padding: 5px;
        width: 70%;
        text-align: left;
        border-radius: 25px 50px 50px 25px;
        overflow: hidden;
    `
    videoTitle.classList.add('text-break')
    videoTitle.innerText = name.replace('\n', ' ')
    playerDom.value.appendChild(videoTitle)
    playerDom.value.addEventListener('click', event => {
        const title = playerDom.value.querySelector('.title')
        if (dp.value.controller.isShow()) {
            title.style.display = 'block'
        } else {
            title.style.display = 'none'
        }
    })
}

const mouseover = event => {
    const title = playerDom.value.querySelector('.title')
    title.style.display = 'block'
}

const mouseout = event => {
    const title = playerDom.value.querySelector('.title')
    title.style.display = 'none'
}

defineExpose({
    dp,
    play,
})

</script>
<template>
    <div ref="playerDom" style="height: 70vh" @mouseover="mouseover" @mouseout="mouseout"></div>
</template>