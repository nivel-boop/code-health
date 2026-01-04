# 贡献指南

**中文** | [English](CONTRIBUTING_EN.md)

感谢您对 Code Health Monitor 项目的关注！我们欢迎任何形式的贡献。

## 📋 目录

- [行为准则](#行为准则)
- [我能做什么贡献](#我能做什么贡献)
- [开发环境设置](#开发环境设置)
- [提交指南](#提交指南)
- [代码规范](#代码规范)
- [Pull Request 流程](#pull-request-流程)
- [报告问题](#报告问题)
- [功能建议](#功能建议)

## 🤝 行为准则

我们致力于为所有人提供一个友好、安全和包容的环境。参与本项目即表示您同意：

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

## 💡 我能做什么贡献

### 1. 报告 Bug

发现 Bug？请帮助我们改进：
- 在 [Issues](https://github.com/yzhucn/code-health/issues) 中搜索，确保该问题未被报告
- 如果是新问题，创建一个新的 Issue
- 提供详细的复现步骤
- 说明预期行为和实际行为
- 提供环境信息（操作系统、Python 版本等）

### 2. 提出功能建议

有好的想法？我们很乐意听取：
- 在 [Issues](https://github.com/yzhucn/code-health/issues) 中创建功能请求
- 清楚地描述功能的用途和价值
- 如果可能，提供使用场景示例
- 讨论可能的实现方案

### 3. 改进文档

文档永远可以更好：
- 修正拼写或语法错误
- 改进现有文档的清晰度
- 添加缺失的文档
- 翻译文档到其他语言

### 4. 提交代码

贡献代码是最直接的帮助方式：
- 修复 Bug
- 实现新功能
- 优化性能
- 重构代码

## 🛠️ 开发环境设置

### 前置要求

- Python 3.8+
- Git 2.0+
- Bash shell
- (可选) 钉钉/飞书账号用于测试通知功能

### 克隆仓库

```bash
# Fork 仓库到你的账号
# 然后克隆你的 fork
git clone https://github.com/YOUR_USERNAME/code-health.git
cd code-health

# 添加上游仓库
git remote add upstream https://github.com/yzhucn/code-health.git
```

### 安装依赖

```bash
# 安装 Python 依赖
pip3 install -r requirements.txt

# 复制配置模板
cp config.example.yaml config.yaml

# 根据需要编辑配置
vim config.yaml
```

### 创建开发分支

```bash
# 从 main 分支创建新分支
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

## 📝 提交指南

### 提交信息格式

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行的变动）
- `refactor`: 重构（既不是新增功能，也不是修复 bug）
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

#### Scope 范围（可选）

- `core`: 核心功能
- `report`: 报告生成
- `dashboard`: 仪表盘
- `notification`: 通知推送
- `config`: 配置相关
- `docs`: 文档

#### 示例

```bash
# 好的提交信息
feat(report): 添加月报生成功能
fix(notification): 修复钉钉推送失败的问题
docs(readme): 更新安装说明

# 不好的提交信息
update code
fix bug
update
```

### 详细的提交信息示例

```
feat(dashboard): 添加代码复杂度趋势图

- 新增复杂度计算模块
- 在仪表盘中集成 ECharts 图表
- 支持 7/14/30 天时间范围选择

Closes #123
```

## 🎨 代码规范

### Python 代码规范

遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 风格指南：

```python
# 好的示例
def calculate_health_score(commit_data: dict) -> float:
    """
    计算代码健康评分

    Args:
        commit_data: 提交数据字典

    Returns:
        健康评分 (0-100)
    """
    if not commit_data:
        return 0.0

    score = 100.0
    # 计算逻辑...
    return score

# 不好的示例
def calc(d):
    if not d: return 0
    s=100
    return s
```

**代码风格要点**：
- 使用 4 个空格缩进（不使用 Tab）
- 函数和类名使用描述性名称
- 添加文档字符串（docstring）
- 保持函数简短（一般不超过 50 行）
- 使用类型注解（Python 3.8+）

### Shell 脚本规范

```bash
#!/bin/bash
# 脚本用途的简短描述

set -e  # 遇到错误立即退出

# 使用有意义的变量名
REPORT_DATE=$(date +%Y-%m-%d)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 函数命名使用小写和下划线
generate_daily_report() {
    local date=$1
    echo "生成 $date 的日报..."
    # 实现...
}

# 好的示例：清晰的错误处理
if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误: 配置文件不存在: $CONFIG_FILE" >&2
    exit 1
fi
```

## 🔄 Pull Request 流程

### 1. 确保代码是最新的

```bash
# 获取上游更新
git fetch upstream

# 合并到你的分支
git checkout main
git merge upstream/main

# 更新你的功能分支
git checkout feature/your-feature-name
git rebase main
```

### 2. 测试你的更改

```bash
# 运行现有测试（如果有）
python3 -m pytest tests/

# 手动测试核心功能
cd scripts
python3 daily-report.py
python3 weekly-report.py
```

### 3. 创建 Pull Request

- 推送你的分支到 GitHub
- 在 GitHub 上创建 Pull Request
- 填写 PR 模板（如果有）
- 链接相关的 Issue（使用 `Closes #123`）

### 4. PR 描述模板

```markdown
## 📝 变更说明

简要描述这个 PR 做了什么。

## 🔧 变更类型

- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 性能优化
- [ ] 代码重构

## ✅ 测试

描述你如何测试这些变更：
- [ ] 手动测试通过
- [ ] 添加了单元测试
- [ ] 更新了文档

## 📸 截图（如果适用）

如果有 UI 变更，请提供截图。

## 📋 检查清单

- [ ] 代码遵循项目规范
- [ ] 提交信息遵循规范
- [ ] 已添加必要的文档
- [ ] 已测试所有变更
- [ ] 无敏感信息（Token、IP 等）
```

### 5. 代码审查

- 维护者会审查你的代码
- 可能会要求修改
- 请及时响应评论
- 完成修改后推送更新

### 6. 合并

- 审查通过后，维护者会合并你的 PR
- 你的贡献会出现在下一个版本中
- 感谢你的贡献！🎉

## 🐛 报告问题

创建 Issue 时请提供：

### Bug 报告模板

```markdown
**Bug 描述**
简要描述 bug 是什么。

**复现步骤**
1. 执行 '...'
2. 运行 '...'
3. 查看错误 '...'

**预期行为**
描述你期望发生什么。

**实际行为**
描述实际发生了什么。

**环境信息**
- OS: [e.g. macOS 13.0, Ubuntu 22.04]
- Python 版本: [e.g. 3.9.7]
- Git 版本: [e.g. 2.39.0]
- Bash 版本: [e.g. 5.1.16]

**日志/错误信息**
```
粘贴相关的错误信息或日志
```

**截图**
如果适用，添加截图帮助说明问题。

**额外信息**
其他有助于解决问题的信息。
```

## 💭 功能建议

创建功能请求时请提供：

### 功能请求模板

```markdown
**功能描述**
清楚简洁地描述你想要的功能。

**问题背景**
这个功能要解决什么问题？为什么需要它？

**建议的解决方案**
描述你希望如何实现这个功能。

**备选方案**
描述你考虑过的其他解决方案。

**使用场景**
提供 1-2 个实际使用场景示例。

**额外信息**
其他相关信息或截图。
```

## 📞 联系方式

- **Issues**: [GitHub Issues](https://github.com/yzhucn/code-health/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yzhucn/code-health/discussions)
- **Email**: 通过 GitHub profile 联系维护者

## 🙏 致谢

感谢所有贡献者！你的努力让这个项目变得更好。

### 贡献者列表

<!-- 贡献者列表将在这里自动生成 -->

查看所有贡献者：[Contributors](https://github.com/yzhucn/code-health/graphs/contributors)

---

**再次感谢你的贡献！** 🎉

如果你有任何问题，请随时在 [Issues](https://github.com/yzhucn/code-health/issues) 中提问。
