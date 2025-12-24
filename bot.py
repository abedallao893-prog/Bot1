from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Your movies and shows
MOVIES = ['Movie 1', 'Movie 2']
TV_SHOWS = ['Show 1', 'Show 2']

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Movies", callback_data='movies')],
        [InlineKeyboardButton("TV Shows", callback_data='tvshows')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose category:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == 'movies':
        keyboard = [[InlineKeyboardButton(title, callback_data=f"movie_{title}")] for title in MOVIES]
        query.edit_message_text("Select a movie:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == 'tvshows':
        keyboard = [[InlineKeyboardButton(title, callback_data=f"tv_{title}")] for title in TV_SHOWS]
        query.edit_message_text("Select a TV show:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data.startswith("movie_") or query.data.startswith("tv_"):
        title = query.data.split("_", 1)[1]
        # Replace this with your channel file sending logic
        query.edit_message_text(f"Here is your selection: {title}")

def main():
    updater = Updater("8555310397:AAFo28I_yZ6HMoNxAg8cR3sCfbmVg42W-D4")
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
