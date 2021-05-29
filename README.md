# react-django-boilerplate

- バックエンド
  - Django REST framework : https://www.django-rest-framework.org/
- フロントエンド
  - Create React App : https://create-react-app.dev/

同一オリジンで動かす設定をしたテンプレ。

## Django プロジェクトを作成

https://docs.djangoproject.com/ja/3.2/intro/tutorial01/<br>
https://qiita.com/okoppe8/items/6227d753185fccf21c75

```
django-admin startproject config .
```

カレントディレクトリ(.)を指定することで、
プロジェクト全体に関する設定が config ディレクトリに作成される。

### .gitignore を作成

https://www.toptal.com/developers/gitignore/api/django,macos,react

### .editorconfig を作成

### SECRET_KEY を git 管理外に

https://qiita.com/haessal/items/abaef7ee4fdbd3b218f5

## api アプリケーションを作成

https://docs.djangoproject.com/ja/3.2/intro/tutorial01/

```
python manage.py startapp api
```

### DRF を INSTALLED_APPS に追加

https://www.django-rest-framework.org/tutorial/quickstart/

### hello API を作成

https://www.django-rest-framework.org/tutorial/3-class-based-views/

### migrate

```
python manage.py migrate
```

## frontend アプリケーションを作成

```
python manage.py startapp frontend
```

### create-react-app

適当な場所で React アプリケーションを作成して、frontend にコピー<br>
※node_modules はコピーしない

```
npx create-react-app my-app --template typescript
cd my-app
mv .gitignore README.md package* public src tsconfig.json ../frontend
```

とりあえず build。

```
npm install
npm run build
```

### Django 側の設定変更

TEMPLATES.DIR に BASE_DIR/frontend/build を指定。<br>
https://kokiblog.com/2019/08/19/templates_dir/

STATICFILES_DIRS に BASE_DIR/frontend/build/static を指定。<br>
https://noumenon-th.net/programming/2019/10/29/django-static/

URL を設定
https://qiita.com/sand/items/15da91117c680a618c2b

### 表示確認

http://localhost:8000/ で React の初期ページが表示された。

### 不要ファイルの削除

https://absarcs.info/how-to/minimize-react-app/

```
[frontend/public]
rm favicon.ico logo* manifest.json robots.txt

[frontend/src]
rm App.css App.test.tsx index.css logo.svg reportWebVitals.ts setupTests.ts
```

#### ファイル修正

- App.tsx
- index.tsx
- index.html

## hello API のテスト

### frontend

axios をインストール。

```
npm install axios
```

Django への proxy を設定。<br>
https://qiita.com/geekduck/items/6f99a3da15dd39658fff
