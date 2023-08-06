<template>
    <div>
        <div @click="top" @mouseenter="bg1.background = '#61e9b0'" @mouseleave="bg1.background = '#b1e9e0aa'" :style="bg1" class="border-bottom border-dark"><span><i class="fa fa-angle-up mr-3 ml-3" aria-hidden="true"></i></span></div>
        <div @click="bottom" @mouseenter="bg2.background = '#61e9b0'" @mouseleave="bg2.background = '#b1e9e0aa'" :style="bg2" class="border-top border-dark"><span><i class="fa fa-angle-down mr-3 ml-3" aria-hidden="true"></i></span></div>
    </div>
</template>

<script>
export default {
    data() {
            return {
                bg1: {
                    background: '#b1e9e0aa',
                },
                bg2: {
                    background: '#b1e9e0aa',
                },
                scroll: {
                    top: true,
                    bottom: false,
                }
            }
        },
    props: ['content'],
    emits: ['show'],
    mounted() {
        // this.modal('show')
        window.addEventListener('scroll', this.getScroll)
    },
    methods: {
        top() {
            document.querySelector('html').scrollTo(0, 0)
        },
        bottom() {
            let topMax = document.querySelector('html').scrollHeight - document.querySelector('html').clientHeight
            document.querySelector('html').scrollTo(0, topMax)
        },
        getScroll() {
            // this.scroll.top = document.querySelector('html').scrollTop === 0
            // let topMax = document.querySelector('html').scrollHeight - document.querySelector('html').clientHeight
            // this.scroll.bottom = document.querySelector('html').scrollTop === topMax
        },
    },
    watch: {
    },
    computed: {
    }
}
</script>

<style>
</style>

<custom1>
  This could be e.g. documentation for the component.
</custom1>
