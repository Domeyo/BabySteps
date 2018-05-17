from DataBase import dbmodule as db

dbModule = db.Database()

class Appointments:

	def fetchAll(self, user_id):
		query = "select id, user_id, description, date, time from appointments where user_id = %s order by created_at desc"%user_id
		results = dbModule.selectStuff(query)
		if not results:
			return {'status':'failed','error':'no appointments found for this user'}
		appointments = {}
		for count,result in enumerate(results):
			appointments['appointment(%s)'%count] = {'appointment_id':result[0], 'user_id':result[1], 'description':result[2],'date':result[3], 'time':result[4]}
		return {'status':'success', 'appointments':appointments}	

	def fetchAppointment(self, user_id, appointment_id):
		query = "select id, user_id, description, date, time from appointments where user_id = %s and id = %s"%(user_id, appointment_id)
		result = dbModule.selectStuff(query)
		if not result:
			return {'status':'failed','error':'no exercises found for this user'}
		result = result[0]
		appointment =  {'appointment_id':result[0], 'user_id':result[1], 'description':result[2], 'date':result[3], 'time':result[4]}
		return {'status':'success', 'appointment':appointment}

	def create(self, user_id, description, date, time):
		query = 'insert into appointments(user_id, description, date, time) values (%s, "%s","%s","%s")'%(user_id, description, date, time)
		if dbModule.insertToDB(query):
			return {'status':'success','response':'appointment recorded successfully'}
		return {'status':'failed','error':'failed while inserting data'}

	def edit(self, user_id, appointment_id, description, date, time):
		query = "select user_id from appointments where id=%s"%(appointment_id)
		user = dbModule.selectStuff(query)
		if not user or user[0][0] != str(user_id):
			return {'status':'failed','error':'users is unauthorized to modify this'}
		commit = False
		if description:
			query = 'update appointments set description = "%s" where id= %s'%(description,appointment_id)
			if dbModule.insertToDB(query):
				commit = True
		if date:
			query = 'update appointments set date = "%s" where id= %s'%(date,appointment_id)
			if dbModule.insertToDB(query):
				commit = True
		if time:
			query = 'update appointments set time = "%s" where id= %s'%(time,appointment_id)
			if dbModule.insertToDB(query):
				commit = True
		if commit:
			return {'status':'success','response':'edit successful'}
		return {'status':'failed','error':'edit failed'}

	def delete(self, user_id,appointment_id):
		query = "select user_id from appointments where id=%s"%(appointment_id)
		user = dbModule.selectStuff(query)
		if not user or user[0][0] != str(user_id):
			return {'status':'failed','error':'users is unauthorized to modify this'}
		query = "delete from appointments where id = %s"%appointment_id
		if dbModule.insertToDB(query):
			return {'status':'success','response':'delete successful'}
		return {'status':'failed', 'error':'delete failed'}  

