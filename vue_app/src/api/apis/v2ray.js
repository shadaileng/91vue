import request from "@/api/request";
import config from "@/config";

const porn91 = config.apis['porn91']


export default {
    getV2ray(params) {
        return request({
            url: `${porn91}/v2ray/items`,
            method: "get",
            data: params,
            mock: false,
        });
    },
    doDeleteV2rays(params) {
        return request({
            url: `${porn91}/v2ray/delete`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doEnableV2ray(params) {
        return request({
            url: `${porn91}/v2ray/enable`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    getV2rayConfig(params) {
        return request({
            url: `${porn91}/v2ray/subs`,
            method: "get",
            data: params,
            mock: false,
        });
    },
    doV2rayConfigSave(params) {
        return request({
            url: `${porn91}/v2ray/subs/save`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doV2rayConfigDel(params) {
        return request({
            url: `${porn91}/v2ray/subs/delete`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doSubsUpdate(params) {
        return request({
            url: `${porn91}/v2ray/subs/update`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    importClip(params) {
        return request({
            url: `${porn91}/v2ray/import`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doExport(params) {
        return request({
            url: `${porn91}/v2ray/export/${params}`,
            method: "get",
            data: params,
            mock: false,
        });
    },
}