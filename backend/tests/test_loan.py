from backend.app import db
from backend.models.models import Bank, Loan


def test_get_bank(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.get("/bank/1", headers=flask_login_admin)

    assert res.status_code == 200

    data = res.json

    assert data["reserve"] == 100000.0


def test_get_bank_error(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.get("/bank/10", headers=flask_login_admin)

    assert res.status_code == 404


def test_get_loan(app_with_data, flask_login):
    res = app_with_data.get("/loan/1", headers=flask_login)

    assert res.status_code == 200

    data = res.json

    assert data["debt"] == 10000.0


def test_get_loan_error(app_with_data, flask_login):
    res = app_with_data.get("/loan/10", headers=flask_login)

    assert res.status_code == 404


def test_update_loan(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.put("/loan", headers=flask_login_admin, json={
        "loan_id": "1",
        "debt": 1000
    })

    assert res.status_code == 200
    assert db.session.query(Loan).get(1).debt == 9000.0


def test_update_loan_error(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.put("/loan", headers=flask_login_admin, json={
        "loan_id": "19",
        "debt": 1000
    })

    assert res.status_code == 404


def test_create_loan(app_with_data, flask_login):
    res = app_with_data.post("/loan", headers=flask_login, json={
        "debt": 4000,
        "user_id": "1",
        "date": "2022-11-02"
    })

    assert res.status_code == 200
    assert db.session.query(Loan).get(2).debt == 4000.0


def test_create_loan_error(app_with_data, flask_login):
    res = app_with_data.post("/loan", headers=flask_login, json={
        "debt": 400000,
        "user_id": "1",
        "date": "2022-11-02"
    })

    assert res.status_code == 402


def test_create_loan_valerror(app_with_data, flask_login):
    res = app_with_data.post("/loan", headers=flask_login, json={
        "debt": 4000,
        "user_id": "1",
        "date": 47
    })

    assert res.status_code == 405


def test_delete_loan(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.delete("/loan/1", headers=flask_login_admin)

    assert res.status_code == 200
    assert len(db.session.query(Loan).all()) == 0


def test_delete_loan_error(app_with_data_admin, flask_login_admin):
    res = app_with_data_admin.delete("/loan/20", headers=flask_login_admin)

    assert res.status_code == 404
