from decouple import config

if config('FLASK_ENV') == 'development':
    DEBUG = True
else:
    DEBUG = False

DEBUG = True

SECRET_KEY = config('SECRET_KEY')