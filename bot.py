from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater, CallbackContext
from scraper import scrape
import time
import schedule
from telegram import Bot


# Replace 'YOUR_BOT_TOKEN' with your actual bot token.
BOT_TOKEN = "6417881790:AAEjaaYvjP95Ny_CKc8LAnZyrooPHgvf9Pw"
bot_username = "@fonscraper"

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    time.sleep(3)
    change = scrape()

    # get the bot results from the display_results.txt file
    file = open('display_results.txt', 'r')
    data = file.read()
    file.close()

    await update.message.reply_text(data)
    

async def auto_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # how often we check for changes in seconds
    timer = 60

    while True:
        time.sleep(timer)
        change = scrape()
        print(change)
        if change:
            # if there are changes get the bot results from the display_results.txt file
            file = open('display_results.txt', 'r')
            data = file.read()
            file.close()
            await update.message.reply_text(data)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    message.reply_dice()
    

    await update.message.reply_text("hello khairi")
        
if __name__ == '__main__':
    print("starting bot...")
    app = Application.builder().token(BOT_TOKEN).build()

    # commands
    app.add_handler(CommandHandler('check', check_command))

    # use the auto update command to turn the automatic update feature on
    app.add_handler(CommandHandler('auto_update', auto_message))
    app.add_handler(CommandHandler('hello', hello))

    print("polling")
    app.run_polling(poll_interval=3)

    


