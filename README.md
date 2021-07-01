# mosq

- バックエンド
  - Django
  - Django REST framework
- フロントエンド
  - Create React App
  - axios
  - React Hook Form
  - React Router
  - Material-UI

## git clone 後にやること

### バックエンド

```
pip install -r reuirements.txt
cd config
python generate_secretkey_setting.py > local_settings.py
cd ..
python manage.py migrate
python manage.py import_questions
python manage.py loaddata api_printtype.json
```
