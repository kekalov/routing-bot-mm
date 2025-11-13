import os, json, re, logging
from pathlib import Path
from dotenv import load_dotenv

# Импорты для работы с корпоративным мессенджером
# ПРИМЕР: Используется библиотека slack-bolt для одного из мессенджеров
# Адаптируйте импорты под ваш мессенджер (Telegram Bot API, VK Teams, и др.)
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_prompt(user_text: str) -> str:
    prompt_path = Path(__file__).resolve().parents[1] / "evaluation" / "prompt.txt"
    system_prompt = (
        prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else "Return JSON only."
    )
    return f"{system_prompt}\n\nNow classify this message:\n{user_text}"


def parse_text_fallback(content: str) -> dict:
    def extract(key: str) -> str:
        m = re.search(rf"{key}:\s*(.*)", content, re.IGNORECASE)
        return m.group(1).strip() if m else "N/A"

    return {
        "topic": extract("Topic"),
        "analyst": extract("Analyst"),
        "channel": extract("Channel"),
        "reason": extract("Reason") if re.search(r"Reason:\s*", content, re.IGNORECASE) else "No reason provided",
    }


def classify_message(user_text: str) -> dict:
    """
    Классифицирует сообщение через LLM провайдер.
    Адаптируйте код под ваш LLM провайдер (любой с REST API или собственный).
    """
    prompt = get_prompt(user_text)
    try:
        # Пример 1: LLM провайдер с REST API (стандартный формат запросов)
        # Раскомментируйте и адаптируйте под ваш провайдер:
        # from your_llm_library import Client  # используйте библиотеку вашего провайдера
        # 
        # client = Client(
        #     api_key=os.getenv("LLM_API_KEY"),
        #     base_url=os.getenv("LLM_API_BASE_URL", "https://api.your-llm-provider.com/v1")
        # )
        # resp = client.chat.completions.create(
        #     model=os.getenv("LLM_MODEL_NAME", "your-model-name"),
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=0.1,
        #     max_tokens=450,
        # )
        # content = resp.choices[0].message.content
        
        # Пример 2: Собственный HTTP API для LLM
        # import requests
        # response = requests.post(
        #     os.getenv("LLM_API_URL"),
        #     headers={"Authorization": f"Bearer {os.getenv('LLM_API_KEY')}"},
        #     json={"prompt": prompt, "temperature": 0.1, "max_tokens": 450}
        # )
        # content = response.json()["text"]
        
        # ВАЖНО: Раскомментируйте один из примеров выше и адаптируйте под ваш LLM провайдер
        # Для демо-режима возвращаем заглушку:
        content = '{"topic": "Other", "analyst": "N/A", "channel": "N/A", "reason": "LLM не настроен. Раскомментируйте код в classify_message()"}'
        
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning("JSON parse failed, using text fallback")
            return parse_text_fallback(content)
    except Exception as e:
        logger.exception("LLM error")
        return {"topic": "Other", "analyst": "N/A", "channel": "N/A", "reason": f"Error: {e}"}


# ============================================================================
# НАСТРОЙКА БОТА ДЛЯ КОРПОРАТИВНОГО МЕССЕНДЖЕРА
# ============================================================================
# ПРИМЕР: Используется библиотека slack-bolt для одного из мессенджеров
# Адаптируйте код под ваш мессенджер (Telegram Bot API, VK Teams, и др.)
# Замените App и SocketModeHandler на соответствующие классы вашего мессенджера

def create_bot_app():
    """Создает и настраивает бота. Вызывается только при запуске бота."""
    app = App(token=os.getenv("BOT_TOKEN"))

    @app.event("app_mention")
    def handle_app_mention(event, say, ack):
        """
        Обработчик упоминания бота в корпоративном мессенджере.
        Адаптируйте под API вашего мессенджера.
        """
        ack()
        text = event.get("text", "").strip()
        result = classify_message(text)
        say(
            text=(
                "🧠 Classification Result\n"
                f"Topic: {result.get('topic', 'N/A')}\n"
                f"Analyst: {result.get('analyst', 'N/A')}\n"
                f"Channel: {result.get('channel', 'N/A')}\n"
                f"Reason: {result.get('reason', 'N/A')}"
            ),
            thread_ts=event.get("ts"),
        )
    
    return app


if __name__ == "__main__":
    # Адаптируйте запуск бота под ваш мессенджер
    app = create_bot_app()
    handler = SocketModeHandler(app, os.getenv("APP_TOKEN"))
    handler.start()
