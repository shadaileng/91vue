import request from "./request";
import {proxy} from "./request";
import config from "@/config";
import birdpaper from "./apis/birdpaper";
import porn91 from "./apis/porn91";
import admin from "./apis/admin";
import v2ray from "./apis/v2ray";

const porn91_prefix = config.apis['porn91']
const github = config.apis['github']
export const setProxy = (params) => {
    Object.assign(proxy, params)
}

export default {
    ...birdpaper,
    ...porn91,
    ...admin,
    ...v2ray,
    getusers(params) {
        return request({
            url: `${github}/users${params == undefined ? "" : "/" + params}`,
            method: "get",
            data: '',
            mock: false,
        });
    },
    doExecute(params) {
        return request({
            url: `${porn91_prefix}/database/execute`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doScriptExecute(params) {
        return request({
            url: `${porn91_prefix}/script/execute`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doScriptImport(params) {
        return request({
            url: `${porn91_prefix}/script/import`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    getScripts(params) {
        return request({
            url: `${porn91_prefix}/script/items`,
            method: "get",
            data: params,
            mock: false,
        });
    },
    doDeleteScripts(params) {
        return request({
            url: `${porn91_prefix}/script/delete`,
            method: "post",
            data: params,
            mock: false,
        });
    },
};