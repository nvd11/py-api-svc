# 使用 Fluentd 官方的镜像作为基础镜像
FROM fluentd:latest
USER root
RUN mkdir -p /app/logs/
RUN mkdir /app/gcp-key/

# 安装 fluent-plugin-bigquery 插件
RUN gem install fluent-plugin-bigquery fluent-plugin-grok-parser

# 复制 Fluentd 配置文件到镜像中
#COPY fluent.conf /fluentd/etc/fluent.conf

COPY fluentd-ingress-jason-hsbc.json /app/gcp-key/fluentd-ingress-jason-hsbc.json

# 定义 CMD 指令用于启动 Fluentd 并指定配置文件
CMD ["fluentd", "-c", "/fluentd/etc/fluent.conf"]
