<script setup>
import QRCode from 'qrcode'
import menuLayout from '@/components/menuLayout.vue'
import list from '@/components/list.vue'
import modal from '@/components/modal.vue'
import config from '@/components/config.vue'
import { computed } from 'vue';
import { reactive } from '@vue/reactivity'

import { storeToRefs } from "pinia";
import { user } from "@/store/user";
import config_ from "@/config"
const VUE_91_API = config_.apis.porn91

const userStore = user();
const { token, roles } = storeToRefs(userStore);

const { proxy } = getCurrentInstance();

const v2rays = reactive([])
const fields = reactive([
    {
        name: 'protocol',
        text: '协议',
        order: 0,
        show: ()=>{return {
            'd-none': true,
            'd-md-block': true,
        }},
    },
    {
        name: 'subscribe',
        text: '订阅',
        order: 0,
        show: ()=>{return {
            'd-none': true,
            'd-md-block': true,
        }},
    },
    {
        name: 'remarks',
        text: '名称',
        order: 0,
    },
    {
        name: 'result',
        text: '校验结果',
        order: 0,
    },
    {
        name: 'enabled',
        text: '启动服务',
        order: 0,
        type: 'sign',
    },
])


const updateV2rays = (v2rays, v2rays_, fields) => {
    v2rays.length = 0
    Object.assign(v2rays, v2rays_)

    fields.forEach(field_ => {
        field_['order'] = 0
    })
}

const getlist = async (params) => {
    if (!userStore.hasRole('admin')) {
        updateV2rays(v2rays, [], fields)
        return
    }
    const res = await proxy.$api.getV2ray();
    if (res.code === 0) {
        // v2rays.length = 0
        // Object.assign(v2rays, res.msg.items)
        updateV2rays(v2rays, res.msg.items, fields)
    }
};

const trancsConfig = (data) => {
    const items = []
    data.forEach(item => {
        items.push({id: item.id, key: item.name, value: item.url, enable: item.enable})
    })
    return items
}

const subs = reactive([])

const getV2rayConfig = async (params) => {
    const res = await proxy.$api.getV2rayConfig(params);
    if (res) {
        if (res.code === 0) {
            subs.length = 0
            Object.assign(subs, res.msg.items)
        } else {
            proxy.$toast(`获取配置: ${res.msg}`)
        }
    }
};

const doV2rayConfig = async (items, remove) => {
    if (remove instanceof Array && remove.length > 0) {
        const res = await proxy.$api.doV2rayConfigDel({ids: remove});
        if (res) {
            // console.log(res)
            if (res.code === 0) {
                subs.length = 0
                Object.assign(subs, res.msg.items)
                modalSlots.opt = {'items': trancsConfig(subs) }
                proxy.$toast(`保存成功`)
            } else {
                proxy.$toast(`保存配置: ${res.msg}`)
            }
        }
    }
    if (items instanceof Array && items.length > 0) {
        const items_ = []
        items.forEach(item=> {
            items_.push({id: item.id, name: item.key, url: item.value, enable: item.enable})
        })
        const res = await proxy.$api.doV2rayConfigSave({items: items_});
        if (res) {
            // console.log(res)
            if (res.code === 0) {
                subs.length = 0
                Object.assign(subs, res.msg.items)
                modalSlots.opt = {'items': trancsConfig(subs) }
                proxy.$toast(`保存成功`)
            } else {
                proxy.$toast(`保存配置: ${res.msg}`)
            }
        }
    }
}

const doSubsUpdate = async (params) => {
    const res = await proxy.$api.doSubsUpdate(params);
    if (res.code === 0) {
        // v2rays.length = 0
        // Object.assign(v2rays, res.msg.items)
        updateV2rays(v2rays, res.msg.items, fields)
    }
};

const doDeleteV2rays = async (params) => {
    const res = await proxy.$api.doDeleteV2rays(params);
    if (res.code === 0) {
        // v2rays.length = 0
        // Object.assign(v2rays, res.msg.items)
        updateV2rays(v2rays, res.msg.items, fields)
    }
}

const doEnableV2ray = async (params) => {
    const res = await proxy.$api.doEnableV2ray(params);
    if (res.code === 0) {
        // v2rays.length = 0
        // Object.assign(v2rays, res.msg.items)
        updateV2rays(v2rays, res.msg.items, fields)
    }
}

const onPaste = async (event) => {
    if (navigator.clipboard) {
        (async () => {
            const text = await navigator.clipboard.readText();
            importClip(text)
        })();
    } else {
        modalSlots.item.import = true
        modalSlots.opt.content = ''
        modal_.value.show()
    }
}

const doExport = async (params) => {
    if (!userStore.hasRole('admin')) {
        return
    }
    const res = await proxy.$api.doExport(selectItems[0].id);
    if (res.code === 0) {
        // v2rays.length = 0
        // Object.assign(v2rays, res.msg.content)
        modalSlots.item.export = true
        modalSlots.opt = {'content': res.msg.content, 'readonly': true }
        modal_.value.show()
    }
};

const importClip = async (text) => {
    const res = await proxy.$api.importClip({text});
    if (res) {
        if (res.code === 0) {
            updateV2rays(v2rays, res.msg.items, fields)
            proxy.$toast(`导入成功`)
        } else {
            proxy.$toast(`导入失败: ${res.msg}`)
        }
    }
}

const selectItems = reactive([])

const select = (ids) => {
    selectItems.length = 0
    v2rays.forEach(v2ray => {
        ids.forEach(id => {
            if (v2ray.id === id) {
                selectItems.push(v2ray)
            }
        })
    })
}

const sort = (field) => {
    if (field['order'] === 1) {
        field['order'] = -1
    } else if (field['order'] === -1) {
        field['order'] = 1
    } else {
        field['order'] = 1
    }
    fields.forEach(field_ => {
        if (field_['name'] !== field['name']) {
            field_['order'] = 0
        }
    })
    v2rays.sort((a, b) => {
        let name = field['name']
        if (!a[name] || !b[name]) {
            if (field['order'] >= 0) {
                if (!a[name] && b[name]) return -1
                if (a[name] && !b[name]) return 1
            } else {
                if (!a[name] && b[name]) return 1
                if (a[name] && !b[name]) return -1
            }
            if (!a[name] && !b[name]) return 0
        }
        if (typeof (a[name]) === 'number') {
            if (field['order'] >= 0) {
                return a[name] - b[name]
            } else {
                return b[name] - a[name]
            }
        }
        else {
            if (field['order'] >= 0) {
                return a[name].localeCompare(b[name])
            } else {
                return b[name].localeCompare(a[name])
            }
        }
    })
}

const logger = () => {
    let url = 'ws://' + location.host + `${VUE_91_API}/tail`
    let ws = new WebSocket(url);
    ws.onopen = (event) => {
        modalSlots.opt = {
            content: '',
            ws: ws,
            readonly: true,
        }
        console.log(url + " Connection open ...");
        ws.send('1 info.log');
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


const test_progress = reactive({
    num: 0,
    total: 0,
    scale: 100,
})
const optlist = computed(()=>{
    const optlist_ = reactive({
        'config': {
            name: '订阅配置',
            show: () => {userStore.hasRole('admin')},
            click: ()=>{
                getV2rayConfig().then(()=>{
                    modalSlots.item.config = true
                    modalSlots.opt = {'items': trancsConfig(subs) }
                    modal_.value.show()
                })
            },
        },
        'update': {
            name: '更新订阅',
            show: () => {userStore.hasRole('admin')},
            click: () => {
                doSubsUpdate({items: subs})
            },
        },
        'logger': {
            name: '日志',
            show: () => {userStore.hasRole('admin')},
            click: () => {
                modalSlots.item.logger = true
                const ws = logger()
                modal_.destroy_ = ()=>{ws.close()}
                modal_.value.show()
            },
        },
        'import': {
            name: '导入',
            show: () => {userStore.hasRole('admin')},
            click: onPaste,
        },
        'export': {
            name: '导出',
            show: computed(()=>{return userStore.hasRole('admin') && selectItems.length === 1}),
            click: doExport
        },
        'copy': {
            name: '复制',
            show: computed(()=>{return userStore.hasRole('admin') && selectItems.length > 0}),
            click: ()=>{
                if (selectItems.length <= 0) return
                let text = ""
                selectItems.forEach(item => {
                    text += item.url + "\n"
                })
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(text).then(function () {
                        /* clipboard successfully set */
                        // console.log('复制: \n' + text)
                        proxy.$toast('已复制')
                    }, function () {
                        /* clipboard write failed */
                        console.log('复制失败')
                        proxy.$toast('复制失败')
                    })
                } else {
                    console.log('粘贴板已禁用')
                    let el = event.target
                    let coptel = el.querySelector('textarea')
                    if (!coptel) {
                        coptel = document.createElement('textarea')
                        coptel.style = "opacity: 0;position: absolute; padding: 0px; border: 0px none;"
                        el.appendChild(coptel)
                    }
                    coptel.value = text
                    coptel.focus();
                    if (coptel.setSelectionRange) coptel.setSelectionRange(0, coptel.value.length);
                    else coptel.select();
                    document.execCommand('Copy')
                    // console.log('复制: \n' + coptel.value)
                    proxy.$toast('已复制')
                }
            }
        },
        'share': {
            name: '分享',
            show: computed(()=>{return userStore.hasRole('admin') && selectItems.length > 0}),
            click: ()=>{
                if (selectItems.length <= 0) return
                let text = ""
                selectItems.forEach(item => {
                    text += item.url + "\n"
                })
                QRCode.toDataURL(text, {
                        colorDark: "#111111",
                        colorLight: "#ffeeff",
                        correctLevel: 'L',
                    })
                    .then(url => {
                        // console.log(url)
                        modalSlots.item.share = true
                        modalSlots.opt = {'content': url }
                        modal_.value.show()
                    })
                    .catch(err => {
                        console.error(err)
                        proxy.$toast(JSON.stringify(err))
                    })
            }
        },
        'delete': {
            name: '删除',
            show: computed(()=>{return userStore.hasRole('admin') && selectItems.length > 0}),
            click: ()=>{
                if (selectItems.length <= 0) return
                let info = selectItems[0].remarks
                if (selectItems.length >= 2) {
                    info += ", " + selectItems[1].remarks + "..]等" + selectItems.length + '项'
                } else {
                    info += "]"
                }
                const ids = []
                selectItems.forEach(item => {
                    ids.push(item.id)
                })
                if (confirm('删除[' + info)) {
                    doDeleteV2rays({ids})
                }
            }
        },
        'enable': {
            name: computed(() => {return (selectItems.length > 0 && selectItems[0].enabled) ? '关闭': '启动'}),
            show: computed(()=>{return userStore.hasRole('admin') && selectItems.length === 1}),
            click: ()=>{
                if (selectItems.length !== 1) return
                const item = selectItems[0]
                const ids = [item.id]
                doEnableV2ray({
                    ids: ids,
                    enable: (item.enabled ? 0 : 1)
                })
            }
        },
        'test': {
            name: '测试',
            show: computed(()=>{return userStore.hasRole('admin') && selectItems.length > 0}),
            click: ()=>{
                if (selectItems.length <= 0) return
                const url = 'ws://' + location.host + `${VUE_91_API}/v2ray/v2ray_test`
                const ws = new WebSocket(url);
                const ids = []
                let index = 0
                selectItems.forEach(item => {
                    ids.push(item.id)
                })
                const cmd = 'v2ray_test ' + JSON.stringify(ids)
                ws.onopen = (event) => {
                    console.log(url + " Connection open ...");
                    ws._send(cmd)
                    test_progress.num = 0
                    test_progress.total = ids.length
                    test_progress.scale = 0
                }
                ws._send = function (cmd) {
                    console.log("send " + cmd);
                    ws.send(cmd);
                }
                ws.onmessage = (event) => {
                    // console.log(event.data)
                    let data = JSON.parse(event.data)
                    for (let v2ray of v2rays) {
                        if (v2ray['id'] === data['id']) {
                            v2ray['result'] = data['result']
                            // v2ray['enabled'] = data['enabled']
                            index++
                            test_progress.num = index
                            test_progress.total = ids.length
                            test_progress.scale = ids.length === 0 ? 100.00 : index / ids.length * 100
                            break
                        }
                    }
                };
                ws.onclose = (event) => {
                    console.log("Connection closed.");
                };
                return ws
            }
        },
    })
    return optlist_
})


const text_show = ref(null)
const modal_ = ref(null)
const modalSlots = reactive({
    item: {},
    opt: {},
})
const hiden = () => {
    Object.keys(modalSlots.item).forEach(el=>{
        modalSlots.item[el] = false
    })
    if (modal_.destroy_){
        if (modal_.destroy_ instanceof Array) {
            modal_.destroy_.forEach(callback => {
                callback()
            })
        } else if (modal_.destroy_ instanceof Function) {
            modal_.destroy_()
        }
    }
}

onMounted(()=>{
    getlist()
    getV2rayConfig()
})
watch(token, (newVal, oldVal)=>{
    if (newVal === null || oldVal === null) {
        getlist()
    }
})

</script>
<template>
    <menuLayout>
        <template v-slot:section>
            <div class="list-group-item list-group-item-action disabled" data-bs-toggle="list" href="#list-home" role="tab">
                {{ selectItems.length }} / {{ v2rays.length }}
            </div>
            <a class="list-group-item list-group-item-action" data-bs-toggle="list" href="#list-home" role="tab"
                v-for="item, index in optlist" :key="item.name"
                v-show="item.show"
                @click="item.click"
                v-hasRole="'admin'">
                {{ item.name }}
            </a>
            <div class="progress" v-if="test_progress.scale < 100">
                <div class="progress-bar" role="progressbar" :style="{width: `${Math.max(25, test_progress.scale)}%`}" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">{{`${test_progress.num} / ${test_progress.total}`}}</div>
            </div>
        </template>
        <template v-slot:main>
            <list :fields="fields" :items="v2rays" @select='select' @sort="sort"></list>
        </template>
    </menuLayout>
    <modal ref="modal_" @hiden="hiden">
        <textarea class="show" ref="text_show"
            :readonly="modalSlots.opt['readonly']"
            v-if="modalSlots.item.export || modalSlots.item.import || modalSlots.item.logger"
            @paste="importClip(modalSlots.opt['content'])"
            v-model="modalSlots.opt['content']">
        </textarea>
        <img v-if="modalSlots.item.share" :src="modalSlots.opt['content']">
        <config
            v-if="modalSlots.item.config"
            @save="doV2rayConfig"
            :items="modalSlots.opt['items']">
        </config>
    </modal>
</template>
<style scoped>
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
</style>
