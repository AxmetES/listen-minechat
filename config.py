from environs import Env

env = Env()
env.read_env()


class Settings:
    # FILENAME = 'chat_log.txt'
    CACHE_NAME = env("CACHE_NAME")
    CACHE_PORT = env("CACHE_PORT")
    CACHE_HOST = env("CACHE_HOST")
    HOST = env("HOST")
    PORT = env("PORT")
    FILENAME = env.str("FILENAME")
    NICKNAME = env.str("NICKNAME")


settings = Settings()
