<script setup>
const props = defineProps({
    data: Boolean,
})
</script>
<template>
    <span class="badge" :class="{'bg-success': data, 'bg-danger': !data}">{{data}}</span>
</template>
