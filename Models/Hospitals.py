#this models models gets data only
from DataBase import dbmodule as db
dbModule = db.Database()
from Validator import UserValidation as uv


def getAllHospitals():
	query = "select * from BSadmin_hospital"
	results = dbModule.selectStuff(query)
	if not results:
		return {'status':'failed','error':'no hospitals recorded'}
	hospitals = []
	for count,result in enumerate(results):
		hospitals.append({'id':result[0], 'name':result[1], 'location':result[2], 'address':result[3], 'telephone':result[4]})
	return hospitals

def getHospitalDoctors(hospital_id):
	query = "select * from BSadmin_hospital where id = %s"%hospital_id
	result = dbModule.selectStuff(query)
	if not result:
		return {'status':'failed','error':'hospial not found in records'}
	result = result[0]
	hospital = {'id':result[0], 'name':result[1], 'location':result[2], 'address':result[3], 'telephone':result[4]}
	query = "select id, fullname, email from BSadmin_doctor where hospital_id = %s"%hospital_id
	results = dbModule.selectStuff(query)
	doctors = []
	if results:
		for count,result in enumerate(results):
			doctors.append({'id':result[0], 'fullname':result[1], 'email':result[2]})
	hospital['doctors'] = doctors
	return {'status':'success', 'hospital':hospital}

def assignUserToDoctor(user_id, doctor_id):
	if not uv.loginStatus(user_id):
		return {'status':'failed', 'error':'user not logged in'}
	query = 'insert into user_doctors(user_id, doctor_id) values (%s,%s)'%(user_id,doctor_id)
	if dbModule.insertToDB(query):
		return {'status':'success', 'response':'user assign'}
	return {'status':'failed', 'response':'failed to assign user'}

def doctorProfile(doctor_id):
	query = "select fullname, email, hospital_id from BSadmin_doctor where id=%s"%doctor_id
	result = dbModule.selectStuff(query)
	if not result:
		return {'status':'failed', 'error':'record not found'}
	result = result[0]
	doctor = {'fullname':result[0], 'email':result[1]}
	hospital_id = result[2]
	query = "select name, location, address, telephone from BSadmin_hospital where id = %s"%(hospital_id)
	result = dbModule.selectStuff(query)
	hospital = []
	if result:
		result = result[0]
		hospital = {'name':result[0], 'location':result[1], 'address':result[2], 'telephone':result[3]}
	doctor['hospital'] = hospital
	return {'status':'success','doctor':doctor} 