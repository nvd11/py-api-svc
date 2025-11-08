# 指南：如何正确地将GKE服务日志导出到GCP Cloud Logging

本文档以`py-api-svc`服务为例，详细说明了如何配置应用程序以确保其在Google Kubernetes Engine (GKE)上的日志能够被正确地捕获，并在GCP Cloud Logging中显示正确的严重性级别（如 `DEBUG`, `INFO`, `WARNING`, `ERROR`）。

## 1. 问题背景：为何`INFO`日志会显示为`ERROR`？

在GKE中，集成的Cloud Logging代理会自动捕获容器的标准输出（`stdout`）和标准错误（`stderr`）。其默认行为是：
-   所有写入 **`stdout`** 的日志，其严重性（`severity`）被标记为 **`INFO`**。
-   所有写入 **`stderr`** 的日志，其严重性（`severity`）被标记为 **`ERROR`**。

许多日志库（包括Python的`loguru`的默认配置）会将所有级别的日志都输出到`stderr`。这就导致了即使是`logger.info()`或`logger.debug()`产生的日志，在GCP Cloud Logging中也会被错误地显示为`ERROR`级别。

## 2. 解决方案：采用结构化日志（Structured Logging）

最佳解决方案是让应用程序输出 **JSON格式的结构化日志** 到 **`stdout`**。

当GCP Cloud Logging接收到JSON格式的日志时，它会自动解析该JSON，并智能地查找其中代表严重性级别的字段（如`severity`或`level`），从而正确地设置日志条目的严重性。

## 3. 在`py-api-svc`中的实现 (`loguru`)

我们使用`loguru`库来实现结构化日志。

### 步骤1：安装`loguru`
确保`loguru`已添加到您的`requirements.txt`中：
```
loguru
```

### 步骤2：配置`loguru`输出JSON

在我们的项目`py-api-svc`中，我们在`src/configs/config.py`文件中对日志进行了统一配置。核心配置如下：

```python
# src/configs/config.py

import sys
from loguru import logger

# 移除所有默认的处理器，特别是默认输出到stderr的处理器
logger.remove()

# 添加一个新的处理器，用于向stdout输出JSON格式的日志
# 1. serialize=True: 告诉loguru将日志记录序列化为JSON字符串。
# 2. level="DEBUG": 设置此处理器的过滤阈值，确保DEBUG及以上所有级别的日志都会被处理。
# 3. sys.stdout: 指定输出目标为标准输出。
logger.add(sys.stdout, serialize=True, level="DEBUG")

# (可选) 添加一个用于本地调试的文件处理器
logger.add("logs/app.log", level="DEBUG")

logger.info("日志系统已配置为输出JSON到stdout")
```

### 工作原理

当您在代码中调用`logger.info("Root endpoint accessed!")`时：
1.  `loguru`会生成一条JSON记录，大致如下：
    ```json
    {
        "text": "2025-11-08 10:50:00.123 | INFO     | __main__:read_root:14 - Root endpoint accessed!",
        "record": {
            "level": {
                "name": "INFO",  // <-- GCP Logging会读取这个字段
                "no": 20
            },
            "message": "Root endpoint accessed!",
            ...
        }
    }
    ```
2.  这条JSON字符串被打印到`stdout`。
3.  GKE的日志代理捕获`stdout`的内容，并将其发送到GCP Cloud Logging。
4.  GCP Cloud Logging服务识别出这是一个JSON载荷，自动解析它，并使用`record.level.name`的值（`"INFO"`）来设置该日志条目的`severity`。

## 4. GKE配置注意事项

- **无需额外代理**：只要您的GKE集群启用了与Cloud Logging的集成（默认开启），您**不需要**为这个功能部署任何额外的日志代理或sidecar（如Fluentd）。
- **本项目中的Fluentd**：本项目`k8s/deployment.yaml`中包含的`sidecar-fluentd`容器是用于将日志从共享卷中读取并归档到**BigQuery**的，它与导出到**GCP Cloud Logging**的流程是独立且不冲突的。

## 5. 验证

1.  将您的服务部署到GKE。
2.  在GCP控制台中，导航到 **日志浏览器 (Logs Explorer)**。
3.  使用查询过滤器来查找您的服务日志，例如：
    ```
    resource.type="k8s_container"
    resource.labels.cluster_name="my-cluster2"
    resource.labels.container_name="py-api-svc"
    ```
4.  观察日志条目。您会看到`logger.debug()`产生的日志其`severity`为`DEBUG`，`logger.info()`产生的日志其`severity`为`INFO`，并且日志的`jsonPayload`字段包含了完整的JSON结构。

通过以上配置，您就可以确保GKE服务的日志在GCP Cloud Logging中得到准确、可靠的记录。
