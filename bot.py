import logging
import asyncio
import aiohttp
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from config import TELEGRAM_TOKEN, OPENROUTER_API_KEY, QWEN_MODEL, SYSTEM_PROMPT, MAX_HISTORY

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Хранилище истории чатов: {user_id: [{"role": ..., "content": ...}, ...]}
chat_histories: dict[int, list[dict]] = {}


async def ask_qwen(messages: list[dict]) -> str:
    """Отправляет запрос в OpenRouter (Qwen) и возвращает ответ."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/your_bot",
        "X-Title": "Qwen Telegram Bot",
    }
    payload = {
        "model": QWEN_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2048,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=60),
        ) as resp:
            if resp.status != 200:
                error_text = await resp.text()
                logger.error(f"OpenRouter error {resp.status}: {error_text}")
                return f"❌ Ошибка API ({resp.status}). Попробуйте позже."
            data = await resp.json()
            return data["choices"][0]["message"]["content"]


def get_history(user_id: int) -> list[dict]:
    """Возвращает историю чата с системным промптом."""
    if user_id not in chat_histories:
        chat_histories[user_id] = []
    return [{"role": "system", "content": SYSTEM_PROMPT}] + chat_histories[user_id]


def add_to_history(user_id: int, role: str, content: str):
    """Добавляет сообщение в историю и обрезает до MAX_HISTORY."""
    if user_id not in chat_histories:
        chat_histories[user_id] = []
    chat_histories[user_id].append({"role": role, "content": content})
    # Оставляем только последние MAX_HISTORY пар (user + assistant)
    if len(chat_histories[user_id]) > MAX_HISTORY * 2:
        chat_histories[user_id] = chat_histories[user_id][-(MAX_HISTORY * 2):]


# ──────────────────────────── Handlers ────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        f"Я бот с интеграцией **Qwen AI** (модель: `{QWEN_MODEL}`).\n\n"
        "Просто напиши мне что-нибудь — и я отвечу 🤖\n\n"
        "📌 Команды:\n"
        "/start — приветствие\n"
        "/new — начать новый чат\n"
        "/model — текущая модель\n"
        "/help — помощь",
        parse_mode="Markdown",
    )


async def cmd_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_histories[user_id] = []
    await update.message.reply_text(
        "🔄 История очищена. Начнём новый разговор!"
    )


async def cmd_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🤖 Текущая модель: `{QWEN_MODEL}`\n\n"
        "Чтобы сменить модель — отредактируй `QWEN_MODEL` в `config.py`.",
        parse_mode="Markdown",
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *Справка*\n\n"
        "Этот бот использует модель Qwen через OpenRouter API.\n\n"
        "*Команды:*\n"
        "/start — запуск бота\n"
        "/new — очистить историю и начать заново\n"
        "/model — узнать текущую модель\n"
        "/help — эта справка\n\n"
        f"💬 История чата: последние {MAX_HISTORY} сообщений\n"
        "📡 API: openrouter.ai",
        parse_mode="Markdown",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text.strip()

    if not user_text:
        return

    # Показываем индикатор набора текста
    await update.message.chat.send_action("typing")

    # Добавляем сообщение пользователя в историю
    add_to_history(user_id, "user", user_text)

    # Формируем полный контекст и запрашиваем ответ
    messages = get_history(user_id)

    try:
        reply = await ask_qwen(messages)
    except asyncio.TimeoutError:
        reply = "⏳ Превышено время ожидания. Попробуйте ещё раз."
    except Exception as e:
        logger.exception("Unexpected error")
        reply = f"⚠️ Произошла ошибка: {e}"

    # Сохраняем ответ в историю
    add_to_history(user_id, "assistant", reply)

    # Отправляем ответ (с fallback на plain text если Markdown сломан)
    try:
        await update.message.reply_text(reply, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(reply)


# ──────────────────────────── Main ────────────────────────────

def main():
    import asyncio
    from telegram.request import HTTPXRequest

    # Создаём и устанавливаем event loop для Python 3.14+
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Настраиваем request с увеличенными таймаутами для обхода проблем с подключением
    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30,
    )

    app = Application.builder().token(TELEGRAM_TOKEN).request(request).build()

    # Команды
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("new", cmd_new))
    app.add_handler(CommandHandler("model", cmd_model))
    app.add_handler(CommandHandler("help", cmd_help))

    # Текстовые сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🤖 Бот запущен!")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
