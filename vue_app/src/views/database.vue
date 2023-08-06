<script setup>
const { proxy } = getCurrentInstance();
const isJSON = function (str) {
    if (str.length <= 0) return false
    if (typeof str !== 'string') return false
    str = str.replace(/\\["\\\/bfnrtu]/g, '@').
        replace(/"[^"\\\n\r]*"|true|false|null|-?\d(?:\.\d*)?(?:[eE][\-]?\d)?/g, '').
        replace(/(?:^|:|,)(?:\s*\[) /g, '')
    return /^[\[\{].*[\}\]]$/.test(str)
}
const formatItem = (item) => {
    let result
    if (Object.prototype.toString.call(item) === '[object Array]') {
        result = []
        for (let key in item) {
            result.push(isJSON(item[key]) ? this.formatItem(JSON.parse(item[key])) : item[key])
        }
    } else {
        result = {}
        for (let key in item) {
            // console.log(item[key])
            result[key] = isJSON(item[key]) ? this.formatItem(JSON.parse(item[key])) : item[key]
            // result[key] = item[key]
        }
    }
    return JSON.stringify(result, null, "\t")
}
const result = ref(''), sql = ref('')
const doExecute = async (sql) => {
    const res = await proxy.$api.doExecute({sql});
    console.log( res['msg'], isJSON(res['msg']))
    if (res.code === 0) {
        result.value =  formatItem(JSON.parse(res['msg']))
    }else {
        result.value = res['msg']
    }
    console.log(result.value)
}

</script>

<template>
    <div class="row" style="height: 70%;">
        <div class="col-md-12 row" style="height: 10%; min-height: 100px;">
            <textarea class="col-md-10" style="resize: none;" v-model="sql"></textarea>
            <button class="btn btn-primary col-md-2" @click="doExecute(sql)">Execute</button>
        </div>
        <div class="col-md-12 row" style="height: 90%;">
            <textarea class="col-md-12" style="resize: none;" v-model="result"></textarea>
        </div>
    </div>
</template>
