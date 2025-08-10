import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings, SecretStr

load_dotenv()


class BotSettings(BaseSettings):
    token: SecretStr = os.getenv("BOT_TOKEN", None)


class KpoiskSettings(BaseSettings):
    api: SecretStr = os.getenv("KPOISK_API_KEY", None)
