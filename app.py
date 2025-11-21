from flask import Flask
from database import init_db

#Employee
from controller.employee.create import create_bp
from controller.employee.delete import delete_bp
from controller.employee.update import update_bp
from controller.employee.get import get_bp

#Payroll
from controller.payroll.create import payroll_create_bp

app = Flask(__name__)

#Point SQLAlchemy to your SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/iotexpert/Documents/web-dev/python/my-flask-9/database/myimab.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Initialize DB
init_db(app)

#Blueprints

#Employee
app.register_blueprint(create_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(update_bp)
app.register_blueprint(get_bp)

#Payroll
app.register_blueprint(payroll_create_bp)


@app.route("/")
def home():
    return "Welcome to Flask"


if __name__ == "__main__":
    app.run(debug=True)