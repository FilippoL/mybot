#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)


import logging
import sqlite3
import uuid


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, AGE, LOCATION, QUESTION = range(4)

class database:
    def __init__(self):#this is a contrucstor
        db = sqlite3.connect("my_bot_database.db")
        db.row_factory = sqlite3.Row
        db.execute('drop table if exists users')
        db.execute('create table users ( ID text, nationality text, age int, gender text )')
        db.execute('drop table if exists questions')
        db.execute('create table questions ( ID text, question text, topic text )')
        db.execute('drop table if exists answers')
        db.execute('create table answers ( ID_one text, ID_two text, answer text )')
        db.commit
        db.close()
        return

    def getID(self):

        return 1


    def __iter__(self):
        db = sqlite3.connect("my_bot_database.db")
        cursor = db.execute('select * from users')
        for row in cursor:
            yield dict(row)
        db.close()


class t_users(database):

    def FillNewUser(selfm, nationality = "", age = 0, gender = ""):
        _ID = str(uuid.uuid4())
        db = sqlite3.connect("my_bot_database.db")
        db.execute('insert into users (ID, nationality, age, gender) values (?, ?, ?, ?)', (_ID, nationality.lower(), age, gender.lower()))
        db.commit()
        db.close()
        return _ID

    def GetUserAge(self, key):
        pass

def start(bot, update):
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Hi! My name is AnswerMyQuestion Bot. I will be asking you some questions.\n'
        'Honesty is appreciated.\n\n'
        'Send /skip to skip the question\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


    return GENDER

def skip_gender(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send gender." % user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At least, tell me your age.',
                              reply_markup=ReplyKeyboardRemove())
    return AGE


def gender(bot, update):
    user = update.message.from_user
    logger.info("Gender of %s: %s" % (user.first_name, update.message.text))

    file = open("users.txt", 'a')
    file.write("%s\n Gender: %s\n" % (user.first_name, update.message.text))

    update.message.reply_text('How old are you?\n'
                              'Send /skip to skip the question',
                              reply_markup=ReplyKeyboardRemove())

    return AGE

def skip_age(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send gender." % user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At least, send me your location.')

    return LOCATION

def age(bot, update):
    user = update.message.from_user
    logger.info("Age of %s: %s" % (user.first_name, update.message.text))

    file = open("users.txt" , 'a')
    file.write(" Age: %s\n" % update.message.text)

    update.message.reply_text('Thanks! Now, send me your location please,\n'
                              'Send /skip to skip the question')

    return LOCATION

def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send age." % user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'Could you please make me a question?\n'
                              'Bare in mind I might not be able to anwer')

    return QUESTION

def location(bot, update):

    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f"
                % (user.first_name, user_location.latitude, user_location.longitude))
    file = open("users.txt", 'a')
    file.write(" Location: %f / %f\n"
                % (user_location.latitude, user_location.longitude))

    update.message.reply_text('Maybe I can visit you sometime!\n'
                              'Could you please make me a question?\n'
                              'Bare in mind I might not be able to anwer')

    return QUESTION

def recieve_question(bot, update):
    user = update.message.from_user
    logger.info("%s sent some text" % user.first_name)

    file = open('questions.txt', 'w')
    file.write("\n" + update.message.text)

    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def filecheck(file_name):
    try:
        open(file_name, "r") #try open file for reading
        return 1 #return if success

    except IOError: #lets make use of the default file i/o library exception handler
        logger.info("No database found, creating one... \n")
        return 0


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("478466244:AAGx1DMPPeWhpwVnVwwqDM3pQk9IZZ_6xFw")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    _newuser = t_users()
    _newuser.FillNewUser("italian", 23, "male")



    if filecheck('my_bot_database.db'):
        logger.info("Database found \n")
    else:
        initialise_database()


    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            GENDER: [MessageHandler(Filters.text, gender),
                       CommandHandler('skip', skip_gender)],

            AGE: [MessageHandler(Filters.text, age),
                       CommandHandler('skip', skip_age)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            QUESTION: [MessageHandler(Filters.text, recieve_question)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
