import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
    
    # Получаем username канала для кнопки подписки
    @staticmethod
    def get_channel_link():
        channel_id = Config.CHANNEL_ID
        if channel_id.startswith('-100'):
            return f"https://t.me/c/{channel_id[4:]}"
        elif channel_id.startswith('@'):
            return f"https://t.me/{channel_id[1:]}"
        return f"https://t.me/c/{channel_id}"

    @staticmethod
    def validate():
        if not all([Config.BOT_TOKEN, Config.CHANNEL_ID, Config.CLAUDE_API_KEY]):
            raise ValueError("Отсутствуют необходимые переменные окружения") 