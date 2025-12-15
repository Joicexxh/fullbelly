from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

load_dotenv()  # Carrega o .env

# -------------------------------
# BASE
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-temp-key")

DEBUG = os.environ.get("DEBUG", "False") == "True"  # Controla o DEBUG via variável de ambiente

ALLOWED_HOSTS = [
    "fullbellyy.onrender.com",  # Adicione o domínio de produção
    "localhost",  # Para rodar localmente
    "127.0.0.1",  # Para rodar localmente
]

# -------------------------------
# APPS INSTALADOS
# -------------------------------
INSTALLED_APPS = [
    # Django padrão
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps do projeto
    "core",  # Seu app principal

    # CORS
    "corsheaders",
]

# -------------------------------
# MIDDLEWARE
# -------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Deve ser o primeiro
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------------
# URLS & WSGI
# -------------------------------
ROOT_URLCONF = "fullbelly.urls"
WSGI_APPLICATION = "fullbelly.wsgi.application"

# -------------------------------
# TEMPLATES
# -------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Defina os diretórios de templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# -------------------------------
# DATABASE
# -------------------------------
DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get(
            "DATABASE_URL",
            "postgresql://fullbelly_user:LGjXX7iBWNDkrxHHTiN0adYc1j7AWi1Z@dpg-d506nvdactks73fgqee0-a.oregon-postgres.render.com/fullbelly_db"
        ),
        conn_max_age=600,  # Conexões persistentes para melhorar a performance
    )
}

# -------------------------------
# PASSWORD VALIDATION
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------
# INTERNATIONALIZATION
# -------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# -------------------------------
# STATIC FILES
# -------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # Pasta para arquivos estáticos em produção

# -------------------------------
# CORS / FRONT-END
# -------------------------------
CORS_ALLOWED_ORIGINS = [
    "https://fullbelly-front.vercel.app",  # Seu front-end hospedado
]

# -------------------------------
# PRODUÇÃO / SEGURANÇA
# -------------------------------
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS = [
    "https://fullbellyy.onrender.com",  # URL do seu back-end
    "https://fullbelly-front.vercel.app",  # Front-end no Vercel
]

# -------------------------------
# LOGGING
# -------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',  # Ajuste o nível de log conforme necessário
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Nível de logs
            'propagate': True,
        },
    },
}

# -------------------------------
# DEFAULT AUTO FIELD
# -------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------
# OUTRAS CONFIGURAÇÕES (por exemplo, para produção)
# -------------------------------
# Para produção, recomendamos desabilitar o DEBUG
# DEBUG = os.environ.get("DEBUG", "False") == "True"
