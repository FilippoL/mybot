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
import uuid
import os

import Database
import Question
import Answer
import User

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

topics = ("brexit", "food")

current_topic = 0
current_question = 0

GENDER, AGE, LOCATION, QUESTION, ANSWER = range(5)

def start(bot, update):
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text('Hi! My name is AnswerMyQuestion Bot')
    update.message.reply_text('I will be asking you few question just before we start our conversation')
    update.message.reply_text('Honesty is appreciated :)')
    #update.message.reply_text('Remember to send /skip if you dont want to answer them')

    update.message.reply_text('Are you a boy or a girl?', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return GENDER

#def skip_gender(bot, update):
#    user = update.message.from_user
#    logger.info("User %s did not send gender." % user.first_name)
#
#    update.message.reply_text('Not a problem, but can you tell me your age?', reply_markup=ReplyKeyboardRemove())
#
#    return AGE

def gender(bot, update):
    user = update.message.from_user
    logger.info("Gender of %s: %s" % (user.first_name, update.message.text))

    final = str(user.id) + ".txt"

    with open(final, "w") as _file:
        _file.write("%s\n" % (update.message.text))
        _file.close()

    update.message.reply_text('Cool! How old are you?', reply_markup=ReplyKeyboardRemove())

    return AGE

#def skip_age(bot, update):
#    user = update.message.from_user
#    logger.info("User %s did not send gender." % user.first_name)
#
#    update.message.reply_text('Not a problem, but can you tell me where are you from?')
#
#    return LOCATION

def age(bot, update):
    user = update.message.from_user
    logger.info("Age of %s: %s" % (user.first_name, update.message.text))

    final = str(user.id) + ".txt"

    with open(final, "a") as _file:
        _file.write("%s\n" % (update.message.text))
        _file.close()
        
    update.message.reply_text('Thanks! Now, where are you from?')

    return LOCATION

#def skip_location(bot, update):
#    user = update.message.from_user
#    logger.info("User %s did not send age." % user.first_name)
#
#    update.message.reply_text('Not a problem')
#
#    update.message.reply_text('Lets start with our conversation then...')
#    update.message.reply_text('Why dont you ask me something?')
#    update.message.reply_text('I might not be able to answer but i will try my best')
#
#    return QUESTION

def location(bot, update):

    user = update.message.from_user
    logger.info("Nationality of %s: %s " % (user.first_name, update.message.text))

    final = str(user.id) + ".txt"

    with open(final, "a") as _file:
        _file.write("%s\n" % (update.message.text))
        _file.close()

    update.message.reply_text('Interesting! Lets start with our conversation then')
    update.message.reply_text('Why dont you begin asking me something?')
    update.message.reply_text('I might not be able to answer but i will try my best')

    return QUESTION

def recieve_question(bot, update):
    user = update.message.from_user
    logger.info("%s sent a question" % user.first_name)

    if current_question > 0:
        return check_question(user, update)
    else :
        return filling_user(user,update)

def filling_user(_user,_update):
    final = str(_user.id) + ".txt"

    try:
            with open(final, "r") as _file:
                lines = _file.readlines()
                lines = [x.strip() for x in lines]

                _newuser = User.t_users()
                _newuser.FillNewUser(str(_user.id), lines[2], int(lines[1]), lines[0])

                _file.close()
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        logger.warn("ERROR")

    os.remove(final)

    return check_question(_user,_update)

def check_question(_user,_update):
    _newquestion = Question.t_questions()

    if(_newquestion.AlreadyExistent(_update.message.text)):
        return answer_question(_user,_update)
    else: 
        return filling_question(_user,_update)

def filling_question(_user,_update):

    _newquestion = Question.t_questions()
    _newquestion.FillNewQuestion(str(uuid.uuid4()), _update.message.text, topics[current_topic])    

    _update.message.reply_text('I dont know how to answer that question yet')
    _update.message.reply_text('Guess its my turn then...')

    return ask_question(_user,_update)

def answer_question(_user, _update):
    _newquestion = Question.t_questions()
    temp_ID = _newquestion.GetIDByQuestion(_update.message.text)[0]

    _newanswer = Answer.t_answers()
   
    if (_newanswer.AlreadyExistent(temp_ID)):#we have an answer
        _update.message.reply_text(_newanswer.GetAnswerByQuestionID(temp_ID)[0])#indexing for answers
    else: 
        _update.message.reply_text('I dont know how to answer that question yet')

    _update.message.reply_text('Guess its my turn now')

    return ask_question(_user, _update) 

def ask_question(_user, _update):
    _newquestion = Question.t_questions()
    _update.message.reply_text(_newquestion.GetQuestionByTopic(topics[current_topic])[0])
    
    return ANSWER

def recieve_answer(bot, update):
    user = update.message.from_user
    logger.info("%s answered a question" % user.first_name)

    _newquestion = Question.t_questions()
    temp_question = _newquestion.GetQuestionByTopic(topics[current_topic])[0]
    temp_id =_newquestion.GetIDByQuestion(temp_question)[0]

    increment_question();

    _newanswer = Answer.t_answers()
    _newanswer.FillNewAnswer(user.id, temp_id, update.message.text)

    update.message.reply_text("Its your turn now! Ask me something...")

    return QUESTION

def increment_question():
    global current_question 
    current_question += 1

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)

    update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())

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

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("478466244:AAGx1DMPPeWhpwVnVwwqDM3pQk9IZZ_6xFw")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    filecheck('my_bot_database.db')

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(

        entry_points =  [CommandHandler('start', start)],

        states = {
            GENDER:     [MessageHandler(Filters.text, gender)],
                        #CommandHandler('skip', skip_gender)],

            AGE:        [MessageHandler(Filters.text, age)],
                        #CommandHandler('skip', skip_age)],

            LOCATION:   [MessageHandler(Filters.text, location)],
                        #CommandHandler('skip', skip_location)],

            QUESTION:   [MessageHandler(Filters.text, recieve_question)],

            ANSWER:     [MessageHandler(Filters.text, recieve_answer)], 
        },

        fallbacks =     [CommandHandler('cancel', cancel)]
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