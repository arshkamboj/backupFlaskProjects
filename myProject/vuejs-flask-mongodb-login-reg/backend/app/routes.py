from flask import request, jsonify, url_for
from app import app
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime
from werkzeug.utils import secure_filename

# from app.models import tbl_users2
from app.models import mongo, bcrypt


@app.route('/users/register', methods=['POST'])
def register():
    users = mongo.db.users
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    user_id = users.insert({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'created': created
    })

    new_user = users.find_one({'_id': user_id})

    result = {'email': new_user['email'] + ' registered'}

    return jsonify({'result': result})


@app.route('/users/updateProfile', methods=['POST'])
def updateProfile():
    users = mongo.db.users2
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        mongo.save_file(profile_image.filename, profile_image)
        mongo.db.users.insert({'email': request.form.get('username'), 'profile_image_name': profile_image.filename})

    return "Done!"


'''
    user_id = users.insert({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'created': created
    })
'''


# new_user = users.find_one({'_id': user_id})

# result = {'email': new_user['email'] + ' registered'}

# return jsonify({'result' : result})


@app.route('/users/login', methods=['POST'])
def login():
    users = mongo.db.users
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""

    response = users.find_one({'email': email})

    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity={
                'first_name': response['first_name'],
                'last_name': response['last_name'],
                'email': response['email']
            })
            result = jsonify({"token": access_token})
        else:
            result = jsonify({"error": "Invalid username and password"})
    else:
        result = jsonify({"result": "No results found"})
    return result


@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    user = mongo.db.users3.find_one_or_404({'username': username})
    return f'''
            <h1>{username}</h1>
            <image src="{url_for('file', filename=user['profile_image_name'])}">
           '''


@app.route('/profile/upload')
def upload():
    return '''
            <form method="POST" action="/create" enctype="multipart/form-data" >
            <input type="text" name="username">
            <input type="file" name="profile_image">
            <input type="submit">
           '''


@app.route('/create', methods=['POST'])
def create():
    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        mongo.save_file(profile_image.filename, profile_image)
        mongo.db.users3.insert({'username': request.form.get('username'), 'profile_image_name': profile_image.filename})

    return "Done!"


'''
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = tbl_users2.get_or_none(tbl_users2.user_name == username, tbl_users2.user_password == password)

    if user is None:
        return jsonify({'success': False, 'message': 'Bad username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'success': True, 'token': access_token}), 200


@app.route('/verify-token', methods=['POST'])
@jwt_required
def verify_token():
    return jsonify({'success': True}), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
'''
