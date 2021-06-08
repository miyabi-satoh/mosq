from django.core.management.utils import get_random_secret_key

"""
SECRET_KEYを生成する
https://qiita.com/haessal/items/abaef7ee4fdbd3b218f5

python generate_secretkey_setting.py > local_settings.py
"""
secret_key = get_random_secret_key()
text = 'SECRET_KEY = \'{0}\''.format(secret_key)
print(text)
