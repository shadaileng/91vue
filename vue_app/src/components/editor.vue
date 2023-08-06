<script setup>
const { proxy } = getCurrentInstance();
import { storeToRefs } from "pinia";
import { script } from "@/store/script";
import menuLayout from '@/components/menuLayout.vue'
import modal from '@/components/modal.vue'
const scriptStore = script();
const { result, content } = storeToRefs(scriptStore);

const props = defineProps({
    content: String,
})
const emit = defineEmits(['save', 'update:content'])

// const result = ref(''), content = ref('')
const doExecute = async (content) => {
    const res = await proxy.$api.doScriptExecute({content});
    result.value =  res['msg']
}

content.value = props.content
const lineNumbers = ref((content.value ? content.value.split('\n').length : 0) + 4)
watch(()=>{return content.value}, (newVal, oldVal)=> {
    lineNumbers.value = content.value.split('\n').length + 4
})

const tabWidth = 4
const tab = event => {
    const el = event.target
    let beg = el.value.substring(0, el.selectionStart).lastIndexOf("\n")+1
    let end = el.value.substring(el.selectionEnd).indexOf("\n") + el.selectionEnd
    // console.log(el.value.substring(beg, end))
    const splits = el.value.substring(beg, end).split('\n')
    const beg_ = el.selectionStart
    const end_ = el.selectionEnd
    let offset_1 = 0
    for (let i = 0, l = splits.length; i < l; ++i) {
        const line = splits[i]
        const num = line.replace(/^(\s*).*/, '$1').length
        splits[i] = line.padStart(line.length + (tabWidth - num % tabWidth), " ")
        if (i === 0) offset_1 = tabWidth - num % tabWidth
    }
    if (el.selectionStart !== el.selectionEnd) {
        // console.log(splits.join("\n"))
        el.selectionStart = beg
        el.selectionEnd = end
        el.setRangeText(splits.join("\n"));
        el.selectionStart = beg_ + offset_1
        el.selectionEnd = end_ + tabWidth * splits.length
    } else {
        el.setRangeText("".padStart(offset_1, ' '));  // 输入两个空格作为tab
        el.selectionStart += offset_1;  // 输入后将光标后移
    }
    content.value = el.value
}

const tab_shift = event => {
    const el = event.target
    let beg = el.value.substring(0, el.selectionStart).lastIndexOf("\n")+1
    let end = el.value.substring(el.selectionEnd).indexOf("\n") + el.selectionEnd
    // console.log(el.value.substring(beg, end))
    const splits = el.value.substring(beg, end).split('\n')
    const beg_ = el.selectionStart
    const end_ = el.selectionEnd
    let offset_1 = 0, offset_2 = 0
    for (let i = 0, l = splits.length; i < l; ++i) {
        const line = splits[i]
        const num = line.replace(/^(\s*).*/, '$1').length
        let sub_start = tabWidth
        if (num > 0) {
            if (num % tabWidth) {
                sub_start = num % tabWidth
            }
            splits[i] = line.substring(sub_start)
            if (i === 0) offset_1 = sub_start
            offset_2 += sub_start
        }
    }
    // console.log(splits.join("\n"))
    el.selectionStart = beg
    el.selectionEnd = end
    el.setRangeText(splits.join("\n"));

    if (beg_ !== end_) {
        el.selectionStart = beg_ - offset_1
        el.selectionEnd = end_ - offset_2
    } else {
        el.selectionStart = beg_ - offset_1
        el.selectionEnd = el.selectionStart
    }
    content.value = el.value
}

const enter = event => {
    const el = event.target
    const line = el.value.substring(el.value.substring(0, el.selectionStart).lastIndexOf("\n")+1, el.selectionStart)
    const space_len = line.replace(/^(\s*).*/, '$1').length + ([':', '{'].includes(el.value.substring(el.selectionStart - 1, el.selectionStart)) ? tabWidth : 0)
    el.setRangeText("\n");  // 换行,输入两个空格作为tab
    el.selectionStart += 1;  // 输入后将光标后移
    el.setRangeText("".padEnd(space_len, " "));  // 换行,输入两个空格作为tab
    el.selectionStart += space_len;  // 输入后将光标后移
    content.value = el.value
}

const delete_line = event => {
    const el = event.target
    let beg = el.value.substring(0, el.selectionStart).lastIndexOf("\n") // 上一行末
    let end = el.value.substring(el.selectionEnd).indexOf("\n") + el.selectionEnd
    const beg_ = el.selectionStart
    // 选择上一行末到末行末
    el.selectionStart = beg
    el.selectionEnd = end
    // 删除选中
    el.setRangeText("");
    // 设置选择为开始
    el.selectionStart = beg_
    el.selectionEnd = beg_
    content.value = el.value
}

const copy_line = event => {
    const el = event.target
    let beg = el.value.substring(0, el.selectionStart).lastIndexOf("\n") // 上一行末
    let end = el.value.substring(el.selectionEnd).indexOf("\n") + el.selectionEnd
    // console.log(el.value.substring(beg, end))
    const beg_ = el.selectionStart
    // 光标设置在末行行末
    el.selectionStart = end
    el.selectionEnd = end
    // 插入选择行
    if (!el.value.substring(beg, end).startsWith('\n')) {
        el.setRangeText('\n' + el.value.substring(beg, end));
    } else {
        el.setRangeText(el.value.substring(beg, end));
    }
    // 设置选择为下行行首
    el.selectionStart = end + 1
    el.selectionEnd = end + 1
    content.value = el.value
}

const other_key = event => {
    const el = event.target
    if (event.key === "'") {
        el.setRangeText("'");
    }
    if (event.key === '"') {
        el.setRangeText('"');
    }
    if (event.key === '{') {
        el.setRangeText('}');
    }
    if (event.key === '(') {
        el.setRangeText(')');
    }
    if (event.key === '[') {
        el.setRangeText(']');
    }
    content.value = el.value
    emit('update:content', content)
}

const rows_cols = ref(`[0, 0]`)
const move = event => {
    const el = event.target
    const content = el.value.substring(0, el.selectionStart)
    rows_cols.value = `[${content.split('\n').length}, ${el.selectionStart - content.lastIndexOf("\n")}]`
    // console.log(rows_cols)
}

</script>
<template>
    <div class="row flex-fill" style="height: calc(100% - 200px);overflow-y: auto; counter-reset: linenumber">
        <div class="col-md-1 line-numbers"><span v-for="num in lineNumbers" :key="num"></span></div>
        <textarea class="col-md-11 edit" rows="3" style="white-space: nowrap;"
            @keydown.tab.prevent.exact="tab"
            @keydown.shift.tab.prevent.exact="tab_shift"
            @keydown.ctrl.shift.k.prevent.exact="delete_line"
            @keydown.ctrl.d.prevent.exact="copy_line"
            @keydown.ctrl.s.prevent.exact="emit('save', content)"
            @keydown.enter.prevent.exact="enter"
            @keydown="other_key"
            @mouseup="move"
            @keyup="move"
            v-model="content"></textarea>
    </div>
    <div class="row" style="height: 200px;">
        <textarea class="col-md-10" rows="5" readonly v-model="result"></textarea>
        <div class="col-md-2 row ms-1">
            <div class="col-12 "><span>{{rows_cols}}</span></div>
            <button class="btn btn-primary col-12" @click="doExecute(content)">Execute</button>
            <button class="btn btn-primary col-12" @click="emit('save', content)">Save</button>
        </div>
    </div>
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
    overflow: hidden;
    outline: 0px;
    color: rgb(171, 178, 191);
    background: rgb(40, 44, 52); */
}
.line-numbers {
    /* width: 30px; */
    padding: 15px 5px 0px;
    font-size: 12px;
    text-align: right;
}

.line-numbers span {
    counter-increment:  linenumber;
}

.line-numbers span::before {
    content: counter(linenumber);
    display: block;
    color: #506882;
}
.edit-info {
    width: 60px;
    padding: 15px 5px 0px;
    font-size: 12px;
    text-align: right;
}

/*
.btn {
    position: relative;
}
.btn::after {
    content: "tooltips";
    background: #333;
    color: white;
    border-radius: 5px;
    position: absolute;
    top: 0;
    left: 50%;
    transform: translate(-50%, calc(-100% - 10px))
}
.btn::before {
    content: '';
    background: #333;
    position: absolute;
    width: 15px;
    height: 15px;
    top: 0;
    left: 50%;
    transform: translate(50%, calc(-100% - 5px)) rotate(45deg);
}
*/
</style>