import os
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY ', 'teste')
DOCKER_IP = os.environ.get('DOCKER_IP', 'localhost')
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'mega'),
        'USER': os.environ.get('DB_USER', 'mega'),
        'HOST': os.environ.get('DB_HOST', DOCKER_IP),
        'PORT': os.environ.get('DB_HOST_PORT', '5432'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'TEST': {
            'NAME': 'mytestdatabase',
        },
    }
}