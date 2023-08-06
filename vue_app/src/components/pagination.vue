<script setup>
const props = defineProps({
    total_count: Number,
    total_page: Number,
    pageno: Number,
    count: Number,
})
const {pageno, total_page, total_count, count} = toRefs(props)
const pages = computed(()=>{
    let page_list = []
    const pageno_ = pageno.value, total_page_ = total_page.value
    let beg = pageno_ - 2, end = pageno_ + 2

    if (total_page_ > 5) {
        if (pageno_ > 3) {
            if (pageno_ + 2 > total_page_) {
                end = total_page_
                beg = total_page_ - 4
            }
        } else {
            beg = 1
            end = 5
        }
    } else {
        beg = 1
        end = total_page_
    }
    for (let i = beg; i <= end; ++i) {
        page_list.push(i)
    }
    if (end < total_page_) {
        if (end < total_page_ - 1) page_list.push('...')
        page_list.push(total_page_)
    }
    if (beg > 1) {
        if (beg > 2) page_list.unshift('...')
        page_list.unshift(1)
    }
    // console.log(page_list)
    return page_list
})
const emit = defineEmits(['pageto'])
const pageto = (pageno) => {
    emit('pageto', pageno)
}
</script>

<template>
    <nav aria-label="Page navigation example">
        <ul class="pagination pagination-sm justify-content-center"  :set="pageno2=pageno">
            <li class="page-item" :class="{disabled: pageno === 1}">
                <a class="page-link" @click="pageto(pageno - 1)" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>
            <li class="page-item"
                v-for="pageno_, index in pages" :key="index"
                :class="{disabled: [pageno, '...'].includes(pageno_)}" >
                <a class="page-link"  @click="pageto(pageno_)">{{pageno_}}</a>
            </li>
            <li class="page-item" :class="{disabled: pageno === total_page}">
                <a class="page-link" @click="pageto(pageno + 1)" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
            <!-- <li class="page-item disabled">
                <span class="page-link">{{ total_count }}/{{ total_page }}</span>
            </li> -->
            <li class="page-item">
                <input v-model="pageno2" @keyup.enter="pageto(pageno2)">
            </li>
            <li class="page-item">
                <a class="page-link" @click="pageto(pageno2)">跳转</a>
            </li>
        </ul>
    </nav>
</template>

<style scoped>
input {
    background-color: transparent;
    border-style: none;
    width: 46px;
    text-align: center;
    outline: none;
    height: 28px;
    line-height: 28px;
    margin: 0 5px;
    color: #99a2aa;
    letter-spacing: .5px;
    border-bottom: 1px solid #99a2aa;
}
.pagination li {
    cursor: pointer;
}
</style>

