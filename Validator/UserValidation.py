#This package has the likely to get bigger
from DataBase import dbmodule as db
dbModule = db.Database()

def loginStatus(user_id):
	query = "select api_token from users where id = %s"%user_id
	result = dbModule.selectStuff(query)
	if not result:
		return False
	result = result[0][0]
	print(result)
	if result == 'None':
		return False
	return True
