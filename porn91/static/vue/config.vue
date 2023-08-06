<template>
    <div ref="config" class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
            <div class="modal-content container">
                <div class="row">
                    <div class="col" style="background-color: rgba(251, 241, 227, 0.95);">
                        <span class="btn" @click="add"><i class="fa fa-plus-square-o"></i></span>
                        <span class="btn"  @click="save"><i class="fa fa-floppy-o"></i></span>
                        <span class="btn"  @click="refresh"><i class="fa fa-refresh"></i></span>
                    </div>
                </div>
                <div class="row line">
                    <div class="col-2">Key</div>
                    <div class="col-8">Value</div>
                    <div class="col-1 text-center">En</div>
                    <div class="col-1 text-center">del</div>
                </div>
                <div class="row line" v-for="(item, key) in items" :key="key">
                    <div class="col-2 overflow-hidden text-break" @dblclick="focus($event)" @blur="change(item, 'key', $event)">{{ item.key }}</div>
                    <div class="col-8 overflow-hidden text-break" style="height: 2.5rem" @dblclick="focus($event)" @blur="change(item, 'value', $event)">{{ item.value }}</div>
                    <div class="col-1 text-center opt" @click="item.enable = !item.enable"><input type="checkbox" v-model="item.enable"></div>
                    <div class="col-1 text-center opt"><i class="fa fa-trash-o" @click="del(item)"></i></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
            return {
                items: [
                    {
                        key: 'sub',
                        value: 'https://jiang.netlify.app/',
                        enable: true,
                    }
                ],
                remove: [],
            }
        },
    props: ['content', 'show'],
    emits: ['save', 'refresh', 'update', 'hide'],
    mounted() {
        if (this.content && this.content instanceof Array && this.content.length > 0) {
            this.items = this.content
        }
        // this.modal('show')
        $(this.$refs.config).on('hide.bs.modal', ()=>{
            this.$emit('hide')
        })
    },
    methods: {
        ok() {
        },
        modal(status) {
            // show || hide
            $(this.$refs.config).modal(status)
        },
        add() {
            this.items.push({
                name: '',
                url: '',
                enable: false,
            })
        },
        refresh() {
            this.$emit('refresh')
            this.remove = []
        },
        save() {
            this.$emit('save', this.items, this.remove)
            this.remove = []

        },
        del(item) {
            if (item['id']) {
                this.remove.push(item['id'])
            }
            this.items.splice(this.items.indexOf(item), 1)
        },
        focus(event) {
            let el = event.target
            el.contentEditable = true
            el.focus()
            el.style.height = ''
        },
        change(item, key, event) {
            let el = event.target
            item[key] = el.innerText
            el.contentEditable = false
            el.style.height = '2.5rem'
        },
        log(str) {
            console.log(JSON.stringify(str))
        },
    },
    watch: {
        content: {
            handler(newVal, oldVal) {
                this.items = newVal
                // log(newVal, 'sub')
            },
            deep: true,
        },
        show(newVal, oldVal) {
            if (newVal) {
                this.modal('show')
            } else {
                this.modal('hide')
            }
        },
    },
    computed: {
    }
}
</script>

<style>
.opt {
  cursor: pointer;
}
.br {
    border-right: 1px solid #cccccc
}
.line {
    border-top: 1px solid #cccccc;
    line-height: 2.5rem;
}
</style>

<custom1>
  This could be e.g. documentation for the component.
</custom1>
