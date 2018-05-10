from DB import dbmodule as db
dbModule = db.DBModule(host='localhost',user='root',pswd='carrot24', db='BabyStepsDB')

class Posts(object):
	def fetchAllPosts(self):
		query = "select id, user_id, title, body from posts order by created_at desc"
		results = dbModule.selectStuff(query)
		if not results:
			return {'status':'failed','error':'no posts found'}
		posts = {}
		for count,result in enumerate(results):
			posts["post(%s)"%count] = {'id':result[0],'user_id':result[1],'title':result[2],'body':result[3]}
		return {'status':'success','posts':posts}

	def userPosts(self, user_id):
		query = "select id, user_id, title, body from posts where user_id=%s order by created_at desc"%id
		results = dbModule.selectStuff(query)
		if not results:
                        return {'status':'failed','error':'no posts found'}
                posts = {}
                for count,result in enumerate(results):
                        posts["post(%s)"%count] = {'id':result[0],'user_id':result[1],'title':result[2],'body':result[3]}
                return {'status':'success','posts':posts}

	def getPost(self, id, user_id=None):
		if not user_id:
			query = "select id, user_id, title, body from posts where id = %s"
		else:
			query = "select id, user_id, title, body from posts where user_id = %s and id = %s"%(user_id,id)
		result = dbModule.selectStuff(query)
		if not result:
			return {'status':'failed','error':'no post found for this id='%id}
		post = {'id':result[0],'user_id':result[1],'title':result[2],'body':result[3]}
		query = "select id, user_id, post_id, comment_id, body from comments where post_id=%s"%result[0]
		results = dbModule.selectStuff(query)
		comments={}
		for count, result in enumerate(results):
			comments['comment(%s)'%count] = {'id':result[0], 'user_id':result[1], 'post_id':result[2], 'comment_id':result[3], 'body':result[4]}
		post['comments'] = comments
		return {'status':'success','post':posts}

	def create(self, user_id, title, body):
		query = "insert into (user_id, title, body) posts values (%s,'%s','%s')"%(user_id,title,body)
		if dbModule.insertToDB(query):
			return {'status':'success','response':'posts created successfully'}
		return {'status':'failed','error':'post creation failed'}

	def edit(self, id, title=None, body=None):
		query = "select user_id from posts where id = %s"%id
                user = dbModule.selectStuff(query)
                if user[0] != str(user_id):
                        return {'status':'failed','error':'this user cannot update this'}

		if not title and not body:
			return {'status':'failed','error':'no field to update'}
		commit = False
		if title:
			query = "update posts set title = '%s' where id = %s"%(title, id)
			if dbModule.insertToDB(query):
				commit = True
		if body:
			query = "update posts set body = '%s' where id = %s"%(body,id)
			if dbModule.insertToDB(query):
				commit = True
		if commit:
			return {'status':'success','response':'post modified'}
		return {'status':'failed','error':'failed to modify post'}

	def delete(self,id,user_id):
		query = "select user_id from posts where id = %s"%id
		user = dbModule.selectStuff(query)
		if user[0] != str(user_id):
			return {'status':'failed','error':'this user cannot delete this'}
		query = "delete from posts where id = %s"%id
		if dbModule.insertToDB(query):
			return {'status':'success','response':'post deleted'}
		return {'status':'failed','error':'deletion of this post failed'}
