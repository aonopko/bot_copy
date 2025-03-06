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
            return f"""Напиши привлекательный пост для социальной сети на тему: {topic}.
            Пост должен быть на русском языке и соответствовать следующим критериям:
            - Захватывающее вступление, которое привлекает внимание
            - Интересные факты или уникальная информация по теме
            - Эмоциональная вовлеченность читателя
            - Четкая структура с абзацами
            - Призыв к действию в конце
            - Использование эмодзи для лучшего восприятия
            - Длина 1000-1500 символов"""
        return f"""Напиши привабливий пост для соціальної мережі на тему: {topic}.
        Пост повинен бути українською мовою та відповідати наступним критеріям:
        - Захоплюючий вступ, який привертає увагу
        - Цікаві факти або унікальна інформація за темою
        - Емоційна залученість читача
        - Чітка структура з абзацами
        - Заклик до дії наприкінці
        - Використання емодзі для кращого сприйняття
        - Довжина 1000-1500 символів""" 