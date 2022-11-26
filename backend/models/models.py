from backend.app import db
from marshmallow import Schema, fields, validate, post_load
from flask import jsonify
import datetime
from flask_jwt_extended import create_access_token


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    passport_number = db.Column(db.String(20), nullable=False, unique=True)
    card_number = db.Column(db.String(30), nullable=False, unique=True)
    loans = db.relationship('Loan', backref='user', lazy=True)
    bank_id = db.Column(db.Integer(), db.ForeignKey('bank.bank_id', ondelete='CASCADE'))
    info = db.relationship("AboutUser", backref="user")

    role = db.Column(db.Enum("User", "Admin"), nullable=False, default="User")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_login(cls, login):
        return cls.query.filter_by(login=login).first()

    @classmethod
    def find_by_passport_number(cls, passport_number):
        return cls.query.filter_by(passport_number=passport_number).first()

    @classmethod
    def find_by_card_number(cls, card_number):
        return cls.query.filter_by(card_number=card_number).first()

    @classmethod
    def delete_by_id(cls, userid):
        if cls.query.get(userid):
            cls.query.filter_by(user_id=userid).delete()
            db.session.commit()

            return jsonify({'message': f'User with id={userid} was successfully deleted'})
        else:
            return jsonify({'error': f'User with id={userid} does not exist!'}), 404

    def get_jwt(self):
        access_token = create_access_token(identity=self.user_id)
        return access_token


class Loan(db.Model):
    __tablename__ = "loan"

    loan_id = db.Column(db.Integer, primary_key=True)
    debt = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.date.today())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id', ondelete='CASCADE'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_current_debt(cls, loan_id):
        loan = cls.query.get(loan_id)
        diff = datetime.date.today() - loan.date
        debt = loan.debt * (1.4) ** (diff.days // 30)
        return debt

    @classmethod
    def get_loan_by_id(cls, loan_id):
        loan = Loan.query.get(loan_id)
        if not loan:
            return {"Error": f"Loan with loan id={loan_id} not found"}, 404
        debt = Loan.get_current_debt(loan_id)
        data = {"date": loan.date, "debt": debt, "user_id": loan.user_id}
        return data

    @classmethod
    def delete_by_id(cls, loanid):
        if cls.query.get(loanid):
            cls.query.filter_by(loan_id=loanid).delete()
            db.session.commit()

            return jsonify({'message': f'Loan with id={loanid} was successfully deleted'})
        else:
            return jsonify({'error': f'Loan with id={loanid} does not exist!'}), 404


class Bank(db.Model):
    __tablename__ = "bank"

    bank_id = db.Column(db.Integer, primary_key=True)
    reserve = db.Column(db.Float, nullable=False)
    users = db.relationship('User', backref='bank', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class AboutUser(db.Model):
    __tablename__ = "about_user"

    about_user_id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    credit_history = db.Column(db.String(45))
    email = db.Column(db.String(45))
    phone_number = db.Column(db.String(20))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id', ondelete='CASCADE'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class UserSchema(Schema):
    login = fields.Str(validate=validate.Length(min=1, max=45), required=True)
    password = fields.Str(required=True)
    full_name = fields.Str(validate=validate.Length(min=1, max=45), required=True)
    passport_number = fields.Str(validate=validate.Regexp(r'^[0-9]{13}$', error="Not valid passport number"),
                                 required=True)
    card_number = fields.Str(
        validate=validate.Regexp(r'^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$', error="Not valid card number"),
        required=True)
    date_of_birth = fields.Date(required=True)
    email = fields.Email(validate=validate.Length(min=1, max=45), required=False)
    phone_number = fields.Str(validate=validate.Regexp(r'^[0-9]{12}$'), required=False)

    role = fields.Str(validate=validate.OneOf(['User', 'Admin']), required=False)

    def get_jwt(self):
        access_token = create_access_token(identity=self.iduser)
        return access_token

    @post_load
    def make_user(self, data, **kwargs):
        user_data = {"login": data["login"], "password": data["password"], "full_name": data["full_name"],
                     "passport_number": data["passport_number"], "card_number": data["card_number"],
                     "role": data["role"]}

        user_about_data = {"date_of_birth": data["date_of_birth"]}
        if "email" in data:
            user_about_data["email"] = data["email"]
        if "phone_number" in data:
            user_about_data["phone_number"] = data["phone_number"]

        return User(**user_data), AboutUser(**user_about_data)


class LoanSchema(Schema):
    date = fields.Date(required=False)
    debt = fields.Integer(required=True)
    user_id = fields.Integer(required=True)

    @post_load
    def make_loan(self, data, **kwargs):
        return Loan(**data)

class UpdateUserSchema(Schema):
    user_id = fields.Integer(required=True)
    login = fields.Str(validate=validate.Length(min=1, max=45), required=False)
    full_name = fields.Str(validate=validate.Length(min=1, max=45), required=False)
    passport_number = fields.Str(validate=validate.Regexp(r'^[0-9]{13}$', error="Not valid passport number"),
                                 required=False)
    card_number = fields.Str(
        validate=validate.Regexp(r'^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$', error="Not valid card number"),
        required=False)
    date_of_birth = fields.Date(required=False)
    email = fields.Email(validate=validate.Length(min=1, max=45), required=False)
    phone_number = fields.Str(validate=validate.Regexp(r'^[0-9]{12}$'), required=False)

    @post_load
    def make_user(self, data, **kwargs):
        return True
