from DB import dbmodule as db
import base64, string, random
dbModule = db.DBModule(host='localhost',user='root',pswd='carrot24',db='BabyStepsDB')

class Users:
	def fetchUserById(self,id):
		query =  "select id, email, phone_no, address, api_token from user where id = %s"%id
		results = dbModule.selectStuff(query)[0]
		if not results:
			return {'response':"user not found"}
		user = {'id':results[0],'email':results[1],'phone_no':results[2],'address':results[3],'api_token':results[4]}
		return user

	def fetchUserByEmail(self, email):
		query =  "select id, email, phone_no, address, api_token from user where email = '%s'"%(email)
		results = dbModule.selectStuff(query)[0]
		if not results:
			return {'response':"user not found"}
		user = {'id':results[0],'email':results[1],'phone_no':results[2],'address':results[3],'api_token':results[4]}
		return user

	def fetchUserByPhone(self, phone):
		query =  "select id, email, phone_no, address, api_token from user where phone_no = '%s'"%phone
		results = dbModule.selectStuff(query)[0]
		if not results:
			return {'response':"user not found"}
		user = {'id':results[0],'email':results[1],'phone_no':results[2],'address':results[3],'api_token':results[4]}
		return user

	def create(self, email,phone,address,password):
		password = base64.b64encode(password)
		query = "insert into user (email,phone_no,address,password) values('%s','%s','%s','%s')"%(email,phone,address,password)
		if dbModule.insertToDB(query):
			return self.fetchUserByEmail(email)
		return {'response':'user creation failed'}

	def delete(self, id):
		query = "delete from user where id = %s"%id
		if dbModule.insertToDB(query):
			return {'status':'success'}
		return {'status':'failed'}

	def update(self, id,email=None,phone_no=None,address=None):
		count = False
		if email:
			if not dbModule.insertToDB("update user set email='%s' where id = %s"%(id,email)):
				count = False
			count = True
		if phone_no:
			if not dbModule.insertToDB("update user set phone_no='%s' where id = %s"%(id,phone_no)):
				count = False
			count = True
		if address:
			if not dbModule.insertToDB("update user set address='%s' where id = %s"%(id,address)):
				count = False
			count = True
		if count:
			return {'status':'sucess'}
		return {'status':'failed'}

	def signIn(self,email=None,phone=None,password=None):
		choice = ""
		if not email and not phone:
			return {'error','email or phone required'}
		if not password:
			return {'error','password required'}
		password = base64.b64encode(password)
		if email:
			choice = "email"
			query = "select * from user where email = '%s' and password = '%s'"%(email, password)
		if phone:
			choice = "phone_no"
			query = "select * from user where phone_no = '%s' and password = '%s'"%(phone, password)
		api_token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(30))
		if dbModule.selectStuff(query):
			if choice == 'phone_no':
				if not dbModule.insertToDB("update user set api_token = '%s' where %s = '%s'"%(api_token,choice,phone)):
					return {'error':'login failed'}
				return self.fetchUserByPhone(phone)
			else:
				if not dbModule.insertToDB("update user set api_token = '%s' where %s = '%s'"%(api_token,choice,email)):
					return {'error':'login failed'}
				return self.fetchUserByEmail(email)
		return {'error':'login failed'}

	def signOut(self, id):
		if dbModule.insertToDB("update user set api_token = null where id = %s"%id):
			return {'status':'success'}
		return {'status':'failed'}