
import os

from flask.cli import load_dotenv


class EnvConifg:
    PRIVATE_GROUP_ID: str = os.getenv('PRIVATE_GROUP_ID')
    LINE_ACCESS_TOKEN: str = os.getenv('LINE_ACCESS_TOKEN')
    LINE_SECRET: str = os.getenv('LINE_SECRET')
    LINE_NOTIFY_TOKEN: str = os.getenv('LINE_NOTIFY_TOKEN')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER: str = os.getenv('POSTGRES_SERVER')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')

    def get_db_connection(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"


# load .env file
load_dotenv()
env_config = EnvConifg()
