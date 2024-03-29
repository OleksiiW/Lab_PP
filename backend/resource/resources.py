import datetime

from backend.app import app
from backend.models.models import User, Bank, LoanSchema, Loan, UpdateUserSchema
from flask import jsonify, request
from marshmallow import ValidationError
# from backend.app import bcrypt
from backend.utils import admin_required
from flask_jwt_extended import jwt_required


@app.route('/user', methods=['PUT'])
@jwt_required()
@admin_required
def update_user():
    data = request.get_json()
    user = User.query.get(data["user_id"])
    if user:
        schema_user = UpdateUserSchema()
        try:
            schema_user.load(data)
        except ValidationError as err:
            return jsonify({"Validation errors": [err.messages[mesg][0] for mesg in err.messages]}), 405

        if "login" in data and User.find_by_login(data["login"]):
            return jsonify({'Error': f'User {data["login"]} already exists'}), 403

        if "passport_number" in data and User.find_by_passport_number(data["passport_number"]):
            return jsonify({'Error': f'User with passport number={data["passport_number"]} already exists'}), 403

        if "card_number" in data and User.find_by_card_number(data["card_number"]):
            return jsonify({'Error': f'User with card number={data["card_number"]} already exists'}), 403
        about_user = user.info[0]

        for info in data:
            if info == "phone_number":
                about_user.phone_number = data[info]
            elif info == "email":
                about_user.email = data[info]
            elif info == "date_of_birth":
                about_user.date_of_birth = data[info]
            elif info == "card_number":
                user.card_number = data[info]
            elif info == "passport_number":
                user.passport_number = data[info]
            elif info == "login":
                user.login = data[info]
            elif info == "full_name":
                user.full_name = data[info]

        user.save_to_db()
        return jsonify({'Message': 'User has been updated successfully.'})

    return jsonify({"Error": f"User with user id={data['user_id']} not found"}), 404


@app.route('/user/<user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"Error": f"User with user id={user_id} not found"}), 404
    about_user = user.info[0]

    user_data = {"login": user.login, "full_name": user.full_name,
                 "passport_number": user.passport_number, "card_number": user.card_number,
                 "date_of_birth": about_user.date_of_birth}
    if about_user.email:
        user_data["email"] = about_user.email
    if about_user.phone_number:
        user_data["phone_number"] = about_user.phone_number
    return jsonify(user_data)


@app.route('/user/<user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user_by_id(user_id: int):
    return User.delete_by_id(user_id)


@app.route('/user/loan/<user_id>', methods=['GET'])
@jwt_required()
def get_all_user_loans(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"Error": f"User with user id={user_id} not found"}), 404

    return jsonify({"loans": [Loan.get_loan_by_id(loan.loan_id) for loan in user.loans]})


@app.route('/bank/<bank_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_bank_reserve(bank_id: int):
    bank = Bank.query.get(bank_id)
    if not bank:
        return jsonify({"Error": f"Bank with bank id={bank_id} not found"}), 404

    return jsonify({"reserve": bank.reserve})


@app.route("/loan", methods=["POST"])
@jwt_required()
def create_loan():
    data = request.get_json()

    if int(data["debt"]) < 100:
        return jsonify({'Error': 'Еhe minimum amount is 100 hryvnias.'}), 406

    schema = LoanSchema()
    try:
        loan = schema.load(data)
    except ValidationError as err:
        return jsonify({"Validation errors": [err.messages[mesg][0] for mesg in err.messages]}), 405

    user = User.query.get(data["user_id"])
    user.loans.append(loan)
    bank = Bank.query.get(1)
    if bank.reserve >= data["debt"]:
        bank.reserve -= data["debt"]
    else:
        return jsonify({'Error': 'Bank has no reserve.'}), 402
    loan.save_to_db()

    return jsonify({'Message': 'Loan has been created successfully.'})


@app.route('/loan/<loan_id>', methods=['GET'])
@jwt_required()
def get_loan(loan_id: int):
    return Loan.get_loan_by_id(loan_id)


@app.route('/loan', methods=['GET'])
@jwt_required()
@admin_required
def get_all_loans():
    return jsonify({"loans": [Loan.get_loan_by_id(loan.loan_id) for loan in Loan.query.all()]})


@app.route('/loan', methods=['PUT'])
@jwt_required()
@admin_required
def update_loan():
    data = request.get_json()
    loan = Loan.query.get(data["loan_id"])
    if loan:
        debt = loan.debt
        bank = Bank.query.get(1)
        bank.reserve += int(data["debt"])
        if Loan.get_current_debt(data["loan_id"]) - int(data["debt"]) <= 0:
            Loan.delete_by_id(data["loan_id"])
            bank.save_to_db()
            return jsonify({'Message': 'Loan has been closed.'})
        else:
            loan_date = datetime.date(loan.date.year, loan.date.month, loan.date.day)
            loan.debt = debt - int(data["debt"])
            if (datetime.date.today() - loan_date).days >= 30:
                loan.date = datetime.date.today()
                loan.debt = Loan.get_current_debt(data["loan_id"])
            else:
                loan.date = loan.date

        loan.save_to_db()
        return jsonify({'Message': 'Loan has been updated successfully.'})
    return jsonify({"Error": f"Loan with loan id={data['loan_id']} not found"}), 404


@app.route('/loan/<loan_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_loan(loan_id: int):
    return Loan.delete_by_id(loan_id)
