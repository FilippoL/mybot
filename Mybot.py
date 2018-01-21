#!/usr/bin/env python
# -*- coding: utf-8 -*-


from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)


import logging
import uuid
import os

import Database
import Question
import Answer
import User
import PhraseManager

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

topics = ("hobbies", "time", "music", "love", "work", "food", "persons", "animals", "learning", "goals", "dreams", "shopping", "money", "politics", "news", "cooking", "sports")

current_topic = ""
current_question = 0

filled = False

GENDER, AGE, LOCATION, QUESTION, ANSWER = range(5)


def toggleFilled():
    global filled
    filled = True

def start(bot, update):
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text('Hi! My name is AnswerMyQuestion Bot')
    update.message.reply_text('I will be asking you few question just before we start our conversation')
    update.message.reply_text('Honesty is appreciated :)')
    #update.message.reply_text('Remember to send /skip if you dont want to answer them')


    update.message.reply_text('Are you a boy or a girl?', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return GENDER


def gender(bot, update):
    user = update.message.from_user
    logger.info("Gender of %s: %s" % (user.first_name, update.message.text))

    final = str(user.id) + ".txt"

    with open(final, "w") as _file:
        _file.write("%s\n" % (update.message.text))
        _file.close()

    update.message.reply_text('Cool! How old are you?', reply_markup=ReplyKeyboardRemove())

    return AGE

def age(bot, update):
    user = update.message.from_user
    logger.info("Age of %s: %s" % (user.first_name, update.message.text))

    final = str(user.id) + ".txt"

    with open(final, "a") as _file:
        _file.write("%s\n" % (update.message.text))
        _file.close()

    update.message.reply_text('Thanks! Now, where are you from?')

    return LOCATION


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

    if filled:
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
                _newuser.FillNewUser(str(_user.id), str(lines[2]), str(lines[1]), str(lines[0]))

                _file.close()
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        logger.warn("ERROR")

    os.remove(final)
    toggleFilled()
    return check_question(_user,_update)

def check_question(_user,_update):
    _newquestion = Question.t_questions()
    _phrase = PhraseManager.Phrase()
    if _phrase.IsAQuestion(_update.message.text):
        _guessed_result = _phrase.GuessTopic(_update.message.text)
        if current_topic != topics[_guessed_result]:
            set_cur_topic(topics[_guessed_result])

        if(_newquestion.AlreadyExistent(_update.message.text)):
            return answer_question(_user,_update)
        else:
            return filling_question(_user,_update)
    else:
        _update.message.reply_text('I cant answer statemets yet. Ask a question :)')
        return QUESTION


def filling_question(_user,_update):

    _newquestion = Question.t_questions()
    _newquestion.FillNewQuestion(str(uuid.uuid4()), _update.message.text, current_topic)

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
    if _newquestion.GetQuestionByTopic(current_topic)[0]:
        _update.message.reply_text(_newquestion.GetQuestionByTopic(current_topic)[0])
        return ANSWER
    else:
        _update.message.reply_text("Dont really know what to say about " + current_topic)
        update.message.reply_text("Its your turn now! Ask me something...")
        return QUESTION


def recieve_answer(bot, update):
    user = update.message.from_user
    logger.info("%s answered a question" % user.first_name)
    _newquestion = Question.t_questions()

    increment_question();

    if current_question >= _newquestion.GetMaxQuestionByTopic(current_topic):
        reset_question()
        #ASK IF WE CAN CHANGE TOPIC CAUSE WE RUN OUT


    temp_question = _newquestion.GetQuestionByTopic(current_topic)[0]
    temp_id =_newquestion.GetIDByQuestion(temp_question)[0]

    _newanswer = Answer.t_answers()
    _newanswer.FillNewAnswer(user.id, temp_id, update.message.text)

    update.message.reply_text("Its your turn now! Ask me something...")

    return QUESTION

def increment_question():
    global current_question
    current_question += 1

def reset_question():
    global current_question
    current_question = 0

def set_cur_topic(_curr):
    global current_topic
    current_topic = _curr


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
            GENDER:     [MessageHandler(Filters.all, gender)],
                        #CommandHandler('skip', skip_gender)],

            AGE:        [MessageHandler(Filters.all, age)],
                        #CommandHandler('skip', skip_age)],

            LOCATION:   [MessageHandler(Filters.all, location)],
                        #CommandHandler('skip', skip_location)],

            QUESTION:   [MessageHandler(Filters.all, recieve_question)],

            ANSWER:     [MessageHandler(Filters.all, recieve_answer)],
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
