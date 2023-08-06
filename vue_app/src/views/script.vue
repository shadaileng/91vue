<script setup>
const { proxy } = getCurrentInstance();
import { storeToRefs } from "pinia";
import { script } from "@/store/script";
import menuLayout from '@/components/menuLayout.vue'
import list from '@/components/list.vue'
import pagination from '@/components/pagination.vue'
import editor from '@/components/editor.vue'
import modal from '@/components/modal.vue'
const scriptStore = script();
const { mode, selectItems, item, page, req_params } = storeToRefs(scriptStore);


const items = reactive([])
// const selectItems = reactive([])
const fields = reactive([
    {
        name: 'name',
        text: '名称',
        order: 0,
        show: ()=>{return {
            'd-none': true,
            'd-md-block': true,
        }},
    },
    {
        name: 'desc',
        text: '描述',
        order: 0,
        show: ()=>{return {
            'd-none': true,
            'd-md-block': true,
        }},
    },
    {
        name: 'category',
        text: '类型',
        order: 0,
    },
    {
        name: 'status',
        text: '状态',
        order: 0,
    },
])

const doScriptImport = async (params) => {
    const res = await proxy.$api.doScriptImport(params);
    if (res) {
        if (res.code === 0) {
            proxy.$toast(res.msg)
        } else {
            proxy.$toast(`导入异常: ${res.msg}`)
        }
    }
};

const doDeleteScripts = async (params) => {
    const res = await proxy.$api.doDeleteScripts(params);
    if (res) {
        if (res.code === 0) {
            proxy.$toast(res.msg)
        } else {
            proxy.$toast(`删除异常: ${res.msg}`)
        }
    }
}
const getlist = async (params) => {
    selectItems.value.length = 0
    scriptStore.updateReqParams(params)
    const res = await proxy.$api.getScripts(scriptStore.getReqParams());
    if (res && res.code === 0) {
        // res.data.items
        // res.data.page
        scriptStore.setPage(res.data.page)
        items.length = 0
        items.push(...res.data.items)
    }
};
getlist()

const select = (ids) => {
    selectItems.value.length = 0
    items.forEach(item => {
        ids.forEach(id => {
            if (item.id === id) {
                selectItems.value.push(item)
            }
        })
    })
    /*
    if (selectItems.value.length > 0) {
        Object.assign(item.value, selectItems.value[0])
    }
    */
}

const doExport = async (params) => {
    modalSlots.item.export = true
    modalSlots.opt = {'content': JSON.stringify(selectItems.value, null, "\t"), 'readonly': true }
    modal_.value.show()
};




// const mode = reactive({
//     list: true,
//     editor: false,
// })
// const item = reactive({
//     id: null,
//     name: '',
//     desc: '',
//     poster: `https://www.python.org/static/img/python-logo.png`,
// })

const optlist = reactive({
    'newOne': {
        name: '新建',
        show: true,
        click: ()=>{
            scriptStore.init()
            Object.keys(mode.value).forEach(key => {
                mode.value[key] = false
            })
            mode.value['editor'] = true
        }
    },
    'import': {
        name: '导入',
        show: true,
        click: ()=>{
            modalSlots.item.import = true
            modalSlots.opt = {'content': '', 'readonly': false }
            modal_.value.show()
        },
        submit: ()=> {
            console.log(JSON.parse(modalSlots.opt.content))
            doScriptImport({'items': JSON.parse(modalSlots.opt.content)})
        }
    },
    'editor': {
        name: '编辑',
        show: computed(()=>{return selectItems.value.length === 1}),
        click: ()=>{
            Object.assign(item.value, selectItems.value[0])
            Object.keys(mode.value).forEach(key => {
                mode.value[key] = false
            })
            mode.value['editor'] = true
        }
    },
    'export': {
        name: '导出',
        show: computed(()=>{return selectItems.value.length >= 1}),
        click: doExport
    },
    'delete': {
        name: '删除',
        show: computed(()=>{return selectItems.value.length >= 1}),
        click: ()=>{
            if(confirm("是否删除选择项?")) {
                doDeleteScripts({items: selectItems.value}).then(()=>{
                    getlist()
                })
            }
        }
    },
    'list': {
        name: '列表',
        show: computed(()=>{return mode.value['editor']}),
        click: ()=>{
            Object.keys(mode.value).forEach(key => {
                mode.value[key] = false
            })
            mode.value['list'] = true
            getlist()
        }
    },
})

const modal_submit = () => {
    if (modalSlots.item.import) {
        optlist['import']['submit']()
    }
    if (modalSlots.item.save) {
        doSave(modalSlots.opt.item)
    }
}

const modal_ = ref(null), edit = ref(null)
const modalSlots = reactive({
    item: {},
    opt: {},
})
const save = value => {
    // console.log(value)
    modalSlots.item.save = true
    modalSlots.opt.item = item.value
    // if (selectItems.value.length > 0) {
    //     modalSlots.opt.item = Object.assign({}, selectItems.value[0])
    // }
    modal_.value.show()
}

const doSave = item => {
    item.category = 'python'
    item.status = 1
    // console.log(item)
    doScriptImport({'items': [item]})
}

const hiden = ()=>{
    modalSlots.item = {}
    modalSlots.opt = {}
    // console.log(modalSlots)
}

// watch(()=>item.value.content, (newval, oldval)=>{
//     console.log(newval, oldval)
// })

</script>

<template>

    <menuLayout>
        <template v-slot:section>
            <a class="list-group-item list-group-item-action" data-bs-toggle="list" href="#list-home" role="tab"
                v-for="item, index in optlist" :key="item.key"
                v-show="item.show"
                @click="item.click">
                {{ item.name }}
            </a>
        </template>
        <template v-slot:main>
            <list v-if="mode['list']" :fields="fields" :items="items" @select="select"></list>
            <editor v-if="mode['editor']" v-model:content="item.content" @save="save"></editor>
            <div class="row" v-if="mode['list']">
                <div class="col-12">
                    <pagination @pageto="index => getlist({index})"
                        :total_count="page.total"
                        :total_page="page.pages"
                        :pageno="page.index"
                        :count="page.size"></pagination>
                </div>
            </div>
        </template>
    </menuLayout>
    <modal ref="modal_" :submitShow="modalSlots.item.import || modalSlots.item.save" @submit="modal_submit" @hiden="hiden">
        <textarea class="text_show" ref="text_show"
            :readonly="modalSlots.opt['readonly']"
            v-if="modalSlots.item.export || modalSlots.item.import"
            v-model="modalSlots.opt['content']">
        </textarea>
        <div v-if="modalSlots.item.save" class="container board">
            <div class="row configLine"><hr></div>
            <div class="row main flex-fill" :set="item = modalSlots.opt.item">
                <div ref="edit" class="col-md-6 edit">
                    <div class="form-floating mb-3">
                        <input type="number" class="form-control" id="id" name='id' v-model="item.id" readonly placeholder="id">
                        <label for="key">id</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="id" name='id' v-model="item.key" :readonly="item.id !== null" placeholder="key">
                        <label for="key">key</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="name" name='name' v-model="item.name" placeholder="名称">
                        <label for="name">名称</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="desc" name='desc' v-model="item.desc" placeholder="描述">
                        <label for="desc">描述</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="poster" name='poster' v-model="item.poster" placeholder="封面地址">
                        <label for="poster">封面地址</label>
                    </div>
                </div>
                <div class="col-md-6 edit">
                    <textarea v-model="item.content" readonly></textarea>
                </div>
            </div>
            <div class="row configLine"><hr></div>
        </div>
    </modal>
</template>

<style scoped>
textarea {
    border: none;
    padding: 0;
    outline: none;
    background-color: rgba(251, 241, 227, 0.95);
    resize: none;

    max-width: 100%;
    overflow-x: auto;
    display: -webkit-box;
    font-family: "Operator Mono", Consolas, Monaco, Menlo, monospace;
    border-radius: 5px;
    border-bottom: 1px solid #ccc;
    box-sizing: border-box !important;
    overflow-wrap: break-word !important;
    padding: 15px 16px 16px;
    font-size: 12px;
    /*
    outline: 0px;
    color: rgb(171, 178, 191);
    background: rgb(40, 44, 52); */
}
.board {
    resize: none;
    /* height: 80vh; */
    background-color: rgba(251, 241, 227, 0.95);
    overflow: hidden;
}
.main {
    position: relative;
    height: 85%;
}
.edit  {
    border-top: 1px solid black;
    border-right: 1px solid black;
}
.main textarea {
    width: 100%;
    height: 100%;
}
textarea.text_show {
    width: 100%;
    height: 70vh;
}

.configLine {
    background-color: rgba(251, 241, 227, 0.95);
    height: 2.5rem;
}
</style>