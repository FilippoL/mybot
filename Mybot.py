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
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, AGE, LOCATION, QUESTION, FILLS_DB = range(5)

class database:
    def __init__(self):#this is a contrucstor
        db = sqlite3.connect("my_bot_database.db")
        db.row_factory = sqlite3.Row
        db.execute('CREATE TABLE IF NOT EXISTS users ( ID text, nationality text, age int, gender text )')
        db.execute('CREATE TABLE IF NOT EXISTS questions ( ID text, question text, topic text )')
        db.execute('CREATE TABLE IF NOT EXISTS answers ( ID_one text, ID_two text, answer text )')
        db.commit()
        db.close()

    def __iter__(self):
        db = sqlite3.connect("my_bot_database.db")
        cursor = db.execute('select * from users')
        for row in cursor:
            yield dict(row)
        db.close()

    def get_property(self, key):
            return self.user_prop.get(None, key)

class t_users(database):

    def FillNewUser(self, _id = "", _nationality = "", _age = 0, _gender = ""):
        db = sqlite3.connect("my_bot_database.db")
        db.execute('insert into users (ID, nationality, age, gender) values (?, ?, ?, ?)', (_id, _nationality.lower(), _age, _gender.lower()))
        db.commit()
        db.close()


    def GetUserAge(self, key):
        pass

class t_questions(database):

    def FillNewQuestion(self, _id = "", _question = "", _topic = ""):
        db = sqlite3.connect("my_bot_database.db")
        db.execute('insert into questions (ID, question, topic) values (?, ?, ?)', (_id, _question.lower(), _topic.lower()))
        db.commit()
        db.close()

    def GetQuestionByTopic(self, _topic = ""):
        db = sqlite3.connect("my_bot_database.db")
        crsr = db.cursor()
        crsr = db.execute('select question from questions where topic = ? ', (_topic, ))
        q_str = crsr.fetchall()
        db.commit()
        db.close()
        return q_str


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

    final = str(user.id) + ".txt"

    with open(final, "w") as _file:
        _file.write("%s\n" % (update.message.text))

    update.message.reply_text('How old are you?\n'
                              'Send /skip to skip the question',
                              reply_markup=ReplyKeyboardRemove())

    return AGE

def skip_age(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send gender." % user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At least, tell me where you are from.')

    return LOCATION

def age(bot, update):
    user = update.message.from_user
    logger.info("Age of %s: %s" % (user.first_name, update.message.text))

    final = str(user.id) + ".txt"

    with open(final, "a") as _file:
        _file.write("%s\n" % (update.message.text))

    update.message.reply_text('Thanks! Now, could you please give me your nationality?\n'
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
    logger.info("Nationality of %s: %s " % (user.first_name, update.message.text))

    final = str(user.id) + ".txt"

    with open(final, "a") as _file:
        _file.write("%s\n" % (update.message.text))

    update.message.reply_text('Maybe I can visit you sometime!\n'
                              'Could you please make me a question?\n'
                              'Bare in mind I might not be able to anwer')

    return QUESTION

def recieve_question(bot, update):
    user = update.message.from_user
    logger.info("%s sent some text" % user.first_name)

    final = str(user.id) + ".txt"

    with open(final, "a") as _file:
        _file.write("%s\n" % (update.message.text))
        _file.close()
    update.message.reply_text('Thank you! ')
    update.message.reply_text('If you agree with your data being anonimously stored press any key ')
    return FILLS_DB

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
        logger.info("File found \n")
        return  #return if success

    except IOError: #lets make use of the default file i/o library exception handler
        logger.info("No file found \n")
        return

def filling_up(bot, update):

    user = update.message.from_user

    final = str(user.id) + ".txt"

    try:
        with open(final, "r") as _file:
            lines = _file.readlines()
            lines = [x.strip() for x in lines]
            _newuser = t_users()
            _newuser.FillNewUser(str(user.id), lines[2], int(lines[1]), lines[0])
            _newquestion = t_questions()
            _newquestion.FillNewQuestion(str(user.id), lines[3], "brexit")
            _newquestion.GetQuestionByTopic("brexit")[1][0]
            _file.close()
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        logger.warn("ERROR")

    os.remove(final)

    return ConversationHandler.END


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("478466244:AAGx1DMPPeWhpwVnVwwqDM3pQk9IZZ_6xFw")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    filecheck('my_bot_database.db')

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            GENDER: [MessageHandler(Filters.text, gender),
                       CommandHandler('skip', skip_gender)],

            AGE: [MessageHandler(Filters.text, age),
                       CommandHandler('skip', skip_age)],

            LOCATION: [MessageHandler(Filters.text, location),
                       CommandHandler('skip', skip_location)],

            QUESTION: [MessageHandler(Filters.text, recieve_question)],


            FILLS_DB:  [MessageHandler(Filters.all, filling_up)],

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
