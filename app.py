import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Tokeni doğrudan burada belirtiyoruz
TOKEN = "7130317633:AAGkQD2f_R3wI9IEhU_pG25BrSK5tD_GxdY"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Merhaba! Hatırlatıcı botuna hoş geldin. /reminder <mesaj> komutu ile hatırlatma oluşturabilirsin.')

def reminder(update: Update, context: CallbackContext) -> None:
    try:
        # Kullanıcının girdiği hatırlatma mesajını al
        reminder_message = ' '.join(context.args)
        chat_id = update.message.chat_id
        
        # Hatırlatma mesajını kaydet
        context.job_queue.run_once(send_reminder, 2 * 24 * 60 * 60, context=(chat_id, reminder_message), name=str(chat_id))
        
        update.message.reply_text('Hatırlatma ayarlandı!')
    except (IndexError, ValueError):
        update.message.reply_text('Doğru format: /reminder <mesaj>')

def send_reminder(context: CallbackContext) -> None:
    job = context.job
    context.bot.send_message(job.context[0], text=f'📅 Hatırlatma: {job.context[1]}')

def main() -> None:
    # Updater oluştur
    updater = Updater(TOKEN)

    # Dispatcher al
    dispatcher = updater.dispatcher

    # Komutları işleyicilere ekle
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("reminder", reminder))

    # Botu başlat
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
