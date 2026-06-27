from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os

from extensions import db, login_manager
from health import health_bp
from routes.auth import auth_bp
from routes.inventory import inventory_bp
from routes.production import production_bp
from routes.dashboard import dashboard_bp


def create_app():
    app = Flask(__name__)

    # ── Config ────────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///automobile.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["WTF_CSRF_ENABLED"] = os.environ.get("FLASK_ENV") != "testing"

    # ── Extensions ────────────────────────────────────────────────
    db.init_app(app)
    login_manager.init_app(app)
    CSRFProtect(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # ── Blueprints ────────────────────────────────────────────────
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(production_bp)

    # ── Create tables ─────────────────────────────────────────────
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
