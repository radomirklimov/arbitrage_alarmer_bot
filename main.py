from typing import Final

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '8312876686:AAEYo8prEArq9eWYIvWgFVCxVv2P6DpNq7s'
BOT_USERNAME: Final = '@arbitrage_alarmer_bot'

#Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Hello, and thanks for using the arbitrage bot which is designed to provide signals" \
  " about price differences on exchange platforms. Let's earn some shit")

#main function to run the bot
def main():
  app = Application.builder().token(TOKEN).build()
  app.add_handler(CommandHandler("start", start))

  app.run_polling()

if __name__=="__main__":
  main()
