import logging
import os
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from barcode import Code128
from barcode.writer import ImageWriter
from config import BOT_TOKEN


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
    :param product_code: строка с номером товара
    :param scale: множитель разрешения (по умолчанию 4 → высокая чёткость)
    :return: BytesIO с PNG-файлом
    """
    barcode = Code128(product_code, writer=ImageWriter())
    barcode.writer.set_options({
        "write_text": True,     # показывать номер под штрихкодом
        "text_distance": 5.0,   # отступ номера от кода
        "module_width": 0.4,    # толщина линии
        "module_height": 80,    # высота штрихов
        "quiet_zone": 6.0,      # поля
        "font_size": 40,        # размер цифр
    })

    buffer = BytesIO()
    barcode.write(buffer, options={"dpi": 300 * scale})
    buffer.seek(0)
    return buffer


# === Команды и обработчики ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Отправь мне номер товара (только цифры), и я сгенерирую для него штрихкод в PNG 📦"
    )


async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    product_code = (update.message.text or "").strip()

    if not product_code.isdigit():
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
    """Обработчик неизвестных команд"""
    await update.message.reply_text("❌ Такой команды не существует. Попробуй ввести номер товара 😉")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Необработанное исключение", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text("⚠️ Произошла ошибка. Уже работаю над этим 🙈")


# === Запуск бота ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    app.add_error_handler(error_handler)
    app.run_polling()


if __name__ == "__main__":
    main()
