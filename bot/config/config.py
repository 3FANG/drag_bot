from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str

@dataclass
class Config:
    tg_bot: TgBot
    admin_ids: list[str] | str

def load_environment():
    env = Env()
    env.read_env()
    return env

def load_config():
    env = load_environment()
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')), admin_ids=env.list('ADMIN_IDS'))
