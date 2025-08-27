import logging
import os
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from barcode import Code128
from barcode.writer import ImageWriter
from config import BOT_TOKEN
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton


# === Настройка логирования ===
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/bot.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# === Генерация штрихкода ===
def generate_barcode_png(product_code: str, scale: int = 4) -> BytesIO:
    """
    Генерация штрихкода Code128 в PNG.
    """
    barcode = Code128(product_code, writer=ImageWriter())

    buffer = BytesIO()
    barcode.write(buffer, options={
        "dpi": 300 * scale,
        "write_text": True, # показывать номер под штрихкодом
        "background": "#ffcd16",   # фон
        "foreground": "#090606",   # штрихкод и текст
        "font_size": 10,    # размер шрифта номера
        "text_distance": 5.0,  # отступ номера от кода
        "module_width": 0.4,  # толщина линии
        "module_height": 20,  # высота штрихов
        "quiet_zone": 6.0,  # поля
    })
    buffer.seek(0)
    return buffer


# === Команды и обработчики ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("❓ Помощь")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Привет! Отправь мне номер товара (только цифры), и я сгенерирую для него штрихкод в PNG 📦",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 *Как пользоваться ботом:*\n\n"
        "1️⃣ Введи номер товара (только цифры).\n"
        "   Пример: `123456789`\n\n"
        "2️⃣ Бот сгенерирует штрихкод Code128 в формате PNG 📦\n\n"
        "⚠️ Правила:\n"
        "• Номер должен состоять только из цифр (без пробелов, букв и спецсимволов).\n"
        "• Минимум 1 цифра.\n\n"
        "💡 Советы:\n"
        "— Если ввёл что-то неверное, бот напомнит о формате.\n"
        "— Используй кнопку *Помощь* для повторной подсказки.\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    product_code = (update.message.text or "").strip()

    if not product_code.isdigit():
        # Если нажата кнопка "Помощь"
        if product_code.lower() in ["❓ помощь", "помощь", "/help"]:
            await help_command(update, context)
            return

        await update.message.reply_text("❌ Пожалуйста, введи корректный номер (только цифры).")
        return

    try:
        barcode_png = generate_barcode_png(product_code)
        await update.message.reply_document(
            barcode_png,
            filename=f"{product_code}.png",
            caption=f"✅ Штрихкод для товара № {product_code}",
        )
        logger.info(f"Сгенерирован штрихкод для {product_code}")
    except Exception as e:
        logger.exception(f"Ошибка при генерации штрихкода для {product_code}: {e}")
        await update.message.reply_text("⚠️ Не удалось сгенерировать штрихкод. Попробуй ещё раз.")


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Такой команды не существует. Попробуй ввести номер товара 😉")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Необработанное исключение", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text("⚠️ Произошла ошибка. Уже работаю над этим 🙈")


# === Запуск бота ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    app.add_error_handler(error_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
