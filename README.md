# Claude Project Docs

ローカルの各プロジェクトの最新情報を自動でMarkdownに生成し、Claude Projects の GitHub連携で同期するためのリポジトリ。

## 使い方

```bash
# ドキュメント生成（プレビュー）
python sync_docs.py

# 生成 + git commit & push
python sync_docs.py --auto
```

## 仕組み

```
[ローカルプロジェクト] → [sync_docs.py] → [docs/*.md] → [GitHub] → [Claude Projects]
                          自動生成          git push      "Sync now" 1クリック
```

## 生成されるドキュメント

| ファイル | 内容 |
|---------|------|
| `docs/x-auto-bot.md` | X Auto Bot - 暗号通貨監視・自動投稿ボット |
| `docs/corporate-site.md` | On The Edge コーポレートサイト |
| `docs/smartnr.md` | SmartNR - ナイトワーク スカウト管理アプリ |
| `docs/line-claude-bot.md` | LINE Claude Bot |
| `docs/company-overview.md` | 全サービス横断まとめ |

## セットアップ

```bash
pip install pyyaml
```

## Claude Projects 連携

1. claude.ai → プロジェクト → ナレッジ → GitHub連携
2. このリポジトリを接続
3. `docs/` 内の全ファイルを選択
4. 以降は `python sync_docs.py --auto` 実行後に「Sync now」を押すだけ
