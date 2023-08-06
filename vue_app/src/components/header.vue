<script setup>

import { storeToRefs } from "pinia";
import { user as user_ } from "@/store/user";
import {Modal} from 'bootstrap'
import sha1 from "sha1"

const { proxy } = getCurrentInstance();

const userStore = user_();
const { token, roles, username } = storeToRefs(userStore);

const user = reactive({
    username: "",
    email: "",
    password: "",
})
const loginModalDom = ref(null), registerModalDom = ref(null)
const modal = {login: null, register: null}
onMounted(()=>{
    modal.login = new Modal(loginModalDom.value)
    modal.register = new Modal(registerModalDom.value)
})
const doLogout = async () => {
    const res = await proxy.$api.doLogout();
    Object.assign(user, {
        username: "",
        email: "",
        password: "",
    })
    userStore.logout()
};

const doLogin = async () => {
    user.password = sha1(user.password).toString()
    user.name = user.username
    const res = await proxy.$api.doLogin(user);
    if (res.code === 0) {
        Object.assign(user, res.data)
        userStore.login(user)
        modal.login.hide()
    } else {
        proxy.$toast(`登录失败: ${res.msg}`)
    }
};

const doRegister = async () => {
    if (user.password != user.password1) {
        proxy.$toast("两次输入的密码不相同")
        return
    }
    user.password = sha1(`${user.username}:${sha1(user.password).toString()}`).toString()
    user.name = user.username
    const res = await proxy.$api.doRegister(user)
    if (res.code === 0) {
        Object.assign(user, res.data)
        userStore.login(user)
        modal.register.hide()
    } else {
        proxy.$toast(`注册失败: ${res.msg}`)
    }
};

const login = ()=>{
    const {username, password} = user
    if (username.length <= 0) {
        proxy.$toast('用户名不能为空')
        return
    }
    if (password.length <= 0) {
        proxy.$toast('密码不能为空')
        return
    }
    doLogin()

}

const register = ()=>{
    const {username, email, password} = user
    if (username.length <= 0) {
        proxy.$toast('用户名不能为空')
        return
    }
    if (email.length <= 0) {
        proxy.$toast('邮箱不能为空')
        return
    }
    if (password.length <= 0) {
        proxy.$toast('密码不能为空')
        return
    }
    doRegister()

}

</script>

<template>
<nav class="navbar navbar-expand-lg navbar-light bg-light ps-5 pe-5">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Website</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item" v-hasRole="'admin'">
                    <a class="nav-link active" aria-current="page" href="#">Home</a>
                </li>
                <li class="nav-item" v-hasRole="'admin'">
                    <router-link class="nav-link" to="loader">Loader</router-link>
                </li>
                <li class="nav-item" v-hasRole="'admin'">
                    <router-link class="nav-link" to="haijiao">Haijiao</router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="birdpaper">Birdpaper</router-link>
                </li>
                <li class="nav-item" v-hasRole="'admin'">
                    <router-link class="nav-link" to="database">DataBase</router-link>
                </li>
                <li class="nav-item" v-hasRole="'admin'">
                    <router-link class="nav-link" to="v2ray">V2ray</router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="threejs">ThreeJS</router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="script">Script</router-link>
                </li>
            </ul>
            <div class="d-flex">
                <div v-if="token" class="dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        {{ username }}
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <li><a class="dropdown-item" href="#" @click="doLogout">logout</a></li>
                    </ul>
                </div>
                <a v-else class="btn btn-sm btn-outline-secondary" href="#" data-bs-toggle="modal" data-bs-target="#loginModal">登录 / 注册</a>
            </div>
        </div>
    </div>
    <!-- Modal -->
    <div class="modal fade" ref="loginModalDom" id="loginModal" data-bs-backdrop="static" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="loginModalLabel">登录</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="username-login" placeholder="username" @keyup.enter="login" v-model="user.username">
                        <label for="username-login">Username</label>
                    </div>
                    <div class="form-floating">
                        <input type="password" class="form-control" id="pwd-login" placeholder="Password" @keyup.enter="login" v-model="user.password">
                        <label for="pwd-login">Password</label>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-target="#registerModal" data-bs-toggle="modal">注册</button>
                    <button type="button" class="btn btn-primary" @click="login">登录</button>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" ref="registerModalDom" id="registerModal" data-bs-backdrop="static" tabindex="-1" aria-labelledby="registerModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="registerModalLabel">注册</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="username-register" placeholder="username" @keyup.enter="register" v-model="user.username">
                        <label for="username-register">Username</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input type="email" class="form-control" id="email-register" placeholder="name@example.com" @keyup.enter="register" v-model="user.email">
                        <label for="email-register">Email address</label>
                    </div>
                    <div class="form-floating">
                        <input type="password" class="form-control" id="pwd-register" placeholder="Password" v-model="user.password">
                        <label for="pwd-register">Password</label>
                    </div>
                    <div class="form-floating">
                         <input type="password" class="form-control" id="pwd-register1" placeholder="Password1" v-model="user.password1">
                         <label for="pwd-register1">Password1</label>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" @click="register">注册</button>
                    <button type="button" class="btn btn-secondary" data-bs-target="#loginModal" data-bs-toggle="modal">登录</button>
                </div>
            </div>
        </div>
    </div>
</nav>
</template>
