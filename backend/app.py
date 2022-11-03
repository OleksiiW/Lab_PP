from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask('__name__')

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1111@localhost/oleksiydb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

