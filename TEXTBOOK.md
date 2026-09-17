# PythonとDjango 入門テキスト

この教材のゴールは、Pythonの基本を思い出しながら、Webアプリがリクエストを
受け取ってデータを保存し、HTMLを返す流れを説明できるようになることです。
まずREADMEのDocker手順でアプリを起動し、動作を確認してください。この教材の
コマンドはすべてコンテナ内で動かすため、ホストへPythonパッケージを入れません。

## 0. このアプリで学べること

- Python: 標準出力、変数、型、条件分岐、繰り返し、関数、クラス
- Django: プロジェクトとアプリ、URL、ビュー、テンプレート、モデル、フォーム
- Web: GETとPOST、リダイレクト、CSRF、ステータスコード
- 開発: マイグレーション、管理画面、自動テスト

処理の流れは次の通りです。

```text
ブラウザ → config/urls.py → tasks/urls.py → tasks/views.py
                                         ├→ tasks/models.py → SQLite
                                         └→ HTMLテンプレート → ブラウザ
```

## 1. Pythonを思い出す

### 標準出力

Pythonで文字を標準出力（通常はターミナル）へ表示するには `print()` を使います。

```python
print("Hello, Python!")

name = "太郎"
count = 3
print(name)
print(f"{name}さんのタスクは{count}件です")
```

`f"..."` の中では、波括弧に変数や式を書けます。試すには次を実行します。

```bash
docker compose run --rm web python
```

対話画面に `print("Hello!")` と入力します。終了は `exit()` です。

### 値と型

```python
title = "Djangoを学ぶ"  # str（文字列）
priority = 2           # int（整数）
is_done = False        # bool（真偽値）
tags = ["Python", "Web"]  # list（リスト）

print(type(title))
print(len(tags))
```

### 条件分岐と繰り返し

Pythonでは波括弧ではなく、コロンとインデントが処理のまとまりを表します。

```python
tasks = ["Pythonを復習", "Djangoを起動", "テストを書く"]

for task in tasks:
    if task == "Djangoを起動":
        print(f"重要: {task}")
    else:
        print(task)
```

### 関数

```python
def task_message(title, is_done=False):
    status = "完了" if is_done else "未完了"
    return f"[{status}] {title}"


print(task_message("モデルを学ぶ"))
print(task_message("標準出力を学ぶ", True))
```

`print()` は画面に表示し、`return` は呼び出し元へ値を返します。この違いは重要です。
Djangoのビューも最後にレスポンスを `return` します。

### クラス

```python
class SimpleTask:
    def __init__(self, title):
        self.title = title
        self.is_done = False

    def complete(self):
        self.is_done = True


task = SimpleTask("クラスを学ぶ")
task.complete()
print(task.title, task.is_done)
```

Djangoのモデルやフォームもクラスとして定義します。

## 2. Djangoの全体像

Djangoでは「プロジェクト」がサイト全体、「アプリ」が特定機能を表します。

- `config/`: サイト全体の設定と最上位URL
- `tasks/`: ToDo機能を担当するDjangoアプリ
- `templates/`: 共通HTML
- `static/`: CSSなど、そのまま配信するファイル
- `manage.py`: 開発サーバーやテストなどを実行する入口
- `Dockerfile`: PythonとDjangoを含むイメージの作り方
- `compose.yaml`: Webコンテナ、ポート、データ領域の定義
- `django_data`: Dockerが管理するSQLite用の名前付きボリューム

## 3. コードをリクエスト順に読む

### URL: どの処理を呼ぶか

`config/urls.py` は空パスの処理を `tasks.urls` に任せます。
`tasks/urls.py` はURLとビューを対応づけます。

```python
path("", views.task_list, name="list")
path("<int:pk>/toggle/", views.task_toggle, name="toggle")
```

`pk` はデータを一意に識別する主キーです。たとえば `/3/toggle/` の `3` が
ビューの `pk` 引数に渡ります。

### ビュー: リクエストを処理する

`tasks/views.py` の `task_list` を読んでください。

- GETなら空のフォームとタスク一覧をHTMLに渡す
- POSTなら送信値をフォームで検証して保存する
- 保存後は一覧へリダイレクトする

保存後のリダイレクトは、ブラウザの再読み込みによる二重登録を防ぎます。

### モデル: データの形を定義する

`tasks/models.py` の `Task` はデータベースの表に対応します。

- `CharField`: 長さに上限のある文字列
- `BooleanField`: 真偽値
- `DateTimeField`: 日時
- `objects`: 検索や保存に使うマネージャー

モデルを変更したら次の2段階を実行します。

```bash
docker compose run --rm web python manage.py makemigrations
docker compose run --rm web python manage.py migrate
```

前者は変更手順のファイルを作り、後者はデータベースに適用します。

### フォーム: 入力を検証する

`tasks/forms.py` の `ModelForm` はモデルから入力欄と検証規則を作ります。
タイトルが空、または101文字以上なら `is_valid()` は偽になり保存されません。

### テンプレート: HTMLを組み立てる

`tasks/templates/tasks/task_list.html` ではDjangoテンプレート構文を使います。

```django
{{ task.title }}
{% for task in tasks %}
{% url 'tasks:toggle' task.pk %}
```

`{{ ... }}` は値の表示、`{% ... %}` は繰り返しなどの処理です。POSTフォームに
`{% csrf_token %}` を置くことで、別サイトから勝手に操作される攻撃を防ぎます。

## 4. Django shellでデータを操作する

```bash
docker compose run --rm web python manage.py shell
```

```python
from tasks.models import Task

task = Task.objects.create(title="shellから作成")
print(task.id)
print(Task.objects.all())

task.is_done = True
task.save()
print(Task.objects.filter(is_done=True))
```

練習後に `task.delete()` を実行すれば、この1件を削除できます。

## 5. 管理画面

管理ユーザーを作ります。

```bash
docker compose run --rm web python manage.py createsuperuser
docker compose up
```

<http://127.0.0.1:8000/admin/> にログインしてください。`tasks/admin.py` に
登録した設定によって、Taskの検索や絞り込みができます。

## 6. テスト

`tasks/tests.py` は一時的なテスト専用DBを使います。

```bash
docker compose run --rm web python manage.py test
```

テスト名は「何を期待しているか」が分かる文章にします。失敗を体験するには、
一時的に期待値を逆にして実行し、エラーを読んでから元に戻してみましょう。

## 7. おすすめ学習順

1. アプリを起動し、追加・完了・削除を試す
2. `tasks/models.py` と `tasks/views.py` に `print()` を置き、いつ表示されるか観察
3. Django shellからデータを作成・検索・更新する
4. テストを1つずつ読み、自分でテストケースを追加する
5. 下の演習を順番に実装する

開発中の `print()` はターミナルに表示されます。ブラウザには表示されない点に
注意してください。確認が終わったデバッグ出力は削除します。

## 8. 演習

### 初級: 詳細メモを追加

1. `Task` に `description = models.TextField(blank=True)` を追加
2. マイグレーションを作成・適用
3. フォームの `fields` に `description` を追加
4. テンプレートで表示
5. 保存テストを追加

### 中級: 未完了だけ表示

`?status=open` が付いた場合に、ビューで次の絞り込みを行います。

```python
if request.GET.get("status") == "open":
    tasks = tasks.filter(is_done=False)
```

一覧に「すべて」「未完了」のリンクを追加し、テストも書いてください。

### 発展: 期限を追加

`DateField` を使って期限を持たせ、期限切れのタスクにCSSで警告色を付けます。
「期限未入力を許すか」「並び順をどうするか」も自分で決めてみましょう。

## 9. つまずいたときの見方

- `docker: command not found`: Docker Desktopなどをインストールして起動
- `ModuleNotFoundError`: `docker compose build --no-cache` でイメージを再構築
- `no such table`: `docker compose run --rm web python manage.py migrate` を実行
- `TemplateDoesNotExist`: テンプレートのパスとファイル名を確認
- `NoReverseMatch`: URLの名前や必要な `pk` を確認
- `403 CSRF`: POSTフォーム内の `{% csrf_token %}` を確認
- `IndentationError`: インデント幅が揃っているか確認

エラー画面では、まず例外名と一番下に近い自作ファイルの行を読みます。
一度に複数箇所を直さず、1箇所直したら再実行するのが近道です。

## 10. 次に学ぶテーマ

このアプリを理解できたら、ユーザー認証、ユーザーごとのデータ分離、
クラスベースビュー、デプロイ、本番用の環境変数・セキュリティ設定へ進みます。
