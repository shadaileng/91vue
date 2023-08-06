<script setup>
import pagination from '@/components/pagination.vue'
import menuLayout from '@/components/menuLayout.vue'
import modal from '@/components/modal.vue'
import offcanvas from '@/components/offcanvas.vue'
import config from '@/components/config.vue'
// import grid from '@/components/grid.vue'
// import gridDetail from '@/components/gridDetail.vue'
import items from '@/components/items.vue'
import slideshow from '@/components/slideshow.vue'
import dplayer from '@/components/dplayer.vue'
import import91 from '@/components/import91.vue'
import scroll from '@/components/scroll.vue'
import DPlayer from 'dplayer';
import config_ from "@/config"
import { useRouter, useRoute } from 'vue-router'
// import { reactive, ref } from "@vue/reactivity";

const VUE_91_API = config_.apis.porn91
const VUE_91_ADMIN = config_.apis.admin
const { proxy } = getCurrentInstance();


import { storeToRefs } from "pinia";
import { haijiao } from "@/store/haijiao";
import { user } from "@/store/user";
import { computed } from 'vue';
import { onBeforeRouteLeave, onBeforeRouteUpdate } from 'vue-router'


const userStore = user();
const { token, roles } = storeToRefs(userStore);

const router = useRouter()
const route = useRoute()

const store = haijiao();
const { page, list, tabName, navigate, req, status } = storeToRefs(store);
onBeforeRouteUpdate((to, from) => {
    let params = {
        index: 1,
        status: null,
        uname: null,
        name: null,
    }
    Object.assign(params, to.query)
    init(params)
})
const getlist = async (params) => {
    const _params = JSON.parse(JSON.stringify(store.getReqParams()))
    store.updateReqParams(params)
    if (!roles.value.includes('admin')) {
        store.setList([])
        store.setNavigate()
        return
    }
    router.push({
        path: '/haijiao',
        query: store.getReqParams(),
        hash: route.hash,
    })
    const params_ = JSON.parse(JSON.stringify(store.getReqParams()))
    let flag = true
    for(let key of Object.keys(params_)) {
        if (_params[key] !== params_[key]) {
            flag = false
            break
        }
    }
    flag && init(params_)
};

const init = async (params) => {
    store.updateReqParams(params)
    if (!roles.value.includes('admin')) {
        store.setList([])
        store.setNavigate()
        return
    }
    const res = await proxy.$api.get91List(store.getReqParams());
    if (res && res.code === 0) {
        store.setList(res.data.items)
        store.setPage(res.data.page)

        store.setNavigate()
    }
}

const do91Import = async (params) => {
    const res = await proxy.$api.do91Import(params);
    if (res) {
        if (res.code === 0) {
            getlist()
            modal_.value.hide()
            proxy.$toast(res.msg)
        } else {
            proxy.$toast(`导入异常: ${res.msg}`)
        }
    }
};

const do91Delete = async (params) => {
    const res = await proxy.$api.do91Delete(params);
    if (res) {
        if (res.code === 0) {
            getlist()
            proxy.$toast(res.msg)
        } else {
            proxy.$toast(`删除异常: ${res.msg}`)
        }
    }
};

const do91Package = async (params) => {
    const res = await proxy.$api.do91Package(params);
    if (res) {
        if (res.code === 0) {
            // console.log(res.msg)
            proxy.$toast(res.msg)
        } else {
            proxy.$toast(`打包异常: ${res.msg}`)
        }
    }
};

const rebootDService = async (params) => {
    const res = await proxy.$api.rebootDService(params);
    if (res) {
        if (res.code === 0) {
            // console.log(res.msg)
            proxy.$toast(res.msg)
        } else {
            proxy.$toast(`重启异常: ${res.msg}`)
        }
    }
};

const get91Config = async (params) => {
    const res = await proxy.$api.get91Config(params);
    if (res) {
        if (res.code === 0) {
            modalSlots.item.config = true
            modalSlots.opt = {'items': res.data['items'] }
            modal_.value.show()
        } else {
            proxy.$toast(`获取配置: ${res.msg}`)
        }
    }
};

const doConfig = async (items, remove) => {
    if (items instanceof Array && items.length > 0) {
        const res = await proxy.$api.doConfig({items: items});
        if (res) {
            // console.log(res)
            if (res.code === 0) {
                modalSlots.opt = {'items': res.msg['items'] }
                proxy.$toast(`保存成功`)
            } else {
                proxy.$toast(`保存配置: ${res.msg}`)
            }
        }
    }
    if (remove instanceof Array && remove.length > 0) {
        const res = await proxy.$api.doConfigDel({ids: remove});
        if (res) {
            // console.log(res)
            if (res.code === 0) {
                modalSlots.opt = {'items': res.msg['items'] }
                proxy.$toast(`保存成功`)
            } else {
                proxy.$toast(`保存配置: ${res.msg}`)
            }
        }
    }
}

const doTopic = async (params) => {
    const res = await proxy.$api.doTopic(params);
    if (res) {
        if (res.code === 0) {
            proxy.$toast(res.msg)
        } else {
            proxy.$toast(`请求异常: ${res.msg}`)
        }
    }
};

const doDownload = async (params) => {
    const res = await proxy.$api.doDownload(params);
    if (res) {
        if (res.code === 0) {
            proxy.$toast(res.msg)
        } else {
            proxy.$toast(`请求异常: ${res.msg}`)
        }
    }
};

const doUid = async (params) => {
    if (!params) {
        proxy.$toast('uid 不能为空')
        return
    }
    const res = await proxy.$api.doUid(params);
    if (res) {
        if (res.code === 0) {
            proxy.$toast(res.msg)
        } else {
            proxy.$toast(`请求异常: ${res.msg}`)
        }
    }
};


const tasks = async (params) => {
    const res = await proxy.$api.tasks(params);
    if (res) {
        if (res.code === 0) {
            modalSlots.item.tasks = true
            modalSlots.opt = {'items': res.data['items'] }
            modal_.value.show()
        } else {
            proxy.$toast(`获取配置: ${res.msg}`)
        }
    }
};

const stopTask = async (params) => {
    const res = await proxy.$api.stopTask(params);
    if (res) {
        if (res.code === 0) {
            proxy.$toast(res.msg)
            modalSlots.opt = {'items': res.data['items'] }
        } else {
            proxy.$toast(`请求异常: ${res.msg}`)
        }
    }
};

const doVideoFun = async (callback, params) => {
    const res = await callback(params);
    if (res) {
        if (res.code === 0) {
            proxy.$toast(res.msg)
        } else {
            proxy.$toast(`请求异常: ${res.msg}`)
        }
    }
}

const doUpdate = async (status) => {
    if (status === undefined || status === null || status === '') {
        proxy.$toast("未选择新状态")
        return
    }
    const items = []
    list.value.forEach(el=>{
        selectItems.forEach(els=>{
            if (el.id === els) {
                const el_ = JSON.parse(JSON.stringify(el))
                el_.status = status
                items.push(el_)
            }
        })
    })

    const res = await proxy.$api.do91Import({items});
    if (res) {
        if (res.code === 0) {
            proxy.$toast(res.msg)
            modal_.value.hide()
            getlist()
        } else {
            proxy.$toast(`请求异常: ${res.msg}`)
        }
    }
};


const size_normalize = (size) => {
    if (size === undefined) return 0
    function foematNum(num) {
        return Math.round(num * 1000) / 1000
    }
    if (size == 0) return 0
    if (size < 1024) return foematNum(size) + "b"
    if (size < 1024 * 1024) return foematNum(size / 1024) + "K"
    if (size < 1024 * 1024 * 1024) return foematNum(size / 1024 / 1024) + "M"
    if (size < 1024 * 1024 * 1024 * 1024) return foematNum(size / 1024 / 1024 / 1024) + "M"
    return 0
}

const selectItems = reactive([])
const selected = ref(false)
const selectAll = () => {
    selectItems.length = 0
    if (!selected.value) {
        list.value.forEach(el=>{
            if (el && el.id) {
                selectItems.push(el.id)
            }
        })
    }
}
const selectOne = (id, event) => {
    if (event && event.target.tagName === "INPUT") {
            if (selectItems.includes(id)) {
                selectItems.splice(selectItems.indexOf(id), 1)
            } else {
                selectItems.push(id);
            }
            return
        }
    if (event.ctrlKey) {
        if (selectItems.includes(id)) {
            selectItems.splice(selectItems.indexOf(id), 1)
        } else {
            selectItems.push(id);
        }
    } else {
        selectItems.length = 0
        selectItems.push(id)
    }
}

const convertItems = (content) => {
    if (!content || content.length <= 0) return
    let objs = []
    try {
        objs = JSON.parse(content)
    } catch (error) {
        console.log(`字符串解析错误: ${error.message}`)
        return []
    }
    if (!(objs instanceof Array)) return
    objs.sort((a, b) => {
        if (Object.keys(a).indexOf('id') < 0) return 0
        if (Object.keys(b).indexOf('id') < 0) return 0
        if (typeof (a['id']) !== 'number') return 0
        if (typeof (b['id']) !== 'number') return 0
        return a['id'] - b['id']
    })
    let items = []
    let fields = ['key', 'name', 'src', 'poster', 'uname', 'uid', 'path', 'content_type', 'duration', 'size', 'publish_date', 'url', 'src_local', 'poster_local', 'status']
    objs.forEach(el => {
        // console.log(el['key'] && el['key'].length > 0)
        // console.log(el['src'] && el['src'].length > 0)
        // console.log(el['poster'] && el['poster'].length > 0)
        // console.log(el['name'] && el['name'].length > 0)
        if (el['key'] && el['key'].length > 0
            && el['src'] && el['src'].length > 0
            && el['poster'] && el['poster'].length > 0
            && el['name'] && el['name'].length > 0
        ) {
            el['content_type'] = 'video'
            el['path'] = '/haijiao'
            let item = {}
            fields.forEach(field => {
                item[field] = el[field]
            })
            items.push(item)
        }
    });
    return items
}
// const tabName = ref('grid')
const currentTab = computed(()=>{
    // return tabs[tabName.value].com
})
const tabs = reactive({
    grid: {
        name: 'grid',
        // com: shallowRef(grid),
    },
    detail : {
        name: 'detail',
        // com: shallowRef(gridDetail),
    }
})

const protocols = {'https:': 'wss', 'http:': 'ws'}
const logger = () => {
    let url = `${protocols[location.protocol]}://${location.host}${VUE_91_ADMIN}/tail`
    let ws = new WebSocket(url);
    ws.onopen = (event) => {
        modalSlots.opt = {
            content: '',
            readonly: true,
        }
        console.log(url + " Connection open ...");
        ws.send('1');
    }
    ws.onmessage = (event) => {
        // console.log("Received Message: " + event.data);
        if (event.data && event.data.length > 0)
            modalSlots.opt.content += event.data + '\n'
            const el = text_show.value
            if (el && el.scrollTop + el.clientHeight > el.scrollHeight * .90) {
                el.scrollTo(0, el.scrollHeight)
            }
        ws.send('2');
    };
    ws.onclose = (event) => {
        console.log("Connection closed.");
        ws = null
    };
    return ws;
}

onMounted(() => {
    // getlist()
    init()
})
watch(selectItems, (newVal, oldVal)=>{
    if (newVal.length === 0 || newVal.length != list.value.length) {
        selected.value = false
    } else {
        selected.value = true
    }
})
watch(list.value, (newVal, oldVal)=>{
    selectItems.length = 0
})
watch(token, (newVal, oldVal)=>{
    if (newVal === null || oldVal === null) {
        getlist()
    }
})

const getItems = (selectItems) => {
    const items = []
    list.value.forEach(el=>{
        selectItems.forEach(els=>{
            if (el.id === els) {
                items.push(el)
            }
        })
    })
    return items
}

const status_running = (item={}) => {
    let url = `${protocols[location.protocol]}://${location.host}${VUE_91_API}/status`
    const ws = new WebSocket(url);
    ws.onopen = (event) => {
        console.log(url + " Connection open ...");
        ws.send(JSON.stringify({ 'command': 'running' }));
    }
    ws.onmessage = (event) => {
        // console.log("Received Message: " + event.data);
        let data = event.data
        try {
            data = JSON.parse(data)
            if (data['command'] === 'running') {
                let status_data = data['params']
                // console.log(status_data)
                Object.assign(item,status_data )
                ws.send(JSON.stringify({ 'command': 'running' }));
            }
        } catch (error) {
            if (data === 'close') {
                ws.send('close');
            }
        }
    };
    ws.onclose = (event) => {
        console.log("Connection closed.");
    };
    return ws;
}

const modalSlots = reactive({
    item: {},
    opt: {},
})
// watch(()=>{return modalSlots.opt.content}, (newVal, oldVal)=> {
//     console.log(newVal, oldVal)
// })

const text_show = ref(null), modal_ = ref(null), offcanvas_ = ref(null), slideshow_ = ref(null)
const optlist = reactive({
    'editable': {
        name: '编辑',
        show: true,
        click: ()=>{
            editable.value = !editable.value
            if (!editable.value) selectItems.length = 0
        }
    },
    'logger': {
        name: '日志',
        show: true,
        click: ()=>{
            modalSlots.item.logger = true
            const ws = logger()
            modal_.destroy_ = ()=>{ws.close()}
            modal_.value.show()
        }
    },
    'local_config': {
        name: '本地配置',
        show: true,
        click: ()=>{
            offcanvas_.value.show()
            offcanvasSlots.opt.progress = {'filename': 'dist/video/0.m3u8', 'total': 0, 'scale': 0.0, 'speed': 0.0, 'threadNum': 0}
            let ws = status_running(offcanvasSlots.opt.progress)
            if (offcanvas_.destroy_ === undefined) offcanvas_.destroy_ = []
            offcanvas_.destroy_.push(()=>{ws.close()})
        }
    },
    'config': {
        name: '下载配置',
        show: true,
        click: ()=>{
            get91Config()
        }
    },
    'import': {
        name: '导入视频',
        show: computed(()=>{return editable.value}),
        click: ()=>{
            modalSlots.item.import = true
            modalSlots.opt = {'content': ''}
            modal_.value.show()
        },
        submit: (content)=>{
            // console.log(modalSlots.opt.content)
            const items = convertItems(content)
            // console.log(items)
            // return 
            if (!items || items.length <= 0) {
                proxy.$toast("items is empty")
                return
            }
            // console.log(items)
            // return
            do91Import({'items': items})
        }
    },
    'topic': {
        name: '解析帖子',
        show: true,
        click: ()=>{
            modalSlots.item.topic = true
            modal_.value.show()
        },
        submit: ()=>{
            doTopic({topid: modalSlots.opt.topid})
        }
    },
    'loadaccuntlist': {
        name: '解析用户',
        show: true,
        click: ()=>{
            modalSlots.item.loadaccuntlist = true
            modal_.value.show()
        },
        submit: ()=>{
            doUid({uid: modalSlots.opt.uid})
        }
    },
    'update': {
        name: '修改状态',
        show: computed(()=>{return selectItems.length > 0}),
        click: ()=>{
            modalSlots.item.update = true
            modal_.value.show()
        },
        submit: ()=>{
            doUpdate(modalSlots.opt.status_)
        }
    },
    'loadvideopage': {
        name: '解析视频',
        show: computed(()=>{return selectItems.length > 0}),
        click: ()=>{
            const items = getItems(selectItems)
            doVideoFun(proxy.$api.doParseVideoPage, {items})
        }
    },
    'downloadsrc': {
        name: '下载视频',
        show: computed(()=>{return selectItems.length > 0}),
        click: ()=>{
            const items = getItems(selectItems)
            doDownload({items})
        }
    },
    'check_keys': {
        name: '检查视频',
        show: computed(()=>{return selectItems.length > 0}),
        click: ()=>{
            const items = getItems(selectItems)
            doVideoFun(proxy.$api.doCheckVideo, {items})
        }
    },
    'tasks': {
        name: '后台任务',
        show: true,
        click: ()=>{
            tasks()
        }
    },
    'poster': {
        name: '更新封面',
        show: computed(()=>{return selectItems.length > 0}),
        click: ()=>{
            const items = getItems(selectItems)
            doVideoFun(proxy.$api.doPoster, {items})
        }
    },
    'thumbnails': {
        name: '更新预览',
        show: computed(()=>{return selectItems.length > 0}),
        click: ()=>{
            const items = getItems(selectItems)
            doVideoFun(proxy.$api.doThumbnails, {items})
        }
    },
    'export': {
        name: '导出',
        show: computed(()=>{return selectItems.length > 0}),
        click: ()=>{
            modalSlots.item.export = true
            const items = getItems(selectItems)
            modalSlots.opt = {'content': JSON.stringify(items, null, "\t"), 'readonly': true }
            modal_.value.show()
        }
    },
    'delete': {
        name: '删除',
        show: computed(()=>{return selectItems.length > 0}),
        click: ()=>{
            const items = []
            list.value.forEach(el=>{
                selectItems.forEach(els=>{
                    if (el.id === els) {
                        items.push(el)
                    }
                })
            })
            if (items.length <= 0) return
            let info = items[0].name
            if (items.length >= 2) {
                info += ", " + items[1].name + "..]等" + items.length + '项'
            } else {
                info += "]"
            }
            if (confirm('删除[' + info)) {
                do91Delete({items})
            }
        }
    },
    'package': {
        name: '打包',
        show: computed(()=>{return selectItems.length > 0}),
        click: ()=>{
            const keys = []
            list.value.forEach(el=>{
                selectItems.forEach(els=>{
                    if (el.id === els) {
                        keys.push(el.key)
                    }
                })
            })
            if (keys.length <= 0) return
            do91Package({keys: keys})
        }
    },
    'clear': {
        name: '清除缓存',
        show: computed(()=>{return editable.value}),
        click: ()=>{
            localStorage.clear('haijiao')
        }
    },
    'test': {
        name: '测试',
        show: true,
        click: ()=>{
            proxy.$toast(12121)
        }
    },
})

const editable = ref(false)

const playerDom = ref(null)
const play = (item) => {
    playerDom.value.play(item)
    modalSlots.item.video = true;
    modal_.value.show()
    modal_.destroy_ = ()=>{playerDom.value.dp.destroy()}
}

const offcanvasSlots = reactive({
    item: {},
    opt: {
        progress: {'filename': 'dist/video/0.m3u8', 'total': 0, 'scale': 0.0, 'speed': 0.0, 'threadNum': 0}
    },
})

const hiden = () => {
    Object.keys(modalSlots.item).forEach(el=>{
        modalSlots.item[el] = false
    })
    modal_.destroy_ && modal_.destroy_()
    modal_.destroy_ = null
}

const offcanvas_hiden = () => {
    if (offcanvas_.destroy_ &&  offcanvas_.destroy_ instanceof Array) {
        offcanvas_.destroy_.forEach(callback => {
            callback()
        })
    }
}

const modal_submit = ()=>{
    if (modalSlots.item.import) {
        optlist['import']['submit'](modalSlots.opt.content)
    }
    if (modalSlots.item.update) {
        optlist['update']['submit']()
    }
    if (modalSlots.item.topic) {
        optlist['topic']['submit']()
    }
    if (modalSlots.item.loadaccuntlist) {
        optlist['loadaccuntlist']['submit']()
    }
}

</script>

<template>
    <menuLayout>
        <template v-slot:section>
            <span class="input-group p-0"
                data-bs-toggle="list"
                v-hasRole="'admin'"
                href="#list-home" role="tab" :set="name=''">
                <!-- <input @keyup.enter="getlist({name, index: 1})" :set="name=''" v-model="name" class="w-100" type="text" placeholder="搜索影片" aria-label="搜索影片" aria-describedby="button-addon2"/> -->
                <input type="text" class="form-control" @keyup.enter="getlist({name, index: 1})" v-model="name" placeholder="搜索视频" aria-label="搜索视频" aria-describedby="button-search">
                <button class="btn btn-outline-secondary" type="button" id="button-search" @click="getlist({name, index: 1})"><i class="bi bi-search"></i></button>
            </span>
            <a class="list-group-item list-group-item-action" data-bs-toggle="list" href="#list-home" role="tab"
                v-for="item, index in status" :key="item.key"
                @click="getlist({status: item.key, index: 1})"
                v-hasRole="'admin'"
                :class="{active: item.current}">
                {{ item.name }}
            </a>
            <a class="list-group-item list-group-item-action pointer" 
                data-bs-toggle="list1" role="tab" 
                v-for="item, index in optlist" :key="item.key"
                v-show="item.show"
                @click="item.click"
                v-hasRole="'admin'">
                {{ item.name }}
            </a>
        </template>
        <template v-slot:main>
            <items :editable="editable" :view="tabName"
                :items="list" :select="selectItems" :page="page"
                @view="item => tabName = item" @getlist="getlist"
                @select-one="selectOne" @select-all="selectAll"
                @play="(item, index)=>{play(item);slideshow_.scrollTo(index);}">
                <template v-slot:navigate v-if="navigate.length > 0">
                    <li v-for="item, index in navigate" :key="index"
                        :class="{active: index === navigate.length - 1, pointer: index !== navigate.length - 1}"
                        class="breadcrumb-item  rounded" aria-current="page">
                        <span v-if="item.type==='root'" @click="getlist({uname: null, status: null, name: null, index: 1})">{{ item.name }}</span>
                        <span v-else-if="item.type==='uname'" @click="getlist({name:null, status: null, index: 1})">{{ item.name }}</span>
                        <span v-else-if="item.type==='name'" @click="getlist({status: null, index: 1})">{{ item.name }}</span>
                        <span v-else>{{ item.name }}</span>
                    </li>
                </template>
            </items>
            <scroll selector="main"></scroll>
            <!-- <div class="top">
                <div @click="event=>{const el = event.target.getRootNode().querySelector('main'); el.scrollTo({left: 0, top: 0, behavior: 'smooth'})}"><i class="bi bi-arrow-up-square"></i></div>
                <div  @click="event=>{const el = event.target.getRootNode().querySelector('main'); el.scrollTo({left: 0, top: el.scrollHeight, behavior: 'smooth'})}"><i class="bi bi-arrow-down-square"></i></div>
            </div> -->
        </template>
    </menuLayout>
    <modal ref="modal_" :submitShow="modalSlots.item.import || modalSlots.item.update || modalSlots.item.topic || modalSlots.item.loadaccuntlist" @submit="modal_submit" @hiden="hiden">
        <dplayer v-show="modalSlots.item.video" ref="playerDom"></dplayer>
        <slideshow ref="slideshow_" v-show="modalSlots.item.video" v-slot="{ item, index }" :items="list" @select="(item)=>{play(item)}" >
            <!-- loadBackPic -->
            <div style="width: 100px; height: 60px;">
                <div v-loadback="{val1: item.poster, val2: `${VUE_91_API}/${item.poster_local}`, width: '95%'}" class="rounded img"></div>
            </div>
            <!-- <img :src="item.poster" style="width: 100px; height: 60px;" :alt="item.tag"> -->
        </slideshow>
        <textarea class="show" ref="text_show"
            :readonly="modalSlots.opt['readonly']"
            v-if="modalSlots.item.export || modalSlots.item.logger"
            v-model="modalSlots.opt['content']">
        </textarea>
        <import91 v-if="modalSlots.item.import" v-model:content="modalSlots.opt.content" path='/haijiao'></import91>
        <config
            v-if="modalSlots.item.config"
            @save="doConfig"
            :items="modalSlots.opt['items']">
        </config>
        <div class="container"
            v-if="modalSlots.item.topic">
            <!-- doTopic({topid}) -->
            <div class="row configLine"></div>
            <div class="row">
                <div class="col-4">topid</div>
                <input class="col-6" v-model="modalSlots.opt.topid">
            </div>
            <div class="row">
                <div class="col configLine"></div>
            </div>
        </div>
        <div class="container"
            v-if="modalSlots.item.loadaccuntlist">
            <!-- doUid(params) -->
            <div class="row configLine"></div>
            <div class="row">
                <div class="col-4">uid</div>
                <input class="col-6" v-model="modalSlots.opt.uid">
            </div>
            <div class="row configLine"></div>
        </div>
        <div class="container"
            v-if="modalSlots.item.update">
            <!-- doUpdate(status_) -->
            <div class="row configLine"></div>
            <div class="row">
                <div class="col-6 offset-3 form-floating">
                    <select class="form-select" v-model="modalSlots.opt.status_">
                        <option value="">未选择</option>
                        <option value="-2">异常</option>
                        <option value="-1">暂停</option>
                        <option value="0">下载中</option>
                        <option value="1">下载完成</option>
                    </select>
                    <label for="floatingInput">状态</label>
                </div>
            </div>
            <div class="row configLine"></div>
        </div>
        <div class="container"
            v-if="modalSlots.item.tasks">
            <div class="row configLine"><div class="col-2">后台任务 [{{ modalSlots.opt['items'].length }}]</div></div>
            <div class="row" v-for="item in modalSlots.opt['items']">
                <div class="col-4 text-truncate">{{item.key}}</div>
                <div class="col-6 text-truncate">{{item.val}}</div>
                <div class="col-2"><button type="button" class="btn btn-outline-primary btn-sm" @click="stopTask({key: item.key})">停止</button></div>
            </div>
            <div class="row" v-if="!modalSlots.opt['items'] || modalSlots.opt['items'].length <= 0"><div class="col-2 offset-5 ">任务列表为空</div></div>
            <div class="row configLine"></div>
        </div>
    </modal>
    <offcanvas ref="offcanvas_" @hiden="offcanvas_hiden">
        <template #title>本地配置</template>
        <template #body>
            <div class="form-floating row mb-3 border rounded">
                <input type="range" class="form-control form-range" min="0" max="1000" step="5" v-model="req.params.pagesize">
                <label for="floatingInput">每页: {{req.params.pagesize}}</label>
            </div>
            <div class="row mb-3 border rounded" :set="progress = offcanvasSlots.opt.progress">
                <div class="progress">
                    <div class="progress-bar" role="progressbar" :style="{width: `${progress.scale}%`}" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">{{progress.scale.toFixed(2)}}%</div>
                </div>
                <div class="col-5 info-s">{{ size_normalize(progress.total) }}</div>
                <div class="col-5 info-v">{{ size_normalize(progress.speed) + '/s' }}</div>
                <div class="col-2 info-t">{{ progress.threadNum }}</div>
                <div class="col-12">{{ progress.item && progress.item.key }}</div>
                <div class="col-12">{{ progress.item && progress.item.name }}</div>
            </div>
        </template>
    </offcanvas>
    <div v-if="false"></div>
</template>
<style scoped>
html {
    scroll-behavior: smooth;
}
.pointer {
    cursor: pointer;
}
textarea.show {
    border: none;
    padding: 0;
    outline: none;
    background-color: rgba(251, 241, 227, 0.95);
    resize: none;
    width: 100%;
    height: 70vh;

    max-width: 100%;
    overflow-x: auto;
    display: -webkit-box;
    font-family: "Operator Mono", Consolas, Monaco, Menlo, monospace;
    border-radius: 5px;
    box-sizing: border-box !important;
    overflow-wrap: break-word !important;
    padding: 15px 16px 16px;
    font-size: 12px;
    /*
    outline: 0px;
    color: rgb(171, 178, 191);
    background: rgb(40, 44, 52); */
}

.btn-submit {
    box-sizing: content-box;
    width: 1em;
    height: 1em;
    padding: .25em .25em;
    color: #000;
    background: transparent url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23000'%3e%3cpath d='M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z'/%3e%3c/svg%3e") center/1em auto no-repeat;
    border: 0;
    border-radius: .25rem;
    opacity: .5;
    filter: invert(1) grayscale(100%) brightness(200%);
    position: absolute;
    top: 10px;
    right: 40px;
    box-shadow: inset 0 0 20px #fff;
}
.btn-submit:hover {
    color: #000;
    text-decoration: none;
    opacity: .75;
}
.nav-link_ {
    line-height: 2.5rem;
    color: #6c757d;
    background-color: transparent;
    border-color: transparent;
    margin-bottom: -1px;
    background: 0 0;
    border: 1px solid transparent;
    border-top-left-radius: 0.25rem;
    border-top-right-radius: 0.25rem;
    padding: 0.5rem 1rem;
    text-decoration: none;
    transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out;
}

.dplayer .title{
    color: rgb(255, 255, 255);
    position: absolute;
    top: 20px;
    left: 80px;
    background: #1b6068;
    padding: 5px;
}

.img {
    height: 100%;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background-size: cover;
    background-repeat: no-repeat;
    background-position: 50%;
}
.configLine {
    background-color: rgba(251, 241, 227, 0.95);
    height: 1.5rem;
}
.top{
    cursor: pointer;
    width: 60px;
    /* height: 40px; */
    border-radius: 10px;
    background: rgba(128, 128, 128, 0.92);
    color: blue;
    opacity: 0.5;
    line-height: 50px;
    text-align: center;
    font-size: 25px;
    position: absolute;
    bottom: 15%;
    right: 10%;
    /* display: none; */
}
</style>

