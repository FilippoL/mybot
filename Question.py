import sqlite3
import Database
import random

class t_questions(Database.database):

    def GetMaxQuestionByTopic(slef, _topic = ""):
        db = sqlite3.connect("chatbox_database.db")

        crsr = db.cursor()
        crsr = db.execute('select question from questions where topic = ? ', (_topic, ))

        questions_array = crsr.fetchall()
        result = len(questions_array)

        db.commit()
        db.close()
        return result

    def FillNewQuestion(self, _id = "", _question = "", _topic = ""):
        db = sqlite3.connect("chatbox_database.db")
        print (_topic)
        db.execute('insert into questions (ID, question, topic) values (?, ?, ?)', (_id, _question.lower(), _topic))
        db.commit()
        db.close()

    def GetQuestionByTopic(self, _topic = ""):
        db = sqlite3.connect("chatbox_database.db")
        crsr = db.cursor()
        crsr = db.execute('select question from questions where topic = ? ', (_topic, ))
        questions_array = crsr.fetchall()
        db.commit()
        db.close()
        result = len(questions_array)
        if result:
            question_str = questions_array[random.randint(0,result-1)]
            return question_str
        else:
            return False

    def GetIDByQuestion(self, _question = ""):
        db = sqlite3.connect("chatbox_database.db")

        crsr = db.cursor()
        crsr = db.execute('select ID from questions where question = ? ', (_question.lower(), ))

        id_str = crsr.fetchall()[0]

        db.commit()
        db.close()

        return id_str

    def AlreadyExistent(self, _question = ""):
        db = sqlite3.connect("chatbox_database.db")

        crsr = db.cursor()
        crsr.execute("select * from questions where question = ?", (_question.lower(),))

        result = len(crsr.fetchall())

        db.commit()
        db.close()

        if result == 0:
            return False
        else:
            return True
