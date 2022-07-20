from config.settings.base import *

DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
]

CURRENT_ENV = "STAGE"
print(CURRENT_ENV)

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

load_dotenv()  # noqa:

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # noqa:
        "NAME": os.getenv("POSTGRES_DB"),  # noqa:
        "USER": os.getenv("POSTGRES_USER"),  # noqa:
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),  # noqa:
        "HOST": os.getenv("POSTGRES_HOST"),  # noqa:
        "PORT": os.getenv("POSTGRES_PORT"),  # noqa:
    },
}
