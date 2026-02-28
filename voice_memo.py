#!/usr/bin/env python3
"""
Voice Memo → Structured Document Script

音声ファイルを文字起こし → 構造化Markdownに変換し shared/docs/ に保存する。

使い方:
    python voice_memo.py recording.m4a
    python voice_memo.py recording.m4a --output 事業計画_2026Q1.md
    python voice_memo.py recording.m4a --transcript-only
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import anthropic
import openai
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).parent.resolve()
DOCS_DIR = Path("/Users/apple/Projects/shared/docs")
TRANSCRIPTS_DIR = DOCS_DIR / "transcripts"

SUPPORTED_FORMATS = {".m4a", ".mp3", ".wav", ".webm", ".ogg", ".flac"}

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


def save_structured(content: str, output_name: str) -> Path:
    """構造化Markdownを保存"""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    path = DOCS_DIR / output_name
    path.write_text(content, encoding="utf-8")
    return path


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

    # Step 3: Claude で構造化
    print("[3/3] 構造化中... (Claude API)")
    structured = structure_transcript(transcript, audio_path.name)

    # 出力ファイル名の決定
    today = datetime.now().strftime("%Y%m%d")
    if args.output:
        output_name = args.output
        if not output_name.endswith(".md"):
            output_name += ".md"
    else:
        output_name = f"{today}_{stem}.md"

    output_path = save_structured(structured, output_name)
    print(f"      完了: {output_path}")

    print(f"\n次のステップ: sync-docs で Claude Projects に反映")


if __name__ == "__main__":
    main()
