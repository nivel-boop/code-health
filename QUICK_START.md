# 快速开始

本指南帮助你在 5 分钟内启动代码健康监控系统。

## 前置要求

- Docker 和 Docker Compose
- Git 访问令牌（用于克隆仓库）

## 方式一：Docker 部署（推荐）

### 1. 创建环境配置

```bash
# 复制示例配置
cp .env.example .env

# 编辑配置
vi .env
```

`.env` 文件内容：

```bash
# 必需配置
GIT_TOKEN=your_git_token_here
PROJECT_NAME=我的项目

# 仓库配置（通过环境变量）
REPOSITORIES=backend|https://github.com/org/backend.git|java|main,frontend|https://github.com/org/frontend.git|vue|main

# 可选：钉钉通知
DINGTALK_ENABLED=true
DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxx
DINGTALK_SECRET=SECxxx

# Web 访问地址
WEB_BASE_URL=http://your-server:8080
```

### 2. 启动服务

```bash
# 构建镜像
docker-compose build

# 生成今天的日报（测试）
docker-compose run --rm code-health daily

# 启动定时任务和 Web 服务
docker-compose up -d scheduler nginx
```

### 3. 查看报告

打开浏览器访问 `http://localhost:8080`

## 方式二：本地运行

### 1. 安装依赖

```bash
pip install pyyaml requests
```

### 2. 创建配置文件

创建 `config/config.yaml`：

```yaml
project:
  name: "我的项目"

repositories:
  - name: backend
    url: https://github.com/org/backend.git
    type: java
    main_branch: main

git:
  token: "your_git_token_here"

notification:
  dingtalk:
    enabled: false
```

### 3. 运行报告

```bash
# 设置配置文件路径
export CODE_HEALTH_CONFIG=./config/config.yaml

# 生成日报
python -m src.main daily

# 生成周报
python -m src.main weekly

# 生成月报
python -m src.main monthly
```

## 定时任务配置

Docker 模式下，scheduler 服务已配置定时任务：

| 时间 | 任务 |
|------|------|
| 每天 18:00 | 生成日报 |
| 每周五 17:00 | 生成周报 |
| 每月 1 日 10:00 | 生成月报 |

如需自定义，编辑 `docker-compose.yml` 中 scheduler 服务的 cron 配置。

## 钉钉通知配置

### 1. 创建钉钉机器人

1. 在钉钉群中添加自定义机器人
2. 选择"加签"安全设置
3. 记录 Webhook URL 和 Secret

### 2. 配置环境变量

```bash
DINGTALK_ENABLED=true
DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxx
DINGTALK_SECRET=SECxxx
```

### 3. 发送测试通知

```bash
# 生成报告
docker-compose run --rm code-health daily

# 发送通知
docker-compose run --rm code-health notify daily
```

## 多仓库配置

### 通过配置文件

```yaml
repositories:
  - name: backend
    url: https://github.com/org/backend.git
    type: java
    main_branch: main
  - name: frontend
    url: https://github.com/org/frontend.git
    type: vue
    main_branch: develop
  - name: mobile
    url: https://github.com/org/mobile.git
    type: flutter
    main_branch: main
```

### 通过环境变量

```bash
# 格式: name|url|type|branch，多个仓库用逗号分隔
REPOSITORIES=backend|https://github.com/org/backend.git|java|main,frontend|https://github.com/org/frontend.git|vue|main
```

## 国内部署 (阿里云 ECS / Podman)

由于 Docker Hub 在国内访问受限，推荐使用 Podman + 国内镜像源部署。

### 1. 安装 Podman 和 podman-compose

```bash
# CentOS/Alinux
dnf install -y podman podman-compose

# 或 Ubuntu
apt install -y podman podman-compose
```

### 2. 配置环境变量

```bash
cp .env.example .env
vi .env
```

云效 Codeup 配置示例：

```bash
# Git 平台
GIT_PLATFORM=codeup
GIT_TOKEN=your_codeup_token

# 云效配置
CODEUP_TOKEN=your_codeup_token
CODEUP_ORG_ID=your_org_id
CODEUP_PROJECT=your_project

# 项目名称
PROJECT_NAME=代码健康监控

# 钉钉通知
DINGTALK_ENABLED=true
DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxx
DINGTALK_SECRET=SECxxx

# Web 访问
WEB_BASE_URL=http://your-server:8080
```

### 3. 使用国内版配置构建和部署

```bash
# 构建镜像 (使用国内镜像源)
podman-compose -f docker-compose.china.yml build

# 启动服务
podman-compose -f docker-compose.china.yml up -d

# 测试生成日报
podman run --rm --env-file .env -v ./reports:/app/reports code-health:latest daily
```

### 4. 不使用容器的本地运行方式

如果容器部署仍有问题，可直接使用 Python 运行：

```bash
# 安装 Python 3.11
dnf install -y python3.11 python3.11-pip

# 安装依赖
python3.11 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 运行（需要先 source .env）
cd /opt/code-health
set -a && source .env && set +a
python3.11 -m src.main daily
python3.11 -m src.main notify daily
```

### 5. 配置 Crontab (本地运行方式)

```bash
crontab -e
```

添加以下内容：

```cron
# 日报 - 每天 7:45 生成, 8:00 发送
45 7 * * * cd /opt/code-health && set -a && source .env && set +a && python3.11 -m src.main daily >> logs/daily.log 2>&1
0 8 * * * cd /opt/code-health && set -a && source .env && set +a && python3.11 -m src.main notify daily >> logs/daily-notify.log 2>&1

# 周报 - 每周一 7:30 生成, 8:00 发送
30 7 * * 1 cd /opt/code-health && set -a && source .env && set +a && python3.11 -m src.main weekly >> logs/weekly.log 2>&1
0 8 * * 1 cd /opt/code-health && set -a && source .env && set +a && python3.11 -m src.main notify weekly >> logs/weekly-notify.log 2>&1

# 月报 - 每月1日 9:00 生成, 9:30 发送
0 9 1 * * cd /opt/code-health && set -a && source .env && set +a && python3.11 -m src.main monthly >> logs/monthly.log 2>&1
30 9 1 * * cd /opt/code-health && set -a && source .env && set +a && python3.11 -m src.main notify monthly >> logs/monthly-notify.log 2>&1
```

## 常见问题

### Q: 克隆仓库失败？

检查：
1. Git Token 是否正确
2. Token 是否有仓库访问权限
3. 仓库 URL 是否正确

### Q: 报告中没有数据？

检查：
1. 指定的时间范围内是否有提交
2. 仓库分支名称是否正确

### Q: 钉钉通知发送失败？

检查：
1. Webhook URL 是否正确
2. Secret 是否正确（如果配置了加签）
3. 机器人是否被禁用

### Q: 如何查看历史报告？

报告保存在 `reports/` 目录下：
- `reports/daily/YYYY-MM-DD.md` - 日报
- `reports/weekly/YYYY-Wxx.md` - 周报
- `reports/monthly/YYYY-MM.md` - 月报

## 下一步

- 查看 [README.md](README.md) 了解更多配置选项
- 自定义健康评分阈值
- 配置多个通知渠道
