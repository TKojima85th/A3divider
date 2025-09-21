# 📄 A3→A4 PDF分割ツール

A3サイズのPDFをA4サイズに分割・並び替えするWebアプリケーションです。シンプル分割と製本復元の2つのモードを提供します。

![A3→A4 PDF分割ツール](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-3.1+-green) ![PWA](https://img.shields.io/badge/PWA-Ready-purple)

## ✨ 機能

### 📄 シンプル分割モード
- A3ページを左右に分割してA4ページ2枚を作成
- 順序: A3ページ1 → A4ページ1,2
- 縦書きモード対応（右→左の順序）
- 90度回転オプション

### 📖 製本復元モード
- 中綴じ製本されたA3資料のスキャンPDFを正しいページ順に復元
- 独自の数学的アルゴリズムでページ配置を解析
- 任意のページ数に対応（4の倍数推奨）
- 自動ページ数検出または手動指定

## 🚀 ライブデモ

**🌐 A3→A4 PDF分割ツール** (Render でホスト中)

![デモ画像](https://via.placeholder.com/800x600/667eea/ffffff?text=A3%E2%86%92A4+PDF%E5%88%86%E5%89%B2%E3%83%84%E3%83%BC%E3%83%AB)

## 🛠️ インストール

### 必要環境
- Python 3.8+
- pip

### セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/a3-pdf-splitter.git
cd a3-pdf-splitter

# 仮想環境を作成
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt

# アプリケーションを起動
python app.py
```

ブラウザで http://127.0.0.1:5000 にアクセス

## 🌐 Renderへのデプロイ

### 手順

1. **GitHubリポジトリの準備**
   ```bash
   git push origin main
   ```

2. **Render ダッシュボードでの設定**
   - [Render](https://render.com) にサインアップ/ログイン
   - "New Web Service" を選択
   - GitHubリポジトリを接続

3. **デプロイ設定**
   ```yaml
   # render.yaml ファイルが自動的に検出されます
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. **環境変数の設定**
   - `SECRET_KEY`: ランダムな文字列（セキュリティ用）
   - `FLASK_ENV`: `production`

5. **デプロイ実行**
   - "Create Web Service" をクリック
   - 自動的にビルドとデプロイが開始されます

### Render デプロイの特徴

✅ **無料プラン利用可能**
✅ **自動HTTPS対応** (PWA要件)
✅ **Git連携** 自動デプロイ
✅ **カスタムドメイン対応**
✅ **高可用性インフラ**

### デプロイ後の確認

- PWAインストールプロンプトの表示
- オフライン機能の動作
- モバイルデバイスでの動作確認

## 📱 PWA対応

このアプリケーションはProgressive Web App (PWA)として設計されており、以下の機能を提供します：

- **オフライン動作**: サービスワーカーによるオフライン対応
- **インストール可能**: ホーム画面に追加可能
- **レスポンシブデザイン**: モバイル・タブレット・デスクトップ対応

### PWAとしてインストール

1. ブラウザでアプリケーションにアクセス
2. アドレスバーの「インストール」ボタンをクリック
3. または「ホーム画面に追加」を選択

## 🎯 使用方法

### シンプル分割

1. **ファイル選択**: A3 PDFファイルをドラッグ&ドロップまたは選択
2. **モード選択**: 「シンプル分割」を選択
3. **オプション設定**:
   - 縦書きモード（必要に応じて）
   - 90度回転（必要に応じて）
4. **実行**: 「PDFを分割」ボタンをクリック
5. **ダウンロード**: `[ファイル名]_simple_split.pdf`がダウンロード

### 製本復元

1. **ファイル選択**: 中綴じ製本をスキャンしたA3 PDFを選択
2. **モード選択**: 「製本復元」を選択
3. **ページ数設定**:
   - 自動検出（推奨）
   - 手動入力（4の倍数）
4. **実行**: 「PDFを分割」ボタンをクリック
5. **ダウンロード**: `[ファイル名]_booklet_reordered.pdf`がダウンロード

## 🔧 技術仕様

### バックエンド
- **フレームワーク**: Flask 3.1+
- **PDF処理**: PyPDF2
- **言語**: Python 3.8+

### フロントエンド
- **HTML5/CSS3/JavaScript**: モダンWeb標準
- **PWA**: Service Worker, Web App Manifest
- **レスポンシブデザイン**: CSS Grid, Flexbox

### ページ配置アルゴリズム

製本復元モードでは、以下の数式を使用してページ配置を計算します：

```
総A4ページ数: T (4の倍数)
A3シート数: S = T / 2
A3シート番号: i (1 ≤ i ≤ S)

Left(i) = S + (2b - 1) * j + b
Right(i) = T + 1 - Left(i)

where:
j = i - 1 (0ベースインデックス)
b = j mod 2 (奇偶判定)
```

## 📁 プロジェクト構造

```
a3-pdf-splitter/
├── app.py                 # Flaskアプリケーション
├── requirements.txt       # Python依存関係
├── README.md             # このファイル
├── static/
│   ├── style.css         # スタイルシート
│   ├── manifest.json     # PWAマニフェスト
│   ├── sw.js            # サービスワーカー
│   └── icons/           # PWAアイコン
├── templates/
│   └── index.html       # メインページテンプレート
├── scripts/             # コマンドライン版スクリプト
│   ├── pdf_a3_to_a4.py            # Phase1 CLI
│   └── phase2_booklet_splitter.py # Phase2 CLI
└── tests/              # テストファイル
```

## 🧪 テスト

### コマンドライン版のテスト

```bash
# Phase 1 (シンプル分割)
python scripts/pdf_a3_to_a4.py sample.pdf

# Phase 2 (製本復元)
python scripts/phase2_booklet_splitter.py --pages 32 booklet.pdf

# 数式検証
python scripts/phase2_booklet_splitter.py --verify
```

### Webアプリケーションのテスト

```bash
# 開発サーバー起動
python app.py

# ブラウザでテスト
# http://127.0.0.1:5000
```

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. Pull Requestを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🙏 謝辞

- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF処理ライブラリ
- [Flask](https://flask.palletsprojects.com/) - Webフレームワーク
- [Claude Code](https://claude.ai/code) - 開発支援AI

## 📧 お問い合わせ

プロジェクトに関する質問や提案がありましたら、[Issues](https://github.com/yourusername/a3-pdf-splitter/issues)でお知らせください。

---

**🤖 Generated with [Claude Code](https://claude.ai/code)**

**Co-Authored-By: Claude <noreply@anthropic.com>**