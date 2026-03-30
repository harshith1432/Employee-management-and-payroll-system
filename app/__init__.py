from flask import Flask
from flask_cors import CORS
from config import Config
from app.extensions import db, migrate, jwt, login_manager, bcrypt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    from app.routes import auth, employee, attendance, payroll, leave, dashboard, schedule, performance, agenda
    app.register_blueprint(auth.bp)
    app.register_blueprint(employee.bp)
    app.register_blueprint(attendance.bp)
    app.register_blueprint(payroll.bp)
    app.register_blueprint(leave.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(schedule.bp)
    app.register_blueprint(performance.bp)
    app.register_blueprint(agenda.bp)

    return app
