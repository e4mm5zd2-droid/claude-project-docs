#!/usr/bin/env python3
"""
事業2 Xツール販売 - 営業資料自動生成スクリプト
Claude APIを使用してLP・営業トークスクリプト・βリクルート文を生成する
実装提案: [advisor] LP・営業トークスクリプトの即時自動生成
"""

import anthropic
import os
from pathlib import Path

client = anthropic.Anthropic()

PRODUCT_CONTEXT = """
## 商品情報: X 自動投稿ツール（by on the edge）

### 機能一覧
- Claude AI による投稿文の自動生成（日本語完全対応）
- X（旧Twitter）への自動投稿
- 投稿スケジュール設定（1日の回数・時間指定）
- 予約投稿機能
- Web管理画面（OAuth 2.0認証）
- 複数アカウント同時管理
- 画像付き自動投稿（Cloudflare R2連携）
- 暗号通貨アカウント監視機能（Discord通知）
- Renderクラウド対応（24時間無人運用）

### 技術スタック
- Python 3.11 / Flask / Tweepy / Anthropic Claude Sonnet
- PostgreSQL on Render / Cloudflare R2

### 開発完成度
95%（予約投稿の微調整のみ残存）

### 価格プラン
- ライト：¥49,800/月
- スタンダード：¥98,000/月
- プレミアム：¥198,000/月
- エンタープライズ：応相談

### ターゲット顧客
1. 個人インフルエンサー・アフィリエイター（暗号通貨・投資・ビジネス系）
2. SNS担当者不在の小規模事業者
3. AI自動化ツールに関心のある中小企業・スタートアップ

### 競合比較
| ツール | AI自動生成 | 日本語最適化 | 月額 |
|--------|-----------|------------|------|
| 本ツール | ✅ Claude完全対応 | ✅ 完璧 | ¥49,800〜 |
| SocialDog | ❌ なし | ✅ | ¥5,000〜 |
| Hootsuite | △ 限定的 | △ 弱い | ¥23,000〜 |
| Hypefury | △ 英語メイン | ❌ 弱い | ¥4,000〜 |

### 差別化ポイント
- AI自動生成＋自動投稿のワンストップ（競合にない）
- 日本語完全対応（Claude Sonnet by Anthropic）
- 140〜5,000字の柔軟な文字数設定
- 非エンジニアでもWeb画面から簡単操作
- AIエージェント連携対応（Anthropic Managed Agents活用）

### 会社情報
- 株式会社 on the edge
- 代表取締役：テラス孝之
- 事業フェーズ：βテスト完了後 → 営業開始
"""

DOCS_DIR = Path(__file__).parent / "docs"
DOCS_DIR.mkdir(exist_ok=True)


def generate_with_cache(system_prompt: str, user_prompt: str, max_tokens: int = 4000) -> str:
    """prompt cachingを活用してコンテンツ生成"""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_prompt}],
    )
    return response.content[0].text


def generate_landing_page() -> str:
    system = f"""あなたは日本のBtoB SaaSのLPコピーライティングの専門家です。
以下の商品情報をもとに、転換率の高いLP構成案と本文を作成してください。

{PRODUCT_CONTEXT}

出力形式：Markdown（セクションごとに見出しを使う）
トーン：プロフェッショナル・信頼感・即決を促す
ターゲット：非エンジニアの経営者・マーケター・インフルエンサー"""

    user = """以下のセクションを含むLP全文を作成してください：

1. ファーストビュー（キャッチコピー＋サブコピー＋CTA）
2. 課題提示（ターゲットが抱えるペイン）
3. 解決策（本ツールの機能・価値）
4. 差別化（競合との比較）
5. 実績・信頼性（βテスト中の訴求）
6. 価格プラン（3プラン表示）
7. FAQ（5項目）
8. CTA（申込・問い合わせ）

AIエージェント向け市場（Anthropic Managed Agents全プラン開放）のトレンドも織り込んでください。"""

    return generate_with_cache(system, user, max_tokens=5000)


def generate_sales_pitch() -> str:
    system = f"""あなたは日本のBtoB IT営業の専門家です。
以下の商品情報をもとに、成約率の高い営業トークスクリプトを作成してください。

{PRODUCT_CONTEXT}

出力形式：Markdown（シーン別のトーク台本）
トーン：誠実・プロ・顧客メリット最優先
想定営業スタイル：対面/電話/オンライン商談"""

    user = """以下の構成で営業トークスクリプト（B-005）を作成してください：

## 1. アイスブレイク（2分）
## 2. ヒアリング（5分）
   - 現在のX運用状況を確認する質問リスト
## 3. 課題の共有（3分）
## 4. デモ＋提案（10分）
   - 機能紹介の順序と説明文
   - AIエージェント活用の訴求（最新トレンド）
## 5. 価格提示と価値の比較（5分）
## 6. 反論処理（よくある5つの反論と切り返し）
## 7. クロージング（3分）
## 8. フォローアップメール文面テンプレート

営業代行（成果報酬型30%）向けのシンプルさも意識してください。"""

    return generate_with_cache(system, user, max_tokens=5000)


def generate_beta_recruit() -> str:
    system = f"""あなたはSNSマーケティングとグロースハックの専門家です。
以下の商品情報をもとに、βテスト参加者を募集するX投稿文と申込LP文を作成してください。

{PRODUCT_CONTEXT}"""

    user = """βテスト参加者募集（B-001）のための以下のコンテンツを作成してください：

## 1. X投稿文（3パターン）
   - パターンA: 機能訴求型（140字以内）
   - パターンB: 限定感訴求型（140字以内）
   - パターンC: 課題共感型（140字以内）

## 2. スレッド投稿（5ツイート構成）
   - 課題提示 → 解決策 → 機能紹介 → 限定募集 → CTA

## 3. βテスト参加者向けLP文
   - 参加条件・特典・申込方法

## 4. DM送付用テキスト
   - インフルエンサー向けパーソナライズDM

AIエージェント向け市場という最新トレンドを訴求に活用してください。"""

    return generate_with_cache(system, user, max_tokens=4000)


def generate_demo_script() -> str:
    system = f"""あなたはプロダクトデモ動画のディレクターです。
以下の商品情報をもとに、スクリーンキャプチャで完成できるデモ動画の構成台本を作成してください。

{PRODUCT_CONTEXT}"""

    user = """3〜5分のデモ動画構成台本を作成してください：

## 台本フォーマット
各シーンは以下を含む：
- [画面]: 表示すべき画面・操作
- [ナレーション]: 読み上げるテキスト
- [テロップ]: 画面に表示する文字

## 必須シーン
1. オープニング（15秒）：課題提示
2. ダッシュボード紹介（45秒）
3. AI投稿生成デモ（90秒）：実際にAIが文章を生成する様子
4. スケジュール設定（45秒）
5. 投稿結果確認（30秒）
6. クロージング＋CTA（30秒）"""

    return generate_with_cache(system, user, max_tokens=3000)


def main():
    print("=== 事業2 Xツール販売 - 営業資料自動生成 ===")
    print(f"モデル: claude-sonnet-4-6 (prompt caching有効)")
    print()

    tasks = [
        ("LP構成案・本文 (B-004)", "LANDING_PAGE_DRAFT.md", generate_landing_page),
        ("営業トークスクリプト (B-005)", "SALES_PITCH.md", generate_sales_pitch),
        ("βテスト募集文 (B-001サポート)", "BETA_RECRUIT.md", generate_beta_recruit),
        ("デモ動画台本 (B-004サポート)", "DEMO_SCRIPT.md", generate_demo_script),
    ]

    for label, filename, fn in tasks:
        print(f"[生成中] {label}...")
        try:
            content = fn()
            output_path = DOCS_DIR / filename
            header = f"# {label}\n\n> 生成日: 2026-04-11 | 生成: Claude Sonnet 4.6 (自動生成初稿)\n> レビュー後に修正指示を再投入してブラッシュアップしてください\n\n---\n\n"
            output_path.write_text(header + content, encoding="utf-8")
            print(f"  ✅ 保存: {output_path}")
        except Exception as e:
            print(f"  ❌ エラー: {e}")
        print()

    print("=== 生成完了 ===")
    print(f"出力先: {DOCS_DIR}")
    print()
    print("次のステップ:")
    print("1. 各ファイルをテラス・松本でレビュー")
    print("2. 修正指示を再投入してブラッシュアップ")
    print("3. B-001 βテスト募集をXに投稿")
    print("4. B-004 LP公開 / B-005 営業代行に配布")


if __name__ == "__main__":
    main()
