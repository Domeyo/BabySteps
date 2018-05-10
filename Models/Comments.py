from DB import dbmodule as db
dbModule = db.DBModule(host='localhost',user='root',pswd='carrot24', db='BabyStepsDB')

class Comments(object):
	def createPostComment(self, user_id, body, post_id):
		query = "insert into comments (user_id, post_id, body) values (%s,'%s',%s)"%(user_id,body,post_id)
		if dbModule.insertToDB(query):
			return {'status':'success','response':'post created success fully'}
		return {'status':'failed','error':'could not make comments'}

	def editComment(self, user_id, comment_id, body):
		query = "select user_id from comments where user_id = %s and id = %s"%(user_id,comment_id)
		user = dbModule.selectStuff(query)
		if user[0] != user_id:
			return {'status':'failed','error':'this user cannot edit this comment'}
		query = "update comments set body = '%s' where id = '%s'"%comment_id
		if dbModule.insertToDB(query):
			return {'status':'success','response':'comment modified'}
		return {'status':'failed','error':'failed to edit comment'}

	def delete(self, user_id, id):
		query = "select user_id from comments where user_id = %s and id = %s"%(user_id,id)
                user = dbModule.selectStuff(query)
                if user[0] != user_id:
                        return {'status':'failed','error':'this user cannot edit this comment'}
		query = "delete from comments where id = %s"%id
		if dbModule.insertToDB(query):
                        return {'status':'success','response':'comment modified'}
                return {'status':'failed','error':'failed to edit comment'}


#class Bookmarks:
