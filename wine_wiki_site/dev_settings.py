from .settings import *  # noqa

ALLOWED_HOSTS.append("127.0.0.1")

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "dev_db" / "db.sqlite3",
    }
}
