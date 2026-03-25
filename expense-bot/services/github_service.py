import subprocess
import os
from pathlib import Path

REPO_PATH = os.getenv(
    "CLAUDE_PROJECT_DOCS_PATH",
    os.path.expanduser("~/Projects/claude-project-docs")
)


def commit_monthly_report(year_month: str, md: str) -> bool:
    try:
        d = Path(REPO_PATH) / "finance" / "monthly_report"
        d.mkdir(parents=True, exist_ok=True)
        f = d / f"{year_month}.md"
        f.write_text(md, encoding="utf-8")
        subprocess.run(["git", "add", str(f)], cwd=REPO_PATH, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"report: {year_month}"],
            cwd=REPO_PATH, check=True
        )
        subprocess.run(["git", "push", "origin", "master"], cwd=REPO_PATH, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e}")
        return False
