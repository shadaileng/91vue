<script setup>
const content = ref('')
const edit = ref(null)

const props = defineProps({
    content: String,
    path: String,
})

const emit = defineEmits(['update:content'])
const additem = () => {
    let _obj = {}
    edit.value.querySelectorAll('input').forEach(el => {
        _obj[el.name] = el.value ? el.value : null
    })
    if (!_obj['key']) return
    _obj['path'] = props.path
    let add_obj = []
    if (content.value) {
        add_obj = JSON.parse(content.value)
    }
    add_obj.push(_obj)
    content.value = JSON.stringify(add_obj, null, "\t")
}

watch(()=>{return content.value}, (newVal, oldVal)=> {
    // console.log(newVal, oldVal)
    emit('update:content', newVal)
})

</script>

<template>
    <div class="container board">
        <div class="row configLine">
            <a class="btn col-2 offset-5" @click="additem"><i class="bi bi-database-fill-add"></i></a>
        </div>
        <div class="row main flex-fill">
            <div ref="edit" class="col-md-6 edit">
                <div class="form-floating mb-3">
                    <input type="text" class="form-control" id="key" name='key' placeholder="Key">
                    <label for="key">Key</label>
                </div>
                <div class="form-floating mb-3">
                    <input type="text" class="form-control" id="name" name='name' placeholder="名称">
                    <label for="name">名称</label>
                </div>
                <div class="form-floating mb-3">
                    <input type="text" class="form-control" id="src" name='src' placeholder="下载地址">
                    <label for="src">下载地址</label>
                </div>
                <div class="form-floating mb-3">
                    <input type="text" class="form-control" id="poster" name='poster' placeholder="封面地址">
                    <label for="poster">封面地址</label>
                </div>
                <div class="form-floating mb-3">
                    <input type="text" class="form-control" id="publish_date" name='publish_date' placeholder="发布日期">
                    <label for="publish_date">发布日期</label>
                </div>
            </div>
            <div class="col-md-6 edit">
                <textarea v-model="content" rows="18"></textarea>
            </div>
        </div>
        <div class="row configLine"><hr></div>
    </div>
</template>

<style>
.board {
    /* resize: none;
    height: 80vh; */
    background-color: rgba(251, 241, 227, 0.95);
}
.main {
    position: relative;
    /* overflow: scroll; */
}
.form  {
    border-top: 1px solid black;
    border-right: 1px solid black;
}
.edit  {
    border-top: 1px solid black;
    border-right: 1px solid black;
}
textarea {
    resize: none;
    width: 100%;
    height: 100%;
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
}
.configLine {
    background-color: rgba(251, 241, 227, 0.95);
    height: 2.5rem;
}
</style>
