<template>
    <div>
        <div class="dropdown" style="width: min-content;">
            <button class="btn btn-sm dropdown-toggle" data-toggle="dropdown" aria-expanded="false">订阅</button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <a class="dropdown-item" href="#" @click="modal('show')"><i class="fa fa-paperclip"></i> 订阅设置</a>
                <a class="dropdown-item" href="#" @click="$emit('update')"><i class="fa fa-cog"></i> 更新订阅</a>
                <a class="dropdown-item" href="#" @click="clip"><i class="fa fa-upload"></i> 导入</a>
            </div>
        </div>
        <div ref="config" class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
                <div class="modal-content container">
                    <div class="row">
                        <div class="col" style="background-color: rgba(251, 241, 227, 0.95);">
                            <span class="btn" @click="add"><i class="fa fa-plus-square-o"></i></span>
                            <span class="btn"  @click="save"><i class="fa fa-floppy-o"></i></span>
                            <span class="btn"  @click="refresh"><i class="fa fa-refresh"></i></span>
                            <!-- <span class="btn"  @click="refresh"><i class="fa fa-paperclip"></i></span> -->
                        </div>
                    </div>
                    <div class="row text-center line">
                        <div class="col-2">Name</div>
                        <div class="col-7">Url</div>
                        <div class="col-1">En</div>
                        <div class="col-1">Py</div>
                        <div class="col-1">del</div>
                    </div>
                    <div class="row line" v-for="(item, key) in items" :key="key">
                        <div class="col-2 overflow-hidden text-break" @dblclick="focus($event)" @blur="change(item, 'name', $event)">{{ item.name }}</div>
                        <div class="col-7 overflow-hidden text-break" @dblclick="focus($event)" @blur="change(item, 'url', $event)">{{ item.url }}</div>
                        <div class="col-1 text-center opt" @click="item.enable = !item.enable"><input type="checkbox" v-model="item.enable"></div>
                        <div class="col-1 text-center opt" @click="item.proxy = !item.proxy"><input type="checkbox" v-model="item.proxy"></div>
                        <div class="col-1 text-center opt"><i class="fa fa-trash-o" @click="del(item)"></i></div>
                    </div>
                </div>
            </div>
        </div>
        <div ref="clipboard" class="modal fade bd-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
                <div class="modal-content board">
                    <textarea class="modal-content board" @paste="onPaste($event)"></textarea>
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
                        name: 'sub',
                        url: 'https://jiang.netlify.app/',
                        enable: true,
                    }
                ],
                remove: [],
            }
        },
    props: ['subs'],
    emits: ['save', 'refresh', 'update', 'importClip'],
    mounted() {
        if (this.subs && this.subs instanceof Array && this.subs.length > 0) {
            this.items = this.subs
        }
        // this.modal('show')
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
            this.$emit('refresh', this.items)
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
        clip() {
            if (navigator.clipboard) {
                (async () => {
                    const text = await navigator.clipboard.readText();
                    this.$emit('importClip', text)
                })();
            } else {
                $(this.$refs.clipboard).modal('show')
            }
        },
        onPaste(event) {
            event.target.value = ""
            let clipped = event.clipboardData.getData('text')
            this.$emit('importClip', clipped)
        },
        log(str) {
            console.log(JSON.stringify(str))
        },
    },
    watch: {
        subs: {
            handler(newVal, oldVal) {
                this.items = newVal
                // log(newVal, 'sub')
            },
            deep: true,
        }
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
