import { defineStore } from "pinia";

export const script = defineStore("script", {
  state: () => {
    return {
        content: '',
        result: '',
        mode: {
            list: true,
            editor: false,
        },
        item: {
            id: null,
            name: '',
            desc: '',
            poster: `https://www.python.org/static/img/python-logo.png`,
        },
        selectItems: [],
        page: {
            "total": 0,
            "pages": 1,
            "index": 1,
            "size": 15
        },
        req_params: {
            pagesize: 15,
            index: 1,
            status: null,
            uname: null,
            name: null,
        }
    };
  },
  getters: {
  },
  actions: {
        init() {
            this.item = {
                id: null,
                name: '',
                desc: '',
                poster: `https://www.python.org/static/img/python-logo.png`,
            }
        },
        setPage(page) {
            Object.assign(this.page, page)
        },
        getReqParams() {
            if (!this.req_params) {
                this.req_params = Object.assign({}, {
                    pagesize: 15,
                    index: 1,
                    status: null,
                })
            }
            return this.req_params
        },
        updateReqParams(params) {
            Object.assign(this.req_params, params)
        },
  },
  persist: {
    enabled: true,
    strategies: [
      {
        key: "script",
        // 默认存储是session,指定localStorage
        storage: localStorage,
        paths: ['result', 'content', 'mode', 'item', 'selectItems', 'page', 'req_params'],
      },
    ],
  },
})