# Quick Start

This guide helps you start the Code Health Monitor in 5 minutes.

## Prerequisites

- Docker and Docker Compose
- Git access token (for cloning repositories)

## Option 1: Docker Deployment (Recommended)

### 1. Create Environment Configuration

```bash
# Copy example configuration
cp .env.example .env

# Edit configuration
vi .env
```

`.env` file contents:

```bash
# Required configuration
GIT_TOKEN=your_git_token_here
PROJECT_NAME=My Project

# Repository configuration (via environment variable)
REPOSITORIES=backend|https://github.com/org/backend.git|java|main,frontend|https://github.com/org/frontend.git|vue|main

# Optional: DingTalk notification
DINGTALK_ENABLED=true
DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxx
DINGTALK_SECRET=SECxxx

# Web access URL
WEB_BASE_URL=http://your-server:8080
```

### 2. Start Services

```bash
# Build image
docker-compose build

# Generate today's daily report (test)
docker-compose run --rm code-health daily

# Start scheduled tasks and web service
docker-compose up -d scheduler nginx
```

### 3. View Reports

Open browser and visit `http://localhost:8080`

## Option 2: Local Execution

### 1. Install Dependencies

```bash
pip install pyyaml requests
```

### 2. Create Configuration File

Create `config/config.yaml`:

```yaml
project:
  name: "My Project"

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

### 3. Run Reports

```bash
# Set configuration file path
export CODE_HEALTH_CONFIG=./config/config.yaml

# Generate daily report
python -m src.main daily

# Generate weekly report
python -m src.main weekly

# Generate monthly report
python -m src.main monthly
```

## Scheduled Task Configuration

In Docker mode, the scheduler service has pre-configured scheduled tasks:

| Time | Task |
|------|------|
| Daily 18:00 | Generate daily report |
| Friday 17:00 | Generate weekly report |
| 1st of month 10:00 | Generate monthly report |

To customize, edit the cron configuration in `docker-compose.yml` scheduler service.

## DingTalk Notification Configuration

### 1. Create DingTalk Robot

1. Add custom robot in DingTalk group
2. Select "Sign" security setting
3. Record Webhook URL and Secret

### 2. Configure Environment Variables

```bash
DINGTALK_ENABLED=true
DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxx
DINGTALK_SECRET=SECxxx
```

### 3. Send Test Notification

```bash
# Generate report
docker-compose run --rm code-health daily

# Send notification
docker-compose run --rm code-health notify daily
```

## Multi-Repository Configuration

### Via Configuration File

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

### Via Environment Variable

```bash
# Format: name|url|type|branch, multiple repos separated by comma
REPOSITORIES=backend|https://github.com/org/backend.git|java|main,frontend|https://github.com/org/frontend.git|vue|main
```

## China Deployment (Alibaba Cloud ECS / Podman)

Due to Docker Hub access restrictions in China, we recommend using Podman with domestic mirror sources.

### 1. Install Podman and podman-compose

```bash
# CentOS/Alinux
dnf install -y podman podman-compose

# Or Ubuntu
apt install -y podman podman-compose
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
vi .env
```

Alibaba Cloud Codeup configuration example:

```bash
# Git Platform
GIT_PLATFORM=codeup
GIT_TOKEN=your_codeup_token

# Codeup Configuration
CODEUP_TOKEN=your_codeup_token
CODEUP_ORG_ID=your_org_id
CODEUP_PROJECT=your_project

# Project Name
PROJECT_NAME=Code Health Monitor

# DingTalk Notification
DINGTALK_ENABLED=true
DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=xxx
DINGTALK_SECRET=SECxxx

# Web Access
WEB_BASE_URL=http://your-server:8080
```

### 3. Build and Deploy with China Configuration

```bash
# Build image (using domestic mirrors)
podman-compose -f docker-compose.china.yml build

# Start services
podman-compose -f docker-compose.china.yml up -d

# Test daily report generation
podman run --rm --env-file .env -v ./reports:/app/reports code-health:latest daily
```

### 4. Local Python Execution (Alternative)

If container deployment still has issues, run directly with Python:

```bash
# Install Python 3.11
dnf install -y python3.11 python3.11-pip

# Install dependencies
python3.11 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# Run (source .env first)
cd /opt/code-health
set -a && source .env && set +a
python3.11 -m src.main daily
python3.11 -m src.main notify daily
```

### 5. Configure Crontab (Local Execution)

```bash
crontab -e
```

Add the following:

```cron
# Daily report - Generate at 7:45, Send at 8:00
45 7 * * * cd /opt/code-health && set -a && source .env && set +a && python3.11 -m src.main daily >> logs/daily.log 2>&1
0 8 * * * cd /opt/code-health && set -a && source .env && set +a && python3.11 -m src.main notify daily >> logs/daily-notify.log 2>&1

# Weekly report - Generate Monday 7:30, Send at 8:00
30 7 * * 1 cd /opt/code-health && set -a && source .env && set +a && python3.11 -m src.main weekly >> logs/weekly.log 2>&1
0 8 * * 1 cd /opt/code-health && set -a && source .env && set +a && python3.11 -m src.main notify weekly >> logs/weekly-notify.log 2>&1

# Monthly report - Generate 1st at 9:00, Send at 9:30
0 9 1 * * cd /opt/code-health && set -a && source .env && set +a && python3.11 -m src.main monthly >> logs/monthly.log 2>&1
30 9 1 * * cd /opt/code-health && set -a && source .env && set +a && python3.11 -m src.main notify monthly >> logs/monthly-notify.log 2>&1
```

## FAQ

### Q: Clone repository failed?

Check:
1. Is Git Token correct
2. Does Token have repository access permission
3. Is repository URL correct

### Q: No data in report?

Check:
1. Are there commits in the specified time range
2. Is the repository branch name correct

### Q: DingTalk notification failed?

Check:
1. Is Webhook URL correct
2. Is Secret correct (if sign is configured)
3. Is the robot disabled

### Q: How to view historical reports?

Reports are saved in `reports/` directory:
- `reports/daily/YYYY-MM-DD.md` - Daily reports
- `reports/weekly/YYYY-Wxx.md` - Weekly reports
- `reports/monthly/YYYY-MM.md` - Monthly reports

## Next Steps

- Check [README.md](README.md) or [README_EN.md](README_EN.md) for more configuration options
- Customize health score thresholds
- Configure multiple notification channels
