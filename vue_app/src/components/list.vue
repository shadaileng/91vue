<script setup>
import text from '@/components/text.vue'
import sign from '@/components/sign.vue'

const props = defineProps({
    items: Array,
    fields: Array,
})

const selectItems = reactive([])
const selected = ref(false)
const selectAll = () => {
    selectItems.length = 0
    if (!selected.value) {
        props.items.forEach(el=>{
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
const emit = defineEmits(['select', 'sort'])
watch(selectItems, (newVal, oldVal)=>{
    if (newVal.length === 0 || newVal.length != props.items.length) {
        selected.value = false
    } else {
        selected.value = true
    }
    emit('select', newVal)
})
// watch(props.items, (newVal, oldVal)=>{
//     selectItems.length = 0
// })

const colType = reactive({
    text: shallowRef(text),
    sign: shallowRef(sign),
})

</script>

<template>
    <div class="row">
        <div class="col-12">
            <div class="card" style="cursor: pointer">
                <div class="card-header">
                    <div class="row text-center">
                        <div @click.stop="selectAll" style="width: auto">
                            <input type="checkbox" v-model="selected">
                            <!-- <small v-if="selectItems.length > 0"> {{ selectItems.length + '/' + (items ? items.length : 0) }}</small> -->
                        </div>
                        <div class="col" v-for="(field, key) in fields" :key="key" @click="$emit('sort', field)" :class="field.show && field.show()">{{field.text}}<i :class="{fa: true, 'fa-level-down': field['order'] > 0, 'fa-level-up': field['order'] < 0}"></i></div>
                    </div>
                </div>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item" v-for="item in items" :key="item.id" @click="selectOne(item.id, $event)">
                        <div class="row d-flex align-items-center">
                            <div class="mr-1" style="width: auto"><input type="checkbox" :value="item.id" v-model="selectItems"></div>
                            <!-- <div class="col border-left text-truncate" v-for="(field, key) in fields" :key="key" :class="field.show && field.show()" data-toggle="tooltip" data-placement="top" :set="val=field.listId ? field.listId[item[field.name]] : item[field.name]" :title="val">{{val}}</div> -->
                            <div class="col border-left text-truncate"
                                v-for="(field, key) in fields" :key="key"
                                :class="field.show && field.show()"
                                :set="val=field.listId ? field.listId[item[field.name]] : item[field.name]"
                                :title="val"
                                data-toggle="tooltip" data-placement="top" >
                                    <component :is="colType[field.type] || colType['text']" :data="val" :opt="field.opt"></component>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>