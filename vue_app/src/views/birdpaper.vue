<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
// import HelloWorld from './components/HelloWorld.vue'
import { ref, reactive } from 'vue'
import modal from '@/components/modal.vue'
import pagination from '@/components/pagination.vue'
import menuLayout from '@/components/menuLayout.vue'
import offcanvas from '@/components/offcanvas.vue'
import slideshow from '@/components/slideshow.vue'
import { computed } from '@vue/reactivity';
import { isFunction } from '@vue/shared';

import { storeToRefs } from "pinia";
import { birdpaper } from "@/store/birdpaper";

const birdpaperStore = birdpaper();
const { categorys, list, navigate, req, defaultCid } = storeToRefs(birdpaperStore);

const { proxy } = getCurrentInstance();
const getcategory = async () => {
    const res = await proxy.$api.getcategory();
    birdpaperStore.setCategorys(res.data)
};
const getlist = async (params) => {
    birdpaperStore.updateReqParams(params)
    const res = await proxy.$api.getlist(birdpaperStore.getReqParams());
    birdpaperStore.setList(res.data)
    birdpaperStore.setNavigate(['高清壁纸', categorys.value.find(el=> el.old_id === birdpaperStore.getReqParams().cids).category])
    birdpaperStore.updateReqFun('getlist')
};

const newestList = async (params) => {
    birdpaperStore.updateReqParams(params)
    const res = await proxy.$api.newestList(birdpaperStore.getReqParams());
    birdpaperStore.setList(res.data)
    birdpaperStore.setNavigate(['高清壁纸', '最新图片'])
    birdpaperStore.updateReqFun('newestList')
};
const search = async (params) => {
    birdpaperStore.updateReqParams(params)
    const res = await proxy.$api.search(birdpaperStore.getReqParams());
    birdpaperStore.setList(res.data)
    birdpaperStore.setNavigate(['高清壁纸', '搜索', birdpaperStore.getReqParams().content])
    birdpaperStore.updateReqFun('search')
};

const fun = {
    getlist,
    newestList,
    search,
}
const getusers = async () => {
    const res = await proxy.$api.getusers("shadaileng");
};
onMounted(() => {
    if (!isFunction(fun[birdpaperStore.getReqFun()])) {
        getcategory().then(()=>{
            getlist({cids: defaultCid.value, pageno: 1})
        })
    }
    // getusers()
});

const pageto = (pageno) => {
    if (pageno === list.pageno) return
    if (pageno > list.total_page) return
    if (pageno < 1) return
    fun[birdpaperStore.getReqFun()]({pageno: pageno})
}
let modal_ = ref(null), offcanvas_ = ref(null), slideshow_ = ref(null)
const modalUrl = ref('')
const testurl = "http://cdn-hw-static.shanhutech.cn/bizhi/staticwp/202209/ea04bd8b013115f105d80e256c0415fc--571789350.jpg"

</script>

<template>
    <menuLayout>
        <template v-slot:section>
            <span class="list-group-item list-group-item-action input-group p-0"
                :class="{active: 'search' === defaultCid}"
                data-bs-toggle="list" href="#list-home" role="tab">
                <input @keyup.enter="search({content, cids: 'search', pageno: 1})" :set="content=''" v-model="content" class="w-100" type="text" placeholder="搜索图片" aria-label="搜索图片" aria-describedby="button-addon2"/>
            </span>
            <a class="list-group-item list-group-item-action"
                data-bs-toggle="list" href="#list-home" role="tab"
                :class="{active: 'newest' === defaultCid}"
                @click="newestList({cids: 'newest', pageno: 1})">
                最新图片
            </a>
            <a class="list-group-item list-group-item-action" data-bs-toggle="list" href="#list-home" role="tab"
                v-for="item, index in categorys" :key="index"
                @click="getlist({cids: item.old_id, pageno: 1})"
                :class="{active: item.old_id === defaultCid}">
                {{ item.show_name }}
            </a>
            <a class="list-group-item list-group-item-action" data-bs-toggle="list" href="#list-home" role="tab"
                @click="offcanvas_.show()"
                v-hasRole="'admin'">
                本地配置
            </a>
        </template>
        <template v-slot:main>
            <nav class="row pt-3 ps-3" aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li v-for="item, index in navigate" :key="index"
                        :class="{active: index === navigate.length - 1}"
                        class="breadcrumb-item" aria-current="page">
                        {{ item }}
                    </li>
                </ol>
            </nav>
            <div class="row">
                <div class="col-xs-12 col-sm-6 col-md-4 pb-3 pointer"
                    @click="current=index;modalUrl=item.url;modal_.show();slideshow_.scrollTo(index);"
                    :title="item.tag"
                    v-for="item, index in list.list" :key="item.id">
                    <img class="rounded" v-loadpic="item.url" :alt="item.tag" >
                    <!-- <div>{{ item.tag }}</div> -->
                </div>
            </div>
            <div class="row" v-if="list.list.length > 0">
                <div class="col-12">
                    <pagination @pageto="pageto"
                        :total_count="list.total_count"
                        :total_page="list.total_page"
                        :pageno="list.pageno"
                        :count="list.count"></pagination>
                </div>
            </div>
        </template>
    </menuLayout>
    <modal ref="modal_">
        <img class="modal-content" :src="modalUrl"/>
        <slideshow ref="slideshow_" :items="list.list" @select="(item)=>{modalUrl=item.url}" v-slot="{ item, index }">
            <img :src="item.url" style="width: 100px; height: 60px;" :alt="item.tag">
        </slideshow>
    </modal>
    <offcanvas ref="offcanvas_">
        <template #title>本地配置</template>
        <template #body>
            <div class="form-floating mb-3">
                <input type="range" class="form-control form-range" min="0" max="30" step="3" v-model="req.params.count">
                <label for="floatingInput">每页: {{req.params.count}}</label>
            </div>
        </template>
    </offcanvas>
</template>

<style scoped>
/* section::-webkit-scrollbar {
    display: none;
}
main::-webkit-scrollbar {
    display: none;
} */
.pointer {
    cursor: pointer;
}
.zoom-in {
    cursor: zoom-in;
}
</style>