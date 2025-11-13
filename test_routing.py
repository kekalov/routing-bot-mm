#!/usr/bin/env python3
"""
Тестовый скрипт для локального тестирования роутинга без запуска бота.
Использует функции из src/bot.py для классификации сообщений.
"""

import sys
import os
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent / "src"))

from bot import classify_message, get_prompt, parse_text_fallback


def test_routing(message: str):
    """
    Тестирует классификацию сообщения.
    
    Args:
        message: Текст сообщения для классификации
    """
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ РОУТИНГА")
    print("=" * 60)
    print()
    print(f"Входящее сообщение: \"{message}\"")
    print()
    
    # Показываем промпт
    prompt = get_prompt(message)
    print("Промпт для LLM:")
    print("-" * 60)
    print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
    print("-" * 60)
    print()
    
    # Классификация
    print("Классификация...")
    try:
        result = classify_message(message)
        print()
        print("✅ Результат классификации:")
        print("-" * 60)
        print(f"Topic:    {result.get('topic', 'N/A')}")
        print(f"Analyst:  {result.get('analyst', 'N/A')}")
        print(f"Channel:  {result.get('channel', 'N/A')}")
        print(f"Reason:   {result.get('reason', 'N/A')}")
        print("-" * 60)
        print()
        
        # Форматированный ответ (как в боте)
        response = (
            "🧠 Classification Result\n"
            f"Topic: {result.get('topic', 'N/A')}\n"
            f"Analyst: {result.get('analyst', 'N/A')}\n"
            f"Channel: {result.get('channel', 'N/A')}\n"
            f"Reason: {result.get('reason', 'N/A')}"
        )
        print("Форматированный ответ (как отправит бот):")
        print("-" * 60)
        print(response)
        print("-" * 60)
        
        return result
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Основная функция для интерактивного тестирования."""
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ РОУТИНГА ANALYTIQA")
    print("=" * 60)
    print()
    
    # Проверка переменных окружения
    print("Проверка настроек...")
    llm_key = os.getenv("LLM_API_KEY")
    llm_url = os.getenv("LLM_API_BASE_URL")
    llm_model = os.getenv("LLM_MODEL_NAME")
    
    if not llm_key:
        print("⚠️  LLM_API_KEY не установлен в .env")
        print("   Скрипт будет использовать заглушку")
        print("   Для реального тестирования:")
        print("   1. Создайте .env файл из .env.template")
        print("   2. Заполните LLM_API_KEY, LLM_API_BASE_URL, LLM_MODEL_NAME")
        print("   3. Раскомментируйте код в src/bot.py в функции classify_message()")
        print()
    else:
        print(f"✅ LLM_API_KEY установлен")
        if llm_url:
            print(f"✅ LLM_API_BASE_URL: {llm_url}")
        if llm_model:
            print(f"✅ LLM_MODEL_NAME: {llm_model}")
        print()
    
    # Тестовые сообщения
    test_messages = [
        "Помогите с SQL запросом для аналитики продаж",
        "Нужна помощь с A/B тестом для новой функции",
        "Вопрос по маркетинговой кампании",
        "Проблема с оплатой и подозрительными транзакциями",
    ]
    
    # Если передан аргумент - используем его
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        test_routing(message)
    else:
        # Интерактивный режим
        print("Доступные тестовые сообщения:")
        for i, msg in enumerate(test_messages, 1):
            print(f"  {i}. {msg}")
        print("  0. Ввести свое сообщение")
        print()
        
        choice = input("Выберите номер (или 0 для ввода): ").strip()
        
        if choice == "0":
            message = input("Введите сообщение: ").strip()
            if message:
                test_routing(message)
            else:
                print("Сообщение не введено")
        elif choice.isdigit() and 1 <= int(choice) <= len(test_messages):
            message = test_messages[int(choice) - 1]
            test_routing(message)
        else:
            print("Неверный выбор")
            # Запускаем первый тест по умолчанию
            print("Запускаем тест по умолчанию...")
            test_routing(test_messages[0])


if __name__ == "__main__":
    main()

