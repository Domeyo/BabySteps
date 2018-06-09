from DataBase import dbmodule as db
dbModule = db.Database()

class Meals:
	def fetchMealsById(self, user_id, meals_id):
		query = "select id, user_id, meal, category from meals where id = %s and user_id = %s "
		query = query%(meals_id, user_id)
		results = dbModule.selectStuff(query)
		if not results:
			return {'response':'meal not found'}
		results = results[0]
		meal={'meal_id':results[0],'user_id':results[1],'meal':results[2],'category':results[3]}
		return {'status':'success','meal':meal}

	def fetchAllMeals(self):
		query = "select id, user_id, meal, category from meals order by created_at desc"
		results = dbModule.selectStuff(query)
		if not results:
			return {'status':'failed','error':'no meals found'}
		meals=[]
		for i,result in enumerate(results):
			meals.append({'meal_id':result[0],'user_id':result[1],'meal':result[2],'category':result[3]})
		return {'status':'success', 'meals':meals }


	def fetchMealsOfUser(self, user_id):
		query = "select id,user_id, meal, category from meals where user_id = %s order by created_at desc"%user_id
		results = dbModule.selectStuff(query)
		if not results:
			return {'status':'failed','response':'meals not found'}
		meals = []
		for i,result in enumerate(results):
			meals.append({'meal_id':result[0],'user_id':result[1],'meal':result[2],'category':result[3]})
		return {'status':'success','meals':meals}

	def createMeal(self, user_id, meal, category):
		query = "insert into meals (user_id, meal, category) values (%s,'%s','%s')"%(user_id,meal,category)
		if dbModule.insertToDB(query):
			return {'status':'success','response':'meal created'}
		return  {'status':'failed','error':'meal creation failed'}

	def editMeal(self, user_id, meal_id, meal=None, category=None):
		commit = False
		query = "select user_id from meals where id = %s"%meal_id
		user = dbModule.selectStuff(query)
		if not user or user[0][0] != str(user_id):
			return {'status':'failed','error':'this user cannot update this'}
		if meal:
			query = "update meals set meal = '%s' where id = %s"%(meal,meal_id)
			if not dbModule.insertToDB(query):
				commit = False
			commit = True
		if category:
			query = "update meals set category = '%s' where id = %s"%(category,meal_id)
			if not dbModule.insertToDB(query):
				commit = False
			commit = True
		if commit:
			return {'status':'success','response':'meal update successfully'}
		return {'status':'failed','error':'failed to update meals'}

	def delete(self, user_id,meal_id):
		query = "select user_id from meals where id = %s"%meal_id
		user = dbModule.selectStuff(query)
		if not user or user[0][0] != str(user_id):
			return {'status':'failed','error':'this user cannot update this'}
		query = "delete from meals where id = %s"%meal_id
		if dbModule.insertToDB(query):
			return {'status':'success','response':'meal deleted'}
		return {'status':'failed','error':'failed to delete meal'}
	
	def foodList(self):
		query = "select week, food, nutrient from foodList"
		results = dbModule.selectStuff(query)
		if not results:
			return {'status':'failed', 'error':'records not found'}
		foods = []
		for result in results:
			foods.append({'week':result[0], 'food':result[1], 'nutrient':result[2]})
		return {'status':'success', 'food_list':foods}

	def foodListWeek(self,week):
		query = "select week, food, nutrient from foodList where week = %s"%week
		results = dbModule.selectStuff(query)
		if not results:
			return {'status':'failed', 'error':'records not found'}
		foods = []
		for result in results:
			foods.append({'week':result[0], 'food':result[1], 'nutrient':result[2]})
		return {'status':'success', 'food_list':foods}

