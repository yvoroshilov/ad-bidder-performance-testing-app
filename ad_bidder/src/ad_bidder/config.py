from starlette.config import Config

config = Config(".env")

LOG_LEVEL = config("LOG_LEVEL", default="ERROR")
DEBUG = config("DEBUG", default=False, cast=bool)
