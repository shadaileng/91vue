<template>
    <div class="row">
        <div class="col-12">
            <div class="card" style="cursor: pointer">
                <div class="card-header">
                    <div class="row text-center">
                        <div @click="selectAll">
                            <input type="checkbox" v-model="selected">
                            <!-- <small class="float-right"  v-if="selectItems.length > 0"> {{ selectItems.length + '/' + (items ? items.length : 0) }}</small> -->
                        </div>
                        <div class="col" v-for="(field, key) in fields" :key="key" @click="$emit('sort', field)">{{field.text}}<i :class="{fa: true, 'fa-level-down': field['order'] > 0, 'fa-level-up': field['order'] < 0}"></i></div>
                    </div>
                </div>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item" v-for="item in items" :key="item.id" @click="selectOne(item.id, $event)">
                        <div class="row d-flex align-items-center">
                            <div class="mr-1"><input type="checkbox" :value="item.id" v-model="selectItems"></div>
                            <div class="col border-left text-truncate" v-for="(field, key) in fields" :key="key" data-toggle="tooltip" data-placement="top" :set="val=field.listId ? field.listId[item[field.name]] : item[field.name]" :title="val">{{val}}</div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
            return {
                selected: false,
                selectItems: [],
            }
        },
    props: ['items', 'fields'],
    emits: ['select', 'sort'],
    methods: {
        selectAll(){
            if (!this.items) return
            this.selectItems = []
            if (!this.selected) {
                this.items.forEach(el => {
                    this.selectItems.push(el.id)
                })
            }
        },
        selectOne(id, event) {
            if (event && event.target.tagName === "INPUT") {
                if (event.target.checked) {
                    this.selectItems.push(id)
                } else {
                    this.selectItems.splice(this.selectItems.indexOf(id), 1)
                }
                this.selectItems = this.selectItems
                return
            }
            this.selectItems = [id]
        },
    },
    watch: {
        selectItems: {
            handler(newVal, oldVal) {
                if (!this.items) return
                if (newVal.length === this.items.length) {
                    this.selected = true
                } else {
                    this.selected = false
                }
                // console.log('selectItems', newVal.length)
                this.$emit('select', newVal)
            },
            deep: true,
        }
    },
    computed: {
    }
}
</script>

<style>
.example {
  color: red;
}
</style>

<custom1>
  This could be e.g. documentation for the component.
</custom1>
