# Python・Django学習用 ToDoアプリ

タスクの追加、一覧表示、完了切替、削除ができる小さなDjangoアプリです。

## 必要なもの

Docker Desktopなど、`docker compose` を実行できる環境だけを使います。
ホストへPython、Django、仮想環境をインストールする必要はありません。

## 起動方法

```bash
docker compose up --build
```

ブラウザで <http://127.0.0.1:8000/> を開きます。終了はターミナルで
`Ctrl+C` です。バックグラウンドで起動する場合は次を使います。

```bash
docker compose up --build -d
docker compose logs -f web
docker compose down
```

テストの実行:

```bash
docker compose run --rm web python manage.py test
```

Pythonの対話画面やDjango shellもコンテナ内で実行します。

```bash
docker compose run --rm web python
docker compose run --rm web python manage.py shell
```

依存パッケージはDockerイメージ、SQLiteデータは `django_data` という名前付き
ボリュームに保存されます。通常の `docker compose down` では学習データを保持します。
データも消して完全に初期化したい場合だけ `docker compose down -v` を実行します。

教材は [TEXTBOOK.md](TEXTBOOK.md) です。
