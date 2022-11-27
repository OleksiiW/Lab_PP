from backend.app import app
from backend.models.models import User, UserSchema
from flask import jsonify, request
from marshmallow import ValidationError
from backend.app import bcrypt


@app.route("/user/register", methods=["POST"])
def register():
    data = request.get_json()

    # pw_hash = bcrypt.generate_password_hash(password=data['password'])
    data["password"] = bcrypt.generate_password_hash(password=data['password'])

    schema_user = UserSchema()
    try:
        user, about_user = schema_user.load(data)
    except ValidationError as err:
        return jsonify({"Validation errors": [err.messages[mesg][0] for mesg in err.messages]}), 405

    if User.find_by_login(data["login"]):
        return jsonify({'Error': f'User {data["login"]} already exists'}), 403

    if User.find_by_passport_number(data["passport_number"]):
        return jsonify({'Error': f'User with passport number={data["passport_number"]} already exists'}), 403

    if User.find_by_card_number(data["card_number"]):
        return jsonify({'Error': f'User with card number={data["card_number"]} already exists'}), 403

    user.bank_id = 1
    user.save_to_db()
    iduser = User.find_by_login(data["login"]).user_id
    about_user.user_id = iduser
    user.info.append(about_user)
    about_user.save_to_db()

    jwt_token = user.get_jwt()
    return jsonify({"access_token": jwt_token})


@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find_by_login(data["login"])

    if not user:
        return jsonify({'message': f'User {data["login"]} doesn\'t exist'}), 404

    if not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({'message': 'Wrong password'}), 403

    access_token = user.get_jwt()

    return jsonify({'message': f'Logged in as {data["login"]}', 'access_token': access_token})
