from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import db
from routes.auth import auth_blueprint
from routes.companies import companies_blueprint

app = Flask(__name__)
app.config.from_object('config.Config') 


db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


migrate = Migrate(app, db)


app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
app.register_blueprint(companies_blueprint, url_prefix = '/api/companies')

if __name__ == "__main__":
    app.run(debug=True)
