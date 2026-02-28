#!/usr/bin/env python3
"""
Claude Project Docs Sync Script
各プロジェクトの最新情報をMarkdownに生成し、GitHub経由でClaude Projectsに同期する。

使い方:
    python sync_docs.py          # ドキュメント生成のみ（プレビュー）
    python sync_docs.py --auto   # 生成 + git commit & push
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).parent.resolve()
CONFIG_PATH = SCRIPT_DIR / "config.yaml"


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def run_cmd(cmd: list[str], cwd: str | None = None) -> str:
    """Run a shell command and return stdout."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=cwd, timeout=30
        )
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def get_git_log(project_path: str, count: int = 10) -> str:
    return run_cmd(
        ["git", "log", f"--oneline", f"-{count}", "--no-decorate"], cwd=project_path
    )


def get_git_branch(project_path: str) -> str:
    return run_cmd(["git", "branch", "--show-current"], cwd=project_path)


def read_file_safe(path: str | Path) -> str | None:
    """Read file contents, return None if not found."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return None


def get_package_json_info(project_path: str) -> dict | None:
    content = read_file_safe(Path(project_path) / "package.json")
    if not content:
        return None
    try:
        data = json.loads(content)
        return {
            "name": data.get("name", ""),
            "version": data.get("version", ""),
            "dependencies": data.get("dependencies", {}),
            "devDependencies": data.get("devDependencies", {}),
            "scripts": data.get("scripts", {}),
        }
    except json.JSONDecodeError:
        return None


def get_requirements_txt(project_path: str) -> list[str] | None:
    """Search for requirements.txt in project root and common subdirs."""
    for subdir in ["", "backend"]:
        path = Path(project_path) / subdir / "requirements.txt"
        content = read_file_safe(path)
        if content:
            return [
                line.strip()
                for line in content.splitlines()
                if line.strip() and not line.startswith("#")
            ]
    return None


def get_directory_tree(project_path: str, max_depth: int = 2) -> str:
    """Generate directory tree string, skipping common non-essential dirs."""
    skip = {
        "node_modules", ".git", "venv", "__pycache__", ".next",
        "dist", ".env", "logs", "data", ".DS_Store", "*.db",
        "package-lock.json", ".venv",
    }
    lines = []
    root = Path(project_path)

    def _walk(current: Path, prefix: str, depth: int):
        if depth > max_depth:
            return
        try:
            entries = sorted(current.iterdir(), key=lambda e: (not e.is_dir(), e.name))
        except PermissionError:
            return
        dirs = [e for e in entries if e.is_dir() and e.name not in skip]
        files = [e for e in entries if e.is_file() and e.name not in skip]
        items = dirs + files
        for i, entry in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            suffix = "/" if entry.is_dir() else ""
            lines.append(f"{prefix}{connector}{entry.name}{suffix}")
            if entry.is_dir():
                extension = "    " if is_last else "│   "
                _walk(entry, prefix + extension, depth + 1)

    _walk(root, "", 0)
    return "\n".join(lines)


def get_render_yaml_info(project_path: str) -> str | None:
    content = read_file_safe(Path(project_path) / "render.yaml")
    return content


def collect_extra_docs(project_path: str, config: dict) -> list[tuple[str, str]]:
    """Collect content from docs_dirs and extra_docs."""
    results = []
    root = Path(project_path)

    # docs_dirs - read all .md files in the directory
    for docs_dir in config.get("docs_dirs", []):
        dir_path = root / docs_dir
        if dir_path.is_dir():
            for md_file in sorted(dir_path.glob("*.md")):
                content = read_file_safe(md_file)
                if content:
                    rel = md_file.relative_to(root)
                    results.append((str(rel), content))

    # extra_docs - specific files
    for doc_path in config.get("extra_docs", []):
        full_path = root / doc_path
        content = read_file_safe(full_path)
        if content:
            results.append((doc_path, content))

    return results


def generate_project_doc(name: str, config: dict) -> str:
    """Generate markdown document for a single project."""
    project_path = config["path"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    sections = []

    # Header
    sections.append(f"# {config['title']}")
    sections.append(f"\n> {config['description']}")
    sections.append(f"\n*最終更新: {now}*")
    sections.append(f"\n**パス**: `{project_path}`")

    branch = get_git_branch(project_path)
    if branch:
        sections.append(f"**ブランチ**: `{branch}`")

    # README.md
    readme = read_file_safe(Path(project_path) / "README.md")
    if readme:
        sections.append("\n---\n## README.md\n")
        sections.append(readme)

    # CLAUDE.md
    claude_md = read_file_safe(Path(project_path) / "CLAUDE.md")
    if claude_md:
        sections.append("\n---\n## CLAUDE.md\n")
        sections.append(claude_md)

    # Tech Stack
    sections.append("\n---\n## 技術スタック\n")
    pkg = get_package_json_info(project_path)
    # Also check frontend subdir
    if not pkg:
        pkg = get_package_json_info(str(Path(project_path) / "frontend"))
        if pkg:
            sections.append("*(frontend/package.json)*\n")
    if pkg:
        if pkg["dependencies"]:
            sections.append("### Dependencies\n")
            sections.append("| Package | Version |")
            sections.append("|---------|---------|")
            for dep, ver in sorted(pkg["dependencies"].items()):
                sections.append(f"| {dep} | {ver} |")

        if pkg["devDependencies"]:
            sections.append("\n### Dev Dependencies\n")
            sections.append("| Package | Version |")
            sections.append("|---------|---------|")
            for dep, ver in sorted(pkg["devDependencies"].items()):
                sections.append(f"| {dep} | {ver} |")

        if pkg["scripts"]:
            sections.append("\n### Scripts\n")
            sections.append("```json")
            sections.append(json.dumps(pkg["scripts"], indent=2))
            sections.append("```")

    reqs = get_requirements_txt(project_path)
    if reqs:
        sections.append("\n### Python Dependencies\n")
        sections.append("```")
        sections.append("\n".join(reqs))
        sections.append("```")

    # Directory Structure
    sections.append("\n---\n## ディレクトリ構成\n")
    sections.append("```")
    sections.append(get_directory_tree(project_path))
    sections.append("```")

    # Render Config
    render_yaml = get_render_yaml_info(project_path)
    if render_yaml:
        sections.append("\n---\n## デプロイ設定 (render.yaml)\n")
        sections.append("```yaml")
        sections.append(render_yaml)
        sections.append("```")

    # Extra docs
    extra_docs = collect_extra_docs(project_path, config)
    if extra_docs:
        sections.append("\n---\n## プロジェクトドキュメント\n")
        for doc_path, content in extra_docs:
            sections.append(f"\n### {doc_path}\n")
            sections.append(content)

    # Recent Changes
    git_log = get_git_log(project_path)
    if git_log:
        sections.append("\n---\n## 最近の変更 (git log)\n")
        sections.append("```")
        sections.append(git_log)
        sections.append("```")

    return "\n".join(sections) + "\n"


def generate_company_overview(config: dict, project_configs: dict) -> str:
    """Generate cross-project overview document."""
    overview = config["company_overview"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    sections = []
    sections.append(f"# {overview['title']}")
    sections.append(f"\n*最終更新: {now}*")

    # Company info from shared docs
    biz_docs_dir = overview.get("business_docs_dir")
    if biz_docs_dir:
        biz_path = Path(biz_docs_dir)
        if biz_path.is_dir():
            sections.append("\n---\n## 会社・ビジネス情報\n")
            for md_file in sorted(biz_path.glob("*.md")):
                content = read_file_safe(md_file)
                if content:
                    sections.append(f"\n### {md_file.name}\n")
                    sections.append(content)

    # Services summary
    sections.append("\n---\n## サービス一覧\n")
    sections.append("| サービス | 概要 | 技術スタック | デプロイ |")
    sections.append("|---------|------|------------|---------|")

    for name, proj in project_configs.items():
        path = proj["path"]
        title = proj["title"]

        # Determine tech stack
        tech = []
        pkg = get_package_json_info(path)
        if not pkg:
            pkg = get_package_json_info(str(Path(path) / "frontend"))
        reqs = get_requirements_txt(path)

        if pkg and pkg["dependencies"]:
            deps = list(pkg["dependencies"].keys())
            key_deps = [d for d in deps if d in [
                "react", "next", "express", "vue", "fastapi",
                "@line/bot-sdk", "@anthropic-ai/sdk", "framer-motion",
                "tweepy", "anthropic", "Flask",
            ]]
            if not key_deps:
                key_deps = deps[:3]
            tech.extend(key_deps)
        if reqs:
            key_reqs = [r.split("==")[0].split(">=")[0] for r in reqs if any(
                k in r.lower() for k in ["fastapi", "flask", "tweepy", "anthropic", "sqlalchemy", "supabase"]
            )]
            tech.extend(key_reqs)

        # Determine deploy info
        render_yaml = read_file_safe(Path(path) / "render.yaml")
        deploy = "Render" if render_yaml else "?"
        dockerfile = read_file_safe(Path(path) / "Dockerfile")
        if dockerfile:
            deploy += " (Docker)"

        tech_str = ", ".join(tech) if tech else "—"
        sections.append(f"| {title} | {proj['description'][:50]} | {tech_str} | {deploy} |")

    # Render configurations
    sections.append("\n---\n## Render デプロイ構成\n")
    for name, proj in project_configs.items():
        render_yaml = read_file_safe(Path(proj["path"]) / "render.yaml")
        if render_yaml:
            sections.append(f"\n### {proj['title']}\n")
            sections.append("```yaml")
            sections.append(render_yaml)
            sections.append("```")

    # Tech stack cross-reference
    sections.append("\n---\n## 技術スタック横断まとめ\n")

    all_deps = {}
    for name, proj in project_configs.items():
        path = proj["path"]
        pkg = get_package_json_info(path)
        if not pkg:
            pkg = get_package_json_info(str(Path(path) / "frontend"))
        if pkg and pkg["dependencies"]:
            for dep, ver in pkg["dependencies"].items():
                if dep not in all_deps:
                    all_deps[dep] = []
                all_deps[dep].append((name, ver))

        reqs = get_requirements_txt(path)
        if reqs:
            for req in reqs:
                dep_name = req.split("==")[0].split(">=")[0].split("[")[0]
                ver = req.replace(dep_name, "").strip("=><[] ")
                if dep_name not in all_deps:
                    all_deps[dep_name] = []
                all_deps[dep_name].append((name, ver or "?"))

    # Show dependencies used across multiple projects
    shared_deps = {k: v for k, v in all_deps.items() if len(v) > 1}
    if shared_deps:
        sections.append("\n### 複数プロジェクトで共通の依存関係\n")
        sections.append("| パッケージ | 使用プロジェクト |")
        sections.append("|-----------|----------------|")
        for dep, projects in sorted(shared_deps.items()):
            proj_str = ", ".join(f"{p} ({v})" for p, v in projects)
            sections.append(f"| {dep} | {proj_str} |")

    return "\n".join(sections) + "\n"


def git_auto_push(output_dir: Path):
    """Commit and push changes to GitHub."""
    repo_dir = str(SCRIPT_DIR)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Check for changes
    status = run_cmd(["git", "status", "--porcelain"], cwd=repo_dir)
    if not status:
        print("No changes to commit.")
        return

    print(f"\nChanges detected:\n{status}")

    # Stage docs
    run_cmd(["git", "add", "docs/"], cwd=repo_dir)
    run_cmd(["git", "add", "config.yaml"], cwd=repo_dir)

    # Commit
    msg = f"docs: sync project docs ({now})"
    result = run_cmd(["git", "commit", "-m", msg], cwd=repo_dir)
    print(f"\n{result}")

    # Push
    print("\nPushing to GitHub...")
    result = run_cmd(["git", "push"], cwd=repo_dir)
    if result:
        print(result)
    print("Done! Go to Claude Projects and click 'Sync now'.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate project docs for Claude Projects sync"
    )
    parser.add_argument(
        "--auto", action="store_true",
        help="Auto commit & push to GitHub after generating docs"
    )
    args = parser.parse_args()

    config = load_config()
    output_dir = SCRIPT_DIR / config["output_dir"]
    output_dir.mkdir(exist_ok=True)

    projects = config["projects"]

    print("=== Claude Project Docs Sync ===\n")

    # Generate per-project docs
    for name, proj_config in projects.items():
        print(f"Generating: {proj_config['output']}...", end=" ")
        if not Path(proj_config["path"]).is_dir():
            print(f"SKIP (path not found: {proj_config['path']})")
            continue
        doc = generate_project_doc(name, proj_config)
        out_path = output_dir / proj_config["output"]
        out_path.write_text(doc, encoding="utf-8")
        print(f"OK ({len(doc):,} chars)")

    # Generate company overview
    print(f"Generating: {config['company_overview']['output']}...", end=" ")
    overview = generate_company_overview(config, projects)
    out_path = output_dir / config["company_overview"]["output"]
    out_path.write_text(overview, encoding="utf-8")
    print(f"OK ({len(overview):,} chars)")

    print(f"\nAll docs written to: {output_dir}/")

    if args.auto:
        git_auto_push(output_dir)
    else:
        print("\nRun with --auto to commit & push to GitHub.")


if __name__ == "__main__":
    main()
