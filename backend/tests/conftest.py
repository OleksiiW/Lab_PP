import pytest

from backend.app import app, db, bcrypt
from backend.models.models import User, AboutUser, Loan, Bank
from sqlalchemy import delete


@pytest.fixture(scope="session")
def flask_app():
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture(scope="session")
def app_with_db(flask_app):
    db.create_all()

    yield flask_app

    db.session.commit()
    db.drop_all()


@pytest.fixture
def app_with_data(app_with_db):
    bank = Bank(
        # bank_id="1",
        reserve="100000"
    )

    user = User(user_id="1",
                login="genius228",
                password=bcrypt.generate_password_hash(password="12345678"),
                full_name="whoasked",
                passport_number="1234667891482",
                card_number="1234-4894-5897-7152"
                )

    about_user = AboutUser(date_of_birth="2004-11-06",
                           email="dmitrslusarcuk@gmail.com",
                           phone_number="380673530318",
                           user_id="1"
                           )

    loan = Loan(
        loan_id="1",
        debt="10000",
        user_id="1",
        date="2022-11-02"
    )

    db.session.add(bank)
    db.session.add(user)
    db.session.add(about_user)
    db.session.add(loan)

    db.session.commit()

    yield app_with_db

    db.session.execute(delete(AboutUser))
    db.session.execute(delete(User))
    db.session.commit()


@pytest.fixture()
def flask_login(app_with_data):
    res = app_with_data.post("/user/login", json={"login": "genius228", "password": "12345678"})

    jwt = res.json["access_token"]
    return {"Authorization": f"Bearer {jwt}"}


@pytest.fixture
def app_with_data_admin(app_with_db):
    bank = Bank(
        # bank_id="1",
        reserve="100000"
    )

    user = User(user_id="1",
                login="genius228admin",
                password=bcrypt.generate_password_hash(password="12345678"),
                full_name="whoasked",
                passport_number="1234667891482",
                card_number="1234-4894-5897-7152",
                role="Admin"
                )

    about_user = AboutUser(date_of_birth="2004-11-06",
                           email="dmitrslusarcuk@gmail.com",
                           phone_number="380673530318",
                           user_id="1"
                           )

    loan = Loan(
        loan_id="1",
        debt="10000",
        user_id="1",
        date="2022-11-02"
    )

    db.session.add(bank)
    db.session.add(user)
    db.session.add(about_user)
    db.session.add(loan)

    db.session.commit()

    yield app_with_db

    db.session.execute(delete(User))
    db.session.commit()


@pytest.fixture()
def flask_login_admin(app_with_data_admin):
    res = app_with_data_admin.post("/user/login", json={"login": "genius228admin", "password": "12345678"})

    jwt = res.json["access_token"]
    return {"Authorization": f"Bearer {jwt}"}