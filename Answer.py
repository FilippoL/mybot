import sqlite3
import Database
import random

class t_answers(Database.database):

    def FillNewAnswer(self, _id = "", _id_question = "", _answer = ""):
        db = sqlite3.connect("chatbox_database.db")
        db.execute('insert into answers (ID_one, ID_two, answer) values (?, ?, ?)', (_id, _id_question, _answer.lower()))

        db.commit()
        db.close()

    def GetAnswerByQuestionID(self, _id = ""):
        db = sqlite3.connect("chatbox_database.db")

        crsr = db.cursor()
        crsr = db.execute('select answer from answers where ID_two = ? ', (_id, ))

        answers_array = crsr.fetchall()
        result = len(answers_array)
        answer_str = answers_array[random.randint(0,result-1)]

        db.commit()
        db.close()

        return answer_str

    def AlreadyExistent(self, _id = ""):
        db = sqlite3.connect("chatbox_database.db")

        crsr = db.cursor()
        crsr.execute("select * from answers where ID_two = ?", (_id,))

        result = len(crsr.fetchall())

        db.commit()
        db.close()

        if result == 0:
            return False
        else:
            return True