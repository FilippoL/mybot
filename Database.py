import sqlite3

class database:
    def __init__(self):#this is a contrucstor
        db = sqlite3.connect("chatbox_database.db")
        
        db.row_factory = sqlite3.Row
        db.execute('CREATE TABLE IF NOT EXISTS users ( ID text, nationality text, age int, gender text )')
        db.execute('CREATE TABLE IF NOT EXISTS questions ( ID text, question text, topic text )')
        db.execute('CREATE TABLE IF NOT EXISTS answers ( ID_one text, ID_two text, answer text )')

        db.commit()
        db.close()

    #def __iter__(self):
    #    db = sqlite3.connect("my_bot_database.db")

    #    crsr = db.execute('select * from users')

    #    for row in crsr:
    #        yield dict(row)

    #    db.commit()
    #    db.close()

    #def get_property(self, key):
    #        return self.user_prop.get(None, key)