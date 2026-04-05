# reels-overlay-tool

## 概要
AI生成動画（Midjourney→Kling AI）にゲーミフィケーション要素をオーバーレイし、Instagram Reels / TikTok / YouTube Shorts向けに自動加工するWebツール。iPhone（Safari）から操作可能。

## 技術スタック
| カテゴリ | 技術 |
|---|---|
| 言語 | Python 3.11 |
| フレームワーク | Streamlit |
| 動画処理 | FFmpeg 8.x |
| 画像処理 | Pillow |
| フォント | NotoSansJP-Bold |
| デプロイ | Mac mini常時稼働（Streamlit, ポート8502） |

## アーキテクチャ
```
reels-overlay-tool/
├── config/
│   ├── default.yaml
│   ├── server.yaml
│   ├── platforms/         # Instagram/TikTok/YouTube Shorts設定
│   └── templates/         # flight/drive/fall/underwater
├── src/
│   ├── core/
│   │   ├── compositor.py       # FFmpeg filter_complex組立・実行
│   │   ├── text_renderer.py    # Pillow日英テキスト描画
│   │   ├── button_generator.py # iOS録画風ボタン生成
│   │   └── audio_mixer.py      # BGMミキシング
│   ├── web/
│   │   ├── app.py              # Streamlitエントリポイント
│   │   ├── components/         # テンプレート選択、動画アップロード
│   │   └── pages/              # 単品加工、バッチ処理
│   └── cli.py
├── tests/
├── assets/                # ボタン画像、オーバーレイ画像
├── uploads/
└── output/
```

## データフロー
```
動画アップロード（iPhone Safari経由）
  → テンプレート選択（飛行/ドライブ/落下/水中）
  → オプション設定（ボタンサイズ、テキスト、スピードランプ、POVオーバーレイ、BGM）
  → [動画結合（2本→1本、20秒用）]
  → スピードランプ前処理（trim+setpts+concat）
  → FFmpeg filter_complex（テキスト画像 + ボタンring/dot + オーバーレイ画像を合成）
  → プラットフォーム別出力
  → ダウンロード → TikTok/Instagram投稿
```

## 主要機能
- テキストオーバーレイ（日本語/英語、位置調整可）
- iOSスクリーン録画風ボタン（白リング常時表示 + 赤丸点滅）
- スピードランプ（1.5x〜4.0x、15%/85%地点で自動加速）
- 動画結合（Kling AI 10秒×2本→20秒）
- POVオーバーレイ（スーパーマン/パラグライダー/気球/車/カスタム画像）
- BGM追加（MP3/WAV/M4A）
- プラットフォーム別出力（Instagram Reels / TikTok / YouTube Shorts）

## 起動方法
```bash
streamlit run src/web/app.py --server.port 8502 --server.address 0.0.0.0
```

### アクセス
- Tailscale経由: http://100.111.159.72:8502
- iPhone Safari: 「常にHTTPSを使用」をオフにする必要あり

## 現在の状態
- [ ] 開発中 / [x] 稼働中 / [ ] 停止中

## 関連事業
事業1(アフィリ)
