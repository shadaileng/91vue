<template>
    <div ref="loading" class="fixed-bottom vw-100 vh-100 text-center bg" >
        <div class="spinner-border center" role="status">
            <span class="sr-only">Loading...</span>
        </div>
    </div>
</template>

<script>
export default {
    data() {
            return {
                items: [
                ],
            }
        },
    props: ['loading'],
    emits: [],
    mounted() {

    },
    methods: {
    },
    watch: {
        loading(newVal, olVal) {
        }
    },
    computed: {
    }
}
</script>

<style>
.center {
    position: absolute;
    top: 50vh;
}
.bg {
    transition: opacity 2s linear;
    background-color: #cccccc22;
    z-index: 2048;
}
</style>

<custom1>
  This could be e.g. documentation for the component.
</custom1>
