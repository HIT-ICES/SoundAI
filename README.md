该模板集成了 gitlab cli 配置，具体见 `.gitlab-cli` 配置文件。主要包含以下功能：

1. 自动测试
2. 代码质量检测（192.168.1.102:9000）
3. 自动构建
4. 镜像打包，并推送到 192.168.1.102:5000

> 每次提交后都会触发上述流程。在gitlab项目页面左侧的 CI/CD 即可查看。请务必确保 CI 通过。通过之后即可直接从 192.168.1.102:5000 上拉取镜像进行测试。

具体详情请见配置文件。

### 使用时，fork 后**务必确保修改** `pom.xml` 以及 `applications.yaml` 以及 `Dockerfile`  中的项目名称

### **务必确保** 修改一下 `/src/main/java/com.hitices.xxx` 包名中的 `xxx` 为你自己的包名。统一格式为 `com.hitices.vedioai`，IDEA 右键 Refactor 即可
