import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
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

# Hatırlatma fonksiyonu
async def remind(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(job.context, text="Hatırlatma: İki gün önce planladığınız işi yapmayı unutmayın!")

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Merhaba! Hatırlatılmak istediğiniz işi /hatirlat komutu ile belirtebilirsiniz.')

# /hatirlat komutu
async def hatirlat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    scheduler = BackgroundScheduler()
    scheduler.start()
    remind_time = datetime.now() + timedelta(days=2)
    scheduler.add_job(remind, 'date', run_date=remind_time, args=[context], job_context=user_id)
    await update.message.reply_text('İki gün sonra hatırlatılacak!')

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hatirlat", hatirlat))

    application.run_polling()

if __name__ == '__main__':
    main()
