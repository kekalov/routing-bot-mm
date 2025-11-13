# 🚀 Быстрый старт AnalytiQA

## 1. Склонируйте или скачайте проект

```bash
git clone https://github.com/kekalov/analytiqa-template.git
cd analytiqa-template
```

## 2. Настройте своё окружение

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Подготовьте переменные окружения
Переименуйте `.env.template` в `.env` и впишите свои токены и host (смотри комментарии в файле)

## 4. Напишите свой prompt

Откройте `evaluation/prompt.txt` и опишите правила, категории, возвращаемый формат. Пример:
```
{
  "topic": "SQL Issues",
  "analyst": "Data Team",
  "channel": "analytics",
  "reason": "Запрос касается SQL"
}
```

## 5. (Опционально) Протестируйте
Вы можете локально запускать тестовые функции через свои заглушки в `src/`. Например, напишите dummy-файл, который подтягивает prompt, и проверьте на своих примерах.

## 6. Запустите бота
```
./start_bot.sh
```

---

**Минимальные требования:** Python 3.9+, pip, базовые знания ботов/Prompt Engineering

Всё остальное — гибко под себя!


