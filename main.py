from flask import Flask, Response, request, json, jsonify
from Models import Users as ur, Meals as ml, Posts as pst, Comments as cmt, Appointments as apts, Exercises as exe, Hospitals as hsp
from Validator import EmailValidation as ev, UserValidation as uv 
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
		return jsonify({'status':'failed','error':'missing fields'})
	if not password == password_confirm:
		return jsonify({'status':'failed','error':'passwords do not match'})
	if not ev.validateFormat(email):
		return jsonify({'status':'failed','error':'invalid email format'})
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
	if not ev.validateFormat(email):
		return jsonify({'status':'failed','error':'invalid email format'}) 
	return jsonify(ur.Users().signIn(email=email, phone=phone, password=password))

@app.route('/logout/<int:user_id>', methods=['GET'])
def logout(user_id):
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(ur.Users().signOut(user_id))

@app.route('/users/<int:id>',methods=['PUT','PATCH'])
def update(id):
	email = request.args.get('email')
	phone = request.args.get('phone')
	address = request.args.get('address')
	if not email or not phone or not address:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(id):
                return jsonify({'status':'failed','error':'user not logged in'})
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
	if not user_id or not meal or not category:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(ml.Meals().createMeal(user_id=user_id, meal=meal, category=category))

@app.route('/users/<int:user_id>/meals', methods=['GET'])
def userMeals(user_id):
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(ml.Meals().fetchMealsOfUser(user_id))

@app.route('/users/<int:user_id>/meals/<int:meal_id>', methods=['GET'])
def userMeal(user_id, meal_id):
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(ml.Meals().fetchMealsById(user_id, meal_id))

@app.route('/meals/<int:meal_id>',methods=['PUT','PATCH'])
def alterMeals(meal_id):
	user_id = request.args.get('user_id')
	meal = request.args.get('meal')
	category = request.args.get('category')
	if not user_id or not meal or not category:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(ml.Meals().editMeal(user_id, meal_id, meal, category))

@app.route('/meals/<int:meal_id>',methods=['DELETE'])
def dropMeal(meal_id):
	user_id = request.args.get('user_id')
	if not user_id:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(ml.Meals().delete(user_id,meal_id))

#posts
@app.route('/posts',methods=['GET'])
def getPosts():
	return jsonify(pst.Posts().fetchAllPosts())

@app.route('/posts/<int:id>',methods=['GET'])
def getPost(id):
	return jsonify(pst.Posts().getPost(id))

@app.route('/posts',methods=['POST'])
def makePost():
	user_id = request.args.get('user_id')
	title = request.args.get('title')
	body = request.args.get('body')
	if not user_id or not title or not body:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(pst.Posts().create(user_id=user_id, title=title, body=body))

@app.route('/posts/<int:id>',methods=['PUT','PATCH'])
def editPost(id):
	user_id = request.args.get('user_id')
	title = request.args.get('title')
	body = request.args.get('body')
	if not user_id or not title or not body:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(pst.Posts().edit(id=id, user_id=user_id, title=title, body=body))

@app.route('/posts/<int:id>',methods=['DELETE'])
def dropPost(id):
	user_id = request.args.get('user_id')
	if not user_id:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(pst.Posts().delete(id=id, user_id=user_id))

#user posts
@app.route('/users/<int:ser_id>/posts',methods=['GET'])
def getUserPosts(user_id):
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(pst.Posts().userPosts(user_id))

@app.route('/users/<int:user_id>/posts/<int:id>',methods=['GET'])
def getUserPost(user_id, id):
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(pst.Posts().getPost(id,user_id))

#comments
@app.route('/comments',methods=['POST'])
def newComment():
	user_id = request.args.get('user_id')
	post_id = request.args.get('post_id')
	body = request.args.get('body')
	if not user_id or not post_id or not body:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(cmt.Comments().createPostComment(user_id,body,post_id))

@app.route('/comments/<int:id>',methods=['PUT','PATCH'])
def editComment(id):
	user_id = request.args.get('user_id')
	body = request.args.get('body')
	if not user_id or not body:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(cmt.Comments().editComment(user_id, id, body))

@app.route('/comments/<int:id>',methods=['DELETE'])
def deleteComment(id):
	user_id = request.args.get('user_id')
	if not user_id:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})

	return jsonify(cmt.Comments().delete(user_id, id))

#appointments
@app.route('/users/<int:user_id>/appointments')
def getAppointments(user_id):
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(apts.Appointments().fetchAll(user_id))

@app.route('/users/<int:user_id>/appointments/<int:appointment_id>')
def getAppointment(user_id, appointment_id):
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(apts.Appointments().fetchAppointment(user_id,appointment_id))

@app.route('/appointments', methods=['POST'])
def makeAppointment():
	user_id = request.args.get('user_id')
	description = request.args.get('description')
	date = request.args.get('date')
	time = request.args.get('time')
	if not user_id or not description or not date or not time:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(apts.Appointments().create(user_id, description, date, time))


@app.route('/appointments/<int:appointment_id>', methods=['PUT','PATCH'])
def editAppointment(appointment_id):
	user_id = request.args.get('user_id')
	description = request.args.get('description')
	date = request.args.get('date')
	time = request.args.get('time')
	if not user_id:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(apts.Appointments().edit(user_id, appointment_id, description, date, time))

@app.route('/appointments/<int:appointment_id>',methods=['DELETE'])
def deleteAppointment(appointment_id):
	user_id = request.args.get('user_id')
	if not user_id:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(apts.Appointments().delete(user_id,appointment_id))

#Exercise
@app.route('/users/<int:user_id>/exercises')
def getExercises(user_id):
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(exe.Exercises().fetchAll(user_id))

@app.route('/users/<int:user_id>/exercises/<int:exercise_id>')
def getExercise(user_id, exercise_id):
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(exe.Exercises().fetchExercise(user_id,exercise_id))

@app.route('/exercises', methods=['POST'])
def makeExercise():
	user_id = request.args.get('user_id')
	exercise = request.args.get('exercise')
	duration = request.args.get('duration')
	if not user_id or not exercise or not duration:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(exe.Exercises().create(user_id, exercise))


@app.route('/exercises/<int:exercise_id>', methods=['PUT','PATCH'])
def editExercise(exercise_id):
	user_id = request.args.get('user_id')
	exercise = request.args.get('exercise')
	duration = request.args.get('duration')
	if not user_id:
		return jsonify({'status':'failed','error':'missing fields'})
	return jsonify(exe.Exercises().edit(user_id, exercise_id, exercise, duration))

@app.route('/exercises/<int:exercise_id>',methods=['DELETE'])
def deleteExercise(exercise_id):
	user_id = request.args.get('user_id')
	if not user_id:
		return jsonify({'status':'failed','error':'missing fields'})
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(exe.Exercises().delete(user_id, exercise_id))

#weight



#hospital
@app.route('/hospitals',methods=['GET'])
def getHospitals():
	return jsonify(hsp.getAllHospitals())

@app.route('/hospitals/<int:hospital_id>')
def getHospitalDetail(hospital_id):
	return jsonify(hsp.getHospitalDoctors(hospital_id))

@app.route('/assignDoctor',methods=['POST'])
def assign():
	user_id = request.args.get('user_id')
	doctor_id = request.args.get('doctor_id')
	if not user_id or not doctor_id:
		return {'status':'failed', 'error':'missing fields'}
	if not uv.loginStatus(user_id):
                return jsonify({'status':'failed','error':'user not logged in'})
	return jsonify(hsp.assignUserToDoctor(user_id, doctor_id))

@app.route('/doctor_profile/<int:doctor_id>')
def docProfile(doctor_id):
	return jsonify(hsp.doctorProfile(doctor_id))

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="5000", debug=True)
