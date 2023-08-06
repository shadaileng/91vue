import { defineStore } from "pinia";

export const user = defineStore("user", {
  state: () => {
    return {
        username: 'shadaileng',
        roles: ['admin'],
        token: null
    };
  },
  getters: {

  },
  actions: {
      logout(){
        Object.assign(this, {username: '', roles: [], token: null})
      },
      login(user) {
        Object.assign(this, user)
      },
      hasRole(role) {
        return this.roles.includes(role)
      }
  },
  persist: {
    enabled: true,
    strategies: [
      {
        key: "user",
        // 默认存储是session,指定localStorage
        storage: localStorage,
        paths: ['username', 'roles', 'token'],
      },
    ],
  },
})