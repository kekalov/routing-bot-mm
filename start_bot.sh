#!/bin/bash
# 🚦 Стартовый скрипт для AnalytiQA (template)
# Для локального запуска и быстрой проверки

set -e

echo "🤖 Запуск AnalytiQA Template..."
echo "=================================="

if [ ! -d ".venv" ]; then
    echo "📦 Виртуальное окружение не найдено, создаём..."
    python3 -m venv .venv
fi

source .venv/bin/activate

if [ -f requirements.txt ]; then
    echo "🔧 Устанавливаем зависимости..."
    pip install -r requirements.txt
fi

# 👉 Здесь стартуйте свой ENTRYPOINT, например: python src/bot.py
# Сейчас бот не стартует, т.к. это шаблон. Дальше — по вашей инструкции.

echo "✅ Всё готово! Настройте src/, добавьте promt.txt и логику — потом запускайте свой bot."

python src/bot.py
