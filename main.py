from flask import Flask, Response, request, json, jsonify
from Models import Users as ur, Meals as ml, Posts as pst, Comments as cmt
app = Flask(__name__)

#users
@app.route('/register',methods=['POST'])
def register():
	email = request.args.get('email')
	phone = request.args.get('phone')
	address = request.args.get('address')
	password = request.args.get('password')
	password_confirm = request.args.get('password_confirm')
	if not email and not phone and not password and not password_confirm and not address:
		return jsonify({'error':'missing fields'})
	if not password == password_confirm:
		return jsonify({'error':'passwords do not match'})
	return jsonify(ur.Users().create(email,phone,address,password))

@app.route('/users',methods=['GET'])
def getUsers():
	return jsonify({'response':'build this'})

@app.route('/users/<int:id>',methods=['GET'])
def user(id):
	return jsonify(ur.Users().fetchUserById(id))

@app.route('/login', methods=['POST'])
def login():
	email = request.args.get('email')
	phone = request.args.get('phone')
	password = request.args.get('password')
	if not email and not phone:
		return jsonify({'status':'failed','error':'email or phone number required'})
	if not password:
		return jsonify({'status':'failed','error':'password required'}) 
	return jsonify(ur.Users().signIn(email=email, phone=phone, password=password))

@app.route('/logout/<int:user_id>', methods=['GET'])
def logout(user_id):
	return jsonify(ur.Users().signOut(user_id))

@app.route('/users/<int:id>',methods=['PUT','PATCH'])
def update(id):
	email = request.args.get('email')
	phone = request.args.get('phone')
	address = request.args.get('address')
	return jsonify(ur.Users().update(id,email=email,phone_no=phone,address=address))

#meals
@app.route('/meals',methods=['GET'])
def getMeals():
	return jsonify(ml.Meals().fetchAllMeals())

@app.route('/meals',methods=['POST'])
def meals():
	user_id = request.args.get('user_id')
	meal = request.args.get('meal')
	category = request.args.get('category')
	return jsonify(ml.Meals().createMeal(user_id=user_id, meal=meal, category=category))

@app.route('/users/<int:user_id>/meals', methods=['GET'])
def userMeals(user_id):
	return jsonify(ml.Meals().fetchMealsOfUser(user_id))

@app.route('/users/<int:user_id>/meals/<int:meal_id>', methods=['GET'])
def userMeal(user_id, meal_id):
	return jsonify(ml.Meals().fetchUserById(user_id, meal_id))

@app.route('/meals/<int:meal_id>',methods=['PUT','PATCH'])
def alterMeals(meal_id):
	user_id = request.args.get('user_id')
	meal = request.args.get('meal')
	category = request.args.get('category')
	return jsonify(ml.Meals().editMeal(user_id, meal_id, meal, category))

@app.route('/meals/<int:meal_id>',methods=['DELETE'])
def dropMeal(meal_id):
	user_id = request.args.get('user_id')
	return jsonify(ml.Meals().delete(user_id,meal_id))

#posts
@app.route('/posts',methods=['GET'])
def getPosts():
	return jsonify(pst.Posts().fetchAllPosts())

@app.route('/posts/<int:id>',methods=['GET'])
def getPost(id):
	print(id)
	return jsonify(pst.Posts().getPost(id))

@app.route('/posts',methods=['POST'])
def makePost():
	user_id = request.args.get('user_id')
	title = request.args.get('title')
	body = request.args.get('body')
	return jsonify(pst.Posts().create(user_id=user_id, title=title, body=body))

@app.route('/posts/<int:id>',methods=['PUT','PATCH'])
def editPost(id):
	user_id = request.args.get('user_id')
	title = request.args.get('title')
	body = request.args.get('body')
	return jsonify(pst.Posts().edit(id=id, user_id=user_id, title=title, body=body))

@app.route('/posts/<int:id>',methods=['DELETE'])
def dropPost(id):
	user_id = request.args.get('user_id')
	return jsonify(pst.Posts().delete(id=id, user_id=user_id))
#user posts
@app.route('/users/<int:ser_id>/posts',methods=['GET'])
def getUserPosts(user_id):
	return jsonify(pst.Posts().userPosts(user_id))

@app.route('/users/<int:user_id>/posts/<int:id>',methods=['GET'])
def getUserPost(user_id, id):
	return jsonify(pst.Posts().getPost(id,user_id))

#comments
@app.route('/comments',methods=['POST'])
def newComment():
	user_id = request.args.get('user_id')
	post_id = request.args.get('post_id')
	body = request.args.get('body')
	return jsonify(cmt.Comments().createPostComment(user_id,body,post_id))

@app.route('/comments/<int:id>',methods=['PUT','PATCH'])
def editComment(id):
	user_id = request.args.get('user_id')
	body = request.args.get('body')
	return jsonify(cmt.Comments().editComment(user_id, id, body))

@app.route('/comments/<int:id>',methods=['DELETE'])
def deleteComment(id):
		user_id = request.args.get('user_id')
		return jsonify(cmt.Comments().delete(user_id, id))


if __name__ == "__main__":
	app.run(debug=True)
