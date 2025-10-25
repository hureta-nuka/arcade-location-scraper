# アーケード店舗スクレイパー

KONAMI e-amusementの店舗検索ページから全店舗のデータを自動取得するPythonスクレイパーです。

## 機能

- **自動ページング**: 全ページを自動的に巡回してデータを取得
- **店舗情報取得**: 店舗名、営業時間、住所、電話番号、アクセス情報などを取得
- **JSON出力**: 取得したデータを構造化されたJSON形式で保存
- **エラーハンドリング**: 基本的なエラー処理とログ出力

## インストール

### 前提条件

- Python 3.13以上
- uv（推奨）またはpip

### 依存関係のインストール

```bash
# uvを使用する場合
uv sync

# pipを使用する場合
pip install playwright
```

## 使用方法

### 基本的な使用方法

```bash
uv run main.py
python main.py
```

実行すると、KONAMI e-amusementの店舗検索ページから全店舗のデータを自動取得し、`shop_data.json`ファイルに保存されます。

### 実行例

```bash
$ python main.py
KONAMI e-amusementの全ページから店舗データを取得中...
データが取得できなくなるまで自動的に次のページに移動します。
ページ 1 にアクセス中: https://p.eagate.573.jp/game/facility/search/p/list.html?gkey=PLRS&paselif=false&finder=ll&latitude=11&longitude=11&page=1
ページ 1 の店舗ブロック数: 20
  店舗 1: アミパラ佐世保店
  店舗 2: 楽市楽座イオンモール福岡伊都店
...
ページ 1 から 20 個の店舗データを取得しました
...
全ページから合計 378 個の店舗データを取得しました

=== 取得結果 ===
総店舗数: 378
取得完了時刻: 2025-01-25 22:04:58
結果を shop_data.json に保存しました
```

## 出力データ形式

取得したデータは以下のJSON形式で保存されます：

```json
{
  "shops": [
    {
      "name": "アミパラ佐世保店",
      "operation_time": "10:00～24:00",
      "holiday": "無し",
      "latitude": "33.15005741",
      "longitude": "129.7804145",
      "tel": "0956-34-8880",
      "address": "佐世保市大塔町18-15",
      "access": "JR大塔駅徒歩3分"
    }
  ],
  "count": 378,
  "source": "https://p.eagate.573.jp/game/facility/search/p/list.html",
  "timestamp": "2025-01-25T22:04:58.788059",
  "description": "KONAMI e-amusement店舗検索から取得した全店舗データ"
}
```

### データ項目

- **name**: 店舗名
- **operation_time**: 営業時間
- **holiday**: 定休日
- **latitude**: 緯度
- **longitude**: 経度
- **tel**: 電話番号
- **address**: 住所
- **access**: アクセス情報

## プロジェクト構造

```
arcade-location-scraper/
├── main.py              # メインスクリプト
├── pyproject.toml       # プロジェクト設定
├── shop_data.json       # 取得したデータ（実行後に生成）
├── logs/                # ログファイル（将来の拡張用）
├── backups/             # バックアップファイル（将来の拡張用）
└── tests/               # テストファイル（将来の拡張用）
```

## カスタマイズ

### 最大ページ数の変更

`main.py`の119行目を編集して最大ページ数を変更できます：

```python
# 安全のため、最大50ページまで制限
if page_num > 50:  # 50ページに変更
    print("最大ページ数（50ページ）に達しました。終了します。")
    break
```

### タイムアウト設定の変更

`main.py`の24行目と27行目でタイムアウト設定を変更できます：

```python
# ページにアクセス
await page.goto(url, wait_until="networkidle", timeout=60000)  # 60秒に変更

# ページが完全に読み込まれるまで少し待機
await page.wait_for_timeout(5000)  # 5秒に変更
```

### ヘッドレスモードの無効化

ブラウザの動作を確認したい場合は、`main.py`の15行目を編集：

```python
browser = await p.chromium.launch(headless=False)  # ブラウザを表示
```

## トラブルシューティング

### よくある問題

1. **ブラウザが起動しない**
   ```bash
   playwright install chromium
   ```

2. **ページが読み込まれない**
   - ネットワーク接続を確認
   - タイムアウト値を増やす
   - ヘッドレスモードを無効にして動作を確認

3. **データが取得できない**
   - 対象サイトの構造が変更されていないか確認
   - セレクター（`div.cl_shop_bloc`）が正しいか確認

### デバッグ方法

1. **ヘッドレスモードを無効化**
   ```python
   browser = await p.chromium.launch(headless=False)
   ```

2. **詳細なログを確認**
   - コンソール出力で各ステップの動作を確認
   - エラーメッセージを確認

3. **単一ページでテスト**
   ```python
   # main.pyのwhileループを一時的に無効化して1ページのみテスト
   if page_num > 1:
       break
   ```

## 注意事項

- このスクレイパーは教育目的で作成されています
- 対象サイトの利用規約を遵守してください
- 過度なリクエストは避け、適切な間隔を空けて実行してください
- 取得したデータの使用は自己責任で行ってください
- サイトの構造変更により動作しなくなる可能性があります

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

プルリクエストやイシューの報告を歓迎します。

## 更新履歴

- v0.1.0: 初回リリース
  - KONAMI e-amusement店舗検索からのデータ取得機能
  - 自動ページング機能
  - JSON形式でのデータ出力
