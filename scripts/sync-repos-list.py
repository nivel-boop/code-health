#!/usr/bin/env python3
"""
云效 Codeup 仓库自动发现脚本
通过 API 自动获取组织下的所有仓库，生成 repos-list.txt

使用方法:
    python3 sync-repos-list.py [--dry-run] [--filter ecomind]

环境变量:
    CODEUP_TOKEN: 云效个人访问令牌
    CODEUP_ORG_ID: 云效组织ID
"""

import json
import urllib.request
import os
import sys
from datetime import datetime

# 配置
API_DOMAIN = "openapi-rdc.aliyuncs.com"
DEFAULT_TOKEN = os.environ.get("CODEUP_TOKEN", "")
DEFAULT_ORG_ID = os.environ.get("CODEUP_ORG_ID", "69094bdef9c52e7d8c272ffc")

# 脚本目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
REPOS_LIST_FILE = os.path.join(PROJECT_ROOT, "repos-list.txt")


def fetch_repositories(token: str, org_id: str) -> list:
    """从云效 API 获取所有仓库列表"""
    url = f"https://{API_DOMAIN}/oapi/v1/codeup/organizations/{org_id}/repositories?page=1&perPage=100"

    req = urllib.request.Request(url, headers={
        "Content-Type": "application/json",
        "x-yunxiao-token": token
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"❌ API 调用失败: {e}")
        sys.exit(1)


def filter_repos(repos: list, namespace_filter: str = None) -> list:
    """过滤仓库列表"""
    filtered = []
    for repo in repos:
        # 跳过已归档的仓库
        if repo.get("archived", False):
            continue

        # 跳过 demo 仓库
        if repo.get("demoProject", False):
            continue

        path = repo.get("pathWithNamespace", "")

        # 如果指定了命名空间过滤
        if namespace_filter:
            if not path.startswith(f"{repo.get('namespaceId', '')}/") and namespace_filter not in path:
                # 检查路径是否包含过滤关键词
                if namespace_filter.lower() not in path.lower():
                    continue

        filtered.append(repo)

    return filtered


def generate_repos_list(repos: list, include_groups: list = None) -> str:
    """生成 repos-list.txt 内容"""
    lines = [
        "# EcoMind 仓库列表 (自动生成)",
        f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "# 格式: 仓库名|Git URL",
        ""
    ]

    # 按命名空间分组
    groups = {}
    for repo in repos:
        path = repo.get("pathWithNamespace", "")
        parts = path.split("/")

        # 获取组名 (第二层)
        if len(parts) >= 2:
            group = parts[1]
        else:
            group = "other"

        if include_groups and group not in include_groups:
            continue

        if group not in groups:
            groups[group] = []
        groups[group].append(repo)

    # 生成配置
    for group in sorted(groups.keys()):
        lines.append(f"# === {group} ===")
        for repo in sorted(groups[group], key=lambda x: x["name"]):
            name = repo["path"]  # 使用 path 作为目录名
            web_url = repo.get("webUrl", "")
            git_url = web_url + ".git" if web_url else ""
            lines.append(f"{name}|{git_url}")
        lines.append("")

    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="云效 Codeup 仓库自动发现")
    parser.add_argument("--token", default=DEFAULT_TOKEN, help="云效个人访问令牌")
    parser.add_argument("--org-id", default=DEFAULT_ORG_ID, help="云效组织ID")
    parser.add_argument("--dry-run", action="store_true", help="仅显示不写入文件")
    parser.add_argument("--groups", nargs="+", default=["ecomind"], help="要包含的组 (默认: ecomind)")
    parser.add_argument("--all", action="store_true", help="包含所有组")

    args = parser.parse_args()

    if not args.token:
        print("❌ 请设置 CODEUP_TOKEN 环境变量或使用 --token 参数")
        sys.exit(1)

    print("🔍 正在从云效获取仓库列表...")
    repos = fetch_repositories(args.token, args.org_id)
    print(f"   找到 {len(repos)} 个仓库")

    # 过滤
    filtered = filter_repos(repos)
    print(f"   过滤后 {len(filtered)} 个仓库 (排除归档和demo)")

    # 生成内容
    include_groups = None if args.all else args.groups
    content = generate_repos_list(filtered, include_groups)

    if args.dry_run:
        print("\n📋 预览 repos-list.txt:\n")
        print(content)
    else:
        with open(REPOS_LIST_FILE, "w") as f:
            f.write(content)
        print(f"\n✅ 已更新 {REPOS_LIST_FILE}")

        # 统计
        repo_count = len([l for l in content.split("\n") if l and not l.startswith("#")])
        print(f"   共 {repo_count} 个仓库")


if __name__ == "__main__":
    main()
