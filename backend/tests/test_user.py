from backend.app import db
from backend.models.models import User


def test_get_user(app_with_data, flask_login):
    res = app_with_data.get("/user/1", headers=flask_login)

    assert res.status_code == 200

    data = res.json

    assert data["login"] == "genius228"


def test_get_user_error(app_with_data, flask_login):
    res = app_with_data.get("/user/10", headers=flask_login)

    assert res.status_code == 404


def test_register_user(app_with_data):
    res = app_with_data.post("/user/register", json={
        "user_id": "2",
        "login": "login2",
        "password": "54321",
        "full_name": "ftgyihujiko",
        "passport_number": "1234667671482",
        "card_number": "1234-4894-1297-7152",
        "date_of_birth": "2004-12-06",
        "email": "dfghjkl@gmail.com",
        "phone_number": "380903530318"
    })

    assert res.status_code == 200
    assert db.session.query(User).get(2).login == "login2"


def test_register_user_error(app_with_data):
    res = app_with_data.post("/user/register", json={
        "user_id": "3",
        "login": "genius228",
        "password": "54321",
        "full_name": "ftgyihujiko",
        "passport_number": "1234667671482",
        "card_number": "1234-4894-1297-7152",
        "date_of_birth": "2004-12-06",
        "email": "dfghjkl@gmail.com",
        "phone_number": "380903530318"
    })

    assert res.status_code == 403


def test_register_user_valerror(app_with_data):
    res = app_with_data.post("/user/register", json={
        "user_id": "3",
        "login": "genius228",
        "password": "54321",
        "full_name": "ftgyihujiko",
        "passport_number": "1234667671482",
        "card_number": "1234-4894-1297-7152",
        "date_of_birth": "2004-12-06",
        "email": "dfghjkl@gmail.com",
        "phone_number": 15
    })

    assert res.status_code == 405


def test_update_user(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.put("/user", headers=flask_login_admin, json={
        "user_id": "1",
        "login": "notgenius228admin",
        "full_name": "iasked"
    })

    assert res.status_code == 200
    assert db.session.query(User).get(1).full_name == "iasked"


def test_update_user_error(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.put("/user", headers=flask_login_admin, json={
        "user_id": "10",
        "login": "notgenius228admin",
        "full_name": "iasked"
    })

    assert res.status_code == 404


def test_update_user_valerror(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.put("/user", headers=flask_login_admin, json={
        "user_id": "1",
        "login": "notgenius228admin",
        "full_name": 5
    })

    assert res.status_code == 405


def test_update_user_error2(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.put("/user", headers=flask_login_admin, json={
        "user_id": "1",
        "login": "genius228admin",
        "full_name": "whosked"
    })

    assert res.status_code == 403


def test_delete_user(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.delete("/user/1", headers=flask_login_admin)

    assert res.status_code == 200
    assert len(db.session.query(User).all()) == 0


def test_delete_user_error(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.delete("/user/10", headers=flask_login_admin)

    assert res.status_code == 404


def test_get_users_loan(app_with_data, flask_login):
    res = app_with_data.get("/user/loan/1", headers=flask_login)

    assert res.status_code == 200

    data = res.json

    assert data["loans"][0]["debt"] == 10000.0


def test_get_users_loan_error(app_with_data, flask_login):
    res = app_with_data.get("/user/loan/10", headers=flask_login)

    assert res.status_code == 404
