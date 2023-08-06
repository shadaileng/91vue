<template>
    <div class="row" style="cursor: pointer" v-if="page.total > 0">
        <nav class="col-6" aria-label="Page navigation">
            <ul class="pagination pagination-sm">
                <li class="page-item" :class="{disabled: page.index == 1}">
                    <a class="page-link"
                        @click="$emit('pageTo', page.index - 1)"
                        aria-label="Previous">
                        <span aria-hidden="true">«</span>
                    </a>
                </li>
                <li class="page-item" v-for="index in range" :class="{disabled: index==page.index}">
                    <a class="page-link" @click="$emit('pageTo', index)"> {{index}}</a>
                </li>
                <li class="page-item" :class="{disabled: page.index >= page.pages}">
                    <a class="page-link"
                        @click="$emit('pageTo', page.index + 1)"
                        aria-label="Next">
                        <span aria-hidden="true">»</span>
                    </a>
                </li>
                <li class="page-item ">
                    <input @keyup.enter="$emit('pageTo', $event.currentTarget.value)" class="page-link" style="width:50px">
                </li>
                <li class="page-item disabled">
                    <input class="page-link text-center" style="width:70px" :value="page.index + '/' + page.pages">
                </li>
                <li class="page-item">
                    <input type="number" min="1" max="100" class="page-link" v-model="pagesize">
                </li>
            </ul>
        </nav>
    </div>
</template>

<script>
export default {
    data() {
            return {
                pagesize: 1
            }
    },
    props: ['page'],
    emits: ['pageTo', 'resize'],
    mounted() {
    },
    methods: {
    },
    watch: {
        pagesize(newVal, oldVal) {
            this.$emit('resize', newVal)
        }
    },
    updated() {
        this.pagesize = this.pageSize
    },
    computed: {
        pageSize() {
            return this.page.size
        },
        range() {
            let range = []
            let max = 3, half = ~~(max / 2), half1 = half + 1
            if (this.page.pages <= max) {
                for (let i = 1; i <= this.page.pages; ++i) {
                    range.push(i)
                }
            } else {
                if (this.page.index <= half1) {
                    for (let i = 1; i <= max; ++i) {
                        range.push(i)
                    }
                }
                if (this.page.index > half1 && this.page.index < this.page.pages - half) {
                    for (let i = this.page.index - half; i <= this.page.index + half; ++i) {
                        range.push(i)
                    }
                }
                if (this.page.index >= this.page.pages - half) {
                    for (let i = this.page.pages - max + 1; i <= this.page.pages; ++i) {
                        range.push(i)
                    }
                }
            }
            if (range.length === 0) range = [1]
            // log(range)
            return range
        }
    },
}
</script>

<style>
.board {
  resize: none;
  height: 80vh;
}
</style>

<custom1>
  This could be e.g. documentation for the component.
</custom1>
