from flask import Flask
from database import init_db
from flask_cors import CORS

from config import Config

# Employee controllers
from controller.employee.create import create_bp
from controller.employee.delete import delete_bp
from controller.employee.update import update_bp
from controller.employee.get import get_bp

# Payroll controllers
from controller.payroll.create import payroll_create_bp
from controller.payroll.delete import payroll_delete_bp
from controller.payroll.get import payroll_get_bp
from controller.payroll.update import payroll_update_bp


def create_app():
    app = Flask(__name__)


    # Load configuration
    app.config.from_object(Config)

    # CORS
    CORS(app)

    # Logging
    app.logger.setLevel(app.config["LOG_LEVEL"])

    app.logger.info("Test")


    # Initialize database
    init_db(app)

    # Register Blueprints

    # Employee
    app.register_blueprint(create_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(update_bp)
    app.register_blueprint(get_bp)

    # Payroll
    app.register_blueprint(payroll_create_bp)
    app.register_blueprint(payroll_delete_bp)
    app.register_blueprint(payroll_get_bp)
    app.register_blueprint(payroll_update_bp)

    @app.route("/")
    def home():
        return "Welcome to Flask"

    return app

# Run Flask 
app = create_app()

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
