#!/usr/bin/env python3
"""
Voice Memo → Structured Document Script

音声ファイルを文字起こし → 構造化Markdownに変換 → 事業別フォルダに自動振り分け。

使い方:
    python voice_memo.py recording.m4a                    # 自動振り分け
    python voice_memo.py recording.m4a -b jigyou2         # 手動で事業指定
    python voice_memo.py recording.m4a --auto-push        # 自動git push
    python voice_memo.py recording.m4a --output 計画.md   # ファイル名指定
    python voice_memo.py recording.m4a --transcript-only  # 文字起こしのみ
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import anthropic
import openai
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).parent.resolve()
DOCS_DIR = SCRIPT_DIR / "shared" / "docs"
TRANSCRIPTS_DIR = DOCS_DIR / "transcripts"

SUPPORTED_FORMATS = {".m4a", ".mp3", ".wav", ".webm", ".ogg", ".flac"}

# 事業別議事録フォルダ
BUSINESS_MINUTES_DIRS = {
    "sokatsu": "sokatsu/minutes",
    "jigyou1": "jigyou1/minutes",
    "jigyou2": "jigyou2/minutes",
    "jigyou3": "jigyou3/minutes",
    "jigyou4": "jigyou4/minutes",
}

STRUCTURING_PROMPT = """\
以下は音声メモの文字起こしテキストです。これを構造化されたミーティングメモに変換してください。

ルール:
- フィラー（えーと、あのー、まあ、その、うーん等）を除去
- 議題ごとにセクション分け
- 決定事項・TODO・今後のアクションを抽出
- 要約は3行程度で簡潔に
- 担当者が言及されていれば記載

以下のMarkdownフォーマットで出力してください（```マークダウン```で囲まないこと）:

# ミーティングメモ: [内容から適切なタイトルを生成]
*日時: {date}*
*音声ファイル: {filename}*

## 要約
[3行程度の要約]

## 議題

### 1. [トピック名]
- 内容の要約
- 詳細ポイント

### 2. [トピック名]
...

## 決定事項
- [ ] xxx
- [ ] xxx

## 今後のアクション
- [ ] xxx（担当: xxx）

---

文字起こしテキスト:

{transcript}
"""

# 自動振り分け用プロンプト
ROUTING_PROMPT = """\
以下の文字起こしテキストの内容を分析し、どの事業に該当するか判定してください。

事業一覧:
- jigyou1: 暗号通貨アフィリエイト（仮想通貨、取引所、アフィリ、広告運用）
- jigyou2: Xツール販売（Twitter/X関連ツール、SNSマーケ、自動化ツール）
- jigyou3: 京都ボーイ求人（求人、ナイトワーク、京都、ボーイ、スカウト）
- jigyou4: スカウトCRM（CRM、顧客管理、スカウト管理、営業支援）
- sokatsu: 統括/全社（経営、複数事業にまたがる、該当なし、会社全体の話）

判定ルール:
- 1つの事業に明確に該当 → その事業名を返す
- 複数事業にまたがる → sokatsu
- どの事業にも該当しない → sokatsu
- 判断できない → sokatsu

JSONのみで回答してください（他のテキスト不要）:
{{"business": "jigyou1〜4またはsokatsu", "reason": "判定理由を1行で"}}

文字起こしテキスト:

{transcript}
"""


def load_env():
    env_path = SCRIPT_DIR / ".env"
    if env_path.exists():
        load_dotenv(env_path)


def transcribe(audio_path: Path) -> str:
    """OpenAI Whisper APIで音声ファイルを文字起こし"""
    client = openai.OpenAI()
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language="ja",
            response_format="text",
        )
    return result.strip()


def structure_transcript(transcript: str, audio_filename: str) -> str:
    """Claude APIで文字起こしテキストを構造化"""
    client = anthropic.Anthropic()
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = STRUCTURING_PROMPT.format(
        date=today,
        filename=audio_filename,
        transcript=transcript,
    )

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def save_transcript(transcript: str, stem: str) -> Path:
    """元の文字起こしテキストを保存"""
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    path = TRANSCRIPTS_DIR / f"{today}_{stem}_transcript.txt"
    path.write_text(transcript, encoding="utf-8")
    return path


def auto_route(transcript: str) -> tuple[str, str]:
    """Claudeで文字起こし内容を分析し、該当事業を自動判定"""
    client = anthropic.Anthropic()
    prompt = ROUTING_PROMPT.format(transcript=transcript[:3000])

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    try:
        data = json.loads(raw)
        business = data.get("business", "sokatsu")
        reason = data.get("reason", "")
    except json.JSONDecodeError:
        business = "sokatsu"
        reason = "JSONパース失敗、sokatsuにフォールバック"

    if business not in BUSINESS_MINUTES_DIRS:
        business = "sokatsu"
        reason = f"不明な事業名 → sokatsuにフォールバック"

    return business, reason


def save_structured(content: str, output_name: str, business: str = None) -> Path:
    """構造化Markdownを保存"""
    if business and business in BUSINESS_MINUTES_DIRS:
        target_dir = SCRIPT_DIR / BUSINESS_MINUTES_DIRS[business]
    else:
        target_dir = SCRIPT_DIR / BUSINESS_MINUTES_DIRS["sokatsu"]

    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / output_name
    path.write_text(content, encoding="utf-8")
    return path


def git_push(file_path: Path, business: str) -> bool:
    """git add → commit → push を実行"""
    try:
        subprocess.run(["git", "pull", "--rebase"], cwd=SCRIPT_DIR, check=True, capture_output=True)
        subprocess.run(["git", "add", str(file_path)], cwd=SCRIPT_DIR, check=True, capture_output=True)
        msg = f"update: {business} 音声メモ追加 ({file_path.name})"
        subprocess.run(["git", "commit", "-m", msg], cwd=SCRIPT_DIR, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "master"], cwd=SCRIPT_DIR, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"git操作エラー: {e}", file=sys.stderr)
        if e.stderr:
            print(f"  詳細: {e.stderr.decode()}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="音声メモを構造化ドキュメントに変換"
    )
    parser.add_argument("audio_file", help="音声ファイル (.m4a/.mp3/.wav/.webm)")
    parser.add_argument("--output", "-o", help="出力ファイル名 (例: 事業計画.md)")
    parser.add_argument(
        "--transcript-only",
        action="store_true",
        help="文字起こしのみ（Claude構造化なし）",
    )
    parser.add_argument(
        "--business", "-b",
        choices=list(BUSINESS_MINUTES_DIRS.keys()),
        default=None,
        help="事業別フォルダに手動指定 (例: -b jigyou2)。省略時はClaude自動振り分け",
    )
    parser.add_argument(
        "--auto-push",
        action="store_true",
        help="保存後に自動で git add → commit → push",
    )
    args = parser.parse_args()

    load_env()

    audio_path = Path(args.audio_file).resolve()
    if not audio_path.exists():
        print(f"Error: ファイルが見つかりません: {audio_path}", file=sys.stderr)
        sys.exit(1)

    if audio_path.suffix.lower() not in SUPPORTED_FORMATS:
        print(
            f"Error: 非対応フォーマット: {audio_path.suffix}  "
            f"(対応: {', '.join(sorted(SUPPORTED_FORMATS))})",
            file=sys.stderr,
        )
        sys.exit(1)

    stem = audio_path.stem

    # Step 1: 文字起こし
    print(f"[1/3] 文字起こし中... ({audio_path.name})")
    transcript = transcribe(audio_path)
    print(f"      完了 ({len(transcript):,} 文字)")

    # Step 2: 文字起こし原本を保存
    transcript_path = save_transcript(transcript, stem)
    print(f"[2/3] 文字起こし保存: {transcript_path}")

    if args.transcript_only:
        print("\n--transcript-only: 文字起こしのみ完了")
        print(f"\n--- 文字起こし ---\n{transcript}")
        return

    # Step 3: 事業振り分け（手動 or 自動）
    if args.business:
        business = args.business
        print(f"[3/4] 事業振り分け: {business}（手動指定）")
    else:
        print("[3/4] 事業振り分け中... (Claude自動判定)")
        business, reason = auto_route(transcript)
        print(f"      → {business}（理由: {reason}）")

    # Step 4: Claude で構造化
    print("[4/4] 構造化中... (Claude API)")
    structured = structure_transcript(transcript, audio_path.name)

    # 出力ファイル名の決定
    today = datetime.now().strftime("%Y%m%d")
    if args.output:
        output_name = args.output
        if not output_name.endswith(".md"):
            output_name += ".md"
    else:
        output_name = f"{today}_{stem}.md"

    output_path = save_structured(structured, output_name, business)
    print(f"      保存先: {output_path}")

    # auto-push
    if args.auto_push:
        print("\ngit push中...")
        if git_push(output_path, business):
            print(f"✅ 保存・push完了（{output_path}）")
        else:
            print("⚠️ git pushに失敗。手動でpushしてください。", file=sys.stderr)
    else:
        print(f"\n次のステップ: git add & push で Claude Projects に反映 (事業: {business})")


if __name__ == "__main__":
    main()
