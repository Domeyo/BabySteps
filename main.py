from flask import Flask, Response, request, json, jsonify
from Models import Users as ur, Meals as ml
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
@app.route('/meals',methods=['POST'])
def meals():
	user_id = requst.args.get('user_id')
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
	user_id = requst.args.get('user_id')
	meal = request.args.get('meal')
	category = request.args.get('category')
	return jsonify(ml.Meals().editMeal(user_id,meal_id,meal=meal,category=category))

@app.route('/meals/<int:meal_id>',methods=['DELETE'])
def dropMeal(meal_id):
	user_id = requst.args.get('user_id')
	return jsonify(ml.Meals().delete(user_id,meal_id))
	
if __name__ == "__main__":
	app.run(debug=True)
