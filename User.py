import sqlite3
import Database

class t_users(Database.database):

    def FillNewUser(self, _id = "", _nationality = "", _age = 0, _gender = ""):
        db = sqlite3.connect("chatbox_database.db")
        db.execute('insert into users (ID, nationality, age, gender) values (?, ?, ?, ?)', (_id, _nationality.lower(), _age, _gender.lower()))

        db.commit()
        db.close()