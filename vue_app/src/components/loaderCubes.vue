<script setup>

</script>
<template>
    <div class="cubes">
        <div class="cube">
            <div style="--x: -1; --y: 0">
                <span style="--i: 3"></span>
                <span style="--i: 2"></span>
                <span style="--i: 1"></span>
            </div>
            <div style="--x: 0; --y: 0">
                <span style="--i: 3"></span>
                <span style="--i: 2"></span>
                <span style="--i: 1"></span>
            </div>
            <div style="--x: 1; --y: 0">
                <span style="--i: 3"></span>
                <span style="--i: 2"></span>
                <span style="--i: 1"></span>
            </div>
        </div>
        <div class="cube">
            <div style="--x: -1; --y: 0">
                <span style="--i: 3"></span>
                <span style="--i: 2"></span>
                <span style="--i: 1"></span>
            </div>
            <div style="--x: 0; --y: 0">
                <span style="--i: 3"></span>
                <span style="--i: 2"></span>
                <span style="--i: 1"></span>
            </div>
            <div style="--x: 1; --y: 0">
                <span style="--i: 3"></span>
                <span style="--i: 2"></span>
                <span style="--i: 1"></span>
            </div>
        </div>
        <div class="cube">
            <div style="--x: -1; --y: 0">
                <span style="--i: 3"></span>
                <span style="--i: 2"></span>
                <span style="--i: 1"></span>
            </div>
            <div style="--x: 0; --y: 0">
                <span style="--i: 3"></span>
                <span style="--i: 2"></span>
                <span style="--i: 1"></span>
            </div>
            <div style="--x: 1; --y: 0">
                <span style="--i: 3"></span>
                <span style="--i: 2"></span>
                <span style="--i: 1"></span>
            </div>
        </div>
    </div>
</template>

<style scoped>
.cubes {
    transform: skewY(-20deg)
}
.cubes .cube {
    position: relative;
    z-index: 2;
}
.cubes .cube:nth-child(2) {
    z-index: 1;
    translate: -60px -60px;
}
.cubes .cube:nth-child(3) {
    z-index: 3;
    translate: 60px 60px;
}
.cubes .cube div {
    position: absolute;
    display: flex;
    flex-direction: column;
    gap: 30px;
    translate: calc(-70px * var(--x)) calc(-60px * var(--y));
}
.cubes .cube div span {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 50px;
    background: #dcdcdc;
    z-index: calc(1 * var(--i));
    transition: 1.5s;
}
.cubes .cube div span:hover {
    transition: 0s;
    background: #ff0000;
    filter: drop-shadow(0 0 30px #ff0000);
}
.cubes .cube div span::before {
    content: '';
    position: absolute;
    left: -40px;
    width: 40px;
    height: 100%;
    background: #dfdfdf;
    transform-origin: right;
    transform: skewY(45deg);
    transition: 1.5s;
}
.cubes .cube div span:hover::before {
    transition: 0s;
    background: #ff00cc;
    filter: drop-shadow(0 0 30px #ff00cc);
}
.cubes .cube div span::after {
    content: '';
    position: absolute;
    top: -40px;
    left: 0;
    width: 100%;
    height: 40px;
    background: #efefef;
    transform-origin: bottom;
    transform: skewX(45deg);
    transition: 1.5s;
}
.cubes .cube div span:hover::after {
    transition: 0s;
    background: #ffcc00;
    filter: drop-shadow(0 0 30px #ffcc00);
}
</style>
