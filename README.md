# 🤖 Qwen Telegram Bot

Telegram-бот с чатом через Qwen AI (бесплатно через OpenRouter).

---

## 🚀 Быстрый старт

### 1. Получи токен Telegram-бота
1. Открой [@BotFather](https://t.me/BotFather) в Telegram
2. Отправь `/newbot` и следуй инструкциям
3. Скопируй токен вида `123456789:AAF...`

### 2. Получи бесплатный API-ключ OpenRouter
1. Зарегистрируйся на [openrouter.ai](https://openrouter.ai)
2. Перейди в **Keys** → **Create Key**
3. Скопируй ключ вида `sk-or-v1-...`

### 3. Настрой config.py
```python
TELEGRAM_TOKEN = "твой_токен_от_BotFather"
OPENROUTER_API_KEY = "sk-or-v1-..."
QWEN_MODEL = "qwen/qwen3-32b:free"  # или другая модель
```

### 4. Установи зависимости и запусти
```bash
pip install -r requirements.txt
python bot.py
```

---

## 📋 Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие |
| `/new` | Очистить историю (новый чат) |
| `/model` | Показать текущую модель |
| `/help` | Справка |

---

## 🆓 Бесплатные модели Qwen на OpenRouter

| Модель | Параметры | Скорость |
|--------|-----------|----------|
| `qwen/qwen3-8b:free` | 8B | ⚡ Быстрая |
| `qwen/qwen3-14b:free` | 14B | 🏃 Средняя |
| `qwen/qwen3-32b:free` | 32B | 🐢 Медленнее |
| `qwen/qwen3-235b-a22b:free` | 235B | 🐌 Самая медленная |
| `qwen/qwq-32b:free` | 32B | 🧠 С reasoning |

---

## 🗂 Структура проекта

```
qwen_telegram_bot/
├── bot.py           # Основной файл бота
├── config.py        # Настройки (токены, модель, промпт)
├── requirements.txt # Зависимости
└── README.md        # Инструкция
```

---

## ☁️ Деплой (бесплатный хостинг)

**Oracle Cloud Free Tier** (рекомендуется):
```bash
# На VPS:
pip install -r requirements.txt
nohup python bot.py &  # запуск в фоне
```

**Railway / Render**: загрузи файлы и укажи команду `python bot.py`
