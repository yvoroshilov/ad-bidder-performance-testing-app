from starlette.config import Config

config = Config(".env")

LOG_LEVEL = config("LOG_LEVEL", default="ERROR")
DEBUG = config("DEBUG", default=False, cast=bool)
MONGODB_USERNAME = config("MONGODB_USERNAME")
MONGODB_PASSWORD = config("MONGODB_PASSWORD")
MONGODB_HOST = config("MONGODB_HOST")
MONGODB_DB_NAME = config("MONGODB_DB_NAME")
