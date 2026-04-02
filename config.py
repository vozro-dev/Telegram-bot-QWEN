# ╔══════════════════════════════════════════════════════╗
# ║              НАСТРОЙКИ БОТА — config.py              ║
# ╚══════════════════════════════════════════════════════╝

# 1) Токен Telegram бота (получить у @BotFather)
TELEGRAM_TOKEN = "Токен Telegram бота"

# 2) API-ключ OpenRouter (бесплатно на openrouter.ai)
OPENROUTER_API_KEY = "API-ключ OpenRouter"

# 3) Модель Qwen (бесплатные варианты на OpenRouter):
#    "qwen/qwen3.6-plus:free"           — мощная модель
#    "qwen/qwen3.6-plus-preview:free"   — preview версия
#    "qwen/qwen3-next-80b-a3b-instruct:free" — 80B модель
#    "qwen/qwen3-coder:free"            — для кода
QWEN_MODEL = "qwen/qwen3.6-plus:free"

# 4) Системный промпт (личность бота)
SYSTEM_PROMPT = (
    "Ты умный и дружелюбный ИИ-ассистент. "
    "Отвечай развёрнуто, чётко и по делу. "
    "Если вопрос на русском — отвечай на русском. "
    "Используй Markdown-форматирование там, где уместно."
)

# 5) Максимальное количество пар сообщений в истории чата
MAX_HISTORY = 20
