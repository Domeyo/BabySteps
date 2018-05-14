from DB import dbmodule as db

class Database(db.DBModule):
	def __init__(self):
		super().__init__(host='localhost', user='root', pswd='carrot24', db='BabySteps')

