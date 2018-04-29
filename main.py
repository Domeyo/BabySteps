from flask import Flask, Response, request, json, jsonify
from Models import Users as ur
app = Flask(__name__)


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

if __name__ == "__main__":
	app.run(debug=True)