import request from "@/api/request";
import config from "@/config";

const birdpaper = config.apis['birdpaper']


export default {
    getcategory(params) {
        return request({
            url: `${birdpaper}/getCategory`,
            method: "get",
            data: params,
            mock: false,
        });
    },
    getlist(params) {
        // ?cids=分类ID&pageno=1&count=10
        return request({
            url: `${birdpaper}/GetListByCategory`,
            method: "get",
            data: params,
            mock: false,
        });
    },
    newestList(params) {
        // ?pageno=1&count=10
        return request({
            url: `${birdpaper}/newestList`,
            method: "get",
            data: params,
            mock: false,
        });
    },
    search(params) {
        // ?content=搜索关键字&pageno=1&count=10
        return request({
            url: `${birdpaper}/search`,
            method: "get",
            data: params,
            mock: false,
        });
    },
}