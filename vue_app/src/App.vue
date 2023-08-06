<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
// import birdpaper from '@/views/birdpaper.vue'
import THeader from '@/components/header.vue'
import TFooter from '@/components/footer.vue'
import { user } from "@/store/user";
const { proxy } = getCurrentInstance();


const getLoginInfo = async (params) => {
    const userStore = user();
    // proxy.$loading && proxy.$loading()
    const res = await proxy.$api.getLoginInfo();
    // proxy.$loading && proxy.$loading(false)
    if (res && res.code === 0 && res.data && res.data.login) {
        const data = res.data
        userStore.login({username: data.name, roles: data.roles, token: data.token})
    } else {
        proxy.$toast("用户未登录")
        userStore.logout()
    }
};
getLoginInfo()
//  .then(loading)

</script>

<template>
    <div class="d-flex flex-column vh-100">
        <!--header-->
        <THeader></THeader>
        <!--header-->
        <!-- content -->
        <div class="flex-fill container h-75">
            <router-view></router-view>
        </div>
        <!-- // content -->
        <!--footer-->
        <TFooter></TFooter>
        <!--footer-->
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

</style>
