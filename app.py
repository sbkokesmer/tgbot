import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

# Bot token
TOKEN = '7130317633:AAGkQD2f_R3wI9IEhU_pG25BrSK5tD_GxdY'

# Loglama ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# APScheduler nesnesini global olarak tanımla
scheduler = BackgroundScheduler()
scheduler.start()

# Hatırlatma fonksiyonu
async def remind(context: ContextTypes.DEFAULT_TYPE, chat_id):
    await context.bot.send_message(chat_id, text="Hatırlatma: İki gün önce planladığınız işi yapmayı unutmayın!")

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Merhaba! Hatırlatılmak istediğiniz işi /hatirlat komutu ile belirtebilirsiniz.')

# /hatirlat komutu
async def hatirlat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    remind_time = datetime.now() + timedelta(days=2)
    scheduler.add_job(remind, 'date', run_date=remind_time, args=[context, chat_id])
    await update.message.reply_text('İki gün sonra hatırlatılacak!')

# Mesajları dinleme fonksiyonu
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "en büyük" in text.lower():
        await update.message.reply_text("FENERBAHÇE")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hatirlat", hatirlat))
    # Grup mesajlarını da içeren mesajları dinle
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE), handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
