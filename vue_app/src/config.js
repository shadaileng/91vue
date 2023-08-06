/**
 * 环境配置文件
 * development: 开发环境
 * test:测试环境
 * prod: 生产环境
 */

// 当前环境
const env = import.meta.env.MODE || "prod";
const EnvConfig = {
  development: {
    baseApi: "/",
    mockApi: "/mock",
  },
  test: {
    baseApi: "/test",
    mockApi: "/mock",
  },
  prod: {
    baseApi: "/prod",
    mockApi: "/mock",
  },
};

const apis = {
    birdpaper: '/vue/birdpaper/intf',
    porn91: '/vue/91/api',
    admin: '/vue/91/admin',
    github: '/vue/github/api',
}

export default {
  env,
  mock: true,
  apis: apis,
  ...EnvConfig[env],
};