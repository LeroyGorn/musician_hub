from config.settings.base import *

DEBUG = True

CURRENT_ENV = "DEV"
print(CURRENT_ENV)

load_dotenv()  # noqa:
if os.environ.get("GITHUB_WORKFLOW"):  # noqa:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        },
    }
else:
    DATABASES = {
        # "default": {
        #     "ENGINE": "django.db.backends.postgresql",
        #     "NAME": os.getenv("POSTGRES_DB"),
        #     "USER": os.getenv("POSTGRES_USER"),
        #     "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        #     "HOST": os.getenv("POSTGRES_HOST"),
        #     "PORT": os.getenv("POSTGRES_PORT"),
        # },
        # "default": {
        #     "ENGINE": "django.db.backends.postgresql",
        #     "NAME": "mushub",
        #     "USER": "postgres",
        #     "PASSWORD": "110802",
        #     "HOST": "localhost",
        #     "PORT": "5432",
        # },
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa:
        },
    }
