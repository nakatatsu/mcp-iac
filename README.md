# MCP IaC Documentation Server

MCP (Model Context Protocol) サーバーです。Infrastructure as Code (IaC) のドキュメントをAIエージェントに提供します。

## 機能

- IaC開発ガイドラインの提供
- Terraformモジュールテンプレートの配信
- リソース固有のルール検索
- キーワード検索機能

## アーキテクチャ

- **FastMCP**: MCP プロトコル実装
- **Python 3.13**: アプリケーションランタイム
- **Terraform**: インフラストラクチャデプロイ

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

- Python 3.13
- Terraform（インフラストラクチャデプロイ用）

### インストール

```bash
# 依存関係のインストール
make install
```

### ローカル開発

```bash
# 直接実行
make run

# スクリプトを使って実行（デフォルトポート: 8000）
make local

# スクリプトを使って実行（ポート指定）
./scripts/local.sh 8080
```

### デプロイ・更新

```bash
# Lambda関数の更新（環境名を指定）
ENVIRONMENT=development make update

# または直接スクリプトを実行
./scripts/update.sh development
```

## 使用方法

デプロイ後、APIエンドポイントが利用可能になります。

### 例: ドキュメント一覧の取得

```bash
curl -X POST ${API_URL}/mcp/tools/list_documents \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 例: 開発ガイドラインの取得

```bash
curl -X POST ${API_URL}/mcp/tools/get_development_guidelines \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 設定

ドキュメントファイルは以下のディレクトリに配置してください：

- `documents/` - 一般的なドキュメント（YAML形式）
- `resouces_specification/` - リソース固有の仕様（YAML形式）

## テスト

```bash
# APIのテスト（API_URL環境変数が必要）
make test-api
```

## ライセンス

このプロジェクトは親プロジェクトのライセンスに従います。