import { defineStore } from "pinia";

export const birdpaper = defineStore("birdpaper", {
  state: () => {
    return {
        list: {
            total_count: 0,
            total_page: 0,
            pageno: 1,
            count: 9,
            list: []
        },
        categorys: [],
        navigate: [],
        req: {
            fun: null,
            params: {
                content: '',
                cids: '',
                pageno: '',
                count: 9,
            }
        }
    };
  },
  getters: {
      defaultCid() {
            if (['newest', 'search'].includes(this.getReqParams().cids)) return this.getReqParams().cids
            const category = this.categorys.find(el=> el.old_id === this.getReqParams().cids)
            if (category) {
                return category.old_id
            }
            if (this.categorys[0]) {
                return this.categorys[0].old_id
            }
            return "newest"
      }
  },
  actions: {
    setList(list) {
        Object.assign(this.list, list)
    },
    setCategorys(list) {
        this.categorys.length = 0
        this.categorys.push(...list)
    },
    setNavigate(list) {
        this.navigate.length = 0
        this.navigate.push(...list)
    },
    getReqFun() {
        return this.req.fun
    },
    getReqParams() {
        if (!this.req.params) {
            this.req.params = Object.assign({}, {
                content: '',
                cids: '',
                pageno: '',
                count: 9,
            })
        }
        return this.req.params
    },
    updateReqFun(funName) {
        this.req.fun = funName
    },
    updateReqParams(params) {
        Object.assign(this.req.params, params)
    },
  },
  persist: {
    enabled: true,
    strategies: [
      {
        key: "birdpaper",
        // 默认存储是session,指定localStorage
        storage: localStorage,
        paths: ["list", "categorys", "navigate", "req"],
      },
    ],
  },
})