import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

    @staticmethod
    def validate():
        if not all([Config.BOT_TOKEN, Config.CHANNEL_ID, Config.CLAUDE_API_KEY]):
            raise ValueError("Отсутствуют необходимые переменные окружения") 