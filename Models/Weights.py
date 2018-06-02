#weights
from DataBase import dbmodule as db
dbModule = db.Database()

def fetchWeights(user_id):
	query =  "select id, user_id, weight from weights where user_id = %s"%(user_id)
	results = dbModule.selectStuff(query)
	if not results:
		return {'status':'failed', 'error':'no records found for this user'}
	weights = []
	for weight in results:
		weights.append({'id':weight[0],'user_id':weight[1],'weight':weight[2]})
	return {'status':'success','weights':weights}

def fetchWeight(user_id,weight_id):
	query = "select id, user_id, weight from weights where user_id = %s and id=%s "%(user_id,weight_id)
	result = dbModule.selectStuff(query)
	if not result:
		return {'status':'failed', 'error':'record not found'}
	result =result[0]
	weight = {'id':result[0],'user_id':result[1],'weight':result[2]}
	return {'status':'success', 'weight':weight}

def create(user_id, weight):
	query = "insert into weights(user_id,weight) values (%s,%s)"%(user_id,weight)
	if dbModule.insertToDB(query):
		return {'status':'success','response':'record created successfully'}
	return {'status':'failed', 'error':'failed to create record'}

def edit(user_id, weight_id, weight):
	query = "select user_id from weights where id=%s"%(weight_id)
	user = dbModule.selectStuff(query)
	if not user or user[0][0] != str(user_id):
		return {'status':'failed','error':'users is unauthorized to modify this'}
	query = 'update weights set weight="%s" where id = %s'%(weight,weight_id)
	if dbModule.insertToDB(query):
		return {'status':'success', 'response':'edit was successfully recorded'}
	return {'status':'failed','error':'editing failed'}

def delete(user_id, weight_id):
	query = "select user_id from weights where id=%s"%(weight_id)
	user = dbModule.selectStuff(query)
	if not user or user[0][0] != str(user_id):
		return {'status':'failed','error':'users is unauthorized to modify this'}
	query = 'delete from weights where id=%s'%(weight_id)
	if dbModule.insertToDB(query):
		return {'status':'success','response':'recorded deleted'}
	return {'status':'failed','error':'delete unsuccessful'}