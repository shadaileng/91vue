# download_91

#### 介绍

基于`aiohttp`的`web`服务下载和管理`91porn`视频项目

#### 软件架构

- `aiohttp`处理`web`请求和响应
- `nginx`代理`aiohttp`服务
- `porn91.py`提供下载和`91`视频的接口
- `server.py`下载服务
- `download`模块实现具体的下载任务
- `shadowsocks`科学上网
- 提供本地启动和`docker`部署两种使用方式

#### 安装教程

1.  下载项目到本地

```bash
$ git clone https://gitee.com/shadaileng/download_91.git
$ cd download_91
```

2. 修改`config/website.yml`配置

- `sqlite.db_file`: `sqlite`数据库路径
- `log.path`: 日志路径
- `host`: `web`服务对外访问主机`ip`
- `port`: `web`服务对外访问端口
- `proxy`: 本地代理地址

3. 本地启动

```bash
# 新建本地虚拟环境
$ virtualenv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
# 后台启动下载服务器
$ nohup python server.py start &
# 启动web服务
$ python app.py
```

5. `docker`镜像构建和启动

```bash
$ sudo docker-compose build
$ sudo docker-compose up -d
```

#### 使用说明

1.  启动之后访问`config/website.yml`配置的主机和端口

```text
http://127.0.0.1:8080
```

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 码云特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  码云官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解码云上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是码云最有价值开源项目，是码云综合评定出的优秀开源项目
5.  码云官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  码云封面人物是一档用来展示码云会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)


- [python---异步IO(asyncio)协程](https://www.cnblogs.com/ssyfj/p/9219360.html)
- [stpyV8](https://github.com/area1/stpyv8)
- [p_spider]https://github.com/PerryDP/p_spider)
- [python如何快速将项目代码制作成pip安装包并进行安装](https://blog.csdn.net/weixin_43922901/article/details/89815055?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~first_rank_v2~rank_v25-5-89815055.nonecase&utm_term=pip%E5%BF%AB%E9%80%9Fgit%E9%A1%B9%E7%9B%AE%E5%AE%89%E8%A3%85)
- [Vue 3 + Vite 如何使用Bootstrap 5](https://nii.cn/4142.html)
- [在 Vue 3 中使用 v-model 自定义组件](https://devpress.csdn.net/vue/632fc951357a883f870c8be2.html)
- [TinyDB](https://github.com/msiemens/tinydb)
- [textarea中使用TAB --- 使用javascript触发一个键盘输入事件](https://www.jianshu.com/p/2732f6a2f398)
- [Nginx笔记](https://zhuanlan.zhihu.com/p/602563924)
```bash
$ sudo apt  install libboost-dev libboost-system-dev
$ pip install -e git+https://github.com/username/project.git#egg=project
```











## websocket

nginx需要配置属性才能使用websocket

```
location / {
	proxy_http_version 1.1;
	proxy_set_header Upgrade $http_upgrade;
	proxy_set_header Connection "upgrade";
}
```

# 参考

- [ffmpeg命令大全以及视频教程](https://www.kancloud.cn/zhenhuamcu/ffmpeg)

```bash
$ ffmpeg -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp" -i dist/video/419704.m3u8 -c copy 419704.mp4
```

