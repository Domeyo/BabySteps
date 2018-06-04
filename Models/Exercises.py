from DataBase import dbmodule as db

dbModule = db.Database()

class Exercises:
	def fetchAll(self,user_id):
		query = "select id, user_id, exercise, duration from exercises where user_id = %s order by created_at desc"%user_id
		results = dbModule.selectStuff(query)
		if not results:
			return {'status':'failed','error':'no exercises found for this user'}
		exercises = []
		for count,result in enumerate(results):
			exercises.append({'exercise_id':result[0], 'user_id':result[1], 'exercise':result[2], 'duration':result[3]})
		return {'status':'success', 'exercises':exercises}	

	def fetchExercise(self, user_id, exercise_id):
		query = "select id, user_id, exercise, duration from exercises where user_id = %s and id = %s order by created_at desc"%(user_id,exercise_id)
		result = dbModule.selectStuff(query)
		if not result:
			return {'status':'failed','error':'no exercises found for this user'}
		result = result[0]
		exercise =  {'exercise_id':result[0], 'user_id':result[1], 'exercise':result[2], 'duration':result[3]}
		return {'status':'success', 'exercise':exercise}

	def create(self, user_id, exercise, duration):
		query = 'insert into exercises(user_id, exercise, duration) values (%s, "%s", "%s")'%(user_id,exercise, duration)
		if dbModule.insertToDB(query):
			return {'status':'success','response':'exercise recorded successfully'}
		return {'status':'failed','error':'failed while inserting data'}

	def edit(self, user_id,exercise_id,exercise, duration):
		query = "select user_id from exercises where id=%s"%(exercise_id)
		user = dbModule.selectStuff(query)
		if not user or user[0][0] != str(user_id):
			return {'status':'failed','error':'users is unauthorized to modify this'}
		count = False
		if exercise:
			query = 'update exercises set exercise="%s" where id = %s'%(exercise,exercise_id)
			if dbModule.insertToDB(query):
				count = True
		if duration:
			query = 'update exercises set duration="%s" where id = %s'%(duration, exercise_id)
			if dbModule.insertToDB(query):
				count = True
		if count:
			return {'status':'success','response':'editing successful'}
		return {'status':'failed','error':'editing failed'}

	def delete(self, user_id, exercise_id):
		query = "select user_id from exercises where id=%s"%(exercise_id)
		user = dbModule.selectStuff(query)
		if not user or user[0][0] != str(user_id):
			return {'status':'failed','error':'users is cannot delete this'}
		query = "delete from exercises where id = %s"%(exercise_id)
		if dbModule.insertToDB(query):
			return {'status':'success', 'response':'delete successful'}
		return {'status':'failed', 'error':'delete failed'}
		
