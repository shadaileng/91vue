################ Build-NGINX ########################
FROM alpine:3.17 as Build-NGINX

ARG NGINX_VERSION=1.22.1
ARG NGINX_RTMP_VERSION=1.2.2
ARG ALPINE_URL=mirrors.aliyun.com

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPINE_URL}/g" /etc/apk/repositories

# compile nginx
RUN	apk update && apk add \
  gcc \
  openssl-dev \
  pcre \
  linux-headers \
  libc-dev \
  pcre-dev \
  zlib-dev \
  make

# nginx
WORKDIR /usr/local/nginx

ADD nginx-${NGINX_VERSION}.tar.gz .
ADD v${NGINX_RTMP_VERSION}.tar.gz .
RUN cd nginx-${NGINX_VERSION} && \
  ./configure \
  --prefix=/usr/local/nginx \
  --with-select_module \
  --with-poll_module \
#  --with-file-aio \
  --with-http_ssl_module \
  --with-http_realip_module \
  --with-http_gzip_static_module \
  --with-http_secure_link_module \
  --with-http_sub_module \
  --with-http_stub_status_module \
#  --with-http_perl_module \
  --with-http_mp4_module \
  --with-http_flv_module \
  --add-module=/usr/local/nginx/nginx-rtmp-module-${NGINX_RTMP_VERSION} \
  --conf-path=/usr/local/nginx/nginx.conf \
  --error-log-path=/usr/local/nginx/logs/error.log \
  --http-log-path=/usr/local/nginx/logs/access.log \
  --with-debug && \
  make && make install

COPY cert/ /usr/local/nginx/cert/

################ Build-NODE ########################
FROM node:latest

COPY vue_app /usr/local/vue_app

WORKDIR /usr/local/vue_app

RUN npm i && npm run build

################    BASE    ########################
# FROM python:3-alpine
FROM python:3.8.16-alpine3.17
ARG ALPINE_URL=mirrors.aliyun.com

RUN sed -i "s/dl-cdn.alpinelinux.org/${ALPINE_URL}/g" /etc/apk/repositories


# Build dependencies.
RUN	apk update && apk add \
  # python3-dev \
  gcc \
  openssl-dev \
  pcre \
  pcre-dev \
  linux-headers \
  libc-dev \
  patch \
  make \
  git \
  vim \
  curl \
  openssl \
  ffmpeg \
  tzdata # zoneinfo

# start-stop-daemon
RUN	apk update && apk add \
  openrc \
  libsodium

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# proxy
ARG PYPIH=pypi.mirrors.ustc.edu.cn
ARG PYPIH=pypi.douban.com
ARG PYPIM=https://${PYPIH}/simple/

RUN pip3 install --upgrade pip -i ${PYPIM} --trusted-host ${PYPIH} 
# && \
#  pip3 install git+https://github.com/shadowsocks/shadowsocks.git@master

# python
WORKDIR /porn91

COPY porn91/requirements.txt /porn91/requirements.txt

RUN cd /porn91 && \
  pip3 install --upgrade pip -i ${PYPIM} --trusted-host ${PYPIH} && \
  pip3 install -r ./requirements.txt -i ${PYPIM} --trusted-host ${PYPIH}

COPY porn91 /porn91
COPY admin /admin

COPY --from=0 --chown=root:root /usr/local/nginx /usr/local/nginx
COPY --from=1 --chown=root:root /usr/local/vue_app/dist/ /usr/local/vue_app/

RUN chmod +x /porn91/entrypoint.sh
CMD ["/porn91/entrypoint.sh"]
