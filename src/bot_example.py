"""
Mini-demo: как можно использовать prompt.txt и .env для классификации
(Этот файл — только пример, не запускайте его как есть)
"""
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def get_prompt(text):
    """Читать шаблонный prompt.txt"""
    prompt_path = Path(__file__).parent.parent / "evaluation" / "prompt.txt"
    if prompt_path.exists():
        with open(prompt_path, encoding="utf-8") as f:
            system_prompt = f.read()
    else:
        system_prompt = "Заполните evaluation/prompt.txt!"
    return f"{system_prompt}\n\nNow classify: {text}"

# TODO: здесь напишите свою функцию обращения к вашему LLM провайдеру
# def classify_message(text):
#     # Адаптируйте под ваш LLM провайдер (REST API или собственный протокол)
#     ...

if __name__ == "__main__":
    print("Это пример! Для запуска вашей логики напишите свой код и вызовите из start_bot.sh")


