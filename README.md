# Serverless MCP IaC Documentation Server

AWS Lambda上で動作するMCP (Model Context Protocol) サーバーです。Infrastructure as Code (IaC) のドキュメントをAIエージェントに提供します。

## 機能

- IaC開発ガイドラインの提供
- Terraformモジュールテンプレートの配信
- リソース固有のルール検索
- キーワード検索機能

## アーキテクチャ

- **AWS Lambda**: Python 3.13ランタイム（ARM64）
- **API Gateway**: RESTful API エンドポイント
- **Lambda Web Adapter**: HTTP サーバーサポート
- **FastMCP**: MCP プロトコル実装

## 利用可能なツール

| ツール名 | 説明 |
|---------|------|
| `list_documents` | 利用可能なドキュメント一覧を取得 |
| `get_document` | 特定のドキュメントを名前で取得 |
| `get_development_guidelines` | 開発ガイドラインを取得 |
| `get_module_code_template` | モジュールコードテンプレートを取得 |
| `get_module_requirements` | モジュール要件仕様を取得 |
| `get_module_specification_template` | モジュール仕様テンプレートを取得 |
| `get_task_process` | 標準タスクプロセスを取得 |
| `get_resource_specification` | リソース固有のルールを取得 |
| `search_guidelines` | キーワードでガイドラインを検索 |

## セットアップ

### 前提条件

- AWS CLI設定済み
- AWS SAM CLIインストール済み
- Python 3.13

### インストール

```bash
# 依存関係のインストール
make install

# SAMアプリケーションのビルド
make build
```

### デプロイ

初回デプロイ:
```bash
make deploy-guided
```

以降のデプロイ:
```bash
make deploy
```

### ローカル開発

```bash
# SAM Localで実行
make local

# 直接実行
make run
```

## 使用方法

デプロイ後、API GatewayのエンドポイントURLが表示されます。

### 例: ドキュメント一覧の取得

```bash
curl -X POST https://your-api-id.execute-api.region.amazonaws.com/dev/mcp/tools/list_documents \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 例: 開発ガイドラインの取得

```bash
curl -X POST https://your-api-id.execute-api.region.amazonaws.com/dev/mcp/tools/get_development_guidelines \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 設定

`samconfig.toml.example`をコピーして`samconfig.toml`を作成し、必要に応じて設定を変更してください。

```bash
cp samconfig.toml.example samconfig.toml
```

## トラブルシューティング

### ログの確認

```bash
make logs
```

### テンプレートの検証

```bash
make validate
```

## ライセンス

このプロジェクトは親プロジェクトのライセンスに従います。