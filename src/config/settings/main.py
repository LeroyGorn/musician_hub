from config.settings.base import *

load_dotenv()  # noqa:

DEBUG = False


ALLOWED_HOSTS = [
    "localhost",
    "ec2-18-133-230-219.eu-west-2.compute.amazonaws.com",
]

CURRENT_ENV = "MAIN"
print(CURRENT_ENV)

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


DATABASES = {
    "default_pg": {
        "ENGINE": "django.db.backends.postgresql",  # noqa:
        "NAME": os.getenv("POSTGRES_DB"),  # noqa:POSTGRES_PASSWORD=admin
        "USER": os.getenv("POSTGRES_USER"),  # noqa:
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),  # noqa:
        "HOST": os.getenv("POSTGRES_HOST"),  # noqa:
        "PORT": os.getenv("POSTGRES_PORT"),  # noqa:
    },
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa:
    },
}
