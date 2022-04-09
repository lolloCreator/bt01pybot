import logging
from dbhelper import DBHelper
import os


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

PORT = int(os.environ.get('PORT', '5000'))

logger = logging.getLogger(__name__)

db = DBHelper()

TIPO, COMUNE, SOPRALLUOGO, CAVOGUASTO = range(4)
NODO1, NODO2, SALVA, CANCELLA, COMPLETA = 8, 9, 10, 11, 12

dizionario = {"tipo":"", "comune":"", "nodo1":"", "nodo2":""}


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['SOPRALLUOGO'], ['CAVO GUASTO']]

    message = 'Ciao, seleziona una attività da aggiungere.\n\n' \
              'Se non visualizzi il menù, clicca sull\'icona in basso a destra sulla barra di scrittura. \n\n' \
              'Puoi annullare questa conversazione in qualsiasi punto utilizzando il comando:\n /cancel'

    reply_markup = ReplyKeyboardMarkup(reply_keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True,
                                       input_field_placeholder='Boy or Girl?')

    update.message.reply_text(message, reply_markup= reply_markup)

    return TIPO


def gender(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Nome utente: %s e Tipo attività: %s", user.first_name, update.message.text)
    dizionario['tipo'] = update.message.text

    message = 'Okay, per l\'attività: "%s", ho bisogno di sapere il comune' % update.message.text

    reply_keyboard = [['Arienzo'], ['Capodrise'], ['Cervino'], ['Macerata Campania'], ['Maddaloni'], ['Marcianise'], ['Portico di Caserta'], ['Recale'], ['S.Felice a Cancello'], ['S.N.La Strada'], ['S.Maria a Vico'], ['Valle di Maddaloni'], ['S.Marco Evangelista']]

    reply_markup = ReplyKeyboardMarkup(reply_keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True,
                                       input_field_placeholder='Seleziona un comune')



    update.message.reply_text(message,reply_markup= reply_markup)

    return COMUNE

''''
def photo(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(
        'Gorgeous! Now, send me your location please, or send /skip if you don\'t want to.'
    )

    return LOCATION
'''

def photo(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    logger.info("Photo of %s: %s", user.first_name, update.message.text)
    dizionario['comune'] = update.message.text

    print(dizionario['tipo'])
    if dizionario['tipo'] == 'SOPRALLUOGO':
        update.message.reply_text(
            'Sopralluoghi non ancora implementati', reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    elif dizionario['tipo'] == 'CAVO GUASTO':
        update.message.reply_text(
            'Scrivi nodo 1', reply_markup=ReplyKeyboardRemove()
        )
        return NODO1

def nodo1(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Photo of %s: %s", user.first_name, update.message.text)
    dizionario['nodo1'] = update.message.text
    update.message.reply_text(
        'Scrivi nodo 2', reply_markup=ReplyKeyboardRemove()
    )
    return NODO2

def printDic(update: Update, context: CallbackContext) -> int:
    dizionario['nodo2'] = update.message.text
    message = ""
    for chiave, valore in dizionario.items():
        message+= chiave + " : " + valore + "\n"
    update.message.reply_text(
        message, reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def completa(update: Update, context: CallbackContext) -> int:
    dizionario['nodo2'] = update.message.text
    message = ""
    for chiave, valore in dizionario.items():
        message+= chiave + " : " + valore + "\n"
    message+= "\nQuesti dati sono corretti?"


    reply_keyboard = [['SALVA'], ['ANNULLA']]

    reply_markup = ReplyKeyboardMarkup(reply_keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True,
                                       input_field_placeholder='Boy or Girl?')

    update.message.reply_text(
        message, reply_markup=reply_markup
    )
    return COMPLETA

def salva(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Salvato', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def annulla(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Cancellato', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

'''
def compliance_selection(update, _: CallbackContext) -> None:
        ############################ NELLA CHIAMATA
        keyboard = [
            [
                InlineKeyboardButton("SALVA", callback_data='end_salva'),
                InlineKeyboardButton("ANNULLA", callback_data='end_annulla'),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            message, reply_markup=reply_markup
        )

        #################################### NELLA MAIN
        updater.dispatcher.add_handler(CallbackQueryHandler(compliance_selection, pattern='end'))

        ################################# IN QUESTA FUNZIONE
        query = update.callback_query
        query.answer()
        if query.data == 'end_salva':
            query.message.reply_text('Compliant')
        elif query.data == 'end_annulla':
            query.message.reply_text('Not Compliant')
        return ConversationHandler.END

'''
def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Operazione annullata', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    db.setup()
    db.add_item("1234")
    # Create the Updater and pass it your bot's token.
    TOKEN = '5111264889:AAFtCG0lLWSiHLLLiSU_jwocWU5RJxO0e3c'
    APP_NAME='https://bt1bot.herokuapp.com/'
    # https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            TIPO: [MessageHandler(Filters.regex('^(SOPRALLUOGO|CAVO GUASTO|Other)$'), gender)],
            COMUNE: [MessageHandler(Filters.regex('^(Arienzo|Capodrise|Cervino|Macerata Campania|Maddaloni|Marcianise|Portico di Caserta|Recale|S.Felice a Cancello|S.N.La Strada|S.Maria a Vico|Valle di Maddaloni|S.Marco Evangelista)$'), photo)],
            NODO1: [MessageHandler(Filters.text, nodo1)],
            NODO2: [MessageHandler(Filters.text, completa)],
            COMPLETA: [MessageHandler(Filters.regex('^(SALVA)$'), salva), MessageHandler(Filters.regex('^(ANNULLA)$'), annulla)],


        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )


    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN,webhook_url=APP_NAME + TOKEN)
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()