import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";
import AutoImport from "unplugin-auto-import/vite";

const evnResolver = {
    'build': {
        plugins: [
            vue(),
            AutoImport({
            // 自动引入vue, vue-router组件
            imports: ["vue", "vue-router"],
            }),
        ],
        resolve: {
            alias: {
                "@": path.resolve(__dirname, "./src"),
                '~bootstrap': path.resolve(__dirname, 'node_modules/bootstrap'),
            },
        },
        // base: '/vue/',
    },
    'serve': {
        plugins: [
            vue(),
            AutoImport({
            // 自动引入vue, vue-router组件
            imports: ["vue", "vue-router"],
            }),
        ],
        resolve: {
            alias: {
                "@": path.resolve(__dirname, "./src"),
                '~bootstrap': path.resolve(__dirname, 'node_modules/bootstrap'),
            },
        },
        base: '/vue/',
        server: {
            hmr: false,
            proxy: {
                "/vue/api": {
                    target: "https://api.github.com",
                    changeOrigin: true,
                    rewrite: (path) => path.replace(/^\/vue\/api/, ""),
                },
                "/vue/birdpaper": {
                    target: "http://wp.birdpaper.com.cn/",
                    changeOrigin: true,
                    rewrite: (path) => path.replace(/^\/vue\/birdpaper/, ""),
                },
            },
        }
    }
}

// https://vitejs.dev/config/
export default defineConfig(({command}) => {
    return evnResolver[command]
})
