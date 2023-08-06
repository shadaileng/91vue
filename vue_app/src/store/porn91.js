import { defineStore } from "pinia";

export const porn91 = defineStore("porn91", {
  state: () => {
    return {
        list: [],
        page: {
            "total": 0,
            "pages": 1,
            "index": 1,
            "size": 15
        },
        status: [
            {
                key: '1',
                name: '完成',
                current: false,
            },
            {
                key: '0',
                name: '下载中',
                current: false,
            },
            {
                key: null,
                name: '全部',
                current: true,
            },
            {
                key: '-1',
                name: '暂停',
                current: false,
            },
            {
                key: '-2',
                name: '异常',
                current: false,
            },
        ],
        navigate: [],
        tabName: 'grid',
        req: {
            fun: null,
            params: {
                path: '/root',
                pagesize: 15,
                index: 1,
                status: null,
                uname: null,
                name: null,
            }
        }
    };
  },
  getters: {
        curStatus() {
            let curEl = null
            if (this.status === undefined || this.status === null || this.status === '') {
                console.log(`local status: ${this.status}`)
                return {
                    key: null,
                    name: '全部',
                    current: true,
                }
            }
            this.status.forEach(el=>{
                if (el.key === this.req.params.status) {
                    curEl = el
                }
            })
            if (curEl) {
                return curEl
            }
            return this.status[2]
      }
  },
  actions: {
    setList(list) {
        this.list.length = 0
        this.list.push(...list)
    },
    setPage(page) {
        Object.assign(this.page, page)
    },
    setNavigate() {
        const navs = [{name: 'root', type: 'root'}]
        const {uname, status, name} = this.getReqParams()
        if (uname) {
            navs.push({name: uname, type: 'uname'})
        }
        if (name) {
            navs.push({name: name, type: 'name'})
        }
        if (status !== null) {
            navs.push({name: this.curStatus['name'], type: 'status'})
        }
        this.navigate.length = 0
        this.navigate.push(...navs)
    },
    getReqFun() {
        return this.req.fun
    },
    getReqParams() {
        if (!this.req.params) {
            this.req.params = Object.assign({}, {
                pagesize: 15,
                index: 1,
                status: null,
            })
        }
        return this.req.params
    },
    updateReqFun(funName) {
        this.req.fun = funName
    },
    updateReqParams(params) {
        if (this.status === undefined || this.status === null || this.status === '') {
            console.log(`local status: ${this.status}`)
            return
        }
        Object.assign(this.req.params, params)
        this.status.forEach(el=>{
            el.current = false
            if (el.key === this.req.params.status) {
                el.current = true
            }
        })
    },
  },
  persist: {
    enabled: true,
    strategies: [
      {
        key: "porn91",
        // 默认存储是session,指定localStorage
        storage: localStorage,
        // paths: ["list", "page", "navigate", "req"],
      },
    ],
  },
})