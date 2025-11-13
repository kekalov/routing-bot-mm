# 🧪 Тестирование роутинга локально

## Быстрый тест без LLM

Для проверки базовой функциональности без настройки LLM:

```bash
python3 test_routing.py "Помогите с SQL запросом"
```

Скрипт покажет:
- Промпт, который будет отправлен в LLM
- Результат классификации (заглушка, если LLM не настроен)
- Форматированный ответ

## Тестирование с реальным LLM

### Шаг 1: Настройте переменные окружения

Создайте файл `.env` из шаблона:
```bash
cp .env.template .env
```

Заполните параметры вашего LLM провайдера:
```bash
LLM_API_KEY=your-api-key-here
LLM_API_BASE_URL=https://api.your-llm-provider.com/v1
LLM_MODEL_NAME=your-model-name
```

### Шаг 2: Раскомментируйте код в `src/bot.py`

Откройте `src/bot.py` и в функции `classify_message()` раскомментируйте один из примеров:

**Для REST API провайдера:**
```python
from your_llm_library import Client  # замените на библиотеку вашего провайдера

client = Client(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_API_BASE_URL", "https://api.your-llm-provider.com/v1")
)
resp = client.chat.completions.create(
    model=os.getenv("LLM_MODEL_NAME", "your-model-name"),
    messages=[{"role": "user", "content": prompt}],
    temperature=0.1,
    max_tokens=450,
)
content = resp.choices[0].message.content
```

**Для собственного HTTP API:**
```python
import requests
response = requests.post(
    os.getenv("LLM_API_URL"),
    headers={"Authorization": f"Bearer {os.getenv('LLM_API_KEY')}"},
    json={"prompt": prompt, "temperature": 0.1, "max_tokens": 450}
)
content = response.json()["text"]
```

Закомментируйте строку с заглушкой:
```python
# content = '{"topic": "Other", ...}'
```

### Шаг 3: Запустите тест

```bash
python3 test_routing.py "Помогите с SQL запросом"
```

Или в интерактивном режиме:
```bash
python3 test_routing.py
```

## Примеры тестовых сообщений

```bash
# SQL запрос
python3 test_routing.py "Помогите с SQL запросом для аналитики продаж"

# A/B тест
python3 test_routing.py "Нужна помощь с A/B тестом для новой функции"

# Маркетинг
python3 test_routing.py "Вопрос по маркетинговой кампании"

# Fraud
python3 test_routing.py "Проблема с оплатой и подозрительными транзакциями"
```

## Что проверяется

- ✅ Генерация промпта из `evaluation/prompt.txt`
- ✅ Отправка запроса в LLM
- ✅ Парсинг JSON ответа
- ✅ Fallback парсер (если LLM вернул текст вместо JSON)
- ✅ Форматирование ответа для мессенджера

## Устранение проблем

**Ошибка "LLM не настроен":**
- Проверьте, что `.env` файл создан и заполнен
- Убедитесь, что код в `classify_message()` раскомментирован
- Проверьте правильность переменных окружения

**Ошибка подключения к LLM:**
- Проверьте `LLM_API_KEY` и `LLM_API_BASE_URL`
- Убедитесь, что API доступен из вашей сети
- Проверьте формат запроса в коде

**Некорректный JSON:**
- Скрипт автоматически использует fallback парсер
- Проверьте промпт в `evaluation/prompt.txt` - он должен требовать строгий JSON

