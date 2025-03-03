from anthropic import Anthropic
from config.config import Config

class ClaudeService:
    def __init__(self, api_key: str):
        self.claude = Anthropic(api_key=api_key)

    async def generate_post(self, topic: str, language: str) -> str:
        prompt = self._get_prompt(topic, language)
        response = self.claude.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def _get_prompt(self, topic: str, language: str) -> str:
        if language == 'ru':
            return f"Напиши привлекательный пост для социальной сети на тему: {topic}. Пост должен быть на русском языке."
        return f"Напиши привабливий пост для соціальної мережі на тему: {topic}. Пост повинен бути українською мовою." 