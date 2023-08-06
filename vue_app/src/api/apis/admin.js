import request from "@/api/request";
import config from "@/config";

const prefix = config.apis['admin']


export default {
    doTopic(params) {
        return request({
            url: `${prefix}/haijiao/topic`,
            method: "get",
            data: params,
            mock: false,
        });
    },
    doUid(params) {
        return request({
            url: `${prefix}/haijiao/uid`,
            method: "get",
            data: params,
            mock: false,
        });
    },
    doDownload(params) {
        return request({
            url: `${prefix}/haijiao/download`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doPoster(params) {
        return request({
            url: `${prefix}/haijiao/poster`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    tasks(params) {
        return request({
            url: `${prefix}/tasks`,
            method: "get",
            data: params,
            mock: false,
        });
    },
    stopTask(params) {
        return request({
            url: `${prefix}/stop`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doLoadrflist(params) {
        return request({
            url: `${prefix}/porn91/loadrflist`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doLoadAccuntlist(params) {
        return request({
            url: `${prefix}/porn91/loadaccuntlist`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doLoadVideoPage(params) {
        return request({
            url: `${prefix}/porn91/loadvideopage`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doDownloadSrc(params) {
        return request({
            url: `${prefix}/porn91/download`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doThumbnails(params) {
        return request({
            url: `${prefix}/thumbnails`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doCheckVideo(params) {
        return request({
            url: `${prefix}/check_keys`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    do91Delete(params) {
        return request({
            url: `${prefix}/delete`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    do91Package(params) {
        return request({
            url: `${prefix}/package`,
            method: "post",
            data: params,
            mock: false,
        });
    },
    doParseVideoPage(params) {
        return request({
            url: `${prefix}/haijiao/parse`,
            method: "post",
            data: params,
            mock: false,
        });
    },
}