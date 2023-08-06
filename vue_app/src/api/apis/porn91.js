import request from "@/api/request";
import config from "@/config";

const porn91 = config.apis['porn91']


export default {
    doLogin(params) {
        return request({
            url: `${porn91}/login`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doRegister(params) {
        return request({
            url: `${porn91}/register`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doLogout(params) {
        return request({
            url: `${porn91}/logout`,
            method: "get",
            data: params,
            mock: false,
        });
    },
    getLoginInfo(params) {
        return request({
            url: `${porn91}/users/logininfo`,
            method: "get",
            data: params,
            mock: false,
        });
    },
    get91List(params) {
        // ?pagesize=15&index=1&status=&uname=&name=
        return request({
            url: `${porn91}/vue/items`,
            method: "get",
            data: params,
            mock: false,
        });
    },
    do91Import(params) {
        return request({
            url: `${porn91}/import`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    get91Config(params) {
        return request({
            url: `${porn91}/configs`,
            method: "get",
            data: params,
            mock: false,
        });
    },
    doConfig(params) {
        return request({
            url: `${porn91}/configs`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doConfigDel(params) {
        return request({
            url: `${porn91}/configs/del`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doTaskStop(params) {
        return request({
            url: `${porn91}/stop`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    rebootDService(params) {
        return request({
            url: `${porn91}/rebootDService`,
            method: "get",
            data: params,
            mock: false,
        });
    },
}