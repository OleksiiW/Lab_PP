from backend.app import db


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    full_name = db.Column(db.String(45), nullable=False)
    passport_number = db.Column(db.String(45), nullable=False, unique=True)
    card_number = db.Column(db.String(45), nullable=False, unique=True)
    loans = db.relationship('Loan', backref='user', lazy=True)
    bank_id = db.Column(db.Integer(), db.ForeignKey('bank.bank_id', ondelete='CASCADE'))
    rating = db.relationship("AboutUser", back_populates="user")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Loan(db.Model):
    __tablename__ = "loan"

    loan_id = db.Column(db.Integer, primary_key=True)
    debt = db.Column(db.DECIMAL, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id', ondelete='CASCADE'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Bank(db.Model):
    __tablename__ = "bank"

    bank_id = db.Column(db.Integer, primary_key=True)
    reserve = db.Column(db.Integer, nullable=False)
    users = db.relationship('User', backref='bank', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class AboutUser(db.Model):
    __tablename__ = "about_user"

    about_user_id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column(db.String(45), nullable=False)
    credit_history = db.Column(db.String(45))
    email = db.Column(db.String(45))
    phone_number = db.Column(db.String(45))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id', ondelete='CASCADE'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
