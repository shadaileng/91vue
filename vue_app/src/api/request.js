import axios from "axios";
import config from "../config";

const NETWORK_ERROR = "网络请求错误,请稍后重试";

// 创建Axios实例
const service = axios.create({
    baseURL: config.baseApi,
});


export const proxy = {}

// 请求拦截器
service.interceptors.request.use(
    (req) => {
        proxy['loading'] && proxy['loading']()
        // loading()
        return req;
    },
    (error) => {
        Promise.reject(error);
    }
);
// 响应拦截器
service.interceptors.response.use(
    (rep) => {
        proxy['loading'] && proxy['loading'](false)
        // loading(false)
        if (rep.status == 200) {
            return rep.data;
        } else {
            // return Promise.reject(NETWORK_ERROR);
            return {'code': -1, msg: {status: rep.status}};
        }
    },
    (error) => {
        proxy['loading'] && proxy['loading'](false)
        // loading(false)
        return {'code': -1, msg: error};
        // Promise.reject(error);
    }
);

const request = (options) => {
    options.method = options.method || "get";
    if (options.method.toLowerCase() == "get") {
        options.params = options.data;
    }
    let isMock = config.mock;
    if (typeof options.mock != "undefined") {
        isMock = options.mock;
    }
    if (config.env == "prod") {
        service.defaults.baseURL = config.baseApi;
    } else {
        service.defaults.baseURL = isMock ? config.mockApi : config.baseApi;
    }
    return service(options);
};

export default request;